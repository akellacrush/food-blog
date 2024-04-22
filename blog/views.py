from django.shortcuts import render, redirect
from .models import *
from .forms import ArticleForm, LoginForm, UserRegistrationForm, CommentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.


class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'blog/index.html'

    def get_queryset(self):
        articles = Article.objects.all()
        articles = articles.order_by('-created_at')
        return articles


class ArticleListByCategory(ArticleList):
    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['category_id'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = f'Категория: {category.title}'
        return context


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': 'добавить статью'
    }


class ArticleDetail(DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()

        user = self.request.user
        if user.is_authenticated:
            mark, created = Like.objects.get_or_create(user=user, article=article)
            if created:
                context['like'] = False
                context['dislike'] = False
            else:
                context['like'] = mark.like
                context['dislike'] = mark.dislike
        else:
            context['like'] = False
            context['dislike'] = False
        likes = Like.objects.filter(article=article)
        likes_count = len([i for i in likes if i.like])
        dislikes_count = len([i for i in likes if i.dislike])
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        context['title'] = f'статья на тему:{article.title}'
        articles = Article.objects.all()
        articles = articles.order_by('-views')
        context['articles'] = articles[:4]
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article=article)
        return context


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'


class SearchResults(ArticleList):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return articles


def about_dev(request):
    return render(request, 'blog/about_dev.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Войдите в аккаунт !')
            return redirect('user_login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('user_register')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
        'title': 'Регистрация пользователя'
    }
    return render(request, 'blog/user_register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Вы успешно авторизовались !')
                return redirect('index')
            else:
                messages.error(request, 'Не верное имя пользователя/пароль !')
                return redirect('user_login')
        else:
            messages.error(request, 'Не верное имя пользователя/пароль !')
            return redirect('user_login')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта !')
    return redirect('index')


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий добавлен!')
        return redirect('article', pk)


def add_or_delete_mark(request, article_id, action):
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if action == 'add_like':
            mark.like = True
            mark.dislike = False
        elif action == 'add_dislike':
            mark.like = False
            mark.dislike = True
        elif action == 'delete_like':
            mark.like = False
        elif action == 'delete_dislike':
            mark.dislike = False
        mark.save()
        return redirect('article', article.pk)
    else:
        return redirect('user_login')
