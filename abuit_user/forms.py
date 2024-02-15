from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control !tw-border !tw-border-auth_btn tw-rounded-md tw-p-2 tw-text-sm tw-font-primary tw-text-auth_btn focus:tw-outline-none focus:!tw-shadow-none focus:tw-border-primary",
        "placeholder": "Password"}),
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control !tw-border !tw-border-auth_btn tw-rounded-md tw-p-2 tw-text-sm tw-font-primary tw-text-auth_btn focus:tw-outline-none focus:!tw-shadow-none focus:tw-border-primary",
        "placeholder": "Confirm Password"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control !tw-border !tw-border-auth_btn tw-rounded-md tw-p-2 tw-text-sm tw-font-primary "
                         "tw-text-auth_btn focus:tw-outline-none focus:!tw-shadow-none focus:tw-border-primary",
                "placeholder": "Username", "autofocus": "autofocus"}),
            "email": forms.EmailInput(attrs={
                "class": "form-control !tw-border !tw-border-auth_btn tw-rounded-md tw-p-2 tw-text-sm tw-font-primary "
                         "tw-text-auth_btn focus:tw-outline-none focus:!tw-shadow-none focus:tw-border-primary",
                "placeholder": "Email"}),
        }
