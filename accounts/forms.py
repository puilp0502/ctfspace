from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                "Invalid Credential"
            )
        cleaned_data['user'] = user
        return cleaned_data


class JoinForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'password_again', 'email', 'name', 'age_type', 'school', ]

    error_css_class = 'invalid'

    username = forms.CharField(label='ID')
    password = forms.CharField(widget=forms.PasswordInput)
    password_again = forms.CharField(widget=forms.PasswordInput, label='Password (Again)')
    name = forms.CharField(label='Nickname:')
    age_type = forms.ChoiceField(choices=(
        (User.Age.MIDDLE_S, "중등부"),
        (User.Age.HIGH_S, "고등부"),
        (User.Age.ADULT, "성인"),
    ))

    def clean(self):
        cleaned_data = super(JoinForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('password_again'):
            self.add_error('password_again', "Passwords do not match")
        age_type = cleaned_data.get('age_type')
        if int(age_type) != User.Age.ADULT and cleaned_data.get('school') == '' :
            self.add_error('school', "You need to specify school.")

        return cleaned_data

    def save(self, commit=True):
        user = super(JoinForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user