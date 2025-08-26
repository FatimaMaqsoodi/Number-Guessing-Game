from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secret_key_for_sessions"  # Needed for session handling

MIN_ALLOWED = 0
MAX_ALLOWED = 100


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Parse inputs
        try:
            min_val = int(request.form.get("min_val"))
            max_val = int(request.form.get("max_val"))
        except (TypeError, ValueError):
            return render_template("game.html", error="Please enter valid integers between 0 and 100.")

        # Enforce 0–100 and min < max
        if not (MIN_ALLOWED <= min_val < max_val <= MAX_ALLOWED):
            return render_template(
                "game.html",
                error=f"Range must be within {MIN_ALLOWED}–{MAX_ALLOWED} and Min < Max."
            )

        start_game(min_val, max_val)
        return redirect(url_for("index"))

    return render_template("game.html")


@app.route("/guess", methods=["POST"])
def guess():
    # Guard: game must be started
    if "number_to_guess" not in session:
        return jsonify({"message": "Game not started!", "status": "error"})

    payload = request.get_json(silent=True) or {}
    # Parse guess safely
    try:
        raw_guess = payload.get("guess", None)
        guess = int(raw_guess)
    except (TypeError, ValueError):
        return jsonify({"message": "Please enter a valid integer.", "status": "warn"})

    # Validate 0–100 hard rule first (does NOT consume attempts)
    if guess < MIN_ALLOWED or guess > MAX_ALLOWED:
        return jsonify({
            "message": f"Your guess must be between {MIN_ALLOWED} and {MAX_ALLOWED}.",
            "status": "warn"
        })

    # Validate within chosen session range (still do not consume attempts if outside)
    min_val = session["min_val"]
    max_val = session["max_val"]
    if guess < min_val or guess > max_val:
        return jsonify({
            "message": f"Your guess must be between {min_val} and {max_val} for this round.",
            "status": "warn",
            "attempts": session.get("attempts", 0),
            "max_attempts": session.get("max_attempts")
        })

    # Valid numeric & in-range guess -> consume attempt
    session["attempts"] = session.get("attempts", 0) + 1
    number_to_guess = session["number_to_guess"]

    # Win
    if guess == number_to_guess:
        prev_best = session.get("best_score")
        new_best = False
        if prev_best is None or session["attempts"] < prev_best:
            session["best_score"] = session["attempts"]
            new_best = True

        message = (f"Correct! You guessed it in {session['attempts']} attempts. "
                   + ("New best score!" if new_best else f"Best score so far: {session.get('best_score')}."))

        # Clear round state (but keep best_score)
        session.pop("number_to_guess", None)
        return jsonify({
            "message": message,
            "status": "won",
            "best_score": session.get("best_score"),
            "new_best": new_best,
            "attempts": session["attempts"],
            "max_attempts": session.get("max_attempts")
        })

    # Out of attempts -> reveal
    if session["attempts"] >= session["max_attempts"]:
        message = f"Out of attempts! The correct number was {number_to_guess}."
        best_score = session.get("best_score")
        session.pop("number_to_guess", None)
        return jsonify({
            "message": message,
            "status": "lost",
            "best_score": best_score,
            "attempts": session["attempts"],
            "max_attempts": session.get("max_attempts")
        })

    # Hints
    if guess < number_to_guess:
        return jsonify({
            "message": "Too low.",
            "status": "continue",
            "attempts": session["attempts"],
            "max_attempts": session.get("max_attempts")
        })
    else:
        return jsonify({
            "message": "Too high.",
            "status": "continue",
            "attempts": session["attempts"],
            "max_attempts": session.get("max_attempts")
        })


@app.route("/reset", methods=["POST"])
def reset():
    # Reset current round but keep best_score
    for key in ("number_to_guess", "attempts", "max_attempts", "min_val", "max_val"):
        session.pop(key, None)
    return jsonify({"message": "Game has been reset. Set a new range to start again.", "status": "reset"})


def start_game(min_val, max_val):
    """Initialize a new round using the provided range."""
    session["min_val"] = min_val
    session["max_val"] = max_val
    session["number_to_guess"] = random.randint(min_val, max_val)
    session["attempts"] = 0
    # Attempts scale with range size (square root keeps difficulty fair)
    range_size = max_val - min_val + 1
    session["max_attempts"] = max(3, int(range_size ** 0.5))


if __name__ == "__main__":
    app.run(debug=True)
