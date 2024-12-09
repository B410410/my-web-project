from django.db import models

class ToDo(models.Model):
    title  = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    imput_time = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
