from django.shortcuts import render
from .models import Todo, UserSession
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse
from typing import Optional

from .form import UserCreationForm ,UserRegistrationForm, UserRegistrationConfirmForm, LoginForm, TodoForm, TodoRegistrationConfirmForm

import uuid
import datetime
import re

#Todo_list
def todo_list(request):
    # is_deletedが0のみ取得
    todos = Todo.objects.filter(is_deleted=False)
    now = timezone.localtime(timezone.now())
    context = {'todos': todos, 'now': now }
    return render(request, 'todo_app/todo_list.html', context)

# もし is_deleted が Boolean 型の場合はフィルタリング
def todo_list_boolean(request):
    todos = Todo.objects.filter(is_deleted=False)
    context = {'todos': todos}
    return render(request, 'todo_app/todo_list.html', context)

# もし is_deleted が Integer 型で 1 が削除済みの場合は以下のようにフィルタリング
def todo_list_integer(request):
    todos = Todo.objects.filter(is_deleted=0)
    context = {'todos': todos}
    return render(request, 'todo_app/todo_list.html', context)

@login_required
def todo_list(request):
    # 現在のログインユーザーに紐づくTodoアイテムを取得
    # is_deleted=False で削除されていないもののみ表示
    all_todos = Todo.objects.filter(user=request.user, is_deleted=False).order_by('created_at')

    # 1ページあたりの表示件数をGETパラメータから取得、デフォルトは10件
    per_page_options = ['10', '20', '50'] # 選択肢として提供する件数
    per_page = request.GET.get('per_page', '10')

    # 不正な値が渡された場合はデフォルト値に戻す
    if per_page not in per_page_options:
        per_page = '10'

    paginator = Paginator(all_todos, per_page) # Paginatorオブジェクトを作成

    page = request.GET.get('page') # 現在のページ番号を取得

    try:
        todos = paginator.page(page) # 指定されたページのTodoアイテムを取得
    except PageNotAnInteger:
        # ページ番号が整数でない場合、最初のページを表示
        todos = paginator.page(1)
    except EmptyPage:
        # ページ番号が範囲外の場合（例: 存在しないページ）、最後のページを表示
        todos = paginator.page(paginator.num_pages)

    context = {
        'todos': todos,
        'user': request.user,
        'now': timezone.now(), # 現在時刻をテンプレートに渡す
        'per_page_options': per_page_options, # 選択肢をテンプレートに渡す
        'current_per_page': per_page, # 現在選択されている件数をテンプレートに渡す
    }
    return render(request, 'todo_app/todo_list.html', context)

@login_required
def todo_list(request):
    # 現在のログインユーザーに紐づくTodoアイテムを取得
    # is_deleted=False で削除されていないもののみ表示
    all_todos = Todo.objects.filter(user=request.user, is_deleted=False).order_by('created_at')

    # 1ページあたりの表示件数をGETパラメータから取得、デフォルトは10件
    per_page_options = ['10', '20', '50'] # 選択肢として提供する件数
    per_page = request.GET.get('per_page', '10')

    # 不正な値が渡された場合はデフォルト値に戻す
    if per_page not in per_page_options:
        per_page = '10'

    paginator = Paginator(all_todos, per_page) # Paginatorオブジェクトを作成

    page = request.GET.get('page') # 現在のページ番号を取得

    try:
        todos = paginator.page(page) # 指定されたページのTodoアイテムを取得
    except PageNotAnInteger:
        # ページ番号が整数でない場合、最初のページを表示
        todos = paginator.page(1)
    except EmptyPage:
        # ページ番号が範囲外の場合（例: 存在しないページ）、最後のページを表示
        todos = paginator.page(paginator.num_pages)

    context = {
        'todos': todos,
        'user': request.user,
        'now': timezone.now(), # 現在時刻をテンプレートに渡す
        'per_page_options': per_page_options, # 選択肢をテンプレートに渡す
        'current_per_page': per_page, # 現在選択されている件数をテンプレートに渡す
    }
    return render(request, 'todo_app/todo_list.html', context)


#Todo_create
@login_required
def Todo_Create_view(request):
    form = TodoForm()
    return render(request, 'todo_app/todo_create.html', {'form': form})

