from django import forms
from . models import Posts

# Форма создания нового поста
class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'text']