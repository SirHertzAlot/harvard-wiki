from django.db import models

# Create your models here.

class Entry(models.Model):
    content = models.TextField()

    class Meta:
        verbose_name_plural = "Encyclopedia Entry - Markdown content"

    def __str__(self):
        return self.content