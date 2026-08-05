from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
 
def login_required_custom(f):
    """Custom login required decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Silakan login terlebih dahulu", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
 
def admin_required(f):
    """Admin only decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Silakan login terlebih dahulu", "warning")
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash("Anda tidak memiliki akses ke halaman ini", "danger")
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function
 
def json_response(f):
    """Convert response to JSON"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import jsonify
        result = f(*args, **kwargs)
        return jsonify(result)
    return decorated_function