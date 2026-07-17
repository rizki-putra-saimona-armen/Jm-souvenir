from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.product import Product

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart")
def view_cart():
    cart  = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            total   += subtotal
            items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", {})
    key  = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    flash("Produk ditambahkan ke keranjang!", "success")
    return redirect(request.referrer or url_for("cart.view_cart"))

@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    key  = str(product_id)
    if key in cart:
        del cart[key]
        session["cart"] = cart
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_qty(product_id):
    cart = session.get("cart", {})
    key  = str(product_id)
    qty  = int(request.form.get("qty", 1))
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty
    session["cart"] = cart
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart/clear", methods=["POST"])
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/checkout")
def checkout():
    return render_template("checkout.html")

@cart_bp.route("/confirmation")
def confirmation():
    session.pop("cart", None)
    return render_template("confirmation.html")