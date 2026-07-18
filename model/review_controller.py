from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from database import db
from models.review import Review
from models.product import Product
from models.order import Order, OrderItem
from utils.decorators import login_required_custom
 
review_bp = Blueprint("review", __name__, url_prefix="/review")
 
@review_bp.route("/product/<int:product_id>/create", methods=["POST"])
@login_required_custom
def create_review(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if user has purchased
    has_purchased = OrderItem.query.filter(
        OrderItem.product_id == product_id,
        Order.user_id == current_user.id
    ).join(Order).first()
    
    rating = request.form.get("rating", type=int)
    title = request.form.get("title", "").strip()
    comment = request.form.get("comment", "").strip()
    
    # Validasi
    if not (1 <= rating <= 5):
        flash("Rating harus 1-5", "danger")
        return redirect(url_for("product.detail", product_id=product_id))
    
    if len(title) < 5:
        flash("Judul minimal 5 karakter", "danger")
        return redirect(url_for("product.detail", product_id=product_id))
    
    if len(comment) < 20:
        flash("Komentar minimal 20 karakter", "danger")
        return redirect(url_for("product.detail", product_id=product_id))
    
    # Check if already reviewed
    existing = Review.query.filter_by(
        product_id=product_id,
        user_id=current_user.id
    ).first()
    
    if existing:
        flash("Anda sudah memberikan review", "warning")
        return redirect(url_for("product.detail", product_id=product_id))
    
    review = Review(
        product_id=product_id,
        user_id=current_user.id,
        rating=rating,
        title=title,
        comment=comment,
        is_verified=bool(has_purchased)
    )
    
    db.session.add(review)
    
    # Update product rating
    update_product_rating(product_id)
    
    db.session.commit()
    
    flash("Review berhasil ditambahkan", "success")
    return redirect(url_for("product.detail", product_id=product_id))
 
def update_product_rating(product_id):
    """Update rating produk"""
    reviews = Review.query.filter_by(product_id=product_id).all()
    
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        product = Product.query.get(product_id)
        product.average_rating = round(avg_rating, 1)
        product.total_reviews = len(reviews)
 
@review_bp.route("/<int:review_id>/helpful", methods=["POST"])
@login_required_custom
def mark_helpful(review_id):
    review = Review.query.get_or_404(review_id)
    review.helpful += 1
    db.session.commit()
    
    return jsonify({'success': True, 'helpful': review.helpful})