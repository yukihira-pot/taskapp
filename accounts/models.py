from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    icon = models.ImageField(verbose_name="アイコン", null=True, blank=True)

    class Meta:
        verbose_name_plural = "CustomUser"  # admin 画面での表示がこれになる
