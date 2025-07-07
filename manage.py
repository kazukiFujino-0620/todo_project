# manage.py

# 必要なモジュールをインポート
import os # ★この行を追加またはコメント解除★
import sys
from django.conf import settings # この行はすでに存在しているはずです

# DEBUG 設定と環境変数からのデバッグフラグ取得
DEBUG = True  # あなたの Django の DEBUG 設定
ENABLE_DEBUG = os.environ.get('DEBUG') == 'True' # ここで os が必要

# 通常の Django アプリケーションの起動処理
if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
