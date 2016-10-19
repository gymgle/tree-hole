from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class MsgDB(models.Model):
    openid = models.CharField(max_length=32)
    time = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.content