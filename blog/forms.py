from django import forms
from .models import Article, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = (
            'title',
            'content',
            'ingredients',
            'cooking',
            'photo',
            'category'
        )

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Название статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание статьи'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ингредиенты'
            }),
            'cooking': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Шаги приготовления'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите фотографию'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите категорию'
            })
        }


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16, help_text='Максимум 16 символов',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'
                               }))

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(render_value=True, attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ваш пароль'
                               }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий к статье',
                'row': 3,
                'style': 'border: none; border-bottom: 1 px solid #ddd'
            })
        }
