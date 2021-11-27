from django.contrib import admin
from SportMeet.models import Profile, Team, Game, GameField, AppMessage, Attendance


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sport')

class GameFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region','is_for_football', 'is_for_basketball', 'is_for_tennis')


admin.site.register(Team, TeamAdmin)
admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(GameField, GameFieldAdmin)
admin.site.register(AppMessage)
admin.site.register(Attendance)

