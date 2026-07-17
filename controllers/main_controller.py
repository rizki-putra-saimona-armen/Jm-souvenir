from flask import Blueprint, render_template, request
from models.product import Product
from models.category import Category

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    products = Product.query.limit(8).all()
    return render_template("home.html", products=products)

@main_bp.route("/catalog")
def catalog():
    category_slug = request.args.get("category", "").strip()
    keyword       = request.args.get("q", "").strip()

    query = Product.query

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    if keyword:
        query = query.filter(Product.name.ilike(f"%{keyword}%"))

    products   = query.order_by(Product.id.desc()).all()
    categories = Category.query.order_by(Category.id).all()

    return render_template("catalog.html",
                           products=products,
                           categories=categories,
                           keyword=keyword,
                           active_category=category_slug)

@main_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

@main_bp.route("/cara-order")
def cara_order():
    return render_template("cara_order.html")

@main_bp.route("/kontak")
def kontak():
    return render_template("kontak.html")