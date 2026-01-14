// Update the date
document.addEventListener('DOMContentLoaded', function() {
    const dateElement = document.querySelector('.date');
    const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
    const currentDate = new Date().toLocaleDateString('en-GB', options);
    dateElement.textContent = currentDate;
});

// Add hover effects to news items
const newsItems = document.querySelectorAll('.news-item, .story');
newsItems.forEach(item => {
    item.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    item.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

// Mobile menu toggle (if needed)
const moreButton = document.querySelector('.nav-links a:last-child');
moreButton.addEventListener('click', function(e) {
    e.preventDefault();
    // Add mobile menu functionality here
});