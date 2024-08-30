from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import *
from django import forms

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,

class PostFilter(FilterSet):
    title = CharFilter(field_name='title',
                       lookup_expr='icontains',
                       label='Название статьи содержит:',
                       widget=forms.TextInput(attrs={'class': 'form-control'}))

    time_in = DateFilter(field_name='time_in',
                         lookup_expr='date__gt',
                         label='Опубликовано после',
                         widget=forms.DateInput(attrs={'type': 'date',  # TODO: Русский формат 'дд-мм-ггг'
                                                       'class': 'form-control'}))

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',)


    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post

        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {'title', 'time_in', 'category'}
        ordering = '-time_in'