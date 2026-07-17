from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import db
from models.product import Product
from models.order import Order
from models.category import Category
from utils.decorators import admin_required
from PIL import Image
import os
import io

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ── Helper: Simpan gambar sebagai WebP otomatis ──
def save_image_as_webp(file, upload_folder="static/images", quality=82):
    """Terima file upload apapun (PNG/JPG/WEBP) → simpan sebagai WebP."""
    os.makedirs(upload_folder, exist_ok=True)

    # Baca gambar dengan Pillow
    img = Image.open(file.stream)

    # Konversi RGBA → RGB jika perlu (WebP mendukung keduanya, tapi aman)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")

    # Resize jika terlalu besar (max 1200px di sisi terpanjang)
    max_size = 1200
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)

    # Nama file → selalu .webp
    original_name = os.path.splitext(file.filename)[0]
    safe_name     = original_name.replace(" ", "_").replace("/", "_")
    filename      = f"{safe_name}.webp"
    save_path     = os.path.join(upload_folder, filename)

    # Simpan sebagai WebP
    img.save(save_path, "WebP", quality=quality, method=6)

    return f"/static/images/{filename}"


@admin_bp.route("/")
@admin_required
def dashboard():
    product_count = Product.query.count()
    order_count   = Order.query.count()
    return render_template("admin/dashboard.html",
                           product_count=product_count,
                           order_count=order_count)

@admin_bp.route("/products")
@admin_required
def products():
    products = Product.query.all()
    return render_template("admin/products.html", products=products)

@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def product_form():
    categories = Category.query.all()
    if request.method == "POST":
        image_url = request.form.get("image_url", "")

        # Auto-convert upload ke WebP
        file = request.files.get("image_file")
        if file and file.filename:
            try:
                image_url = save_image_as_webp(file)
                flash(f"✅ Gambar otomatis dikonvert ke WebP!", "success")
            except Exception as e:
                flash(f"⚠️ Gagal proses gambar: {e}", "warning")

        product = Product(
            name           = request.form["name"],
            description    = request.form.get("description", ""),
            price          = float(request.form["price"]),
            original_price = float(request.form["original_price"]) if request.form.get("original_price") else None,
            stock          = int(request.form["stock"]),
            category_id    = int(request.form["category_id"]),
            image_url      = image_url,
            slug           = request.form["name"].lower().replace(" ", "-")
        )
        db.session.add(product)
        db.session.commit()
        flash("Produk berhasil ditambahkan!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", categories=categories, product=None)


@admin_bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def product_edit(product_id):
    product    = Product.query.get_or_404(product_id)
    categories = Category.query.all()

    if request.method == "POST":
        product.name        = request.form["name"]
        product.description = request.form.get("description", "")
        product.price       = float(request.form["price"])
        product.original_price = float(request.form["original_price"]) if request.form.get("original_price") else None
        product.stock       = int(request.form["stock"])
        product.category_id = int(request.form["category_id"])
        product.slug        = request.form["name"].lower().replace(" ", "-")

        # Prioritas 1: upload file → auto convert ke WebP
        file = request.files.get("image_file")
        if file and file.filename:
            try:
                product.image_url = save_image_as_webp(file)
                flash("✅ Gambar otomatis dikonvert ke WebP!", "success")
            except Exception as e:
                flash(f"⚠️ Gagal proses gambar: {e}", "warning")

        # Prioritas 2: URL manual
        elif request.form.get("image_url"):
            product.image_url = request.form["image_url"]

        db.session.commit()
        flash("Produk berhasil diperbarui!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_edit.html", product=product, categories=categories)


@admin_bp.route("/products/delete/<int:product_id>", methods=["POST"])
@admin_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    # Hapus file gambar juga jika ada di static/images
    if product.image_url and product.image_url.startswith("/static/images/"):
        img_path = product.image_url.lstrip("/")
        if os.path.exists(img_path):
            os.remove(img_path)
    db.session.delete(product)
    db.session.commit()
    flash("Produk berhasil dihapus.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/orders")
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)