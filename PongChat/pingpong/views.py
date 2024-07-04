from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# @login_required
# def index(request):
#     return render(request, "pingpong/index.html")


User = get_user_model()


# @login_required
def index(request):
    return render(request, "pingpong/home.html")


@login_required
def game_play(request):
    return render(request, "pingpong/game_play.html")


# @login_required
def home(request):
    return render(request, "pingpong/home.html")


# @login_required
def multiplayer_play_local(request):
    return render(request, "pingpong/multiplayer_play_local.html")


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
def multiplayer_play_remote(request, game_id):
    context = {"game_id": game_id}
    return render(request, "pingpong/multiplayer_play_remote.html", context)


# @login_required
def single_play_setup(request):
    if request.method == "POST":
        difficulty = request.POST.get("difficulty")
        return redirect("pingpong:game_play", difficulty=difficulty)
    return render(request, "pingpong/single_play_setup.html")


# @login_required
def single_play_start(request):
    difficulty = request.POST.get("difficulty")
    return render(
        request, "pingpong/single_play_start.html", {"difficulty": difficulty}
    )


def tournament_play(request):
    return render(request, "pingpong/tournament_play.html")


# @login_required
def tournament_bracket(request):
    participants = request.session.get("participants")
    participant_names = request.session.get("participant_names")
    if request.method == "POST":
        return redirect("pingpong:tournament_play")
    return render(
        request,
        "pingpong/tournament_bracket.html",
        {"participants": participants, "participant_names": participant_names},
    )


# @login_required
def tournament_registration(request):
    if request.method == "POST":
        participants = int(request.POST.get("participants"))
        participant_names = [request.POST.get(f"name{i}") for i in range(participants)]

        request.session["participants"] = participants
        request.session["participant_names"] = participant_names

        return redirect("pingpong:tournament_bracket")
    return render(request, "pingpong/tournament_registration.html")
