from django.urls import path

from . import views

app_name = "main"  # 複数のアプリを作る場合、url 名に名前空間を設定する
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path(
        "my-tasks/",
        views.TemplateView.as_view(template_name="main/my-tasks.html"),
        name="my_tasks",
    ),
]
