from django.contrib import admin
from SportMeet.models import Profile, Team, TeamPrivileges


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sport')

class TeamPrivilegesAdmin(admin.ModelAdmin):
    list_display = ('team', 'member', 'can_invite_new_members')

admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPrivileges, TeamPrivilegesAdmin)
