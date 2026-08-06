from app import app
from database import db
from models.user import User
from models.category import Category
from models.product import Product
from werkzeug.security import generate_password_hash

with app.app_context():
    # Kategori
    cats = [
        Category(name="Piala",    slug="piala"),
        Category(name="Trofi",    slug="trofi"),
        Category(name="Medali",   slug="medali"),
        Category(name="Plakat",   slug="plakat"),
        Category(name="Souvenir", slug="souvenir"),
    ]
    for c in cats:
        if not Category.query.filter_by(slug=c.slug).first():
            db.session.add(c)
    db.session.commit()

    piala    = Category.query.filter_by(slug="piala").first()
    trofi    = Category.query.filter_by(slug="trofi").first()
    medali   = Category.query.filter_by(slug="medali").first()
    plakat   = Category.query.filter_by(slug="plakat").first()
    souvenir = Category.query.filter_by(slug="souvenir").first()

    # Produk
    products = [
        Product(name="Piala Emas Premium",    slug="piala-emas-premium",    price=85000,  original_price=120000, stock=50,  category_id=piala.id,    image_url="https://picsum.photos/seed/p1/400/400",  is_featured=True, total_sold=120),
        Product(name="Piala Perak Klasik",    slug="piala-perak-klasik",    price=65000,  original_price=90000,  stock=40,  category_id=piala.id,    image_url="https://picsum.photos/seed/p2/400/400",  total_sold=80),
        Product(name="Piala Marmer Mewah",    slug="piala-marmer-mewah",    price=150000, stock=20,              category_id=piala.id,    image_url="https://picsum.photos/seed/p3/400/400",  is_featured=True, total_sold=45),
        Product(name="Trofi Bintang Emas",    slug="trofi-bintang-emas",    price=95000,  original_price=130000, stock=35,  category_id=trofi.id,    image_url="https://picsum.photos/seed/p4/400/400",  is_featured=True, total_sold=200),
        Product(name="Trofi Akrilik Modern",  slug="trofi-akrilik-modern",  price=75000,  stock=45,              category_id=trofi.id,    image_url="https://picsum.photos/seed/p5/400/400",  total_sold=95),
        Product(name="Trofi Kristal Premium", slug="trofi-kristal-premium", price=200000, stock=15,              category_id=trofi.id,    image_url="https://picsum.photos/seed/p6/400/400",  total_sold=30),
        Product(name="Medali Emas Olimpiade", slug="medali-emas-olimpiade", price=45000,  stock=100,             category_id=medali.id,   image_url="https://picsum.photos/seed/p7/400/400",  total_sold=300),
        Product(name="Medali Perak Custom",   slug="medali-perak-custom",   price=35000,  stock=100,             category_id=medali.id,   image_url="https://picsum.photos/seed/p8/400/400",  total_sold=250),
        Product(name="Medali Perunggu Sport", slug="medali-perunggu-sport", price=30000,  stock=100,             category_id=medali.id,   image_url="https://picsum.photos/seed/p9/400/400",  total_sold=180),
        Product(name="Plakat Kayu Jati",      slug="plakat-kayu-jati",      price=120000, original_price=160000, stock=30,  category_id=plakat.id,   image_url="https://picsum.photos/seed/p10/400/400", is_featured=True, total_sold=60),
        Product(name="Plakat Akrilik Laser",  slug="plakat-akrilik-laser",  price=85000,  stock=40,              category_id=plakat.id,   image_url="https://picsum.photos/seed/p11/400/400", total_sold=75),
        Product(name="Plakat Marmer Premium", slug="plakat-marmer-premium", price=175000, stock=20,              category_id=plakat.id,   image_url="https://picsum.photos/seed/p12/400/400", total_sold=25),
        Product(name="Gantungan Kunci Custom",slug="gantungan-kunci-custom",price=15000,  stock=200,             category_id=souvenir.id, image_url="https://picsum.photos/seed/p13/400/400", total_sold=500),
        Product(name="Mug Custom Foto",       slug="mug-custom-foto",       price=55000,  stock=80,              category_id=souvenir.id, image_url="https://picsum.photos/seed/p14/400/400", total_sold=150),
        Product(name="Bingkai Foto Kayu",     slug="bingkai-foto-kayu",     price=70000,  original_price=95000,  stock=60,  category_id=souvenir.id, image_url="https://picsum.photos/seed/p15/400/400", total_sold=90),
    ]
    for p in products:
        if not Product.query.filter_by(slug=p.slug).first():
            db.session.add(p)
    db.session.commit()

    # Hapus admin lama jika ada, buat ulang
    old_admin = User.query.filter_by(email="rizkiputrasaimonaarmen@students.amikom.ac.id").first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()

    admin = User(
        username="rizki_admin",
        email="rizkiputrasaimonaarmen@students.amikom.ac.id",
        password=generate_password_hash("Saimona12345"),
        full_name="Rizki Putra Saimona Armen",
        is_admin=True,
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()

    print("Seed selesai!")
    print("Login Admin:")
    print("  Email    : rizkiputrasaimonaarmen@students.amikom.ac.id")
    print("  Password : Saimona12345")
    print("  URL      : http://127.0.0.1:5000/auth/admin-login")