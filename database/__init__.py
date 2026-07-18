import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def init_db(app):
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login terlebih dahulu'
    login_manager.login_message_category = 'warning'

    mail.init_app(app)

    with app.app_context():
        from models.user import User
        from models.product import Product
        from models.category import Category
        from models.order import Order, OrderItem
        from models.address import Address
        from models.review import Review
        from models.wishlist import Wishlist
        from models.notification import Notification
        from models.payment import PaymentMethod
        from models.promo import Promotion

        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))
