from django.shortcuts import render
from django.urls import reverse_lazy
import random
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from pprint import pprint   # для просмотра кларисета

# Create your views here.

class NewsListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 2  # вот так мы можем указать количество записей на странице
    context_object_name = 'newslist'



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        #context['newslist'] = context['newslist'].order_by("-time_in")
        #context['newslist'] = Post.objects.order_by("-time_in")
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class Search(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def get_absolute_url(self):
        return HttpResponseRedirect('/news/')

    def form_valid(self, form):
        numbers = [1, 2, 4, 5, 6]  # исключил id админа из списка
        au = random.choice(numbers)  #случайно задаем автора
        post = form.save(commit=False)
        post.post_news = 'NEWS'
        post.author_id = au
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def get_absolute_url(self):
        return HttpResponseRedirect('/news/')

    def form_valid(self, form):
        numbers = [1, 2, 4, 5, 6]  # исключил id админа из списка
        post = form.save(commit=False)
        post.post_news = 'POST'
        post.author_id = random.choice(numbers)  # TODO: случайно задаем автора
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

# Добавляем представление для изменения товара.
class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

class ArticlesEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

# Представление удаляющее новость
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list') # TODO: перенаправляем после успешного удаления

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list') # TODO: перенаправляем после успешного удаления