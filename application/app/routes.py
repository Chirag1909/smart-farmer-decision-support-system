from flask import Blueprint, render_template, request, redirect, session
from .ml_engine import *

main = Blueprint("main", __name__)

users = {}

@main.route("/")
def home():
    return redirect("/login")

@main.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/dashboard")

    return render_template("login.html")


@main.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        users[u] = p
        return redirect("/login")

    return render_template("register.html")


@main.route("/dashboard", methods=["GET","POST"])
def dashboard():
    states = get_states()
    crops = None

    if request.method == "POST":
        state = request.form["state"]
        crops = top_k_crops(state).to_dict("records")

    return render_template("dashboard.html", states=states, crops=crops)


@main.route("/profit", methods=["GET","POST"])
def profit():
    states = get_states()
    data = None

    if request.method == "POST":
        state = request.form["state"]
        data = profit_forecast(state).to_dict("records")

    return render_template("profit.html", states=states, data=data)


@main.route("/mandi", methods=["GET","POST"])
def mandi():
    states = get_states()
    data = None

    if request.method == "POST":
        state = request.form["state"]
        data = mandi_prices(state).to_dict("records")

    return render_template("mandi.html", states=states, data=data)


@main.route("/weather", methods=["GET","POST"])
def weather():
    data = None

    if request.method == "POST":
        state = request.form["state"]

        API_KEY = "9809ac00cd0f719f6bb4f02ca140c36a"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={state},IN&appid={API_KEY}&units=metric"

        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            data = {
                "temp": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "condition": weather_data["weather"][0]["description"],
                "wind": weather_data["wind"]["speed"]
            }
        else:
            data = {"error": "City not found"}

    states = get_states()
    return render_template("weather.html", data=data, states=states)