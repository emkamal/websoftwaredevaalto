import itertools

from django import forms
#from django.contrib.auth.models import User
from django.utils.text import slugify
from gameapp.models import User, Game, Taxonomy
from django.utils import timezone


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

        instance.slug = orig = '-'.join((slugify(instance.first_name), slugify(instance.last_name)))
        #instance.slug = orig = slugify(instance.username)

        for x in itertools.count(1):
            if not User.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

        instance.save()

        return instance



#class LoginForm(forms.Form):
#    username = forms.CharField()
#    password = forms.CharField(widget=forms.PasswordInput)


#    class Meta:
#    model = User # We want to use User model ...
#    # ... and the form should have the following fields
#
#        #fields = ('first_name', 'last_name', 'username', 'password', 'email', 'slug', 'user_type')
#        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'user_type')
#
#    def save(self):
#        instance = super(UserForm, self).save(commit=False)
#
#        #instance.slug = orig = slugify(instance.first_name)
#        instance.slug = orig = '-'.join((slugify(instance.first_name), slugify(instance.last_name)))
#
#        for x in itertools.count(1):
#            if not User.objects.filter(slug=instance.slug).exists():
#                break
#            instance.slug = '%s-%d' % (orig, x)
#
#        instance.save()
#
#        return instance


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Game # referencing the Game model and its fields
        fields = ['title', 'desc', 'instruction', 'url', 'price']

    categories = forms.ModelMultipleChoiceField(Taxonomy.objects.filter(taxonomy_type='game_category'))
    image = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SubmitForm, self).__init__(*args, **kwargs)

    def save(self, request):
        instance = super(SubmitForm, self).save(commit=False)

        instance.owner_id = request.user.id
        instance.added_date = timezone.now()
        instance.slug = orig = slugify(instance.title)

        for x in itertools.count(1):
            if not Game.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

        instance.save()

        return instance
