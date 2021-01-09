import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import datetime

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
db = SQL("sqlite:///project.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
def index():
    return render_template("index.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/portal")

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
    if request.method == "POST":

        if len(request.form.get("password")) < 8:
            return apology("Password must be 8 or more characters long", 403)

        if not request.form.get("username"):
            return apology("You must provide a username!", 403)

        if not request.form.get("firstname"):
            return apology("You must provide a First Name!", 403)

        if not request.form.get("lastname"):
            return apology("You must provide a Last Name!", 403)

        if not request.form.get("email"):
            return apology("You must provide an email address!", 403)

        if not request.form.get("password"):
            return apology("You must provide a password!", 403)

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Password and Confirmation must match!")


        hash = generate_password_hash(request.form.get("password"))

        usernames = db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username"))

        if len(usernames) != 0:
            return apology("username taken", 400)

        new_user_id = db.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES(:username, :password, :firstname, :lastname, :email)",
                                username=request.form.get("username"),
                                password=hash,
                                firstname=request.form.get("firstname"),
                                lastname=request.form.get("lastname"),
                                email=request.form.get("email"))

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect("/portal")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        #The actual matching algorithm with match_count as the total number of people I matched to you

        role=request.form.get("role")

        if role == "tutor":
            match_role = "student"
        else:
            match_role = "tutor"

        grade_info = db.execute("SELECT match.id FROM grades match JOIN grades main WHERE main.id=:main_id AND main.id != match.id AND match.role=:match_role AND (main.kindergarten=match.kindergarten OR main.first= match.first OR main.second=match.second OR main.third=match.third OR main.fourth=match.fourth OR main.fifth= match.fifth OR main.sixth=match.sixth OR main.seventh=match.seventh OR main.eighth=match.eighth OR main.ninth=match.ninth OR main.tenth=match.tenth OR main.eleventh=match.eleventh OR main.twelfth=match.twelfth)", main_id=session["user_id"], match_role=match_role)

        grade_match_usernames = []

        for match in grade_info:
            grade_id = match["id"]
            grade_match_usernames.append(grade_id)

        grade_match_usernames = list(set(grade_match_usernames))

        subject_info = db.execute("SELECT match.id FROM subjects match JOIN subjects main WHERE main.id=:main_id AND main.id != match.id AND match.role=:match_role AND (main.english=match.english OR main.history= match.history OR main.math=match.math OR main.chemistry=match.chemistry OR main.physics=match.physics OR main.biology= match.biology OR main.music=match.music OR main.compsci=match.compsci OR main.french=match.spanish OR main.other=match.other)", main_id=session["user_id"], match_role=match_role)

        subject_match_usernames = []

        for match in subject_info:
            subject_id = match["id"]
            subject_match_usernames.append(subject_id)



        #Housekeeping
        #db.execute("UPDATE users SET active=:active WHERE id=:id", active="no", id=session["user_id"])

        #Email the person

        return redirect("/portal")
    else:
        return render_template("match.html", match_count=3)

@app.route("/portal")
@login_required
def portal():
    name = db.execute("SELECT firstname FROM users WHERE id = :id", id=session["user_id"])
    firstname = name[0]["firstname"]
    return render_template("portal.html", name=firstname)

