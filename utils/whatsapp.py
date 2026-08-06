"""
WhatsApp integration utility for inquiry and ordering
Supports generating WhatsApp messages and URLs for customer inquiries
"""
import urllib.parse


class WhatsAppService:
    """Service class for WhatsApp integration"""
    
    # CS (Customer Service) contact numbers
    CS_NUMBERS = {
        'andi': '6285664322214',
       
        
    }
    
    DEFAULT_CS = '6285664322214',# andi as default
    
    @staticmethod
    def get_cs_number(cs_name=None):
        """Get CS WhatsApp number by name or return default"""
        if cs_name and cs_name.lower() in WhatsAppService.CS_NUMBERS:
            return WhatsAppService.CS_NUMBERS[cs_name.lower()]
        return WhatsAppService.DEFAULT_CS
    
    @staticmethod
    def generate_inquiry_message(product_name, product_price=None, quantity=None, description=None):
        """
        Generate WhatsApp inquiry message for a specific product
        
        Args:
            product_name: Name of the product
            product_price: Price of the product (optional)
            quantity: Quantity requested (optional)
            description: Additional description (optional)
        
        Returns:
            Formatted message string
        """
        message = f"Halo, saya tertarik dengan produk: *{product_name}*"
        
        if product_price:
            message += f"\n💰 Harga: Rp {product_price:,}"
        
        if quantity:
            message += f"\n📦 Jumlah: {quantity}"
        
        message += "\n\nBisakah saya mendapatkan informasi lebih lanjut dan penawaran terbaik?"
        
        if description:
            message += f"\n\nKeterangan tambahan: {description}"
        
        return message
    
    @staticmethod
    def generate_cart_message(cart_items):
        """
        Generate WhatsApp message from cart items
        
        Args:
            cart_items: List of cart items with product_name, price, quantity
        
        Returns:
            Formatted message string
        """
        message = "Halo, saya ingin melakukan konsultasi untuk pemesanan berikut:\n\n"
        
        total_price = 0
        for i, item in enumerate(cart_items, 1):
            product_name = item.get('product_name', 'Produk')
            price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            item_total = price * quantity
            total_price += item_total
            
            message += f"{i}. *{product_name}*\n"
            message += f"   Harga: Rp {price:,} x {quantity}\n"
            message += f"   Subtotal: Rp {item_total:,}\n\n"
        
        message += f"📊 Total Harga Estimasi: Rp {total_price:,}\n\n"
        message += "Mohon berikan penawaran terbaik dan informasi pengiriman. Terima kasih!"
        
        return message
    
    @staticmethod
    def generate_consultation_message(name=None, email=None, subject=None, message_text=None):
        """
        Generate WhatsApp message for general consultation/contact
        
        Args:
            name: Customer name
            email: Customer email
            subject: Inquiry subject
            message_text: Detailed message
        
        Returns:
            Formatted message string
        """
        message = "Halo, saya ingin menghubungi tim layanan pelanggan.\n\n"
        
        if name:
            message += f"👤 Nama: {name}\n"
        
        if email:
            message += f"📧 Email: {email}\n"
        
        if subject:
            message += f"📝 Topik: {subject}\n"
        
        message += "\n"
        
        if message_text:
            message += f"Pesan: {message_text}"
        else:
            message += "Saya ingin mendapatkan informasi lebih lanjut."
        
        return message
    
    @staticmethod
    def get_whatsapp_url(phone_number=None, message=""):
        """
        Generate WhatsApp URL for opening chat
        
        Args:
            phone_number: Recipient phone number (without + symbol)
            message: Message text to pre-fill
        
        Returns:
            WhatsApp URL string
        """
        if not phone_number:
            phone_number = WhatsAppService.DEFAULT_CS
        
        # Ensure phone number doesn't have + symbol
        phone_number = str(phone_number).replace('+', '').replace(' ', '')
        
        # Encode message for URL
        encoded_message = urllib.parse.quote(message)
        
        return f"https://wa.me/{phone_number}?text={encoded_message}"
    
    @staticmethod
    def get_direct_whatsapp_link(phone_number=None, message="", button_text="Chat via WhatsApp", class_name="whatsapp-link"):
        """
        Generate HTML link for WhatsApp
        
        Args:
            phone_number: Recipient phone number
            message: Message text
            button_text: Display text for the link/button
            class_name: CSS class name for styling
        
        Returns:
            HTML string with WhatsApp link
        """
        url = WhatsAppService.get_whatsapp_url(phone_number, message)
        
        return f'''<a href="{url}" target="_blank" class="{class_name}" title="{button_text}">
    {button_text}
</a>'''
    
    @staticmethod
    def get_floating_button_html():
        """
        Get HTML/CSS for floating WhatsApp button in bottom-right corner
        
        Returns:
            HTML string with button and styling
        """
        return '''<!-- Floating WhatsApp Button -->
<style>
    .whatsapp-floating-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background-color: #25d366;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 999;
        transition: all 0.3s ease;
        text-decoration: none;
    }
    
    .whatsapp-floating-button:hover {
        background-color: #20ba5c;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        transform: scale(1.1);
    }
    
    .whatsapp-floating-button svg {
        width: 35px;
        height: 35px;
        fill: white;
    }
    
    @media (max-width: 600px) {
        .whatsapp-floating-button {
            bottom: 20px;
            right: 20px;
            width: 55px;
            height: 55px;
        }
        
        .whatsapp-floating-button svg {
            width: 30px;
            height: 30px;
        }
    }
</style>

<a href="https://wa.me/6281328029729?text=Halo%2C%20saya%20tertarik%20dengan%20produk%20Anda" 
   class="whatsapp-floating-button" 
   target="_blank" 
   title="Chat with Customer Service">
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.67-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.076 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.403h-.004a9.87 9.87 0 00-5.031 1.378c-3.055 2.11-5.005 5.644-5.005 9.393 0 1.104.143 2.198.427 3.245L1.9 23.8l3.8-1.188c.95.518 2.027.79 3.178.79h.006c5.546 0 10.045-4.5 10.045-10.045 0-2.686-1.04-5.23-2.93-7.15-1.89-1.92-4.44-2.98-7.1-2.98M12 0C5.383 0 0 5.383 0 12s5.383 12 12 12 12-5.383 12-12S18.617 0 12 0"/>
    </svg>
</a>'''