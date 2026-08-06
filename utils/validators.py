import re
from flask import flash
 
class FormValidator:
    """Validasi form"""
    
    @staticmethod
    def validate_email(email):
        """Validasi email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validasi nomor telepon Indonesia"""
        # Hapus spasi dan karakter khusus
        clean_phone = re.sub(r'[^\d+]', '', phone)
        # Harus dimulai dengan 62 atau 0 dan minimal 10 digit
        if clean_phone.startswith('62'):
            return len(clean_phone) >= 11
        elif clean_phone.startswith('0'):
            return len(clean_phone) >= 10
        return False
    
    @staticmethod
    def validate_password(password):
        """Validasi password"""
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
        if not any(c.isupper() for c in password):
            return False, "Password harus memiliki huruf besar"
        if not any(c.isdigit() for c in password):
            return False, "Password harus memiliki angka"
        return True, "Password valid"
    
    @staticmethod
    def validate_address(street, city, postal_code):
        """Validasi alamat"""
        if len(street) < 5:
            return False, "Alamat jalan terlalu pendek"
        if len(city) < 3:
            return False, "Nama kota tidak valid"
        if not re.match(r'^\d{5}$', postal_code):
            return False, "Kode pos harus 5 digit"
        return True, "Alamat valid"