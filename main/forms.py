import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

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
        initial=datetime.datetime.now(),
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


class UsernameChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)


class EmailChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)
