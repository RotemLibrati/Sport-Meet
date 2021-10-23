from django.contrib import admin
from SportMeet.models import Profile, Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sport')


admin.site.register(Team, TeamAdmin)
