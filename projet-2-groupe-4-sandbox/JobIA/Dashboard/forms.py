from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .modules.database import get_all_skills
from .models import Skills

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

skills = get_all_skills()
class Skills_for_user(forms.Form):
    skills = forms.MultipleChoiceField(
        required=False, 
        widget=forms.CheckboxSelectMultiple,
        choices=skills,
    )