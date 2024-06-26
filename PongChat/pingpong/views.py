from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# from .models import Game

# Create your views here.


# @login_required
# def index(request):
#     return render(request, "pingpong/index.html")


User = get_user_model()


# @login_required
def index(request):
    return render(request, "pingpong/home.html")


# @login_required
# def create_game(request):
#     if request.method == "POST":
#         player2_id = request.POST.get("player2")
#         player2 = User.objects.get(id=player2_id)
#         game = Game.objects.create(player1=request.user, player2=player2)
#         return redirect("pingpong:game", game_id=game.id)
#     return render(request, "pingpong/create_game.html")


@login_required
def game_play(request):
    return render(request, "pingpong/game_play.html")


# @login_required
def home(request):
    return render(request, "pingpong/home.html")


# @login_required
def multiplayer_local_play(request):
    return render(request, "pingpong/multiplayer_local_play.html")


@login_required
def multiplayer_lobby(request):
    online_players = User.objects.filter(is_remote_multiplayer_active=True).exclude(
        id=request.user.id
    )
    return render(
        request, "pingpong/multiplayer_lobby.html", {"online_players": online_players}
    )


# @login_required
def multiplayer_options(request):
    return render(request, "pingpong/multiplayer_options.html")


@login_required
def multiplayer_play(request, game_id):
    context = {"game_id": game_id}
    return render(request, "pingpong/multiplayer_play.html", context)


# @login_required
def single_play_setup(request):
    if request.method == "POST":
        difficulty = request.POST.get("difficulty")
        return redirect("pingpong:game_play", difficulty=difficulty)
    return render(request, "pingpong/single_play_setup.html")


# @login_required
def start_single_play(request):
    difficulty = request.POST.get("difficulty")
    return render(
        request, "pingpong/start_single_play.html", {"difficulty": difficulty}
    )


@login_required
def tournament_bracket(request):
    return render(request, "pingpong/tournament_bracket.html")


@login_required
def tournament_registration(request):
    return render(request, "pingpong/tournament_registration.html")
