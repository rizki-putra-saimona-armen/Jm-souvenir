from models.promo import Promotion
from datetime import datetime
 
class PromoService:
    """Layanan untuk mengelola promo"""
    
    @staticmethod
    def validate_promo_code(code, order_total):
        """Validasi dan dapatkan diskon dari kode promo"""
        promo = Promotion.query.filter_by(code=code.upper()).first()
        
        if not promo:
            return {
                'valid': False,
                'message': 'Kode promo tidak ditemukan'
            }
        
        if not promo.is_valid():
            return {
                'valid': False,
                'message': 'Kode promo sudah expired atau tidak aktif'
            }
        
        if order_total < promo.min_purchase:
            return {
                'valid': False,
                'message': f'Pembelian minimum Rp {promo.min_purchase:,.0f}'
            }
        
        # Hitung diskon
        if promo.discount_type == 'percent':
            discount = order_total * promo.discount_value / 100
            if promo.max_discount:
                discount = min(discount, promo.max_discount)
        else:
            discount = promo.discount_value
        
        return {
            'valid': True,
            'message': 'Kode promo valid',
            'discount': discount,
            'promo': promo
        }
    
    @staticmethod
    def apply_promo_code(order, promo_code):
        """Apply promo ke order"""
        result = PromoService.validate_promo_code(promo_code, order.subtotal)
        
        if result['valid']:
            order.promo_code = promo_code
            order.discount = result['discount']
            result['promo'].used_count += 1
            return True, result['discount']
        
        return False, result['message']