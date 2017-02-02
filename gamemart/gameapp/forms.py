from django import forms
from django.contrib.auth.models import User




class UserForm(forms.ModelForm):
  # use password widget so password isn't shown
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User # We want to use User model ...
    # ... and the form should have the following fields

    fields = ('first_name', 'last_name', 'username', 'password', 'email')
    #fields = ('first_name', 'last_name', 'username', 'password', 'password', 'email', 'user_type',)


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Game # referencing the Game model and its fields
        fields = [
            "title",
            "desc",
            "instruction",
            "url",
            "price"
        ]
