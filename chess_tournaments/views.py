import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from chess_tournaments.models import Tournament, Player, Round, Game
from dateutil import parser
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def create_tournament(request):
    logger.debug("Attempting to connect to API")
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        # ✅ Ensure JSON is properly loaded
        data = json.loads(request.body)
        tournament_data = data.get("tournament", {})
        players_data = data.get("players", [])
        rounds_data = data.get("rounds", [])

        # ✅ Step 1: Create Tournament
        tournament, created = Tournament.objects.update_or_create(
            id=tournament_data["id"],
            defaults={
                "name": tournament_data.get("name", "Unknown Tournament"),
                "fide_event_id": tournament_data.get("fide_event_id", None),
                "organiser": tournament_data.get("organiser", "Unknown Organiser"),
                "director": tournament_data.get("director", "Unknown Director"),
                "location": tournament_data.get("location", "Unknown Location"),
                "arbiter": tournament_data.get("arbiter", "Unknown Arbiter"),
                "start_date": parse_date(tournament_data.get("start_date", None)),
                "end_date": parse_date(tournament_data.get("end_date", None)),
                "rounds": tournament_data.get("rounds", 0),
                "time_control": tournament_data.get("time_control", "Unknown"),
                "rating_average": tournament_data.get("rating_average", None),
                "rated_fide": tournament_data.get("rated_fide", False),
                "rated_national": tournament_data.get("rated_national", False),
                "federation": tournament_data.get("federation", "Unknown Federation"),
                "tie_breaks": tournament_data.get("tie_breaks", []),
            },
        )


        # ✅ Step 2: Create ALL Players First
        player_map = {f"{p['name']}": None for p in players_data}  # Initialize with names
        for player_data in players_data:
            # Ensure "rating" key exists before accessing subfields
            rating_data = player_data.get("rating", {}) if "rating" in player_data else {}
            fide_rating = rating_data.get("fide")  # Use `.get()` instead of `None` default
            national_rating = rating_data.get("national")

            player, _ = Player.objects.update_or_create(
                id=int(player_data["id"]),
                tournament=tournament,
                defaults={
                    "fide_id": player_data.get("fide_id"),
                    "name": player_data["name"],
                    "title": player_data.get("title"),
                    "federation": player_data["federation"],
                    "club": player_data.get("club"),
                    "fide_rating": fide_rating,
                    "national_rating": national_rating,
                    "birth_year": player_data.get("birth_year"),
                    "gender": player_data.get("gender"),
                    "category": player_data.get("category"),
                    "points": player_data.get("points", 0),
                    "performance": player_data.get("performance"),
                    "tie_breaks": player_data.get("tie breaks", {}),
                },
            )
            player_map[player.name] = player  # Store player reference by name

        # ✅ Step 3: Create Rounds and Games (Now all players exist)
        for round_data in rounds_data:
            round_obj, _ = Round.objects.update_or_create(
                tournament=tournament,
                round_number=round_data["round_number"],
                defaults={"date": parse_date(round_data["date"])},
            )

            for game_data in round_data["games"]:
                white_name = game_data["white"]
                black_name = game_data["black"]
                # Handle "bye" by setting player to None
                white = player_map.get(white_name) if white_name.lower() != "bye" else None
                black = player_map.get(black_name) if black_name.lower() != "bye" else None
                white_rating = game_data["white_rating"] if white else None
                black_rating = game_data["black_rating"] if black else None
                # Create the game with NULL ratings if necessary
                Game.objects.update_or_create(
                    round=round_obj,
                    board=int(game_data["board"]),
                    defaults={
                        "white": white,
                        "black": black,
                        "white_rating": white_rating,
                        "black_rating": black_rating,
                        "result": game_data["result"],
                    },
                )
        return JsonResponse({"message": "Tournament created successfully!"}, status=201)
    except Exception as e:
        logger.info(e, exc_info=True)
        return JsonResponse({"error": str(e)}, status=400)

def tournament_list(request):
    """Display a list of all tournaments."""
    tournaments = Tournament.objects.all().order_by("-start_date")
    return render(request, "chess_tournaments/tournament_list.html", {"tournaments": tournaments})

def tournament_detail(request, tournament_id):
    """Show a single tournament overview with final standings and game rounds."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    players = Player.objects.filter(tournament=tournament).order_by("-points")
    rounds = Round.objects.filter(tournament=tournament).order_by("round_number").prefetch_related("games").all()
    for round in rounds:
        round.games_sorted = round.games.all().order_by("board")  # Sort by board

    return render(
        request,
        "chess_tournaments/tournament_detail.html",
        {
            "tournament": tournament,
            "players": players,
            "rounds": rounds,
        },
    )



def parse_date(date_str):
    """Automatically detect and parse any date format into YYYY-MM-DD."""
    if not date_str:
        return None

    try:
        return parser.parse(date_str).strftime("%Y-%m-%d")  # Convert to standard format
    except ValueError:
        return None  # If parsing fails, return None
