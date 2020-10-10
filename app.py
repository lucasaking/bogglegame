from flask import Flask, request, render_template, jsonify, session
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.route("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.route("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    # print({"gameId": f"{game_id}", "board": f"{game.board}"})

    return jsonify(gameId=game_id, board=game.board)


@app.route('/api/score-word', methods=["POST"])
def score_word():
    """Accept a post request with JSON for the game id and the word. Check if word is legal."""

    word = request.json["word"].upper()
    game_id = request.json["gameId"]
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        return jsonify(result="not-word")

    elif not game.check_word_on_board(word):
        return jsonify(result="not_on_board")

    else:
        score = game.play_and_score_word(word)
        return jsonify(result="ok")
