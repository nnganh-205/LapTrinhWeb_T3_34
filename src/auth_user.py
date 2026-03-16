from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from . import db
import re
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User

auth = Blueprint('auth_bp', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email và mật khẩu không được để trống', 'warning')
            return redirect(url_for('auth_bp.login'))

        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            flash('Đăng nhập thành công! Chào mừng bạn quay lại.', 'success')
            return redirect(url_for('main.index')) # Thay 'main.index' bằng trang chủ của m
        
        flash('Email hoặc mật khẩu không chính xác', 'danger')
        return redirect(url_for('auth_bp.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user_name = request.form.get('user_name', '').strip()

        if User.query.filter_by(email=email).first():
            flash('Email này đã được đăng ký rồi!', 'warning')
            return redirect(url_for('auth_bp.signup'))

        if len(password) < 8:
            flash('Mật khẩu phải từ 8 ký tự trở lên', 'danger')
            return redirect(url_for('auth_bp.signup'))

        try:
            new_user = User(
                email=email,
                password=generate_password_hash(password),
                user_name=user_name
            )
                    
            db.session.add(new_user)
            db.session.commit()
            
            flash('Đăng ký tài khoản thành công! Hãy đăng nhập.', 'success')
            return redirect(url_for('auth_bp.login'))
        except Exception as e:
            db.session.rollback()
            flash('Đã xảy ra lỗi hệ thống, vui lòng thử lại sau.', 'danger')
            return redirect(url_for('auth_bp.signup'))

    return render_template('signup.html')