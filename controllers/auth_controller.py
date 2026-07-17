from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models.user import User
from utils.validators import FormValidator
from utils.email import EmailService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username         = request.form.get("username", "").strip()
        email            = request.form.get("email", "").strip()
        password         = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or len(username) < 3:
            flash("Username minimal 3 karakter", "danger")
            return redirect(url_for("auth.register"))

        if not FormValidator.validate_email(email):
            flash("Email tidak valid", "danger")
            return redirect(url_for("auth.register"))

        is_valid, msg = FormValidator.validate_password(password)
        if not is_valid:
            flash(msg, "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Password tidak cocok", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email sudah terdaftar", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil! Silakan login", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email, is_admin=False).first()

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash("Akun Anda sudah dinonaktifkan", "danger")
                return redirect(url_for("auth.login"))
            login_user(user, remember=request.form.get("remember"))
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.home"))

        flash("Email atau password salah", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email, is_admin=True).first()

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash("Akun admin dinonaktifkan", "danger")
                return redirect(url_for("auth.admin_login"))
            login_user(user)
            flash("Selamat datang, Admin!", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Email atau password admin salah", "danger")

    return render_template("auth/admin_login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout", "success")
    return redirect(url_for("main.home"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user  = User.query.filter_by(email=email).first()
        if user:
            flash("Link reset password telah dikirim ke email Anda", "success")
            return redirect(url_for("auth.login"))
        flash("Email tidak ditemukan", "danger")
    return render_template("auth/forgot_password.html")