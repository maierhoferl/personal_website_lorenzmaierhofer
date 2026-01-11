/* ============================================
   LORENZ MAIERHOFER - PERSONAL WEBSITE
   JavaScript for interactivity
   ============================================ */

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

// Check for saved theme preference or default to dark
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 50) {
        navbar.style.background = html.getAttribute('data-theme') === 'dark'
            ? 'rgba(10, 14, 23, 0.95)'
            : 'rgba(248, 250, 252, 0.95)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = html.getAttribute('data-theme') === 'dark'
            ? 'rgba(10, 14, 23, 0.8)'
            : 'rgba(248, 250, 252, 0.9)';
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.timeline-item, .expertise-card, .education-card, .news-card, .project-card, .stat-card, .topic-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);

// Stagger animations for grid items
const staggerElements = document.querySelectorAll('.expertise-grid > *, .education-grid > *, .news-grid > *, .projects-grid > *, .topics-grid > *, .tech-grid > *');
staggerElements.forEach((el, index) => {
    el.style.transitionDelay = `${index * 0.1}s`;
});

// Profile image interaction
const profileImage = document.querySelector('.profile-image');
if (profileImage) {
    profileImage.addEventListener('click', () => {
        profileImage.style.transform = 'scale(1.05)';
        setTimeout(() => {
            profileImage.style.transform = 'scale(1)';
        }, 200);
    });
}

// Typing effect for hero subtitle (optional enhancement)
const heroSubtitle = document.querySelector('.hero-subtitle');
if (heroSubtitle) {
    heroSubtitle.style.opacity = '1';
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add hover sound effect to cards (subtle UX enhancement)
const cards = document.querySelectorAll('.expertise-card, .stat-card, .news-card, .project-card, .topic-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = card.classList.contains('featured')
            ? 'translateY(-6px)'
            : 'translateY(-4px)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// Dynamic year in footer
const yearElement = document.querySelector('.footer-bottom p');
if (yearElement) {
    const currentYear = new Date().getFullYear();
    yearElement.innerHTML = yearElement.innerHTML.replace('2025', currentYear);
}

// Console greeting for developers
console.log(`
%c╔═══════════════════════════════════════════════╗
║                                               ║
║   LORENZ MAIERHOFER                          ║
║   AI & Data Science Leader                   ║
║                                               ║
║   Senior Director - AI Factory / GenAI       ║
║   Procter & Gamble                           ║
║                                               ║
╚═══════════════════════════════════════════════╝
`, 'color: #00D4FF; font-family: monospace; font-size: 12px;');

// Performance: Lazy load images if any are added later
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Mobile menu toggle (for future enhancement)
const createMobileMenu = () => {
    const navMenu = document.querySelector('.nav-menu');
    const hamburger = document.createElement('button');
    hamburger.className = 'hamburger';
    hamburger.setAttribute('aria-label', 'Toggle menu');
    hamburger.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    // Only add hamburger on mobile
    if (window.innerWidth <= 480) {
        const navContainer = document.querySelector('.nav-container');
        if (navContainer && !document.querySelector('.hamburger')) {
            navContainer.insertBefore(hamburger, navMenu);

            hamburger.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
            });
        }
    }
};

// Add hamburger styles
const hamburgerStyles = document.createElement('style');
hamburgerStyles.textContent = `
    .hamburger {
        display: none;
        flex-direction: column;
        justify-content: space-between;
        width: 24px;
        height: 18px;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
    }

    .hamburger span {
        display: block;
        width: 100%;
        height: 2px;
        background: var(--text-primary);
        transition: var(--transition-base);
    }

    .hamburger.active span:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
    }

    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }

    .hamburger.active span:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
    }

    @media (max-width: 480px) {
        .hamburger {
            display: flex;
        }

        .nav-menu {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--bg-dark);
            flex-direction: column;
            padding: 1rem 2rem;
            border-bottom: 1px solid var(--border-color);
            display: none;
        }

        .nav-menu.active {
            display: flex;
        }
    }
`;
document.head.appendChild(hamburgerStyles);

// Initialize mobile menu
createMobileMenu();
window.addEventListener('resize', createMobileMenu);

// LinkedIn Posts Loader
const loadLinkedInPosts = async () => {
    const container = document.getElementById('linkedinEmbeds');
    if (!container) return;

    try {
        const response = await fetch('linkedin_posts.json');
        const config = await response.json();

        if (config.linkedin && config.linkedin.posts && config.linkedin.posts.length > 0) {
            container.innerHTML = '';

            config.linkedin.posts.forEach((postUrl, index) => {
                const wrapper = document.createElement('div');
                wrapper.className = 'linkedin-embed-wrapper';
                wrapper.style.opacity = '0';
                wrapper.style.transform = 'translateY(20px)';
                wrapper.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                wrapper.style.transitionDelay = `${index * 0.15}s`;

                const iframe = document.createElement('iframe');
                iframe.src = postUrl;
                iframe.height = '600';
                iframe.width = '504';
                iframe.frameBorder = '0';
                iframe.allowFullscreen = true;
                iframe.title = `LinkedIn post ${index + 1}`;

                wrapper.appendChild(iframe);
                container.appendChild(wrapper);

                // Trigger animation
                setTimeout(() => {
                    wrapper.style.opacity = '1';
                    wrapper.style.transform = 'translateY(0)';
                }, 50);
            });

            // Update the CTA link with profile URL from config
            if (config.linkedin.profileUrl) {
                const ctaLink = document.querySelector('.linkedin-cta a');
                if (ctaLink) {
                    ctaLink.href = config.linkedin.profileUrl + 'recent-activity/all/';
                }
            }
        } else {
            container.innerHTML = '<p class="linkedin-empty">No LinkedIn posts configured. Add post URLs to config.json</p>';
        }
    } catch (error) {
        console.error('Error loading LinkedIn posts:', error);
        container.innerHTML = '<p class="linkedin-error">Unable to load LinkedIn posts. Make sure config.json exists.</p>';
    }
};

// Load LinkedIn posts when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadLinkedInPosts);
} else {
    loadLinkedInPosts();
}
