from django.utils import timezone

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, TextInput, Textarea, SplitDateTimeWidget

from .models import Task


class LoginForm(AuthenticationForm):
    pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
        )


class TaskCreationForm(ModelForm):
    deadline = forms.SplitDateTimeField(
        label="締切日時",
        widget=forms.SplitDateTimeWidget(
            date_attrs={"type": "date"},
            time_attrs={"type": "time"},
        ),
        initial=timezone.now()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = (
            "title",
            "content",
            "deadline",
        )
        widgets = {
            'title': TextInput(
                attrs={'class': 'new-task-form-control', 'id': 'new-task-title'}
            ),
            'content': Textarea(
                attrs={'class': 'new-task-form-control', 'id': 'new-task-content'}
            ),
            'deadline': SplitDateTimeWidget(
                attrs={'class': 'new-task-form-control', 'id': 'new-task-deadline'}
            ),
        }


class UsernameChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)


class EmailChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
