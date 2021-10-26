from django.urls import path, re_path

from . import views

urlpatterns = [
    path('profiles', views.ListProfilesView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('users', views.ListUsersView.as_view()),
    path('register', views.RegisterView.as_view()),
    re_path('^games/(?P<username>.+)/$', views.GamesView.as_view()),
    re_path('^teams/(?P<username>.+)/$', views.TeamsView.as_view()),
]
