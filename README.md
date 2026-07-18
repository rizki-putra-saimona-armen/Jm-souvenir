<div align="center">

#  JM Souvenir

### Platform E-Commerce untuk Piala, Trofi, Medali & Plakat

Toko online berbasis Flask untuk pemesanan piala, trofi, medali, plakat, dan souvenir custom — lengkap dengan katalog produk, keranjang belanja, sistem review, dashboard admin, dan integrasi WhatsApp untuk konsultasi pesanan.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-D71F00?style=flat&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#-lisensi)

</div>

---

##  Fitur Utama

###  Untuk Pelanggan
- **Katalog produk** dengan filter kategori (Piala, Trofi, Medali, Plakat, Souvenir) dan pencarian
- **Keranjang belanja** & checkout
- **Autentikasi pengguna** — registrasi, login, kelola profil
- **Alamat pengiriman** & riwayat pesanan
- **Wishlist** produk favorit
- **Ulasan & rating** produk
- **Konsultasi via WhatsApp** langsung dari halaman produk/kontak
- **Notifikasi** status pesanan
- **Kode promo / diskon**

###  Untuk Admin
- **Dashboard** ringkasan penjualan & statistik
- **Manajemen produk** (tambah/edit/hapus, upload gambar)
- **Manajemen pesanan & pelanggan**
- **Manajemen promosi/diskon**
- **Laporan penjualan**
- **Pengaturan toko**

---

##  Tech Stack

| Layer | Teknologi |
|---|---|
| **Backend** | Flask 3.0, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-CORS |
| **Database** | SQLite (default) — siap migrasi ke PostgreSQL (`psycopg2-binary` sudah termasuk) |
| **Task Queue** | Celery + Redis *(opsional, untuk proses async seperti notifikasi email)* |
| **Payment** | Stripe & Midtrans *(siap integrasi)* |
| **Frontend** | Jinja2 Templates, CSS, JavaScript vanilla |
| **Server** | Gunicorn (production) |

---

##  Struktur Proyek

```
trophy-flask/
├── app.py                  # Entry point aplikasi Flask
├── config.py               # Konfigurasi (dev/production/testing)
├── seed.py                 # Script seeding data awal (kategori & produk)
├── requirements.txt
├── controllers/            # Blueprint & route handler
│   ├── auth_controller.py
│   ├── main_controller.py
│   ├── cart_controller.py
│   ├── product_controller.py
│   ├── review_controller.py
│   ├── admin_controller.py
│   └── inquiry_controller.py
├── models/                 # Model SQLAlchemy
│   ├── user.py  ├── product.py  ├── category.py
│   ├── order.py ├── address.py  ├── review.py
│   ├── wishlist.py ├── notification.py
│   ├── payment.py  └── promo.py
├── utils/                  # Helper & utilitas
│   ├── whatsapp.py         # Integrasi WhatsApp CS
│   ├── email.py            # Pengiriman email
│   ├── shipping.py         # Kalkulasi ongkir
│   ├── promo.py            # Logika kode promo
│   ├── validators.py
│   ├── decorators.py       # Auth guard (login_required, admin_required, dll)
│   └── analytics.py
├── templates/               # Halaman HTML (Jinja2)
│   ├── admin/               # Panel admin
│   ├── auth/                # Login/register
│   ├── user/                # Profil, alamat, wishlist, pesanan
│   └── product/
├── static/
│   ├── css/  ├── js/  └── images/
└── instance/
    └── database.db          # Database SQLite (auto-generated)
```

---

##  Instalasi & Menjalankan

### 1. Clone repository
```bash
git clone https://github.com/<username>/JM-Souvenir.git
cd JM-Souvenir/trophy-flask
```

### 2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi environment
Buat file `.env` di root folder `trophy-flask/`:
```env
FLASK_ENV=development
SECRET_KEY=ganti-dengan-secret-key-anda
DATABASE_URL=sqlite:///instance/database.db

# Email (opsional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@jmsouvenir.com
```

### 5. Seed data awal (kategori & produk contoh)
```bash
python seed.py
```

### 6. Jalankan aplikasi
```bash
python app.py
```
Aplikasi akan berjalan di **http://localhost:5000** 🎉

---

##  Konfigurasi WhatsApp CS

Nomor customer service dapat diatur di `config.py`:
```python
WHATSAPP_CS_NUMBERS = {
    'saimona': '6285664322214',
}
WHATSAPP_DEFAULT_CS = '6285664322214'
```

---

##  Deployment (Production)

Gunakan **Gunicorn** sebagai WSGI server:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

>  Untuk production, disarankan:
> - Set `FLASK_ENV=production`
> - Gunakan PostgreSQL alih-alih SQLite
> - Aktifkan `SESSION_COOKIE_SECURE=True` (sudah otomatis pada `ProductionConfig`)
> - Simpan `SECRET_KEY` & kredensial di environment variable, bukan hardcoded

---

##  Roadmap

- [ ] Integrasi pembayaran otomatis (Stripe / Midtrans)
- [ ] Notifikasi email real-time via Celery + Redis
- [ ] Multi-bahasa (i18n)
- [ ] REST API terpisah untuk mobile app
- [ ] Export laporan penjualan ke Excel/PDF

---

##  Kontribusi

Kontribusi sangat terbuka! Silakan:
1. Fork repository ini
2. Buat branch fitur (`git checkout -b fitur/nama-fitur`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur X'`)
4. Push ke branch (`git push origin fitur/nama-fitur`)
5. Buka Pull Request

---


Dibuat dengan ❤️ untuk **JM Souvenir** — solusi piala, trofi, medali & plakat custom Anda.

</div>
