import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # select all possible entries of ratings, artists, and genres from the posts database
    unique_ratings = db.execute("SELECT rating FROM posts GROUP BY rating")
    unique_artists = db.execute("SELECT artist FROM posts GROUP BY artist")
    unique_genres = db.execute("SELECT genre FROM posts GROUP BY genre")

    if request.method == "POST":
        # checks if user is in the database

        if len(db.execute("SELECT username FROM users WHERE id=?", session["user_id"][0].get("id"))) <= 0:
            return apology("user not in database", 400)

        # if the user chooses to apply search filters, get from the form what search filters they applied
        rating = request.form.get("rating")
        artist = request.form.get("artist")
        genre = request.form.get("genre")

        # all posts displayed in descending time order
        if not rating:
            if not artist:
                # no search filter applied
                if not genre:
                    sorted_posts = db.execute("SELECT * FROM posts ORDER BY time DESC")
                # filter search by genre only
                else:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE genre = ? ORDER BY time DESC", genre)
            else:
                # filter search by artist only
                if not genre:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE artist = ? ORDER BY time DESC", artist)
                # filter search by artist and genre
                else:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE artist = ? AND genre = ? ORDER BY time DESC", artist, genre)
        else:
            if not artist:
                # filter search by rating only
                if not genre:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE rating = ? ORDER BY time DESC", rating)
                # filter search by rating and genre
                else:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE rating = ? AND genre = ? ORDER BY time DESC", rating, genre)
            else:
                # filter search by rating and artist
                if not genre:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE rating = ? AND artist = ? ORDER BY time DESC", rating, artist)
                # filter search by artist, rating, and genre
                else:
                    sorted_posts = db.execute("SELECT * FROM posts WHERE artist = ? AND rating = ? AND genre = ? ORDER BY time DESC", artist, rating, genre)


        users = db.execute("SELECT * FROM users")

        # renders explore page
        return render_template("index.html", users=users, sorted_posts = sorted_posts, unique_ratings=unique_ratings, unique_artists=unique_artists, unique_genres=unique_genres)

    else:
        # if form not submitted via POST
        users = db.execute("SELECT * FROM users")
        sorted_posts = db.execute("SELECT * FROM posts ORDER BY time DESC")
        return render_template("index.html", users=users, sorted_posts = sorted_posts, unique_ratings=unique_ratings, unique_artists=unique_artists, unique_genres=unique_genres)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and or password", 403)

        # Remember which user has logged in
        session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", request.form.get("username"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # checks if username has been inputted
        username = request.form.get("username")
        if not username:
            return apology("No input for username", 400)

        # checks if username already exists
        if len(db.execute("SELECT username FROM users WHERE username=?", username)) > 0:
            return apology("username already exists", 400)

        # checks if password has been inputted
        password = request.form.get("password")
        if not password:
            return apology("No input for password", 400)

        # checks if confirmation has been inputted
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("No input for confirmation", 400)

        profile = request.form.get("profile")
        if not confirmation:
            return apology("No input for profile", 400)

        # checks if confirmation equals password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password does not equal confirmation", 400)

        # inserts registration into users sql table
        db.execute("INSERT INTO users (username, hash, profilepic) VALUES (?, ?, ?)", username, generate_password_hash(password), profile)
        session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", username)
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/post", methods=["GET", "POST"])
def post():
    """Makes post"""
    if request.method == "POST":

        # gets required information from fields
        image = request.form.get("image")
        song = request.form.get("song")
        caption = request.form.get("caption")
        rating = request.form.get("rating")
        artist = request.form.get("artist")
        genre = request.form.get("genre")
        session_id = session["user_id"][0].get("id")

        name = ("SELECT username FROM users WHERE id = ?", session_id)

        # checks that all fields have been filled
        if not (image or song or caption or rating or artist or genre) :
            return apology("Lacking input", 400)

        # insert song and all accompanying information into database
        db.execute("INSERT INTO posts (user_id, image, caption, rating, artist, song, genre) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   session_id, image, caption, rating, artist, song, genre)

        return redirect("/")

    else:
        # if form not submitted via POST, return post page
        session_id = session["user_id"][0].get("id")

        user = ("SELECT * FROM users WHERE id = ?", session_id)
        return render_template("post.html", user=user)


@app.route("/profile")
def profile():

    # set session to the current user
    session_id = session["user_id"][0].get("id")

    # get all posts from the "posts" SQL database that this user has specfically posted
    user_posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session_id)
    user = db.execute("SELECT * FROM users WHERE id = ?", session_id)[0]

    # determine the total number of posts for later use in the profile.html template
    num_posts = 0
    for row in user_posts:
        num_posts = num_posts + 1

    return render_template("profile.html", user_posts=user_posts, user=user, num_posts = num_posts)

@app.route("/leaderboard")
def leaderboard():

    # query "posts" SQL database to add the ratings of every unique song
    aggregated = db.execute("SELECT song, artist, SUM(rating) AS totalpoints FROM posts GROUP BY song ORDER BY totalpoints DESC")

    # pass into leaderboard.html template
    return render_template("leaderboard.html", aggregated=aggregated)