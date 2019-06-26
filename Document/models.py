from __future__ import unicode_literals
from django.db import models
import string
import os

from django.db import models
from django.utils.timezone import now as timezone_now
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Document(models.Model):
  user = models.CharField(User,max_length=200, null=True)
  Nombre = models.CharField(max_length=200, blank=True)
  document = models.FileField(upload_to='documents/')
  numb = models.IntegerField(null=True)
  uploaded_at = models.DateTimeField(auto_now_add=True)


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return format(
        filename_ext.lower())

