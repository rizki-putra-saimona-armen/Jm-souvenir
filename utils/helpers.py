from datetime import datetime
import random
import string
 
class Helpers:
    """Helper functions umum"""
    
    @staticmethod
    def generate_order_number():
        """Generate nomor pesanan unik"""
        timestamp = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"ORD-{timestamp}-{random_part}"
    
    @staticmethod
    def generate_tracking_number():
        """Generate nomor resi pengiriman"""
        return 'JMS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    
    @staticmethod
    def format_currency(amount):
        """Format angka menjadi format Rupiah"""
        return f"Rp {amount:,.0f}"
    
    @staticmethod
    def format_date(date_obj):
        """Format tanggal"""
        if date_obj:
            return date_obj.strftime('%d %B %Y')
        return "-"
    
    @staticmethod
    def format_datetime(datetime_obj):
        """Format datetime"""
        if datetime_obj:
            return datetime_obj.strftime('%d %B %Y %H:%M')
        return "-"
    
    @staticmethod
    def slugify(text):
        """Convert text to slug"""
        import re
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')
    
    @staticmethod
    def calculate_discount_amount(original_price, discount_percent):
        """Hitung nilai diskon"""
        return (original_price * discount_percent) / 100
    
    @staticmethod
    def get_user_initials(full_name):
        """Ambil inisial nama"""
        parts = full_name.split()
        return ''.join([p[0].upper() for p in parts])[:2]
    
    @staticmethod
    def paginate(items, page, per_page=12):
        """Paginasi items"""
        total = len(items)
        total_pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        
        return {
            'items': items[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
