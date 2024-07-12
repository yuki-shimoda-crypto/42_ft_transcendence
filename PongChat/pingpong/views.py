import json
import math

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import GuestUser, Tournament, TournamentMatch

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
def how_to_play(request):
    return render(request, "pingpong/how_to_play.html")


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


def tournament_finish(request):
    tournament_id = request.session.get("tournament_id")
    tournament = Tournament.objects.get(id=tournament_id)
    match = TournamentMatch.objects.get(tournament_id=tournament_id, round=1)
    winner = match.winner
    tournament.winner = winner
    tournament.save()
    return render(
        request, "pingpong/tournament_finish.html", {"winner_name": winner.username}
    )


def tournament_play(request):
    if request.method == "POST":
        data = json.loads(request.body)
        match_id = request.session.get("match_id")
        winner_id = data.get("winner_id")
        match = TournamentMatch.objects.get(id=match_id)
        winner = GuestUser.objects.get(id=winner_id)
        match.winner = winner
        match.save()
        return redirect("pingpong:tournament_bracket")
    return render(
        request,
        "pingpong/tournament_play.html",
    )


# @login_required
def tournament_bracket(request):
    participants = request.session.get("participants")
    participant_names = request.session.get("participant_names")
    round = request.session.get("round")
    if request.method == "POST":
        tournament_id = request.session.get("tournament_id")
        matches = TournamentMatch.objects.filter(
            tournament_id=tournament_id, winner=None
        )
        if matches:
            match = matches.first()
            request.session["match_id"] = match.id
            request.session["user1_id"] = match.user1.id
            request.session["user2_id"] = match.user2.id
            request.session["user1_name"] = match.user1.username
            request.session["user2_name"] = match.user2.username
            return redirect("pingpong:tournament_play")
        else:
            matches = TournamentMatch.objects.filter(
                tournament_id=tournament_id, round=round
            )
            round -= 1
            request.session["round"] = round
            if round <= 0:
                return redirect("pingpong:tournament_finish")
            for i in range(2**round // 2):
                TournamentMatch.objects.create(
                    tournament=Tournament.objects.get(id=tournament_id),
                    round=round,
                    user1=matches[2 * i].winner,
                    user2=matches[2 * i + 1].winner,
                ).save()
            matches = TournamentMatch.objects.filter(
                tournament_id=tournament_id, winner=None
            )
            match = matches.first()
            request.session["match_id"] = match.id
            request.session["user1_id"] = match.user1.id
            request.session["user2_id"] = match.user2.id
            request.session["user1_name"] = match.user1.username
            request.session["user2_name"] = match.user2.username
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
        if any(request.POST.get(f"name{i}") == "" for i in range(participants)):
            return render(request, "pingpong/tournament_registration.html")
        participant_names = [request.POST.get(f"name{i}") for i in range(participants)]

        guest_users = []
        for name in participant_names:
            guest_users.append(GuestUser.objects.create(username=name))

        tournament = Tournament.objects.create(participants_amount=participants)

        round = math.ceil(math.log2(participants))
        for i in range(participants // 2):
            TournamentMatch.objects.create(
                tournament=tournament,
                round=round,
                user1=guest_users[2 * i],
                user2=guest_users[2 * i + 1],
            ).save()

        request.session["participants"] = participants
        request.session["participant_names"] = participant_names
        request.session["tournament_id"] = tournament.id
        request.session["round"] = round

        return redirect("pingpong:tournament_bracket")

    return render(request, "pingpong/tournament_registration.html")


def tournament_winner_name_response(request, round):
    tournament_id = request.session.get("tournament_id")
    matches = TournamentMatch.objects.filter(
        tournament_id=tournament_id, round=round + 1, winner__isnull=False
    ).order_by("id")
    if matches:
        winner = []
        for match in matches:
            winner.append(match.winner.username)
        data = {
            "winner": winner,
        }
    else:
        matches = TournamentMatch.objects.filter(
            tournament_id=tournament_id, round=round
        ).order_by("id")
        participants = []
        for match in matches:
            participants.append(match.user1.username)
            participants.append(match.user2.username)
        data = {
            "winner": participants,
        }
    return JsonResponse(data)
