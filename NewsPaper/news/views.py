from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from django import forms
from django.http import request, HttpResponse, HttpResponseRedirect
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm

from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView


class Posts(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id']
    paginate_by = 5  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # получили весь контекст из класса-родителя
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()  # добавили новую контекстную переменную is_not_authors
        context['count_posts'] = self.model.objects.filter(time__date=date.today(), postAuthor__authorUser__username=self.request.user).count()
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'

    # пишем функцию, чтоб ввести доп параметр is_not_subscribed для contextа.
    # в шаблоне, если пользователь подписан на категорию данной новости, то кнопка не видна.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for cat in context['post'].postCategory.all():
            c = Category.objects.get(id=cat.id)
            context['is_not_subscribed'] = not c.subscribers.filter(username=self.request.user.username).exists()
        return context

class LimitForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, PostForm):
        self.object = PostForm.save(commit=False)
        new_author, created = Author.objects.get_or_create(
            authorUser=self.request.user
        )
        self.object.postAuthor = new_author
        # self.object.postAuthor = Author.objects.get(authorUser=self.request.user)
        if Post.objects.filter(time__date=date.today(),
                               postAuthor__authorUser__username=self.request.user).count() < 3:
            self.object = PostForm.save()
            return super().form_valid(PostForm)
        else:
            return HttpResponseRedirect('/')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('news.delete_post',)


# организуем подписку пользователя на категорию новостей
@login_required
def subscribe_me(request, pk=0):
    post = Post.objects.get(id=pk)
    for cat in post.postCategory.all():
        c = Category.objects.get(id=cat.id)
        if not c.subscribers.filter(username=request.user.username).exists():
            c.subscribers.add(request.user)
    return redirect('/')