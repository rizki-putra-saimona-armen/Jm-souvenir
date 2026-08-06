from flask import Flask, render_template, session
from flask_cors import CORS
from config import config
import os

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

from database import init_db, mail
init_db(app)

CORS(app)

# Register blueprints
from controllers.auth_controller import auth_bp
from controllers.main_controller import main_bp
from controllers.cart_controller import cart_bp
from controllers.review_controller import review_bp
from controllers.admin_controller import admin_bp
from controllers.product_controller import product_bp
from controllers.inquiry_controller import inquiry_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(review_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(product_bp)
app.register_blueprint(inquiry_bp)

# Inject variabel global ke semua template
@app.context_processor
def inject_globals():
    try:
        from models.category import Category
        categories = Category.query.all()
    except Exception:
        categories = []

    # Hitung total qty produk di keranjang (session) untuk ditampilkan di badge navbar
    cart = session.get("cart", {})
    cart_count = sum(cart.values()) if cart else 0

    return dict(categories=categories, cart_count=cart_count)

# Template filters
@app.template_filter('currency')
def currency_filter(value):
    from utils.helpers import Helpers
    return Helpers.format_currency(value)

@app.template_filter('date_format')
def date_format_filter(value):
    from utils.helpers import Helpers
    return Helpers.format_date(value)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)