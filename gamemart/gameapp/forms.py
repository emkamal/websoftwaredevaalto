import itertools

from django import forms
#from django.contrib.auth.models import User
from django.utils.text import slugify
from gameapp.models import User, Game


class UserForm(forms.ModelForm):
    # use password widget so password isn't shown
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User # We want to use User model ...
        # ... and the form should have the following fields

        #fields = ('first_name', 'last_name', 'username', 'password', 'email', 'slug', 'user_type')
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'user_type')

    def save(self):
        instance = super(UserForm, self).save(commit=False)

        instance.slug = orig = slugify(instance.username)

        for x in itertools.count(1):
            if not User.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

        instance.save()

        return instance


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
