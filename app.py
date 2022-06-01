"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

# Part Two Routes

@app.route("/users/<int:userid>/posts/new")
def show_new_post_form(userid):
    user = User.query.get(userid)
    return render_template("add-post-form.html",user=user)

@app.route("/users/<int:userid>/posts/new", methods = ["POST"])
def add_new_post(userid):
    now = datetime.now()
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title = title, content=content, created_at=now, user_id = userid )
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user_info',userid=userid))

@app.route("/posts/<int:postid>")
def view_post(postid):
    post = Post.query.get(postid)
    
    return render_template("view-post.html",post=post)

@app.route("/posts/<int:postid>/edit")
def show_edit_post_form(postid):
    post = Post.query.get(postid)
    return render_template("edit-post.html",post=post)

@app.route("/posts/<int:postid>/edit", methods = ["POST"])
def handle_edit_post_from(postid):
    post = Post.query.get(postid)
    title = request.form["title"]
    content = request.form["content"]
    post.title = title
    post.content = content
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('view_post',postid=postid))

@app.route("/posts/<int:postid>/delete", methods = ["POST","GET"])
def handle_delete(postid):
    post = Post.query.get(postid)
    userid = post.user_id
    Post.query.filter_by(id=postid).delete()
    db.session.commit()

    return redirect(url_for('show_user_info',userid=userid))
    
