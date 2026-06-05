/* ============================================
   SHARE2SAVE - Offline Video & Audio Library
   Share2Save-specific JavaScript
   Theme toggle & nav scroll handled by main script.js
   ============================================ */

// Auto language detection & redirect (first visit only)
(function () {
  document.addEventListener('click', function (e) {
    if (e.target.closest('.lang-switch')) {
      localStorage.setItem('langChosen', '1');
    }
  });

  if (localStorage.getItem('langChosen')) return;

  const lang = ((navigator.languages && navigator.languages[0]) || navigator.language || 'en').toLowerCase();
  const path = window.location.pathname;

  const current = path.includes('/share2save/de/') ? 'de' : 'en';
  const target = lang.startsWith('de') ? 'de' : 'en';

  if (target === current) return;
  if (current !== 'en') return; // only redirect from English root

  if (target === 'de') window.location.replace('/share2save/de/');
})();

document.addEventListener('DOMContentLoaded', () => {

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ============================================
    // 1. STATISTICS COUNT-UP ANIMATION
    // ============================================
    const animateStatNumbers = () => {
        const statItems = document.querySelectorAll('.stat-item');

        statItems.forEach(item => {
            const numberEl = item.querySelector('.stat-number');
            if (!numberEl || numberEl.dataset.animated) return;

            const targetText = numberEl.textContent;
            const targetNum = parseInt(targetText.replace(/\D/g, ''), 10);
            const hasPlusSuffix = targetText.includes('+');
            const hasPercentSuffix = targetText.includes('%');
            const suffix = hasPlusSuffix ? '+' : (hasPercentSuffix ? '%' : '');
            const duration = 1500;
            const startTime = performance.now();

            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const easeOutCubic = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(easeOutCubic * targetNum);

                numberEl.textContent = current + suffix;

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    numberEl.textContent = targetText;
                    numberEl.dataset.animated = 'true';
                }
            };

            if (!prefersReducedMotion) {
                numberEl.textContent = '0' + suffix;
                requestAnimationFrame(animate);
            }
        });
    };

    // ============================================
    // 2. CONFETTI ON CTA BUTTON CLICK
    // ============================================
    const createConfetti = (button) => {
        const colors = ['#2563EB', '#06B6D4', '#4F46E5', '#60A5FA', '#67E8F9', '#818CF8'];
        const particleCount = 40;
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 's2s-confetti';
            particle.style.left = centerX + 'px';
            particle.style.top = centerY + 'px';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

            const angle = (Math.PI * 2 * i) / particleCount + (Math.random() - 0.5) * 0.5;
            const velocity = 150 + Math.random() * 100;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;

            particle.style.setProperty('--vx', vx + 'px');
            particle.style.setProperty('--vy', vy + 'px');
            particle.style.setProperty('--rotation', Math.random() * 720 + 'deg');

            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 1000);
        }
    };

    document.querySelectorAll('.btn-s2s-primary').forEach(button => {
        button.addEventListener('click', () => {
            if (!prefersReducedMotion) createConfetti(button);
        });
    });

    // ============================================
    // 3. CARD TILT/3D EFFECT ON HOVER
    // ============================================
    if (!('ontouchstart' in window) && !prefersReducedMotion) {
        document.querySelectorAll('.feature-card, .benefit-card, .step-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const rotateX = (y - rect.height / 2) / rect.height * -5;
                const rotateY = (x - rect.width / 2) / rect.width * 5;
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(8px)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // ============================================
    // 4. BOUNCE/SPRING SCROLL ANIMATIONS
    // ============================================
    const s2sObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.feature-card, .step-card, .benefit-card').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px) scale(0.95)';
        el.style.transition = prefersReducedMotion
            ? 'opacity 0.3s ease, transform 0.3s ease'
            : 'opacity 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
        el.style.transitionDelay = `${index * 0.07}s`;
        s2sObserver.observe(el);
    });

    // Stats count-up trigger
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                animateStatNumbers();
            }
        });
    }, { threshold: 0.3 });

    const statsSection = document.querySelector('.s2s-stats-section');
    if (statsSection) statsObserver.observe(statsSection);

    if (!document.querySelector('#s2s-animate-style')) {
        const style = document.createElement('style');
        style.id = 's2s-animate-style';
        style.textContent = `.animate-in { opacity: 1 !important; transform: translateY(0) scale(1) !important; }`;
        document.head.appendChild(style);
    }

    // ============================================
    // 5. APP ICON INTERACTION
    // ============================================
    const appIcon = document.querySelector('.hero-app-icon img');
    if (appIcon) {
        const emojis = ['⬇️', '📴', '🎬', '🎵', '✅', '📱'];

        appIcon.addEventListener('click', (e) => {
            if (prefersReducedMotion) return;
            e.preventDefault();

            appIcon.classList.add('s2s-wobble');
            setTimeout(() => appIcon.classList.remove('s2s-wobble'), 600);

            const rect = appIcon.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            for (let i = 0; i < 8; i++) {
                const emoji = document.createElement('div');
                emoji.className = 's2s-emoji-burst';
                emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                emoji.style.left = centerX + 'px';
                emoji.style.top = centerY + 'px';

                const angle = (Math.PI * 2 * i) / 8;
                const distance = 120 + Math.random() * 40;
                emoji.style.setProperty('--tx', Math.cos(angle) * distance + 'px');
                emoji.style.setProperty('--ty', Math.sin(angle) * distance + 'px');

                document.body.appendChild(emoji);
                setTimeout(() => emoji.remove(), 1000);
            }
        });
    }

    // ============================================
    // 6. SCROLL PROGRESS BAR
    // ============================================
    const progressBar = document.createElement('div');
    progressBar.className = 's2s-scroll-progress';
    document.body.prepend(progressBar);

    window.addEventListener('scroll', () => {
        if (prefersReducedMotion) return;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        progressBar.style.width = ((scrollTop / scrollHeight) * 100) + '%';
    }, { passive: true });

});

