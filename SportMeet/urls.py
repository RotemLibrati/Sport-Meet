from django.urls import path

from . import views

urlpatterns = [
    path('profiles', views.ListProfilesView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('users', views.ListUsersView.as_view()),
    path('register', views.RegisterView.as_view()),
]
