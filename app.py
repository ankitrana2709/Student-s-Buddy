import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///buddy.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM students WHERE id= ?", user_id)[
        0]["username"]
    username = [username]
    return render_template("index.html", username=username)


@app.route("/boons")
@login_required
def boons():
    return render_template("boons.html")


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
        rows = db.execute(
            "SELECT * FROM students WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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


@app.route("/average", methods=["GET", "POST"])
@login_required
def average():
    if request.method == "POST":
        return render_template("average.html")
    else:
        user_id = session["user_id"]
        Fhours = db.execute("SELECT SUM(hours) FROM logbook WHERE user_id = ? ", user_id)[
            0]["SUM(hours)"]
        Chours = db.execute("SELECT COUNT(hours) FROM logbook WHERE user_id = ? ", user_id)[
            0]["COUNT(hours)"]
        A = Fhours / Chours
        Avg = round(A,2)
        list = [Fhours, Chours, Avg]
    return render_template("average.html", list=list)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # to check if it is empty
        if not username:
            return apology("Username field is Empty.")
        # to check if password is empty
        if not password:
            return apology("Password field is Empty.")
        # to check if Confirmation is empty
        if not confirmation:
            return apology("Confirmation is not Given.")
        # to check if passwords are not same
        if password != confirmation:
            return apology("Passwords do not match.")
        hash = generate_password_hash(password)

        try:
            # INSERT INTO table
            new_user = db.execute(
                "INSERT INTO students (username, hash) VALUES (?,?)", username, hash)
        except:
            return apology("Username already exists")
        session["user_id"] = new_user
        return redirect("/")


@app.route("/My_Report")
@login_required
def My_Report():
    user_id = session["user_id"]
    tasks = db.execute(
        "SELECT date, hours, minutes, progress, new_aim FROM logbook WHERE user_id = ? ORDER BY id DESC", user_id)
    return render_template("My_Report.html", tasks=tasks)


@app.route("/Add_Report", methods=["GET", "POST"])
@login_required
def Add_Report():
    """Register a new report"""
    if request.method == "GET":
        return render_template("Add_Report.html")
    else:
        user_id = session["user_id"]
        date = request.form.get("date")
        hours = request.form.get("hours")
        minutes = request.form.get("minutes")
        progress = request.form.get("progress")
        new_aim = request.form.get("new_aim")
        
        try:
            progress = progress.upper()
            new_aim = new_aim.upper()
            # INSERT INTO table
            new_log = db.execute("INSERT INTO logbook (user_id, date, hours, minutes, progress, new_aim) VALUES (?,?,?,?,?,?)",
                                 user_id, date, hours, minutes, progress, new_aim)
        except:
            return apology("Log already exists")
        flash("Added!")
        return redirect("/My_Report")
