import random
from django.shortcuts import render


def home(request):

    # Initialize scores
    if "user_score" not in request.session:
        request.session["user_score"] = 0
        request.session["computer_score"] = 0
        request.session["draw_score"] = 0

    user_choice = None
    computer_choice = None
    result = None
    winner = None

    # ---------------- RESET ----------------
    if request.method == "POST" and "reset" in request.POST:
        request.session["user_score"] = 0
        request.session["computer_score"] = 0
        request.session["draw_score"] = 0
        request.session.modified = True

    # Check game status
    game_over = (
        request.session["user_score"] >= 5
        or request.session["computer_score"] >= 5
    )

    # ---------------- PLAY ----------------
    if (
        request.method == "POST"
        and "choice" in request.POST
        and not game_over
    ):

        user_choice = request.POST.get("choice")

        computer_choice = random.choice(["snake", "water", "gun"])

        if user_choice == computer_choice:
            result = "🤝 Draw"
            request.session["draw_score"] += 1

        elif (
            (user_choice == "snake" and computer_choice == "water")
            or (user_choice == "water" and computer_choice == "gun")
            or (user_choice == "gun" and computer_choice == "snake")
        ):
            result = "🎉 You Won!"
            request.session["user_score"] += 1

        else:
            result = "🤖 Computer Won!"
            request.session["computer_score"] += 1

        request.session.modified = True

        # Check again after updating scores
        game_over = (
            request.session["user_score"] >= 5
            or request.session["computer_score"] >= 5
        )

    # ---------------- WINNER ----------------
    if request.session["user_score"] >= 5:
        winner = "🏆 Congratulations! You won the match!"

    elif request.session["computer_score"] >= 5:
        winner = "🏆 Computer won the match!"

    context = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result,
        "user_score": request.session["user_score"],
        "computer_score": request.session["computer_score"],
        "draw_score": request.session["draw_score"],
        "game_over": game_over,
        "winner": winner,
    }

    return render(request, "game/home.html", context)