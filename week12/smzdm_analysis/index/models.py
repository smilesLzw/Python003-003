from django.db import models

# Create your models here.
class Comment(models.Model):
    nickname = models.CharField(max_length=30)
    comment = models.TextField()
    sentiment = models.FloatField()
    comment_time = models.DateField()
