from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import Users

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@user_bp.route('/user')
def dashboard():
    if "user" in session:
        user_name = session["user"]
        found_user = Users.query.filter_by(name=user_name).first()

        if not found_user:
            session.clear()
            flash("Session expired, please log in again.")
            return redirect(url_for("auth.login"))

        
        patient_data = {
            'name': user_name,
            'email': found_user.email if found_user else '',
            'age': found_user.age,
            'gender': found_user.gender,
            'height': found_user.height,
            'blood_type': found_user.blood_type
        }
        health_metrics = {
            'weight': found_user.weight,
            'allergies': found_user.allergies,
            'past_illnesses': found_user.past_illnesses
        }
        return render_template("user.html", patient=patient_data, metrics=health_metrics)
    else:
        flash("You are not logged in!")
        return redirect(url_for("auth.login"))