from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Game

# Create your views here.


def index(request):
    return render(request, "pingpong/index.html")


# @login_required
def create_game(request):
    if request.method == "POST":
        player2_id = request.POST.get("player2")
        player2 = User.objects.get(id=player2_id)
        game = Game.objects.create(player1=request.user, player2=player2)
        return redirect("pingpong:game", game_id=game.id)
    return render(request, "pingpong/create_game.html")
