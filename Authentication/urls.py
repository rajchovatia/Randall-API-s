from django.urls import path,include
from Authentication import views


urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name="register"),
    path('login/',views.UserLoginView.as_view(), name="login"),
]
