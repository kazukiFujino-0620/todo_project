# Generated by Django 5.2 on 2025-04-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo_app", "0002_todo_created_at_todo_updated_at_todo_user_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="id",
            field=models.CharField(max_length=100, primary_key=True,serialize=False),
        ),
    ]
