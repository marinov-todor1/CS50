import os
import time

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from js.jquery import jquery
from datetime import date, timedelta, datetime
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, flash
from flask_mail import Mail, Message
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure the mail server
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite db
db = SQL("sqlite:///model.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # Total number of patient with due date in the next 14 days
    try:
        # Check today's date
        today = date.today()
        end_date = today + timedelta(days=14)
        
        # Gather all alerts for the current period
        alerts = db.execute("SELECT * FROM alerts WHERE due_date BETWEEN ? AND ?", today, end_date)
        
        # Collect patients details based on the alerts
        for i in alerts:
            patient = db.execute("SELECT * FROM patients WHERE patients_id = ?", i["patients_id"])
            i["patient_phone"] = patient[0]["patient_phone"]
            i["patient_name"] = patient[0]["patient_name"]
            i["patient_mail"] = patient[0]["patient_mail"]

        patients = alerts
        
        # Render the home page
        return render_template("index.html", patients=patients)

    except:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        # Render the login page
        return render_template("login.html")

    # User reached route via POST
    elif request.method == "POST":

        # Ensure username/email was submitted
        if not request.form.get("user_email"):
            return apology("email is a required field", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("password is a required field", 400)

        # Query databes for username/email
        rows = db.execute("SELECT * FROM users WHERE user_email = ?", request.form.get("user_email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return apology("username or password are incorrect!", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to homepage
        return redirect("/")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "GET":
        return render_template("/change_password.html")

    elif request.method == "POST":

        # retrieve old password hash value
        rows = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])

        # check if the inserted old pass is correct
        if check_password_hash((rows[0]["password_hash"]), request.form.get("old_password")):
            # check if the new password was confirmed correctly
            if request.form.get("new_password") == request.form.get("confirmation"):
                # update the password has with the new value
                db.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", generate_password_hash(
                    request.form.get("new_password")), session["user_id"])
                return redirect("/")
            else:
                return apology("the new password does not match", 400)
        else:
            return apology("the old password does not match", 400)


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route vie POST
    if request.method == "POST":

        # Ensure username/email was submitted
        if not request.form.get("user_email"):
            return apology("must provide email", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted correctly
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        if request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation does not match", 400)

        # Query the db for username/email
        rows = db.execute("SELECT * FROM users WHERE user_email = ?;", request.form.get("user_email"))

        # Check if the email has already been used
        if len(rows) == 0:

            # Register the user
            db.execute("INSERT INTO users (user_first_name, user_last_name, user_phone, user_email, password_hash) VALUES (?, ?, ?, ?, ?);", request.form.get(
                "user_first_name"), request.form.get("user_last_name"), request.form.get("user_phone"), request.form.get(
                    "user_email"), generate_password_hash(request.form.get("password")))

            # Create a session (log the user in) for the user and return them to the index page
            new_usr = db.execute("SELECT * FROM users WHERE user_email = ?", request.form.get("user_email"))
            session["user_id"] = new_usr[0]["user_id"]
            return redirect("/")

        else:
            return apology("the email has already been registered", 400)

    # User reached route vie GET
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():

    # Load the add patient form if the user reaches via GET
    if request.method == "GET":
        return render_template("add_patient.html")

    # Add the patient to the db, linked to the currently logged doc user if reached via POST
    elif request.method == "POST":

        # create new record in the patients table
        patient_name = request.form.get("patient_name")
        patient_phone = request.form.get("patient_phone")
        patient_mail = request.form.get("patient_mail")
        new_patient_id = db.execute("INSERT INTO patients (patient_name, patient_phone, patient_mail) VALUES (?, ?, ?)", patient_name, patient_phone, patient_mail)

        # create new record in the my_patients table
        db.execute("INSERT INTO my_patients VALUES (?, ?)", session["user_id"], new_patient_id)

        # if there is data in the due_date field, create new record in the alerts table
        if not request.form.get("due_date") == "":
            status = "pending"
            db.execute("INSERT INTO alerts (status, due_date, patients_id, user_id) VALUES (?, ?, ?, ?)", status, request.form.get("due_date"), new_patient_id, session["user_id"])

        return redirect("/")


@app.route("/all_patients")
@login_required
def all_patients():

    # gather all patients data for the currently logged doctor
    patients = db.execute("SELECT * FROM patients JOIN alerts ON patients.patients_id = alerts.patients_id WHERE patients.patients_id IN (SELECT patients_id FROM my_patients WHERE user_id = ?);", session["user_id"])

    return render_template("all_patients.html", patients=patients)


@app.route("/edit_patient", methods=["GET", "POST", "PUT"])
@login_required
def edit_patient():

    # if the request comes as a POST -> update the patient data in the sql db
    if request.method == "POST":

        # gather the new data from the submitted form
        patient_name = request.form.get("patient_name")
        patient_phone = request.form.get("patient_phone")
        patient_mail = request.form.get("patient_mail")
        due_date = request.form.get("due_date")
        patient_id = request.form.get("patient_id")

        # update the patients table
        db.execute("UPDATE patients SET patient_name = ?, patient_phone = ?, patient_mail = ? WHERE patients_id = ?", patient_name, patient_phone, patient_mail, patient_id)

        # update the due_date table if the date was changed
        old_due_date = db.execute("SELECT due_date FROM alerts WHERE patients_id = ?", patient_id)

        if old_due_date[0]["due_date"] != due_date:
            db.execute("UPDATE alerts SET due_date = ?, status = ? WHERE patients_id = ? AND user_id = ?", due_date, "pending", patient_id, session["user_id"])
        message = "Patient ID " + patient_id + " details were successfully updated."
        flash(message)
        return redirect("/all_patients")

    # Remove a patient if btn Delete was clicked
    elif request.method == "PUT":

        patient_id = request.form
        db.execute("DELETE FROM my_patients WHERE patients_id = ?", patient_id["patient_id"])
        db.execute("DELETE FROM alerts WHERE patients_id = ?", patient_id["patient_id"])
        db.execute("DELETE FROM patients WHERE patients_id = ?", patient_id["patient_id"])
        
        return redirect("/all_patients")

    return render_template("edit_patient.html")


def notifications():
    """Sends out notifications to soon to be due patients"""
    with app.app_context():

        # Check today's date, the alert period and query the db for the alert's details
        today = date.today()
        due_in_14 = today + timedelta(days=14)
        due_alerts = db.execute("SELECT * FROM alerts WHERE due_date = ?", due_in_14)
        
        # Get all patients which need to be notified
        for i in due_alerts:
            patient = db.execute("SELECT * FROM patients WHERE patients_id = ?", i["patients_id"])
            doc = db.execute("SELECT * FROM users WHERE user_id = ?", i["user_id"])
            i["patient_phone"] = patient[0]["patient_phone"]
            i["patient_name"] = patient[0]["patient_name"]
            i["patient_mail"] = patient[0]["patient_mail"]
            i["doc_last_name"] = doc[0]["user_last_name"]
            i["doc_first_name"] = doc[0]["user_first_name"]
            i["doc_email"] = doc[0]["user_email"]
            i["doc_phone"] = doc[0]["user_phone"]
        
        # Send all notifications from the preconfigured email box
        try:
            # Open a connection with the mail server
            with mail.connect() as conn:
    
                # Loop through the patients and generate a message
                for alert in due_alerts:

                    message = ("Dear " + alert["patient_name"] + ", your periodic profilactic examination wis due on " + str(due_in_14) +
                    ". Please consider reaching out to doctor " + alert["doc_first_name"] + " " + alert["doc_last_name"] + " at phone number: " +
                    str(alert["doc_phone"]) + " or email: " + alert["doc_email"])
    
                    subject = "Periodic prolicatic examination is due on " + str(due_in_14)
                    msg = Message(recipients=[alert["patient_mail"]],
                          body=message,
                          subject=subject)
                    # Send the message
                    conn.send(msg)

                    db.execute("UPDATE alerts SET status = 'sent' WHERE alert_id = ?;", alert["alert_id"])
        except:
            print("notification failed!")

# Prevent scheduled job duplication in debug environment
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    
    # Schedule the notification job to run every day
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=notifications, trigger="interval", days=1)
    scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())