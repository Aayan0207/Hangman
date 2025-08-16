from flask import Flask, render_template, request, session, jsonify
import secrets
import os
from . import hangman

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))


@app.route("/", methods=["GET", "POST"])
def play_hangman():
    if request.method == "GET":
        session.clear()
        word = hangman.random_word()
        session["hangman_word"] = word
        session["mistakes"] = 8
        session["lettersGuessed"] = []
        (
            string,
            session["curr_word"],
            available_letters,
            mistakes,
            mistakes_str,
        ) = hangman.hangman(
            word,
            guess="_",
            mistakes=session["mistakes"],
            lettersGuessed=session["lettersGuessed"],
        )
        string = "Welcome to Hangman."
        session["curr_word"] = " ".join(session["curr_word"])
        pic = hangman.Hangmanimg(mistakes)
        return render_template(
            "hangman.html",
            string=string,
            available_letters=available_letters,
            mistakes_str=mistakes_str,
            curr_word=session["curr_word"],
            pic=pic,
        )
    elif request.method == "POST":
        word = session.get("hangman_word")
        if session["curr_word"].count("_") == 0:
            word = hangman.random_word()
            session["hangman_word"] = word
            session["mistakes"] = 8
            session["lettersGuessed"] = []
        guess = request.values.get("guess", "_")
        (
            string,
            session["curr_word"],
            available_letters,
            session["mistakes"],
            mistakes_str,
        ) = hangman.hangman(
            word,
            guess.lower(),
            mistakes=session["mistakes"],
            lettersGuessed=session["lettersGuessed"],
        )
        session["lettersGuessed"] = list(
            set("abcdefghijklmnopqrstuvwxyz") - set(available_letters)
        )
        session["curr_word"] = " ".join(session["curr_word"])
        if session["curr_word"].count("_") == 0 and string == "Good guess.":
            string = "Congratulations. You won!"
        pic = hangman.Hangmanimg(session["mistakes"])
        return jsonify(
            {
                "string": string,
                "available_letters": available_letters,
                "mistakes_str": mistakes_str,
                "curr_word": session["curr_word"],
                "pic": pic,
            }
        )
