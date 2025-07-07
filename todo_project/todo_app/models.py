from django.db import models

class Todo(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title