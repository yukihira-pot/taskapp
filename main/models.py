from django.conf import settings
from django.db import models


class Task(models.Model):
    """タスクモデル"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザー", on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name="タイトル", max_length=256)
    content = models.TextField(verbose_name="内容", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="更新日時", auto_now_add=True)
    # 後から付け足した項目のため null=True にする。締切を設けないタスクを許容するため blank=True にする。
    deadline = models.DateTimeField(verbose_name="締切日時", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Task"

    def __str__(self) -> str:
        return self.title + ": " + self.content[:10]
