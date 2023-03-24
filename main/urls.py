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
    path("settings/", views.TemplateView.as_view(template_name="main/settings.html")),
    path(
        "username_change/", views.UsernameUpdateView.as_view(), name="username_change"
    ),
    path("email_change", views.EmailUpdateView.as_view(), name="email_change"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
