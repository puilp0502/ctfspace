from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=150)
    contents = models.TextField(help_text="HTML is supported")
    created_at = models.DateTimeField(auto_now_add=True)