@login_required
def Todo_Create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            estimated_completion_date = form.cleaned_data['Estimated_completion_date']
            request.session['todo_data'] = {
                'title': form.cleaned_data['title'],
                'detail': form.cleaned_data['detail'],
                'Estimated_completion_date': estimated_completion_date.isoformat(),
            }
            return redirect(reverse('todo_app:todo_create_confirm')) # 名前空間 'todo_app' を追加
        else:
            return render(request, 'todo_app/todo_create.html', {'form': form})
    else:
        form = TodoForm()
        return render(request, 'todo_app/todo_create.html', {'form': form})

@login_required
def Todo_Create_confirm(request):
    if request.method == 'POST':
        # 確認画面で「登録実行」ボタンが押された場合
        todo_data = request.session.get('todo_data')
        if todo_data:
            # user_id の設定に注意: Todo モデルの user フィールドが ForeignKey('auth.User') の場合
            # user_id=request.user.id ではなく user=request.user を使うのが一般的です
            # id=str(uuid.uuid4()) は、TodoモデルでUUIDFieldを使っていない限り不要かもしれません
            # Todoモデルの定義に合わせて調整してください
            todo = Todo(
                title=todo_data['title'],
                detail=todo_data['detail'],
                Estimated_completion_date=datetime.datetime.fromisoformat(todo_data['Estimated_completion_date']),
                user=request.user, # user_id=request.user.id ではなく user=request.user を推奨
                created_at=timezone.now(),
                # id=str(uuid.uuid4()) # モデルのIDFieldが自動生成するIDで十分な場合、この行は削除してください
            )
            todo.save()
            messages.success(request, 'Todo を登録しました。')
            del request.session['todo_data']
            # *** ここを修正します ***
            return redirect(reverse('todo_app:todo_list')) # 名前空間 'todo_app' を追加
        else:
            messages.error(request, '登録データが見つかりませんでした。')
            # *** ここを修正します ***
            return redirect(reverse('todo_app:todo_create')) # 名前空間 'todo_app' を追加
    else:
        # 確認画面をGETリクエストで表示する場合
        todo_data = request.session.get('todo_data')
        if todo_data and 'Estimated_completion_date' in todo_data and todo_data['Estimated_completion_date']:
            estimated_completion_date_str = todo_data['Estimated_completion_date']
            try:
                # 正規表現によるタイムゾーン部分の考慮
                match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?)([+-]\d{2}:\d{2}|Z)?', estimated_completion_date_str)
                if match:
                    datetime_str = match.group(1)
                    # fromisoformat はタイムゾーン情報も扱えるので、厳密にはgroup(2)は不要かもしれません
                    # しかし、ISO形式が完全でない場合に備えてmatch.group(1)のみで試すのは良いアプローチです
                    dt_object = datetime.datetime.fromisoformat(datetime_str)

                    # aware_dtにする前に、元の日付文字列にタイムゾーン情報が含まれているか確認
                    if dt_object.tzinfo is None:
                        aware_dt = timezone.make_aware(dt_object, timezone.get_current_timezone())
                    else:
                        aware_dt = dt_object # 既にタイムゾーン情報が含まれている場合はそのまま

                    return render(request, 'todo_app/todo_create_confirm.html', {
                        'confirm_form': TodoForm(initial=todo_data),
                        'todo_data': todo_data,
                        'formatted_date': aware_dt.strftime('%Y/%m/%d %H:%M'),
                        'TIME_ZONE': settings.TIME_ZONE,
                    })
                else:
                    # 正規表現にマッチしない場合
                    return render(request, 'todo_app/todo_create_confirm.html', {
                        'confirm_form': TodoForm(initial=todo_data),
                        'todo_data': todo_data,
                        'formatted_date': '日付形式が無効です (解析失敗)',
                        'TIME_ZONE': settings.TIME_ZONE,
                    })
            except ValueError:
                # fromisoformat で解析できない場合のエラーハンドリング
                return render(request, 'todo_app/todo_create_confirm.html', {
                    'confirm_form': TodoForm(initial=todo_data),
                    'todo_data': todo_data,
                    'formatted_date': '日付形式が無効です',
                    'TIME_ZONE': settings.TIME_ZONE,
                })
        else:
            # *** ここを修正します ***
            return redirect(reverse('todo_app:todo_create')) # 名前空間 'todo_app' を追加
        
