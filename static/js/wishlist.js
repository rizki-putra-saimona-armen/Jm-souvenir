// Wishlist Management
class Wishlist {
    constructor() {
        this.wishlist = this.loadWishlist();
        this.initEventListeners();
    }
    
    loadWishlist() {
        const wishlist = localStorage.getItem('wishlist');
        return wishlist ? JSON.parse(wishlist) : [];
    }
    
    saveWishlist() {
        localStorage.setItem('wishlist', JSON.stringify(this.wishlist));
    }
    
    toggleProduct(productId) {
        const index = this.wishlist.indexOf(productId);
        if (index > -1) {
            this.wishlist.splice(index, 1);
            this.updateUI(productId, false);
        } else {
            this.wishlist.push(productId);
            this.updateUI(productId, true);
        }
        this.saveWishlist();
    }
    
    isInWishlist(productId) {
        return this.wishlist.includes(productId);
    }
    
    updateUI(productId, isFavorite) {
        const button = document.querySelector(`[data-wishlist="${productId}"]`);
        if (button) {
            if (isFavorite) {
                button.classList.add('active');
                button.innerHTML = '<i class="fas fa-heart"></i>';
            } else {
                button.classList.remove('active');
                button.innerHTML = '<i class="far fa-heart"></i>';
            }
        }
    }
    
    initEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-wishlist]')) {
                e.preventDefault();
                const button = e.target.closest('[data-wishlist]');
                const productId = button.dataset.wishlist;
                this.toggleProduct(parseInt(productId));
            }
        });
    }
}
 
// Initialize wishlist
const wishlist = new Wishlist();