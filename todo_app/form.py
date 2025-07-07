# todo_app/forms.py
from django import forms
from .models import Todo
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label='ユーザー名')
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='パスワード確認')
    first_name = forms.CharField(max_length=30, label='氏名（姓）')
    last_name = forms.CharField(max_length=30, label='氏名（名）')
    email = forms.EmailField(label='メールアドレス')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password") # type: ignore
        confirm_password = cleaned_data.get("confirm_password") # type: ignore

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません。")
        return cleaned_data
        
class UserRegistrationConfirmForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=30, widget=forms.HiddenInput())
    last_name = forms.CharField(max_length=30, widget=forms.HiddenInput())
    email = forms.EmailField(widget=forms.HiddenInput())
    execute = forms.BooleanField(widget=forms.HiddenInput(), initial=True) # 実行ボタンの送信を識別

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='ユーザー名')
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','detail','Estimated_completion_date']
        widgets ={
            'Estimated_completion_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
class TodoRegistrationConfirmForm(forms.Form):
    title = forms.CharField(max_length=150, widget=forms.HiddenInput())
    detail = forms.CharField(max_length=255, widget=forms.HiddenInput())
    Estimated_completion_date = forms.CharField(widget=forms.HiddenInput())
    userid = forms.CharField(max_length=30, widget=forms.HiddenInput())
    created_at = forms.EmailField(widget=forms.HiddenInput())
    execute = forms.BooleanField(widget=forms.HiddenInput(), initial=True) # 実行ボタンの送信を識別