@login_required
def Todo_Create_execute(request):
    # この関数は Todo_Create_confirm から直接 POST されるため、ここではセッションからデータを取得して処理します
    if request.method == 'POST':
        todo_data = request.session.get('todo_data')
        if todo_data:
            todo = Todo(
                title=todo_data['title'],
                detail=todo_data['detail'],
                Estimated_completion_date=datetime.datetime.fromisoformat(todo_data['Estimated_completion_date']),
                user_id=request.user.id if request.user.is_authenticated else 'anonymous',
                created_at=timezone.now(),
                id=str(uuid.uuid4())
            )
            todo.save()
            messages.success(request, 'Todo を登録しました。')
            del request.session['todo_data']
            return redirect(reverse('todo_app:todo_list'))
        else:
            messages.error(request, '登録データが見つかりませんでした。')
            return redirect(reverse('todo_app:todo_create'))
    else :
        return redirect(reverse('todo_app:todo_create_confirm'))

#Todo_Update
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title) # タイトルがPOSTに含まれない場合、元のタイトルを使用
        todo.completed = request.POST.get('completed') == 'on'
        todo.is_deleted = False
        todo.save()
        todos = list(Todo.objects.values())
        return JsonResponse({'todos': todos})
    context = {'todo': todo}
    return render(request, 'todo_app/todo_update.html', context)

@login_required
def Todo_Update_view(request, pk):
    print(f"--- Todo_Update_view にアクセス (PK: {pk}) ---")
    todo_instance = get_object_or_404(Todo, pk=pk, user_id=request.user.id)

    if request.method == 'POST':
        print("リクエストメソッド: POST")
        form = TodoForm(request.POST, instance=todo_instance)
        if form.is_valid():
            print("フォームバリデーション成功！")
            estimated_completion_date = form.cleaned_data['Estimated_completion_date']
            request.session['todo_update_data'] = {
                'id': str(pk),
                'title': form.cleaned_data['title'],
                'detail': form.cleaned_data['detail'],
                'Estimated_completion_date': estimated_completion_date.isoformat(),
            }
            
            request.session.save()
            
            # セッションにデータが正常に保存されたか確認
            print("セッションに保存されたデータ:", request.session.get('todo_update_data'))
            print("セッションキーの確認 (Todo_Update_view):", request.session.keys())

            return redirect(reverse('todo_app:todo_update_confirm_display', kwargs={'pk': pk}))
        else:
            print("フォームバリデーション失敗！エラー:", form.errors)
            messages.error(request, '入力内容に誤りがあります。')
            return render(request, 'todo_app/todo_update.html', {'form': form, 'pk': pk})
    else: # GETリクエストの場合
        print("リクエストメソッド: GET")
        form = TodoForm(instance=todo_instance)
        return render(request, 'todo_app/todo_update.html', {'form': form, 'pk': pk})


@login_required
def Todo_Update_confirm(request, pk):
    # GETリクエストの場合 (確認画面表示)
    if request.method == 'GET':
        try:
            todo_data = Todo.objects.get(pk=pk, user_id=request.user.id)
        except Todo.DoesNotExist:
            return redirect('todo_app:todo_list') # ToDoリストにリダイレクトするか、404エラーを出す

        # 日付のフォーマット（あれば）
        formatted_date = None
        if todo_data.Estimated_completion_date:
            formatted_date = todo_data.Estimated_completion_date.strftime('%Y年%m月%d日')

        context = {
            'pk': pk, # pkをテンプレートに渡す
            'todo_data': todo_data,
            'formatted_date': formatted_date,
        }
        return render(request, 'todo_app/todo_update_confirm.html', context) # <-- ここにカンマがないことを確認！

    # POSTリクエストの場合 (確認画面からのデータ送信)
    elif request.method == 'POST':
        # ここは本来 Todo_Update_execute で処理されるべきなので、
        # このビューではPOSTを受け付けないか、Todo_Update_executeにリダイレクトするのが良い。
        # 例: 確認画面でPOSTされた場合は、処理せずにリダイレクト
        return redirect('todo_app:todo_update_execute', pk=pk)

