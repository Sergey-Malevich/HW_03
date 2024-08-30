from django.shortcuts import render
from django.urls import reverse_lazy
import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponseRedirect
from datetime import date
from django.core.mail import send_mail, EmailMultiAlternatives  # Для отправки писем
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


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
    paginate_by = 10  # вот так мы можем указать количество записей на странице
    context_object_name = 'newslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    paginate_by = 10

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

class PostFormView(PermissionRequiredMixin, FormView):
    model = Post
    form_class = PostForm

class NewsCreate(CreateView, PostFormView):
    template_name = 'news_create.html'
    permission_required = 'news.add_post'

    def get_absolute_url(self):
        return HttpResponseRedirect('/news/')

    def post(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=request.user.username)
        return super(NewsCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get_or_create(user=self.user)[0]
        post.post_news = "NEWS"
        today = date.today()
        post_limit = Post.objects.filter(author=post.author, time_in__date=today).count()
        if form.is_valid():
            if post_limit >= 3:
                return render(self.request, 'post_limit.html', {'author':post.author})
            form.save()
            return HttpResponseRedirect('/news/')

class ArticlesCreate(PostFormView,CreateView):
    template_name = 'news_create.html'
    permission_required = 'news.add_post'

    def get_absolute_url(self):
        return HttpResponseRedirect('/news/')

    def post(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=request.user.username)
        return super(ArticlesCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get_or_create(user=self.user)[0]
        post.post_news = 'POST'
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

# Добавляем представление для изменения новости.
#@method_decorator(login_required, name='dispatch') # TODO: работает отлично, но по заданию используем миксин
class NewsEdit( PostFormView,UpdateView):
    template_name = 'news_create.html'
    permission_required = 'news.change_post'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

class ArticlesEdit(PostFormView,UpdateView):
    template_name = 'news_create.html'
    permission_required = 'news.change_post'

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

# вывод всех категорий
class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categorylist'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategorySubscribe(ListView):
    model = CategoryUser
    template_name = 'category_subscribe.html'
    #permission_required = 'news.add_CategoryUser'
    context_object_name = 'categorysubscribe'

    def get(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['pk'])
        self.user = get_object_or_404(User, username=request.user.username)
        CategoryUser.objects.get_or_create(category=self.category, user=self.user)
        return super(CategorySubscribe, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = not CategoryUser.objects.filter(category=self.category, user=self.user).exists()
        #context['user_has_email'] = self.request.user.email
        context['category'] = self.category
        return context
'''
    def post(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['pk'])
        self.user = get_object_or_404(User, username=request.user.username)
        CategoryUser.objects.get_or_create(category=self.category, user=self.user)
        #return redirect('subscribe', pk=self.category.pk)
'''