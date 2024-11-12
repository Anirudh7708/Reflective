from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.forms import formset_factory
from .models import Survey, Question
from .forms import SurveyForm, QuestionForm


def about(request):
    context = {
        'testimonials': [
            {
                'content': 'This platform transformed how we gather user feedback. The AI sentiment analysis is invaluable for identifying key areas for improvement.',
                'author': 'Emma W.',
                'position': 'Product Manager'
            },
            {
                'content': 'We\'ve never understood our users so well. The feedback insights help us make data-backed decisions faster than ever.',
                'author': 'John D.',
                'position': 'CEO'
            }
        ]
    }
    return render(request, 'backend/about.html', context)


def about(request):
    context = {
        'testimonials': [
            {
                'content': 'This platform transformed how we gather user feedback. The AI sentiment analysis is invaluable for identifying key areas for improvement.',
                'author': 'Emma W.',
                'position': 'Product Manager'
            },
            {
                'content': 'We\'ve never understood our users so well. The feedback insights help us make data-backed decisions faster than ever.',
                'author': 'John D.',
                'position': 'CEO'
            }
        ]
    }
    return render(request, 'backend/about.html', context)


@login_required
def create_survey(request):
    # Allows dynamic question addition
    QuestionFormSet = formset_factory(
        QuestionForm, extra=1, min_num=1, validate_min=True)

    if request.method == 'POST':
        survey_form = SurveyForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        try:
            if survey_form.is_valid() and question_formset.is_valid():
                # Save the survey details
                survey = survey_form.save(commit=False)
                survey.creator = request.user  # Associate survey with user
                survey.save()

                questions = []
                for question_form in question_formset:
                    if question_form.cleaned_data:  # Avoid saving empty forms
                        question = question_form.save(commit=False)
                        question.survey = survey  # Link question to the survey
                        questions.append(question)

                # Bulk create for better performance
                Question.objects.bulk_create(questions)

                messages.success(request, 'Survey created successfully!')
                return redirect('survey_success')
            else:
                messages.error(request, 'Please correct the errors below.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    else:
        survey_form = SurveyForm()
        question_formset = QuestionFormSet()

        context = {
            'survey_form': survey_form,
            'question_formset': question_formset,
        }
        return render(request, 'backend/create_survey.html', context)


def survey_success(request):
    return render(request, 'backend/home.html')


def home_view(request):
    if request.user.is_authenticated:
        surveys = Survey.objects.filter(
            creator=request.user).order_by('-created_at')
        return render(request, 'backend/home.html', {'surveys': surveys})
    return render(request, 'backend/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', 'home')
                    messages.success(
                        request=request, message=f'Welcome back, {username}!')
                    return redirect(to=next_url)
                else:
                    messages.error(request=request,
                                   message='Your account is disabled.')
            else:
                messages.error(request=request,
                               message='Invalid username or password.')
        else:
            messages.error(request=request,
                           message='Please fill in all fields.')
    return render(request=request, template_name='backend/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request=request,
                  message='You have been logged out successfully.')
    return redirect('login')  # Redirect to login page


@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request=request, message=error)
    else:
        form = UserCreationForm()
    return render(request, 'backend/register.html', {'form': form})


@login_required
def profile_view(request):
    if Survey.objects.filter(creator=request.user):
        context = {
            'user_surveys': Survey.objects.filter(creator=request.user),
            'total_surveys': Survey.objects.filter(creator=request.user).count(),
        }
        return render(request, 'backend/profile.html', context)
    return render(request, "backend/profile.html")


@login_required
def survey_detail(request, survey_id: int):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)
    return render(request=request, template_name='backend/survey_detail.html', context={'survey': survey})


@login_required
def survey_delete(request, survey_id: int):
    survey = get_object_or_404(Survey, id=survey_id, creator=request.user)
    if request.method == 'POST':
        survey.delete()
        # messages.success(request=request, message='Survey deletereturn redirect(to='profile')
    return render(request=request, template_name='backend/survey_delete.html', context={'survey': survey})
