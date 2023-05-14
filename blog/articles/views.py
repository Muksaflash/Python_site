# -*- coding: utf-8 -*-

from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login, logout


def archive(request):
    return render(request, 'archive1.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        print(f"post: {post}")
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        print("Article.DoesNotExist")
        raise Http404
        
@login_required
def create_post(request):
    if request.method == "POST":
        # обработать данные формы, если метод POST
        form = {
            'text': request.POST["text"], 'title': request.POST["title"]
        }
        # в словаре form будет храниться информация, введенная пользователем
        if form["text"] and form["title"]:
            # если поля заполнены без ошибок
            if Article.objects.filter(title=form["title"]).exists():
                # если статья с таким названием уже существует
                form['errors'] = "Статья с таким названием уже существует"
                return render(request, 'create_post.html', {'form': form})
            else:
                article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=article.id)
                # перейти на страницу поста
        else:
            # если введенные данные некорректны
            form['errors'] = "Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})
    else:
        # просто вернуть страницу с формой, если метод GET
        return render(request, 'create_post.html', {})

        # Функция для авторизации пользователя
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('archive')
    else:
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

# Функция для выхода из учетной записи пользователя
def user_logout(request):
    logout(request)
    return redirect('archive')

# Функция для регистрации нового пользователя
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} был успешно зарегистрирован. Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
