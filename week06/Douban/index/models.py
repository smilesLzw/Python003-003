from django.db import models


# Create your models here.
class Commentinfo(models.Model):
    nickname = models.CharField(max_length=30)
    star = models.IntegerField(11)
    comment = models.TextField()
    comment_time = models.DateField()
