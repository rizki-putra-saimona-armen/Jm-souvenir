from datetime import datetime
 
class ShippingCalculator:
    """Menghitung ongkos kirim berdasarkan lokasi"""
    
    # Kota-kota di Jogja yang dapat gratis ongkir
    JOGJA_CITIES = [
        'Yogyakarta',
        'Yogyakarta Kota',
        'Sleman',
        'Bantul',
        'Gunung Kidul',
        'Kulon Progo'
    ]
    
    # Koordinat pusat Jogja (untuk perhitungan jarak)
    JOGJA_CENTER = {'lat': -7.7956, 'lng': 110.3695}
    
    @staticmethod
    def is_jogja(city):
        """Cek apakah kota termasuk Jogja"""
        for jogja_city in ShippingCalculator.JOGJA_CITIES:
            if jogja_city.lower() in city.lower():
                return True
        return False
    
    @staticmethod
    def calculate_shipping(city, distance=None):
        """
        Hitung ongkos kirim
        
        Parameters:
        - city: nama kota
        - distance: jarak dalam km (opsional)
        
        Returns:
        - shipping_cost: biaya pengiriman
        - is_free: apakah gratis ongkir
        """
        
        # Gratis ongkir untuk Jogja
        if ShippingCalculator.is_jogja(city):
            return {
                'cost': 0,
                'is_free': True,
                'description': 'Gratis Ongkir - Yogyakarta'
            }
        
        # Perhitungan untuk luar Jogja berdasarkan jarak
        if distance is None:
            distance = 50  # Default jarak jika tidak diketahui
        
        if distance <= 15:
            cost = 15000
        elif distance <= 30:
            cost = 25000
        elif distance <= 50:
            cost = 35000
        else:
            # Rp 2000 per km untuk jarak > 50 km
            cost = 35000 + (distance - 50) * 2000
        
        return {
            'cost': cost,
            'is_free': False,
            'description': f'Ongkos Kirim - {distance} km'
        }
    
    @staticmethod
    def get_estimated_delivery(shipping_cost):
        """Estimasi waktu pengiriman"""
        from datetime import timedelta
        
        if shipping_cost == 0:  # Jogja
            days = 1
        elif shipping_cost <= 15000:
            days = 2
        elif shipping_cost <= 25000:
            days = 3
        else:
            days = 5
        
        delivery_date = datetime.now() + timedelta(days=days)
        return {
            'days': days,
            'estimated_date': delivery_date.strftime('%Y-%m-%d'),
            'description': f'Estimasi tiba dalam {days} hari kerja'
        }