from flask import Blueprint, render_template, request
from models.product import Product
from models.category import Category

product_bp = Blueprint("product", __name__)

@product_bp.route("/catalog")
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

@product_bp.route("/product/<int:product_id>")
def detail(product_id):
    product    = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    return render_template("product_detail.html", product=product, categories=categories)

@product_bp.route("/search")
def search():
    keyword       = request.args.get("q", "").strip()
    category_slug = request.args.get("category", "").strip()

    query = Product.query

    if keyword:
        query = query.filter(Product.name.ilike(f"%{keyword}%"))

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    products   = query.all()
    categories = Category.query.order_by(Category.id).all()

    return render_template("catalog.html",
                           products=products,
                           categories=categories,
                           keyword=keyword,
                           active_category=category_slug)