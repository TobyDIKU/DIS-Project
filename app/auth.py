import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if not re.fullmatch(r"[a-z]{3}[0-9]{3}@alumni\.ku\.dk", email):
            flash("Email must be 3 lowercase letters followed by 3 digits, e.g. rkn812@alumni.ku.dk.", "error")
            return render_template("register.html")

        if not re.fullmatch(r"[a-zA-Z0-9_]{3,20}", username):
            flash("Username must be 3–20 characters and contain only letters, digits, or underscores.", "error")
            return render_template("register.html")

        if not re.fullmatch(r"(?=.*\d).{8,}", password):
            flash("Password must be at least 8 characters and contain at least one digit.", "error")
            return render_template("register.html")

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Email or username already taken.", "error")
            return render_template("register.html")

        flash("Account created — please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
