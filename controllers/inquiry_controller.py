"""
Inquiry Controller - Handles WhatsApp inquiry requests
Routes for product inquiry, cart inquiry, and contact inquiry
"""
from flask import Blueprint, request, jsonify, session
from utils.whatsapp import WhatsAppService

inquiry_bp = Blueprint('inquiry', __name__, url_prefix='/api/inquiry')


@inquiry_bp.route('/product', methods=['POST'])
def product_inquiry():
    """
    Generate WhatsApp inquiry URL for a specific product
    
    Expected JSON:
    {
        "product_id": "123",
        "product_name": "Piala Trophy",
        "product_price": 150000,
        "quantity": 10,
        "cs_name": "saimona" (optional)
    }
    """
    try:
        data = request.get_json()
        
        product_name = data.get('product_name', 'Produk')
        product_price = data.get('product_price')
        quantity = data.get('quantity', 1)
        cs_name = data.get('cs_name')
        
        # Generate WhatsApp message
        message = WhatsAppService.generate_inquiry_message(
            product_name=product_name,
            product_price=product_price,
            quantity=quantity
        )
        
        # Get CS number
        phone_number = WhatsAppService.get_cs_number(cs_name)
        
        # Generate WhatsApp URL
        whatsapp_url = WhatsAppService.get_whatsapp_url(phone_number, message)
        
        return jsonify({
            'success': True,
            'whatsapp_url': whatsapp_url,
            'message': message,
            'cs_number': phone_number
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@inquiry_bp.route('/cart', methods=['POST'])
def cart_inquiry():
    """
    Generate WhatsApp inquiry URL from cart items
    
    Expected JSON:
    {
        "cart_items": [
            {
                "product_name": "Piala Trophy",
                "price": 150000,
                "quantity": 10
            },
            ...
        ],
        "cs_name": "aulian" (optional)
    }
    
    Or uses session['cart'] if cart_items not provided
    """
    try:
        data = request.get_json()
        cart_items = data.get('cart_items')
        cs_name = data.get('cs_name')
        
        # If cart_items not provided, try to get from session
        if not cart_items and 'cart' in session:
            cart_items = session['cart']
        
        if not cart_items:
            return jsonify({
                'success': False,
                'error': 'Cart is empty'
            }), 400
        
        # Generate WhatsApp message from cart
        message = WhatsAppService.generate_cart_message(cart_items)
        
        # Get CS number
        phone_number = WhatsAppService.get_cs_number(cs_name)
        
        # Generate WhatsApp URL
        whatsapp_url = WhatsAppService.get_whatsapp_url(phone_number, message)
        
        return jsonify({
            'success': True,
            'whatsapp_url': whatsapp_url,
            'message': message,
            'cs_number': phone_number
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@inquiry_bp.route('/contact', methods=['POST'])
def contact_inquiry():
    """
    Generate WhatsApp inquiry URL for general contact/consultation
    
    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Pertanyaan tentang produk",
        "message": "Saya tertarik dengan...",
        "cs_name": "aulian" (optional)
    }
    """
    try:
        data = request.get_json()
        
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message_text = data.get('message')
        cs_name = data.get('cs_name')
        
        # Validate minimum required fields
        if not message_text:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Generate WhatsApp message
        message = WhatsAppService.generate_consultation_message(
            name=name,
            email=email,
            subject=subject,
            message_text=message_text
        )
        
        # Get CS number
        phone_number = WhatsAppService.get_cs_number(cs_name)
        
        # Generate WhatsApp URL
        whatsapp_url = WhatsAppService.get_whatsapp_url(phone_number, message)
        
        return jsonify({
            'success': True,
            'whatsapp_url': whatsapp_url,
            'message': message,
            'cs_number': phone_number
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@inquiry_bp.route('/get-cs-list', methods=['GET'])
def get_cs_list():
    """
    Get list of available customer service agents
    
    Returns JSON with all CS numbers and names
    """
    cs_list = [
        {'name': 'saimona', 'phone': '6285664322214', 'key': 'saimona'},
        
    ]
    
    return jsonify({
        'success': True,
        'cs_list': cs_list,
        'default_cs': 'saimona'
    }), 200


@inquiry_bp.route('/open-whatsapp', methods=['POST'])
def open_whatsapp():
    """
    Redirect to WhatsApp with pre-filled message
    This is used for button clicks
    
    Expected JSON:
    {
        "message": "Inquiry message text",
        "cs_name": "saimona" (optional)
    }
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        cs_name = data.get('cs_name')
        
        phone_number = WhatsAppService.get_cs_number(cs_name)
        whatsapp_url = WhatsAppService.get_whatsapp_url(phone_number, message)
        
        return jsonify({
            'success': True,
            'redirect_url': whatsapp_url
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400