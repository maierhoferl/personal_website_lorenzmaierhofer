/* ============================================
   LORENZ MAIERHOFER - PERSONAL WEBSITE
   JavaScript for interactivity
   ============================================ */

// Auto language detection & redirect (first visit only)
(function () {
  if (localStorage.getItem('langChosen')) return;

  const lang = ((navigator.languages && navigator.languages[0]) || navigator.language || 'en').toLowerCase();
  const path = window.location.pathname;

  const isDE = path.startsWith('/de/') || path === '/de';
  const isZH = path.startsWith('/zh/') || path === '/zh';
  const wantsDE = lang.startsWith('de');
  const wantsZH = lang.startsWith('zh');

  if (wantsDE && !isDE) {
    window.location.replace('/de/');
  } else if (wantsZH && !isZH) {
    window.location.replace('/zh/');
  } else if (!wantsDE && !wantsZH && (isDE || isZH)) {
    window.location.replace('/');
  }
})();

// Language preference tracking (no auto-redirect - Google uses hreflang tags)
document.addEventListener('DOMContentLoaded', () => {
    const langSwitch = document.querySelector('.lang-switch');
    if (langSwitch) {
        langSwitch.addEventListener('click', () => {
            // Update language preference when user manually switches
            const isGoingToGerman = langSwitch.textContent.trim() === 'DE';
            localStorage.setItem('langChosen', isGoingToGerman ? 'de' : 'en');
        });
    }
});

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

// Profile image interaction with AI explosion effect
const profileImage = document.querySelector('.profile-image');
if (profileImage) {
    profileImage.style.cursor = 'pointer';

    profileImage.addEventListener('click', (e) => {
        // Scale effect
        profileImage.style.transform = 'scale(1.05)';
        setTimeout(() => {
            profileImage.style.transform = 'scale(1)';
        }, 200);

        // AI Explosion effect
        createAIExplosion(e.clientX, e.clientY);
    });
}

// AI Explosion particle system
function createAIExplosion(x, y) {
    const particleCount = 30;
    const symbols = ['◈', '⬡', '⬢', '◇', '△', '▽', '○', '●', '◎', '⊡', '⊞', '⋈', '∿', '≋'];
    const colors = ['#00D4FF', '#FF00FF', '#00FF88', '#8B5CF6', '#003DA5'];

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'ai-particle';
        particle.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        particle.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            font-size: ${Math.random() * 16 + 10}px;
            color: ${colors[Math.floor(Math.random() * colors.length)]};
            pointer-events: none;
            z-index: 9999;
            opacity: 1;
            text-shadow: 0 0 10px currentColor;
            font-family: var(--font-mono);
        `;
        document.body.appendChild(particle);

        // Random direction and distance
        const angle = (Math.PI * 2 * i) / particleCount + (Math.random() - 0.5);
        const velocity = Math.random() * 150 + 100;
        const dx = Math.cos(angle) * velocity;
        const dy = Math.sin(angle) * velocity;
        const rotation = Math.random() * 720 - 360;

        // Animate particle
        particle.animate([
            {
                transform: 'translate(-50%, -50%) scale(0) rotate(0deg)',
                opacity: 1
            },
            {
                transform: `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(1.5) rotate(${rotation}deg)`,
                opacity: 0
            }
        ], {
            duration: Math.random() * 800 + 600,
            easing: 'cubic-bezier(0, 0.5, 0.5, 1)'
        }).onfinish = () => particle.remove();
    }

    // Add a central flash
    const flash = document.createElement('div');
    flash.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        width: 100px;
        height: 100px;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle, rgba(0, 212, 255, 0.8) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9998;
    `;
    document.body.appendChild(flash);

    flash.animate([
        { transform: 'translate(-50%, -50%) scale(0)', opacity: 1 },
        { transform: 'translate(-50%, -50%) scale(3)', opacity: 0 }
    ], {
        duration: 500,
        easing: 'ease-out'
    }).onfinish = () => flash.remove();
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
║   Senior Director & Global Lead              ║
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

// Hamburger navigation
(function initHamburger() {
    const hamburger = document.getElementById('hamburgerToggle');
    const navMenu = document.getElementById('navMenu');
    if (!hamburger || !navMenu) return;

    function openMenu() {
        navMenu.classList.add('is-open');
        hamburger.setAttribute('aria-expanded', 'true');
        document.addEventListener('click', outsideClick, true);
        document.addEventListener('keydown', escKey);
    }
    function closeMenu() {
        navMenu.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.removeEventListener('click', outsideClick, true);
        document.removeEventListener('keydown', escKey);
    }
    function outsideClick(e) {
        if (!document.querySelector('.navbar').contains(e.target)) closeMenu();
    }
    function escKey(e) {
        if (e.key === 'Escape') { closeMenu(); hamburger.focus(); }
    }

    hamburger.addEventListener('click', () => {
        hamburger.getAttribute('aria-expanded') === 'true' ? closeMenu() : openMenu();
    });
    navMenu.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    window.addEventListener('resize', () => {
        if (window.innerWidth > 480) closeMenu();
    });
})();

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
