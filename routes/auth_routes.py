from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash  # For password security!
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

# Make sure to set the secret key and session lifetime in your app's main file:
# app.secret_key = 'a-very-strong-key'
# app.permanent_session_lifetime = timedelta(days=7)

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if "user" in session:
        flash("Already logged in.")
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        session.permanent = True
        # Ensure your login form input is named 'username'
        user_name = request.form.get("username", "")
        password = request.form.get("password", "")
        found_user = Users.query.filter_by(name=user_name).first()
        if found_user and found_user.check_password(password):
            session["user"] = user_name
            session["email"] = found_user.email
            flash("Login Successful!")
            # Optionally regenerate session ID here for security.
            return redirect(url_for("user.dashboard"))
        else:
            flash("Invalid username or password. Please try again or register.")
    return render_template('login.html')


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if "user" in session:
        flash("Already logged in.")
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        user_name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        age = int(request.form.get("age", 0))
        gender = request.form.get("gender", "")
        height = float(request.form.get("height", 0))
        weight = float(request.form.get("weight", 0))
        blood_type = request.form.get("blood_type", "")
        allergies = request.form.get("allergies", "")
        past_illnesses = request.form.get("past_illnesses", "")

        existing_user = Users.query.filter_by(name=user_name).first()
        existing_email = Users.query.filter_by(email=email).first()
        
        if existing_user:
            flash("Username already exists! Please choose a different one.")
            return render_template('register.html')
        if existing_email:
            flash("Email already exists! Please choose a different one.")
            return render_template('register.html')

        new_user = Users(
            name=user_name,
            email=email,
            password=password,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            blood_type=blood_type,
            allergies=allergies,
            past_illnesses=past_illnesses
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))
    return render_template('register.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()  # safer, clears all session keys
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
