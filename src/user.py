from flask import Blueprint, redirect, url_for, request, render_template, flash,session
from . import db
user_bp = Blueprint('user',__name__)
@user_bp.route('/')
def User():
    return 'hello'