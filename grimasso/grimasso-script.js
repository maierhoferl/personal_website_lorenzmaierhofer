/* ============================================
   GRIMASSO - Tongue Training for Kids
   Grimasso-specific JavaScript
   Theme toggle & nav scroll handled by main script.js
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // Force light theme as default for Grimasso if no preference saved
    const html = document.documentElement;
    const savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        html.setAttribute('data-theme', 'light');
    }

    // Intersection Observer for Grimasso-specific scroll animations
    const grimassoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    // Observe Grimasso cards and sections for animation
    document.querySelectorAll('.feature-card, .step-card, .benefit-card').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        el.style.transitionDelay = `${index * 0.08}s`;
        grimassoObserver.observe(el);
    });

    // Add animate-in style if not already present
    if (!document.querySelector('#grimasso-animate-style')) {
        const style = document.createElement('style');
        style.id = 'grimasso-animate-style';
        style.textContent = `
            .animate-in {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(style);
    }

});