// ============================================
// FAQ ACCORDION
// ============================================
(function () {
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.faq-question').forEach(btn => {
            btn.addEventListener('click', () => {
                const isOpen = btn.getAttribute('aria-expanded') === 'true';

                document.querySelectorAll('.faq-question').forEach(b => {
                    b.setAttribute('aria-expanded', 'false');
                    if (b.nextElementSibling) b.nextElementSibling.classList.remove('open');
                });

                if (!isOpen) {
                    btn.setAttribute('aria-expanded', 'true');
                    btn.nextElementSibling.classList.add('open');
                }
            });
        });
    });
})();

// ============================================
// SCREENSHOT DEVICE TAB SWITCHER
// ============================================
(function () {
    const tabs = document.querySelectorAll('.device-tab');
    const carousels = document.querySelectorAll('.screenshots-carousel');
    if (!tabs.length) return;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const target = tab.dataset.device;
            carousels.forEach(c => {
                c.classList.toggle('hidden', c.dataset.device !== target);
            });
        });
    });
})();

// Email obfuscation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.email-link').forEach(el => {
        const addr = el.dataset.user + '@' + el.dataset.domain;
        el.href = 'mailto:' + addr;
        if (el.dataset.showaddr === 'true') el.textContent = addr;
    });
});

// Patch hamburger close threshold for Share2Save (768px)
window.addEventListener('resize', function () {
    if (window.innerWidth > 768) {
        const navMenu = document.getElementById('navMenu');
        const hamburger = document.getElementById('hamburgerToggle');
        if (navMenu && hamburger) {
            navMenu.classList.remove('is-open');
            hamburger.setAttribute('aria-expanded', 'false');
        }
    }
});

// ANALYTICS - Plausible (GDPR-friendly, no cookies)
(function () {
    var s = document.createElement('script');
    s.defer = true;
    s.setAttribute('data-domain', 'lorenzmaierhofer.com');
    s.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(s);
})();
