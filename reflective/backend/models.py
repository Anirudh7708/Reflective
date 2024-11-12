from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class Survey(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed')
    ]

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_surveys'
    )
    creator_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shareable_link = models.CharField(max_length=255, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Surveys'

    def __str__(self):
        return f"Survey by {self.creator_name} - {self.title}"


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    CHECKBOX = 'checkbox'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (RADIO, 'Multiple Choice'),
        (CHECKBOX, 'Checkbox')
    ]

    survey = models.ForeignKey(
        Survey,
        related_name='questions',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default=TEXT
    )
    options = models.JSONField(
        default=list,
        blank=True,
        help_text="Options for multiple choice/checkbox questions"
    )
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)
    # For soft delete functionality
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Response(models.Model):
    survey = models.ForeignKey(
        Survey,
        related_name='responses',
        on_delete=models.CASCADE
    )
    respondent_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Response to {self.survey.title} by {self.respondent_name}"


class Answer(models.Model):
    response = models.ForeignKey(
        Response,
        related_name='answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text_answer = models.TextField(blank=True)
    choice_answers = models.JSONField(
        default=list,
        blank=True,
        help_text="Selected options for multiple choice/checkbox questions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['response', 'question']

    def __str__(self):
        return f"Answer for {self.question.text}"

    def save(self, *args, **kwargs):
        if self.question.type == Question.TEXT:
            self.choice_answers = []
        elif self.question.type in [Question.RADIO, Question.CHECKBOX]:
            self.text_answer = ""
        super().save(*args, **kwargs)