@login_required
def Todo_Update_execute(request, pk):
    print(f"--- Todo_Update_execute にアクセス (PK: {pk}) ---")
    if request.method == 'POST':
        todo_instance = get_object_or_404(Todo, pk=pk, user_id=request.user.id)
        todo_data = request.session.get('todo_update_data')
        print("Todo_Update_execute: セッションから取得したデータ:", todo_data)

        if todo_data and todo_data.get('id') == str(pk):
            # セッションから取得したデータを使ってインスタンスを更新
            todo_instance.title = todo_data['title']
            todo_instance.detail = todo_data['detail']
            todo_instance.Estimated_completion_date = datetime.datetime.fromisoformat(todo_data['Estimated_completion_date'])
            todo_instance.save() # DBに保存！

            messages.success(request, 'Todo を更新しました。')
            del request.session['todo_update_data'] # セッションデータをクリア
            print("Todo を更新し、セッションデータをクリアしました。")
            return redirect(reverse('todo_app:todo_list'))
        else:
            print("エラー: 更新データが見つからないか、IDが一致しません。")
            messages.error(request, '更新データが見つかりませんでした。')
            return redirect(reverse('todo_app:todo_update', kwargs={'pk': pk}))
    else:
        print("エラー: 不正なアクセス (GETリクエスト)。")
        messages.error(request, '不正なアクセスです。')
        return redirect(reverse('todo_app:todo_update', kwargs={'pk': pk}))


#Todo_Delete
def Todo_delete_view(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        # POSTリクエストの場合：削除を実行
        todo.is_deleted = True # 論理削除の場合
        todo.deleted_at = timezone.now() # 削除日時を設定
        todo.save()
        messages.success(request, 'Todo を削除しました。')
        return redirect(reverse('todo_app:todo_list'))
    else:
        # GETリクエストの場合：削除確認画面を表示
        # テンプレートにtodoオブジェクトを渡す
        context = {
            'todo': todo,
            'pk': pk, # テンプレートでpkが必要な場合に備えて渡す
        }
        return render(request, 'todo_app/todo_delete.html', context)


#menu
@login_required
def menu(request):
    now = {'now' : timezone.localtime(timezone.now())}
    return render(request, 'todo_app/menu.html', now )


#login
# 関数ベースビューの例
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f"authenticate の結果: {user}")
            if user is not None:
                #多重ログインの場合
                if UserSession.objects.filter(user=user).exists():
                    print("多重ログインチェック: True")
                    messages.error(request, "このユーザーは既にログインしています。")
                    return render(request, 'todo_app/login.html', {'form': form})
                else:
                    print("多重ログインチェック: False")
                    login(request, user)
                    UserSession.objects.create(user=user, session_key=request.session.session_key)
                    print(f"セッションキー：{request.session.session_key}")
                    return redirect(reverse('todo_app/menu')) 
            else:
                messages.error(request, "ユーザー名またはパスワードが間違っています。")
                return render(request, 'todo_app/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'todo_app/login.html', {'form': form})

def login_view_django_session(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 多重ログインチェック (Django のセッションテーブルを直接参照)
                active_sessions = Session.objects.filter(
                    session_data__contains=f'_auth_user_id":{user.id}', # type: ignore
                    expire_date__gt=timezone.now()
                ).exclude(session_key=request.session.session_key)

                if active_sessions.exists():
                    messages.error(request, "このユーザーは既にログインしています。")
                    return render(request, 'todo_app/login.html', {'form': form})
                else:
                    login(request, user)
                    # 必要に応じてセッション情報を更新・保存 (Django が自動で行います)
                    return redirect('menu')  # ログイン後のリダイレクト先
            else:
                messages.error(request, "ユーザー名またはパスワードが間違っています。")
                return render(request, 'todo_app/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'todo_app/login.html', {'form': form})

#logout
def logout_view(request):
    if request.user.is_authenticated:
        # カスタムモデル UserSession から当該ユーザーのセッション情報を削除
        UserSession.objects.filter(user=request.user, session_key=request.session.session_key).delete()
        logout(request)
        return redirect(reverse('registration:rogin')) 
    else:
        return redirect(reverse('registration:rogin')) 