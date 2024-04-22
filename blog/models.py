from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Описание статьи')
    ingredients = models.TextField(verbose_name='Ингридиенты')
    cooking = models.TextField(verbose_name='Шаги проготовления')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    publish = models.BooleanField(default=True, verbose_name='Статус статьи')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQufUBKNmKGYhA0O8VJg4ynifJt48GxbSoujg&usqp=CAU'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    like = models.BooleanField(default=False, verbose_name="Лайк")
    dislike = models.BooleanField(default=False, verbose_name="Дизлайк")

    def __str__(self):
        return f"{self.article.title} - {self.user.username} - {self.like} - {self.dislike}"

    class Meta:
        verbose_name = 'Лайк и дизлайк'
        verbose_name_plural = 'Лайки и дизлайки'
