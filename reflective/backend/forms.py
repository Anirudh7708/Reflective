from django import forms
from .models import Survey, Question
from django.core.exceptions import ValidationError
import json


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['creator_name', 'description', 'title', 'status']
        widgets = {
            'creator_name': forms.TextInput(attrs={
                'placeholder': 'Enter your name here',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your form here',
                'class': 'form-control',
                'oninput': 'adjustTextarea(this)'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter survey title',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            })
        }


class QuestionForm(forms.ModelForm):
    options_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter options separated by commas (for multiple choice questions)',
            'class': 'form-control',
            'rows': 3
        })
    )

    class Meta:
        model = Question
        fields = ['text', 'type', 'is_required', 'order']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter question here',
                'class': 'form-control',
                'oninput': 'adjustInput(this)'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('type')
        options_text = cleaned_data.get('options_text', '')

        if question_type in [Question.RADIO, Question.CHECKBOX]:
            if not options_text:
                raise ValidationError(
                    "Multiple choice questions must have options")

            # Convert comma-separated options to list
            options = [opt.strip()
                       for opt in options_text.split(',') if opt.strip()]
            if not options:
                raise ValidationError(
                    "Please provide valid options for multiple choice question")

            cleaned_data['options'] = options
        else:
            cleaned_data['options'] = []

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        # If editing existing question, populate options_text
        if instance and instance.options:
            self.initial['options_text'] = ', '.join(instance.options)


class QuestionFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()

        # Ensure at least one question exists
        if any(self.errors):
            return

        if not any(
            form.cleaned_data and not form.cleaned_data.get('DELETE', False)
            for form in self.forms
        ):
            raise ValidationError('At least one question is required.')

        # Validate question order
        orders = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                order = form.cleaned_data.get('order')
                if order in orders:
                    raise ValidationError(
                        'Questions must have unique order numbers.')
                orders.append(order)


# Create the formset factory
QuestionFormSet = forms.modelformset_factory(
    Question,
    form=QuestionForm,
    formset=QuestionFormSet,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)
