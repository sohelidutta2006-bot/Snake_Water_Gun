import random
from django.shortcuts import render, redirect


def home(request):

    # Initialize session variables
    if "user_score" not in request.session:
        request.session["user_score"] = 0
        request.session["computer_score"] = 0
        request.session["draw_score"] = 0

    if "quit_game" not in request.session:
        request.session["quit_game"] = False

    user_choice = None
    computer_choice = None
    result = None
    winner = None

    # ---------------- HANDLE BUTTONS ----------------
    if request.method == "POST":

        # Reset Game
        if "reset" in request.POST:
            request.session["user_score"] = 0
            request.session["computer_score"] = 0
            request.session["draw_score"] = 0
            request.session["quit_game"] = False
            request.session.modified = True

        # Quit Game
        elif "quit" in request.POST:
            request.session.flush()   # Clear all scores
            return redirect("goodbye")

        # Play Game
        elif "choice" in request.POST and not request.session["quit_game"]:

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

    # ---------------- GAME STATUS ----------------
    game_over = (
        request.session["user_score"] >= 5
        or request.session["computer_score"] >= 5
        or request.session["quit_game"]
    )

    # ---------------- WINNER ----------------
    if request.session["user_score"] >= 5:
        winner = "🏆 Congratulations! You won the match!"

    elif request.session["computer_score"] >= 5:
        winner = "🏆 Computer won the match!"

    elif request.session["quit_game"]:
        winner = "❤️ Thanks for Playing!"

    context = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result,
        "user_score": request.session["user_score"],
        "computer_score": request.session["computer_score"],
        "draw_score": request.session["draw_score"],
        "game_over": game_over,
        "winner": winner,
        "quit_game": request.session["quit_game"],
    }

    return render(request, "game/home.html", context)
def goodbye(request):
    return render(request, "game/goodbye.html")