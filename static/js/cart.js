
// Shopping Cart Management
class ShoppingCart {
    constructor() {
        this.cart = this.loadCart();
        this.initEventListeners();
        this.updateBadge();
    }
    
    // Load cart from localStorage
    loadCart() {
        const cart = localStorage.getItem('cart');
        return cart ? JSON.parse(cart) : {};
    }
    
    // Save cart to localStorage
    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
        this.updateBadge();
    }
    
    // Add to cart
    addProduct(productId, quantity = 1) {
        if (this.cart[productId]) {
            this.cart[productId] += quantity;
        } else {
            this.cart[productId] = quantity;
        }
        this.saveCart();
        this.showNotification(`Produk ditambahkan ke keranjang`);
    }
    
    // Remove from cart
    removeProduct(productId) {
        delete this.cart[productId];
        this.saveCart();
    }
    
    // Update quantity
    updateQuantity(productId, quantity) {
        if (quantity <= 0) {
            this.removeProduct(productId);
        } else {
            this.cart[productId] = quantity;
        }
        this.saveCart();
    }
    
    // Get total items
    getTotalItems() {
        return Object.values(this.cart).reduce((a, b) => a + b, 0);
    }
    
    // Clear cart
    clearCart() {
        this.cart = {};
        this.saveCart();
    }
    
    // Update cart badge
    updateBadge() {
        const badge = document.querySelector('.badge-cart');
        if (badge) {
            badge.textContent = this.getTotalItems();
        }
    }
    
    // Initialize event listeners
    initEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-add-cart')) {
                const productId = e.target.dataset.productId;
                const quantity = parseInt(e.target.dataset.quantity || 1);
                this.addProduct(productId, quantity);
            }
        });
    }
    
    // Show notification
    showNotification(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('main').insertAdjacentElement('afterbegin', alert);
        
        setTimeout(() => alert.remove(), 3000);
    }
}
 
// Initialize cart
const cart = new ShoppingCart();
