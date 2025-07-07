from django.contrib import admin
from .models import Todo  # Todo モデルをインポート

admin.site.register(Todo)  # Todo モデルを登録