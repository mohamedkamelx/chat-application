from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import register,login_v,UserListView
urlpatterns = [
    path("register/",register,name='register'),
    path("logout/",LogoutView.as_view(next_page="login"),name='logout'),
    path("login/",login_v,name='login'),
    path("list/",UserListView.as_view(),name='users')
]
