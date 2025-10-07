"""
Author: Dang Duc Viet
University: Posts and Telecommunications Institute of Technology
Major: D25 - IT UDU
Project Name: 
Class Code: D25CQCC05-B
Student ID: B25DCCC269
Created: 2025-10-08 01:28
"""

from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from os import path


app = Flask(__name__)
app.config["SECRET_KEY"] = "adu a viet dep trai z"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nguoidung.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]  = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(100))
    emails = db.Column(db.String(100))

    def __init__(self, full_name, emails):
        self.full_name = full_name
        self.emails = emails

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login.html")
def redirect_url_for_login():
    return redirect(url_for("login"))

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("fullname")
        email_user = request.form.get("email")

        if username:
            session["user"] = username
            found_user = User.query.filter_by(full_name = username).first()

            if found_user:
                session["email"] = found_user.emails
            else:
                user = User(username, email_user)
                session["email"] = email_user

                db.session.add(user)
                db.session.commit()

            return redirect(url_for("user_page"))
        
    if "user" in session:
        name = session["user"]
        return redirect(url_for("user_page"))

    return render_template("login.html")

@app.route("/user")
def user_page():
    if "user" in session and "email" in session:
        name = session["user"]
        email = session["email"]
        
        return render_template("user.html", user = name, email_user = email )
    
    return redirect(url_for("login"))


@app.route("/logout", methods = ["POST", "GET"])
def logout():
    session.pop("user", None)
    session.pop("email", None)

    return redirect(url_for("login"))

if __name__ == "__main__":
    if not path.exists("nguoidung.db"):
        with app.app_context():
            db.create_all()
            print("DATABASE CREATED!")
    app.run(debug = True)