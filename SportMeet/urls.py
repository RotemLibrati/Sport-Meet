from django.urls import path, re_path

from . import views

urlpatterns = [
    path('profiles', views.ListProfilesView.as_view()),
    re_path('^profiles/(?P<username>.+)/$', views.ListProfilesView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('users', views.ListUsersView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('create-game', views.CreateNewGameView.as_view()),
    path('create-team', views.CreateTeamView.as_view()),
    path('locations', views.GameFieldView.as_view()),
    path('import-data', views.ImportData.as_view()),
    path('public-games', views.PublicGamesView.as_view()),
    path('delete-team', views.DeleteTeamView.as_view()),
    re_path('^recent-games/(?P<username>.+)/$', views.RecentGamesView.as_view()),
    re_path('^notification/(?P<username>.+)/$', views.NotificationView.as_view()),
    re_path('^count-teams/(?P<username>.+)/$', views.ProfileDataView.as_view()),
    re_path('^get-attendance/(?P<username>.+)/(?P<game>.+)/$', views.AttendanceView.as_view()),
    re_path('^games/(?P<username>.+)/$', views.ListGamesView.as_view()),
    re_path('^game/(?P<id>.+)/$', views.DetailGameView.as_view()),
    re_path('^teams/(?P<username>.+)/$', views.TeamsView.as_view()),
    re_path('^all-teams/(?P<username>.+)/$', views.AllTeamsView.as_view()),
    re_path('^attendance/(?P<username>.+)/$', views.AttendanceView.as_view()),
    re_path('^attendance-for-game/(?P<gameId>.+)/$', views.AttendancesStatusView.as_view()),
    re_path('^delete-message/(?P<messageId>.+)/$', views.AppMessageView.as_view()),
    re_path('^team-messages/(?P<id>.+)/$', views.AppMessageView.as_view()),
    re_path('^message/(?P<id>.+)/$', views.AppMessageView.as_view()),
    re_path('^new-message/(?P<teamID>.+)/$', views.AppMessageView.as_view()),
    
]
