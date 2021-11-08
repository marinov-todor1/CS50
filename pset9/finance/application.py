import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # query the db to gather all holdings of the current user
    try:
        holdings = db.execute("SELECT * FROM balance WHERE users_id = ? AND balance > 0", session["user_id"])

        # create a list of dicts holding the current cash balance and total (cash+stock value)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        grand_total = cash[0]["cash"]

        # create a list of dicts for current prices of each symbol in holdings
        for item in holdings:
            current_symbol = lookup(item["symbol"])
            item["price"] = current_symbol["price"]
            item["total"] = round(current_symbol["price"] * item["balance"], 2)
            grand_total += item["total"]

        summary = {}
        summary["cash"] = round(cash[0]["cash"], 2)
        summary["grand_total"] = round(grand_total, 2)

        return render_template("index.html", holdings=holdings, summary=summary)

    except:
        return redirect("/login")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":

        # check if the requested symbol is valid
        current_quote = lookup(request.form.get("symbol"))
        if current_quote == None:
            return apology("Invalid ticker symbol", 400)

        # query the db for the available cash of the current user
        usr_cash_temp = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        usr_cash = float(usr_cash_temp[0]['cash'])

        # check if the provided value is a positive integer
        requested_shares = request.form.get("shares")
        if not requested_shares.isnumeric():
            return apology("Number of shares must be a positive integer", 400)
        elif int(requested_shares) <= 0:
            return apology("Number of shares must be a positive integer", 400)
        elif isinstance(requested_shares, int):
            return apology("Number of shares must be a positive integer", 400)

        qty = int(requested_shares)

        current_price = float(current_quote['price'])
        symbol = request.form.get("symbol")
        current_time = datetime.now()

        # check if the amount of cash is sufficient to purchase the requested stock & qty
        if usr_cash - (qty*current_price) >= 0:
            db.execute("INSERT INTO transactions (users_id, symbol, qty, price, time) VALUES (?, ?, ?, ?, ?)",
                       session["user_id"], symbol, qty, current_price, current_time)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", (usr_cash - qty * current_price), session["user_id"])

          # update the balance of holdings if the transaction was successful
            # check if there is any available holding of the same stock
            try:
                balance = db.execute("SELECT balance FROM balance WHERE users_id = ? AND symbol = ?", session["user_id"], symbol)
                db.execute("UPDATE balance SET balance = ? WHERE users_id = ? AND symbol = ?",
                           (qty+balance[0]["balance"]), session["user_id"], symbol)
                return redirect("/")
            # create a holding record for the given stock, since it is a first time buy
            except:
                db.execute("INSERT INTO balance (users_id, symbol, balance) VALUES (?, ?, ?)", session["user_id"], symbol, qty)
                return redirect("/")
        else:
            return apology("Not enough cash", 404)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE users_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
    elif request.method == "POST":

        result = lookup(request.form.get("symbol"))

        # check if the quoted symbol is valid
        if result == None:
            return apology("no such stock was found", 400)

        return render_template("quoted.html", res=result)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change the old password"""

    if request.method == "GET":
        return render_template("/change_password.html")

    elif request.method == "POST":

        # retrieve old password hash
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # check if the inserted old password is correct
        if check_password_hash(rows[0]["hash"], request.form.get("old_password")):
           # check if the new password was confirmed correctly
            if request.form.get("new_password") == request.form.get("confirmation"):
                # update the password hash with the new value
                db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
                    request.form.get("new_password")), session["user_id"])
                return redirect("/")
            else:
                return apology("the new password does not match", 400)
        else:
            return apology("the old password does not match", 400)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submittin a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted correctly
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation does not match", 400)

        # Query the database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check if the username has already been taken
        if len(rows) == 0:

            # Register the user
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

            new_usr = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))
            # Create a session (log them in) for the user and return them to the index page
            session["user_id"] = new_usr[0]["id"]
            return redirect("/")

        else:
            return apology("the user name already exists", 400)

    # User reached route via GET (as by clicking on the Register button, willing to create new reg)
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM balance WHERE users_id = ? AND balance > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        # Retrieve the total holding of shares from the symbol requested for sell
        try:
            usr_stocks_temp = db.execute("SELECT balance FROM balance WHERE users_id = ? AND symbol = ?",
                                         session["user_id"], symbol)
        except:
            return apology("You don't have any shares from that stock")

        usr_shares = usr_stocks_temp[0]["balance"]

        # Check if the user owns enough shares to sell the requested qty
        if usr_shares < shares:
            return apology("Not enough shares", 400)
        elif shares <= 0:
            return apology("You must provide a positve number of shares to be sold", 400)

        # update the user stock balance and cash amount
        try:
            db.execute("UPDATE balance SET balance = ? WHERE users_id = ? AND symbol = ?",
                       usr_shares - shares, session["user_id"], symbol)
            current_quote = lookup(symbol)
            current_price = float(current_quote['price'])
            profit = shares * current_price
            current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash[0]["cash"] + profit, session["user_id"])
        except:
            return apology("something went wrong", 400)

        # record the transaction into the transactions table
        current_time = datetime.now()
        db.execute("INSERT INTO transactions (users_id, symbol, qty, price, time) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares*-1, current_price, current_time)

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
