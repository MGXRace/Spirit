#-*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(UserCreationForm):

    honeypot = forms.CharField(label=_("Leave blank"), required=False)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]

        if value:
            raise forms.ValidationError(_("Do not fill this field."))

        return value

    def clean_username(self):
        # Override
        username = self.cleaned_data["username"]

        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(_("The username is taken."))

    def save(self, commit=True):
        self.instance.slug = slugify(self.cleaned_data["username"])
        self.instance.is_active = False
        return super(RegistrationForm, self).save(commit)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "location", "timezone")


class LoginForm(AuthenticationForm):

    username = forms.CharField(label=_("Username or Email"), max_length=254)


class EmailChangeForm(forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not self.user.check_password(password):
            raise forms.ValidationError(_("Your password was entered incorrectly. "
                                          "Please enter it again."))

        return password

    def clean_email(self):
        email = self.cleaned_data["email"]

        if email == self.user.email:
            raise forms.ValidationError(_("Try a different email."))

        return email

    def get_email(self):
        return self.cleaned_data["email"]


class ResendActivationForm(forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_("The provided email does not exists."))

        if self.user.last_ip:
            raise forms.ValidationError(_("This account was activated."))

        return email

    def get_user(self):
        return self.user