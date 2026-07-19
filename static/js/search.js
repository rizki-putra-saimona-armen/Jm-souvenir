// Search & Filter Functionality
class SearchFilter {
    constructor() {
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Price range filter
        const priceRange = document.getElementById('priceRange');
        if (priceRange) {
            priceRange.addEventListener('change', () => {
                this.applyFilters();
            });
        }
        
        // Sort
        const sortSelect = document.getElementById('sortSelect');
        if (sortSelect) {
            sortSelect.addEventListener('change', () => {
                this.applyFilters();
            });
        }
        
        // Category filter
        document.querySelectorAll('[name="category"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.applyFilters();
            });
        });
    }
    
    applyFilters() {
        const params = new URLSearchParams();
        
        // Price
        const priceRange = document.getElementById('priceRange');
        if (priceRange) {
            params.set('max_price', priceRange.value);
        }
        
        // Sort
        const sortSelect = document.getElementById('sortSelect');
        if (sortSelect) {
            params.set('sort', sortSelect.value);
        }
        
        // Categories
        const categories = document.querySelectorAll('[name="category"]:checked');
        if (categories.length > 0) {
            params.set('categories', Array.from(categories).map(c => c.value).join(','));
        }
        
        // Redirect to filtered results
        window.location.search = params.toString();
    }
}
 
// Initialize search
const searchFilter = new SearchFilter();