// Product Rating System
class RatingSystem {
    constructor() {
        this.initStarRatings();
    }
    
    initStarRatings() {
        const ratingContainers = document.querySelectorAll('.star-rating');
        
        ratingContainers.forEach(container => {
            const stars = container.querySelectorAll('.star');
            
            stars.forEach((star, index) => {
                star.addEventListener('click', () => {
                    this.setRating(container, index + 1);
                });
                
                star.addEventListener('mouseover', () => {
                    this.highlightStars(container, index + 1);
                });
            });
            
            container.addEventListener('mouseleave', () => {
                const currentRating = container.dataset.rating || 0;
                this.highlightStars(container, currentRating);
            });
        });
    }
    
    highlightStars(container, rating) {
        const stars = container.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
            }
        });
    }
    
    setRating(container, rating) {
        container.dataset.rating = rating;
        const input = container.closest('form')?.querySelector('input[name="rating"]');
        if (input) {
            input.value = rating;
        }
    }
}
 
// Initialize ratings
const ratingSystem = new RatingSystem();