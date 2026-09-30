from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key for session management
app.secret_key = "face-attendance-secret-key"

# Temporary admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/attendance")
def attendance():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("attendance.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)