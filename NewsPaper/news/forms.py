from django import forms
from .models import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from datetime import date


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(label='Категория',
                                              queryset=Category.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                              )
    title = forms.CharField(label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            )
    content = forms.Field(label='Текст',
                          widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
        ]