@app.route("/student", methods=["GET", "POST"])
@login_required
def student():
    if request.method == "POST":
        kindergarten = request.form.get("kindergarten")
        first = request.form.get("first")
        second = request.form.get("second")
        third = request.form.get("third")
        fourth = request.form.get("fourth")
        fifth = request.form.get("fifth")
        sixth = request.form.get("sixth")
        seventh = request.form.get("seventh")
        eighth = request.form.get("eighth")
        ninth = request.form.get("ninth")
        tenth = request.form.get("tenth")
        eleventh = request.form.get("eleventh")
        twelfth = request.form.get("twelfth")

        count = db.execute("SELECT id FROM grades WHERE id=:id AND role=:role", id=session["user_id"], role='student')

        if len(count) == 1:
            db.execute("UPDATE grades SET kindergarten=:kindergarten, first=:first, second=:second, third=:third, fourth=:fourth, fifth=:fifth, sixth=:sixth, seventh=:seventh, eighth=:eighth, ninth=:ninth, tenth=:tenth, eleventh=:eleventh, twelfth=:twelfth WHERE id = :user_id AND role=:role", kindergarten=kindergarten, first=first, second=second, third=third, fourth=fourth, fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth, ninth=ninth, tenth=tenth, eleventh=eleventh, twelfth=twelfth, user_id=session["user_id"], role="student")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO grades (id, role, kindergarten, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth) VALUES (:id, :role, :kindergarten, :first, :second, :third, :fourth, :fifth, :sixth, :seventh, :eighth, :ninth, :tenth, :eleventh, :twelfth)",
                    id=session["user_id"], role="student", kindergarten=kindergarten, first=first, second=second, third=third, fourth=fourth, fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth,
                    ninth=ninth, tenth=tenth, eleventh=eleventh, twelfth=twelfth)


        english = request.form.get("english")
        history = request.form.get("history")
        math = request.form.get("math")
        chemistry = request.form.get("chemistry")
        physics = request.form.get("physics")
        biology = request.form.get("biology")
        french = request.form.get("french")
        spanish = request.form.get("spanish")
        music = request.form.get("music")
        compsci = request.form.get("compsci")

        count = db.execute("SELECT id FROM subjects WHERE id=:id AND role=:role", id=session["user_id"], role='student')

        if len(count) == 1:

            db.execute("UPDATE subjects SET english=:english, history=:history, math=:math, chemistry=:chemistry, physics=:physics, biology=:biology, french=:french, spanish=:spanish, music=:music, compsci=:compsci WHERE id = :user_id AND role=:role", english=english, history=history, math=math, chemistry=chemistry, physics=physics, biology=biology, french=french, spanish=spanish, music=music, compsci=compsci, user_id=session["user_id"], role="student")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO subjects (id, role, english, history, math, chemistry, physics, biology, french, spanish, music, compsci) VALUES (:id, :role, :english, :history, :math, :chemistry, :physics, :biology, :french, :spanish, :music, :compsci)",
                    id=session["user_id"], role="student", english=english, history=history, math=math, chemistry=chemistry, physics=physics, biology=biology, french=french, spanish=spanish, music=music, compsci=compsci)



        v_8M = request.form.get("v_8M")
        v_8T =request.form.get("v_8T")
        v_8W =request.form.get("v_8W")
        v_8R = request.form.get("v_8R")
        v_8F = request.form.get("v_8F")
        v_8S =request.form.get("v_8S")
        v_8U = request.form.get("v_8U")

        v_10M = request.form.get("v_10M")
        v_10T =request.form.get("v_10T")
        v_10W =request.form.get("v_10W")
        v_10R = request.form.get("v_10R")
        v_10F = request.form.get("v_10F")
        v_10S =request.form.get("v_10S")
        v_10U = request.form.get("v_10U")

        v_12M = request.form.get("v_12M")
        v_12T =request.form.get("v_12T")
        v_12W =request.form.get("v_12W")
        v_12R = request.form.get("v_12R")
        v_12F = request.form.get("v_12F")
        v_12S =request.form.get("v_12S")
        v_12U = request.form.get("v_12U")

        v_2M = request.form.get("v_2M")
        v_2T =request.form.get("v_2T")
        v_2W =request.form.get("v_2W")
        v_2R = request.form.get("v_2R")
        v_2F = request.form.get("v_2F")
        v_2S =request.form.get("v_2S")
        v_2U = request.form.get("v_2U")

        v_4M = request.form.get("v_4M")
        v_4T =request.form.get("v_4T")
        v_4W =request.form.get("v_4W")
        v_4R = request.form.get("v_4R")
        v_4F = request.form.get("v_4F")
        v_4S =request.form.get("v_4S")
        v_4U = request.form.get("v_4U")

        v_6M = request.form.get("v_6M")
        v_6T = request.form.get("v_6T")
        v_6W =request.form.get("v_6W")
        v_6R = request.form.get("v_6R")
        v_6F = request.form.get("v_6F")
        v_6S =request.form.get("v_6S")
        v_6U = request.form.get("v_6U")

        v_8NM = request.form.get("v_8NM")
        v_8NT =request.form.get("v_8NT")
        v_8NW =request.form.get("v_8NW")
        v_8NR = request.form.get("v_8NR")
        v_8NF = request.form.get("v_8NF")
        v_8NS =request.form.get("v_8NS")
        v_8NU = request.form.get("v_8NU")

        count = db.execute("SELECT user_id FROM schedule WHERE user_id=:id AND role=:role", id=session["user_id"], role='student')

        if len(count) == 1:

            db.execute("UPDATE schedule SET v_8M=:v_8M, v_8T=:v_8T, v_8W=:v_8W, v_8R=:v_8R, v_8F=:v_8F, v_8S=:v_8S, v_8U=:v_8U, v_10M=:v_10M, v_10T=:v_10T, v_10W=:v_10W, v_10R=:v_10R, v_10F=:v_10F, v_10S=:v_10S, v_10U=:v_10U, v_12M=:v_12M, v_12T=:v_12T, v_12W=:v_12W, v_12R=:v_12R, v_12F=:v_12F, v_12S=:v_12S, v_12U=:v_12U, v_2M=:v_2M, v_2T=:v_2T, v_2W=:v_2W, v_2R=:v_2R, v_2F=:v_2F, v_2S=:v_2S, v_2U=:v_2U, v_4M=:v_4M, v_4T=:v_4T, v_4W=:v_4W, v_4R=:v_4R, v_4F=:v_4F, v_4S=:v_4S, v_4U=:v_4U, v_6M=:v_6M, v_6T=:v_6T, v_6W=:v_6W, v_6R=:v_6R, v_6F=:v_6F, v_6S=:v_6S, v_6U=:v_6U, v_8NM=:v_8NM, v_8NT=:v_8NT, v_8NW=:v_8NW, v_8NR=:v_8NR, v_8NF=:v_8NF, v_8NS=:v_8NS, v_8NU=:v_8NU WHERE user_id = :user_id AND role=:role", v_8M=v_8M, v_8T=v_8T, v_8W=v_8W, v_8R=v_8R, v_8F=v_8F, v_8S=v_8S, v_8U=v_8U, v_10M=v_10M, v_10T=v_10T, v_10W=v_10W, v_10R=v_10R, v_10F=v_10F, v_10S=v_10S, v_10U=v_10U, v_12M=v_12M, v_12T=v_12T, v_12W=v_12W, v_12R=v_12R, v_12F=v_12F, v_12S=v_12S, v_12U=v_12U, v_2M=v_2M, v_2T=v_2T, v_2W=v_2W, v_2R=v_2R, v_2F=v_2F, v_2S=v_2S, v_2U=v_2U, v_4M=v_4M, v_4T=v_4T, v_4W=v_4W, v_4R=v_4R, v_4F=v_4F, v_4S=v_4S, v_4U=v_4U, v_6M=v_6M, v_6T=v_6T, v_6W=v_6W, v_6R=v_6R, v_6F=v_6F, v_6S=v_6S, v_6U=v_6U, v_8NM=v_8NM, v_8NT=v_8NT, v_8NW=v_8NW, v_8NR=v_8NR, v_8NF=v_8NF, v_8NS=v_8NS, v_8NU=v_8NU, user_id=session["user_id"], role="student")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO schedule (user_id, role, v_8M, v_8T, v_8W, v_8R, v_8F, v_8S, v_8U, v_10M, v_10T, v_10W, v_10R, v_10F, v_10S, v_10U, v_12M, v_12T, v_12W, v_12R, v_12F, v_12S, v_12U, v_2M, v_2T, v_2W, v_2R, v_2F, v_2S, v_2U, v_4M, v_4T, v_4W, v_4R, v_4F, v_4S, v_4U, v_6M, v_6T, v_6W, v_6R, v_6F, v_6S, v_6U, v_8NM, v_8NT, v_8NW, v_8NR, v_8NF, v_8NS, v_8NU) VALUES(:user_id, :role, :v_8M, :v_8T, :v_8W, :v_8R, :v_8F, :v_8S, :v_8U, :v_10M, :v_10T, :v_10W, :v_10R, :v_10F, :v_10S, :v_10U, :v_12M, :v_12T, :v_12W, :v_12R, :v_12F, :v_12S, :v_12U, :v_2M, :v_2T, :v_2W, :v_2R, :v_2F, :v_2S, :v_2U, :v_4M, :v_4T, :v_4W, :v_4R, :v_4F, :v_4S, :v_4U, :v_6M, :v_6T, :v_6W, :v_6R, :v_6F, :v_6S, :v_6U, :v_8NM, :v_8NT, :v_8NW, :v_8NR, :v_8NF, :v_8NS, :v_8NU)",
                    user_id=session["user_id"], role="student", v_8M=v_8M, v_8T=v_8T, v_8W=v_8W, v_8R=v_8R, v_8F=v_8F, v_8S=v_8S, v_8U=v_8U, v_10M=v_10M, v_10T=v_10T, v_10W=v_10W, v_10R=v_10R, v_10F=v_10F, v_10S=v_10S, v_10U=v_10U, v_12M=v_12M, v_12T=v_12T, v_12W=v_12W, v_12R=v_12R, v_12F=v_12F, v_12S=v_12S, v_12U=v_12U, v_2M=v_2M, v_2T=v_2T, v_2W=v_2W, v_2R=v_2R, v_2F=v_2F, v_2S=v_2S, v_2U=v_2U, v_4M=v_4M, v_4T=v_4T, v_4W=v_4W, v_4R=v_4R, v_4F=v_4F, v_4S=v_4S, v_4U=v_4U, v_6M=v_6M, v_6T=v_6T, v_6W=v_6W, v_6R=v_6R, v_6F=v_6F, v_6S=v_6S, v_6U=v_6U, v_8NM=v_8NM, v_8NT=v_8NT, v_8NW=v_8NW, v_8NR=v_8NR, v_8NF=v_8NF, v_8NS=v_8NS, v_8NU=v_8NU)

        return redirect("/portal")

    else:
        return render_template("student.html")

