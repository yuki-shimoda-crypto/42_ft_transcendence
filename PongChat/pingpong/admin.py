from django.contrib import admin

from .models import Game, GuestUser, Tournament, TournamentMatch

# Register your models here.

admin.site.register(Game)
admin.site.register(GuestUser)
admin.site.register(Tournament)
admin.site.register(TournamentMatch)
