from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'task_manager_app'
