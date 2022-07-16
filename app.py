import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import datetime
import time
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, wrong, login_required, lookup, usd, limit

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")



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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    stocks = db.execute("SELECT symbol,price, SUM(shares) AS Tshares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id =?", user_id)[0]["cash"]
    total = cash
    for stock in stocks:
        total += stock["price"] * stock["Tshares"]

    return render_template("index.html", stocks=stocks, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        result = lookup(symbol)

        if not symbol:
            return apology("Give a Symbol")

        elif not result:
            return apology("Symbol is not valid.")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be integers.")
        if shares <= 0:
            return apology("Share number is not valid.")
        user_id = session["user_id"]
        item_price = result["price"]
        item_name = result["name"]
        symbol = result["symbol"]
        transaction_value = shares * item_price
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cash < transaction_value:
            return apology("Not enough Money.")
        else:
            date = datetime.datetime.now()
            updated_cash = cash - transaction_value
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
            # INSERT INTO table
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                       user_id, result["symbol"], shares, item_price, date)
        message = "Bought! for " + usd(item_price)
        flash(message)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id= :id", id=user_id)
    return render_template("history.html", transactions=transactions_db)


@app.route("/analyst")
@login_required
def analyst():
    return render_template("analyst.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Adding more cash"""
    if request.method == "GET":
        return render_template("add_cash.html")
    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("Put In few bucks atleast.")
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        updated_cash = user_cash + new_cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        return redirect("/")


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
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        #username = db.execute("SELECT username FROM users WHERE id =?", session["user_id"])[0]["username"]

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
    if not symbol:
        return apology("Give a Symbol")
    # symbols are in upper case
    result = lookup(symbol.upper())
    if result == None:
        return apology("Symbol is not valid.")
    return render_template("quoted.html", name=result["name"], price=usd(result["price"]), symbol=result["symbol"])


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
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
        except:
            return apology("Username already exists")
        session["user_id"] = new_user
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Give a Symbol")

         # symbols are in upper case
        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol is not valid.")

        if shares < 0:
            return apology("Share number is not valid.")

        transaction_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id=:id AND symbol = :symbol GROUP BY symbol", id=user_id, symbol=symbol)
        user_shares_now = user_shares[0]["shares"]

        if shares > user_shares_now:
            return apology("Not enough shares!")

        updated_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        date = datetime.datetime.now()
        # INSERT INTO table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1)*shares, stock["price"], date)

        flash("Sold!")
        return redirect("/")

