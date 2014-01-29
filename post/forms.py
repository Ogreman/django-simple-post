from django import forms

from registration.forms import RegistrationForm

from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        widgets = {
            'title' : forms.TextInput(attrs = {'placeholder': 'Snappy title'}),
            'content': forms.Textarea(attrs = {'placeholder': 'Say something...'}),
            'author': forms.HiddenInput(),
        }
        fields = ('title', 'content', 'tags', 'author')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['tags'].widget.attrs['placeholder'] = "Enter a list of tags (e.g.: 'foo, bar')..."


class ReplyForm(PostForm):
    class Meta(PostForm.Meta):
        fields = ('content', 'tags', 'author')


class RegisterForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = _
