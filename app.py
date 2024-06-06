from flask import Flask, render_template, request, redirect, url_for, session, flash
from jinja2 import Environment

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {
    "john_doe": {
        "username": "john_doe",
        "password": "pass1",
        "job": "Mechanic",
        "contact": "john_doe@example.com",
        "phone": "+2347012345678",
        "ratings": [4, 5],
    },
    "jane_smith": {
        "username": "jane_smith",
        "password": "pass2",
        "job": "Plumber",
        "contact": "jane_smith@example.com",
        "phone": "+2347012345679",
        "ratings": [3],
    },
    "michael_lee": {
        "username": "michael_lee",
        "password": "pass3",
        "job": "Sales Girl",
        "contact": "michael_lee@example.com",
        "phone": "+2347012345680",
        "ratings": [],
    },
    "emma_wilson": {
        "username": "emma_wilson",
        "password": "pass4",
        "job": "Electrician",
        "contact": "emma_wilson@example.com",
        "phone": "+2347012345681",
        "ratings": [5, 4, 4],
    },
    "david_clark": {
        "username": "david_clark",
        "password": "pass5",
        "job": "Carpenter",
        "contact": "david_clark@example.com",
        "phone": "+2347012345682",
        "ratings": [4],
    },
}

jobs = [
    "Mechanic",
    "Plumber",
    "Electrician",
    "Carpenter",
    "Painter",
    "Welder",
    "Tailor",
    "Bricklayer",
    "Driver",
    "Security Guard",
    "Cleaner",
    "Gardener",
    "Fisherman",
    "Butcher",
    "Barber",
    "Hairdresser",
    "Sales Girl",
    "Receptionist",
    "Waiter",
    "Chef",
    "Delivery Person",
]


def jinja2_sum(iterable):
    return sum(iterable)


def jinja2_len(iterable):
    return len(iterable)


env = Environment()
env.filters["sum"] = jinja2_sum
env.filters["length"] = jinja2_len


@app.route("/")
def index():
    return render_template("index.html", users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("profile"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        job = request.form["job"]
        email = request.form["email"]
        phone = request.form["phone"]
        if username not in users:
            users[username] = {
                "username": username,
                "password": password,
                "job": job,
                "email": email,
                "phone": phone,
                "ratings": [],
            }
            session["username"] = username
            return redirect(url_for("profile"))
        else:
            flash("Username already exists")
    return render_template("register.html", jobs=jobs)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    if username not in users:
        flash("User not found")
        return redirect(url_for("index"))
    user = users[username]
    if request.method == "POST":
        users[username]["job"] = request.form["job"]
        users[username]["email"] = request.form["email"]
        users[username]["phone"] = request.form["phone"]
        flash("Profile updated")
    return render_template("profile.html", user=user, jobs=jobs)


@app.route("/rate", methods=["POST"])
def rate():
    username = request.form["username"]
    rating = int(request.form["rating"])
    if username in users and 1 <= rating <= 5:
        users[username]["ratings"].append(rating)
        flash("Rating submitted")
    else:
        flash("Invalid rating or user not found")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
