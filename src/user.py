from flask import Blueprint, redirect, url_for, request, render_template, flash,session
from . import db
user_bp = Blueprint('user',__name__)
@user_bp.route('/')
def User():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('home.html')
@user_bp.route('/department/<int:id>')
def department(id):
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))
    return render_template('user.html')
