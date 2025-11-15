from django.db import models

# Create your models here.
class Headline(models.Model):
    title = models.CharField(max_length=350)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=50, default='Unknown')