// Main JavaScript File
 
// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Format currency
    formatCurrencies();
    
    // Add animation to elements
    observeElements();
});
 
// Format currency display
function formatCurrencies() {
    document.querySelectorAll('[data-currency]').forEach(element => {
        const amount = parseFloat(element.dataset.currency);
        element.textContent = new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR'
        }).format(amount);
    });
}
 
// Intersection Observer for animations
function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    });
    
    document.querySelectorAll('[data-observe]').forEach(el => {
        observer.observe(el);
    });
}
 
// Utility function to show loading
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm me-2';
    element.prepend(spinner);
    element.disabled = true;
}
 
// Utility function to hide loading
function hideLoading(element) {
    const spinner = element.querySelector('.spinner-border');
    if (spinner) spinner.remove();
    element.disabled = false;
}
 
// AJAX request helper
async function fetchAPI(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    });
    return response.json();
}