@app.route("/tutor", methods=["GET", "POST"])
@login_required
def tutor():
    if request.method == "POST":

        kindergarten = request.form.get("kindergarten")
        first = request.form.get("first")
        second = request.form.get("second")
        third = request.form.get("third")
        fourth = request.form.get("fourth")
        fifth = request.form.get("fifth")
        sixth = request.form.get("sixth")
        seventh = request.form.get("seventh")
        eighth = request.form.get("eighth")
        ninth = request.form.get("ninth")
        tenth = request.form.get("tenth")
        eleventh = request.form.get("eleventh")
        twelfth = request.form.get("twelfth")

        count = db.execute("SELECT id FROM grades WHERE id=:id AND role=:role", id=session["user_id"], role='tutor')


        if len(count) == 1:

            db.execute("UPDATE grades SET kindergarten=:kindergarten, first=:first, second=:second, third=:third, fourth=:fourth, fifth=:fifth, sixth=:sixth, seventh=:seventh, eighth=:eighth, ninth=:ninth, tenth=:tenth, eleventh=:eleventh, twelfth=:twelfth WHERE id = :user_id AND role=:role", kindergarten=kindergarten, first=first, second=second, third=third, fourth=fourth, fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth, ninth=ninth, tenth=tenth, eleventh=eleventh, twelfth=twelfth, user_id=session["user_id"], role="tutor")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO grades (id, role, kindergarten, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth) VALUES (:id, :role, :kindergarten, :first, :second, :third, :fourth, :fifth, :sixth, :seventh, :eighth, :ninth, :tenth, :eleventh, :twelfth)",
                    id=session["user_id"], role="tutor", kindergarten=kindergarten, first=first, second=second, third=third, fourth=fourth, fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth,
                    ninth=ninth, tenth=tenth, eleventh=eleventh, twelfth=twelfth)

        english = request.form.get("english")
        history = request.form.get("history")
        math = request.form.get("math")
        chemistry = request.form.get("chemistry")
        physics = request.form.get("physics")
        biology = request.form.get("biology")
        french = request.form.get("french")
        spanish = request.form.get("spanish")
        music = request.form.get("music")
        compsci = request.form.get("compsci")

        count = db.execute("SELECT id FROM subjects WHERE id=:id AND role=:role", id=session["user_id"], role='tutor')

        if len(count) == 1:

            db.execute("UPDATE subjects SET english=:english, history=:history, math=:math, chemistry=:chemistry, physics=:physics, biology=:biology, french=:french, spanish=:spanish, music=:music, compsci=:compsci WHERE id = :user_id AND role=:role", english=english, history=history, math=math, chemistry=chemistry, physics=physics, biology=biology, french=french, spanish=spanish, music=music, compsci=compsci, user_id=session["user_id"], role="tutor")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO subjects (id, role, english, history, math, chemistry, physics, biology, french, spanish, music, compsci) VALUES (:id, :role, :english, :history, :math, :chemistry, :physics, :biology, :french, :spanish, :music, :compsci)",
                    id=session["user_id"], role="tutor", english=english, history=history, math=math, chemistry=chemistry, physics=physics, biology=biology, french=french, spanish=spanish, music=music, compsci=compsci)

        v_8M = request.form.get("v_8M")
        v_8T =request.form.get("v_8T")
        v_8W =request.form.get("v_8W")
        v_8R = request.form.get("v_8R")
        v_8F = request.form.get("v_8F")
        v_8S =request.form.get("v_8S")
        v_8U = request.form.get("v_8U")

        v_10M = request.form.get("v_10M")
        v_10T =request.form.get("v_10T")
        v_10W =request.form.get("v_10W")
        v_10R = request.form.get("v_10R")
        v_10F = request.form.get("v_10F")
        v_10S =request.form.get("v_10S")
        v_10U = request.form.get("v_10U")

        v_12M = request.form.get("v_12M")
        v_12T =request.form.get("v_12T")
        v_12W =request.form.get("v_12W")
        v_12R = request.form.get("v_12R")
        v_12F = request.form.get("v_12F")
        v_12S =request.form.get("v_12S")
        v_12U = request.form.get("v_12U")

        v_2M = request.form.get("v_2M")
        v_2T =request.form.get("v_2T")
        v_2W =request.form.get("v_2W")
        v_2R = request.form.get("v_2R")
        v_2F = request.form.get("v_2F")
        v_2S =request.form.get("v_2S")
        v_2U = request.form.get("v_2U")

        v_4M = request.form.get("v_4M")
        v_4T =request.form.get("v_4T")
        v_4W =request.form.get("v_4W")
        v_4R = request.form.get("v_4R")
        v_4F = request.form.get("v_4F")
        v_4S =request.form.get("v_4S")
        v_4U = request.form.get("v_4U")

        v_6M = request.form.get("v_6M")
        v_6T = request.form.get("v_6T")
        v_6W =request.form.get("v_6W")
        v_6R = request.form.get("v_6R")
        v_6F = request.form.get("v_6F")
        v_6S =request.form.get("v_6S")
        v_6U = request.form.get("v_6U")

        v_8NM = request.form.get("v_8NM")
        v_8NT =request.form.get("v_8NT")
        v_8NW =request.form.get("v_8NW")
        v_8NR = request.form.get("v_8NR")
        v_8NF = request.form.get("v_8NF")
        v_8NS =request.form.get("v_8NS")
        v_8NU = request.form.get("v_8NU")

        count = db.execute("SELECT user_id FROM schedule WHERE user_id=:id AND role=:role", id=session["user_id"], role='tutor')

        if len(count) == 1:

            db.execute("UPDATE schedule SET v_8M=:v_8M, v_8T=:v_8T, v_8W=:v_8W, v_8R=:v_8R, v_8F=:v_8F, v_8S=:v_8S, v_8U=:v_8U, v_10M=:v_10M, v_10T=:v_10T, v_10W=:v_10W, v_10R=:v_10R, v_10F=:v_10F, v_10S=:v_10S, v_10U=:v_10U, v_12M=:v_12M, v_12T=:v_12T, v_12W=:v_12W, v_12R=:v_12R, v_12F=:v_12F, v_12S=:v_12S, v_12U=:v_12U, v_2M=:v_2M, v_2T=:v_2T, v_2W=:v_2W, v_2R=:v_2R, v_2F=:v_2F, v_2S=:v_2S, v_2U=:v_2U, v_4M=:v_4M, v_4T=:v_4T, v_4W=:v_4W, v_4R=:v_4R, v_4F=:v_4F, v_4S=:v_4S, v_4U=:v_4U, v_6M=:v_6M, v_6T=:v_6T, v_6W=:v_6W, v_6R=:v_6R, v_6F=:v_6F, v_6S=:v_6S, v_6U=:v_6U, v_8NM=:v_8NM, v_8NT=:v_8NT, v_8NW=:v_8NW, v_8NR=:v_8NR, v_8NF=:v_8NF, v_8NS=:v_8NS, v_8NU=:v_8NU WHERE user_id = :user_id AND role=:role", v_8M=v_8M, v_8T=v_8T, v_8W=v_8W, v_8R=v_8R, v_8F=v_8F, v_8S=v_8S, v_8U=v_8U, v_10M=v_10M, v_10T=v_10T, v_10W=v_10W, v_10R=v_10R, v_10F=v_10F, v_10S=v_10S, v_10U=v_10U, v_12M=v_12M, v_12T=v_12T, v_12W=v_12W, v_12R=v_12R, v_12F=v_12F, v_12S=v_12S, v_12U=v_12U, v_2M=v_2M, v_2T=v_2T, v_2W=v_2W, v_2R=v_2R, v_2F=v_2F, v_2S=v_2S, v_2U=v_2U, v_4M=v_4M, v_4T=v_4T, v_4W=v_4W, v_4R=v_4R, v_4F=v_4F, v_4S=v_4S, v_4U=v_4U, v_6M=v_6M, v_6T=v_6T, v_6W=v_6W, v_6R=v_6R, v_6F=v_6F, v_6S=v_6S, v_6U=v_6U, v_8NM=v_8NM, v_8NT=v_8NT, v_8NW=v_8NW, v_8NR=v_8NR, v_8NF=v_8NF, v_8NS=v_8NS, v_8NU=v_8NU, user_id=session["user_id"], role="tutor")
            db.execute("UPDATE users SET active=:active WHERE id=:id", active="yes", id=session["user_id"])

        else:
            db.execute("INSERT INTO schedule (user_id, role, v_8M, v_8T, v_8W, v_8R, v_8F, v_8S, v_8U, v_10M, v_10T, v_10W, v_10R, v_10F, v_10S, v_10U, v_12M, v_12T, v_12W, v_12R, v_12F, v_12S, v_12U, v_2M, v_2T, v_2W, v_2R, v_2F, v_2S, v_2U, v_4M, v_4T, v_4W, v_4R, v_4F, v_4S, v_4U, v_6M, v_6T, v_6W, v_6R, v_6F, v_6S, v_6U, v_8NM, v_8NT, v_8NW, v_8NR, v_8NF, v_8NS, v_8NU) VALUES(:user_id, :role, :v_8M, :v_8T, :v_8W, :v_8R, :v_8F, :v_8S, :v_8U, :v_10M, :v_10T, :v_10W, :v_10R, :v_10F, :v_10S, :v_10U, :v_12M, :v_12T, :v_12W, :v_12R, :v_12F, :v_12S, :v_12U, :v_2M, :v_2T, :v_2W, :v_2R, :v_2F, :v_2S, :v_2U, :v_4M, :v_4T, :v_4W, :v_4R, :v_4F, :v_4S, :v_4U, :v_6M, :v_6T, :v_6W, :v_6R, :v_6F, :v_6S, :v_6U, :v_8NM, :v_8NT, :v_8NW, :v_8NR, :v_8NF, :v_8NS, :v_8NU)",
                    user_id=session["user_id"], role="tutor", v_8M=v_8M, v_8T=v_8T, v_8W=v_8W, v_8R=v_8R, v_8F=v_8F, v_8S=v_8S, v_8U=v_8U, v_10M=v_10M, v_10T=v_10T, v_10W=v_10W, v_10R=v_10R, v_10F=v_10F, v_10S=v_10S, v_10U=v_10U, v_12M=v_12M, v_12T=v_12T, v_12W=v_12W, v_12R=v_12R, v_12F=v_12F, v_12S=v_12S, v_12U=v_12U, v_2M=v_2M, v_2T=v_2T, v_2W=v_2W, v_2R=v_2R, v_2F=v_2F, v_2S=v_2S, v_2U=v_2U, v_4M=v_4M, v_4T=v_4T, v_4W=v_4W, v_4R=v_4R, v_4F=v_4F, v_4S=v_4S, v_4U=v_4U, v_6M=v_6M, v_6T=v_6T, v_6W=v_6W, v_6R=v_6R, v_6F=v_6F, v_6S=v_6S, v_6U=v_6U, v_8NM=v_8NM, v_8NT=v_8NT, v_8NW=v_8NW, v_8NR=v_8NR, v_8NF=v_8NF, v_8NS=v_8NS, v_8NU=v_8NU)

        return redirect("/portal")

    else:
        return render_template("tutor.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
