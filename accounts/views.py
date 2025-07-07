from django.shortcuts import render
from todo_app.models import Todo, UserSession
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from todo_app.form import UserCreationForm ,UserRegistrationForm, UserRegistrationConfirmForm, LoginForm, TodoForm, TodoRegistrationConfirmForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.conf import settings
from typing import Optional
import uuid
import datetime
import re

# クラスベースビューの例
class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'

def signup_view(request):
    form = UserCreationForm()  # フォームオブジェクトを作成
    return render(request, 'accounts/signup.html', {'form': form})  # フォームをコンテキストとして渡す

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #request.session['registration_data'] = form.cleaned_data
            return redirect('signup_confirm')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signup_confirm(request):
    registration_data = request.session.get('registration_data')
    if not registration_data:
        return redirect('signup') # データがない場合は登録画面へ

    confirm_form = UserRegistrationConfirmForm(initial=registration_data)
    return render(request, 'accounts/signup_confirm.html', {'confirm_form': confirm_form, 'registration_data': registration_data})

def signup_execute(request):
    if request.method == 'POST':
        confirm_form = UserRegistrationConfirmForm(request.POST)
        if confirm_form.is_valid():
            registration_data = request.session.get('registration_data')
            if registration_data:
                try:
                    user = User.objects.create_user(
                        username=registration_data['username'],
                        password=registration_data['password'],
                        first_name=registration_data['first_name'],
                        last_name=registration_data['last_name'],
                        email=registration_data['email']
                    )
                    messages.success(request, 'ユーザー登録が完了しました。')
                    del request.session['registration_data'] # セッションデータを削除
                    return redirect('login') # 登録完了後にログイン画面へリダイレクト
                except Exception as e:
                    messages.error(request, f'登録中にエラーが発生しました: {e}')
                    return redirect('signup')
            else:
                messages.error(request, '登録データが見つかりませんでした。')
                return redirect('signup')
    return redirect('signup')