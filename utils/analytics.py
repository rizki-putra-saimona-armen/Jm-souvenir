from models.order import Order
from models.product import Product
from models.user import User
from datetime import datetime, timedelta
 
class AnalyticsService:
    """Layanan analytics untuk admin"""
    
    @staticmethod
    def get_sales_summary(days=30):
        """Dapatkan ringkasan penjualan"""
        start_date = datetime.now() - timedelta(days=days)
        orders = Order.query.filter(Order.created_at >= start_date).all()
        
        total_orders = len(orders)
        total_revenue = sum(o.total for o in orders)
        completed_orders = sum(1 for o in orders if o.status == 'completed')
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'completed_orders': completed_orders,
            'average_order_value': total_revenue / total_orders if total_orders > 0 else 0
        }
    
    @staticmethod
    def get_top_products(limit=10):
        """Produk terlaris"""
        products = Product.query.order_by(Product.total_sold.desc()).limit(limit).all()
        return [{
            'id': p.id,
            'name': p.name,
            'sold': p.total_sold,
            'rating': p.average_rating,
            'price': p.price
        } for p in products]
    
    @staticmethod
    def get_customer_stats():
        """Statistik pelanggan"""
        total_users = User.query.filter_by(is_admin=False).count()
        new_users_today = User.query.filter(
            User.joined_date >= datetime.now().date()
        ).count()
        
        return {
            'total_users': total_users,
            'new_users_today': new_users_today
        }
    
    @staticmethod
    def get_daily_revenue(days=30):
        """Revenue per hari"""
        data = {}
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            orders = Order.query.filter(
                Order.created_at >= date,
                Order.created_at < date + timedelta(days=1)
            ).all()
            
            revenue = sum(o.total for o in orders)
            data[date_str] = revenue
        
        return data
