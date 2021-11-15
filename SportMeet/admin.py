from django.contrib import admin
from SportMeet.models import Profile, Team, Game, GameField, AppMessage


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sport')


admin.site.register(Team, TeamAdmin)
admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(GameField)
admin.site.register(AppMessage)
