from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "main"  # 複数のアプリを作る場合、url 名に名前空間を設定する
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("my-tasks/", views.TaskListView.as_view(), name="my_tasks"),
    path("task-delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
