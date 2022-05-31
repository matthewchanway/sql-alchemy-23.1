"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

connect_db(app)
db.create_all()

@app.route("/users")
def show_users():
    users = User.query.all()
    return render_template("users-list.html",users=users)

@app.route("/users/new")
def show_add_user_form():
    return render_template("add-user-form.html")

@app.route("/users/new", methods = ["POST"])
def add_new_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name = first_name, last_name = last_name, profile_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<userid>", methods = ["GET","POST"])
def show_user_info(userid):
    user = User.query.get(userid)
    return render_template("user-detail.html",user=user)

@app.route("/users/<userid>/edit")
def show_edit_form(userid):
    user = User.query.get(userid)
    return render_template("edit-user-info.html",user=user)

@app.route("/users/<userid>/edit", methods = ["POST"])
def handle_edit_form(userid):
    user = User.query.get(userid)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user.first_name = first_name
    user.last_name = last_name
    user.profile_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<userid>/delete", methods = ["GET","POST"])
def delete_user(userid):
    User.query.filter(User.id == userid).delete()
    db.session.commit()
    return redirect("/users")