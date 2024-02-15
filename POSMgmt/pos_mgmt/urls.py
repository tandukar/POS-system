from django.urls import path
from .views import RegisterUserView, UserLoginView


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
]
