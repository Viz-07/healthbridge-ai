from flask import Blueprint, render_template, session, redirect, url_for, flash
from extensions import db
from models import Users, ChatHistory

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=["GET"])
def settings():
    if "user" not in session:
        flash("You must be logged in to access settings.")
        return redirect(url_for("auth.login"))
    return render_template('settings.html', user=session["user"])

@settings_bp.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        flash('Login required.')
        return redirect(url_for('auth.login'))
    
    user_name = session['user']
    user = Users.query.filter_by(name=user_name).first()
    if user:
        ChatHistory.query.filter_by(user_id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        session.clear()
        flash('Your account has been deleted.')
        return redirect(url_for('auth.register'))
    else:
        flash('User not found.')
        return redirect(url_for('auth.login'))
