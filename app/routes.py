from flask import Blueprint, render_template, request, redirect, session

main = Blueprint('main', __name__)

users = {}

@main.route('/')
def home():
    return redirect('/login')

@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        if u in users and users[u] == p:
            session['user'] = u
            return redirect('/dashboard')

    return render_template("login.html")


@main.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        users[u] = p
        return redirect('/login')

    return render_template("register.html")


@main.route('/dashboard', methods=['GET','POST'])
def dashboard():

    crops = None
    profit = None

    if request.method == 'POST':
        state = request.form['state']

        # Dummy output (replace with ML later)
        crops = [
            {"crop":"Maize","predicted_yield":55,"modal_price":2400},
            {"crop":"Groundnut","predicted_yield":52,"modal_price":9800}
        ]

        profit = [
            {"crop":"Groundnut","expected_profit":270000},
            {"crop":"Maize","expected_profit":48000}
        ]

    return render_template("dashboard.html", crops=crops, profit=profit)
