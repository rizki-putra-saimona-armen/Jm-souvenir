from flask_mail import Message
from database import mail   # pakai instance yang sudah init, bukan buat baru

class EmailService:
    """Layanan email notification"""

    @staticmethod
    def send_order_confirmation(user_email, order):
        subject = f"Pesanan Dikonfirmasi - {order.order_number}"
        html_body = f"""
        <h2>Pesanan Dikonfirmasi!</h2>
        <p>Terima kasih telah berbelanja di JM Souvenir</p>
        <p><strong>Nomor Pesanan:</strong> {order.order_number}</p>
        <p><strong>Total:</strong> Rp {order.total:,.0f}</p>
        <p><strong>Status:</strong> {order.status}</p>
        """
        msg = Message(subject, recipients=[user_email], html=html_body)
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    @staticmethod
    def send_shipping_notification(user_email, order, tracking_number):
        subject = f"Pesanan Dikirim - {order.order_number}"
        html_body = f"""
        <h2>Pesanan Anda Dikirim!</h2>
        <p>Pesanan {order.order_number} telah dikirim</p>
        <p><strong>Nomor Resi:</strong> {tracking_number}</p>
        """
        msg = Message(subject, recipients=[user_email], html=html_body)
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    @staticmethod
    def send_review_request(user_email, order, product):
        subject = f"Bagaimana dengan {product.name}?"
        html_body = f"""
        <h2>Bagikan Ulasan Anda</h2>
        <p>Terima kasih telah membeli {product.name}</p>
        <p><a href="http://yoursite.com/product/{product.id}/review">Tulis Ulasan</a></p>
        """
        msg = Message(subject, recipients=[user_email], html=html_body)
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    @staticmethod
    def send_promo_notification(user_email, promo_code, discount):
        subject = f"Promo Spesial untuk Anda! - {promo_code}"
        html_body = f"""
        <h2>Promo Eksklusif!</h2>
        <p>Dapatkan diskon {discount} dengan kode: <strong>{promo_code}</strong></p>
        """
        msg = Message(subject, recipients=[user_email], html=html_body)
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False