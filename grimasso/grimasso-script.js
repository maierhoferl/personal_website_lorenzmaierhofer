/* ============================================
   GRIMASSO - Tongue Training for Kids
   Grimasso-specific JavaScript
   Theme toggle & nav scroll handled by main script.js
   ============================================ */

// Auto language detection & redirect (first visit only)
(function () {
  // Mark explicit language choice when user clicks switcher
  document.addEventListener('click', function (e) {
    if (e.target.closest('.lang-switch')) {
      localStorage.setItem('langChosen', '1');
    }
  });

  if (localStorage.getItem('langChosen')) return;

  const lang = ((navigator.languages && navigator.languages[0]) || navigator.language || 'en').toLowerCase();
  const path = window.location.pathname;

  let current;
  if (path.includes('/grimasso/de/')) current = 'de';
  else if (path.includes('/grimasso/fr/')) current = 'fr';
  else if (path.includes('/grimasso/zh/')) current = 'zh';
  else current = 'en';

  let target;
  if (lang.startsWith('de')) target = 'de';
  else if (lang.startsWith('fr')) target = 'fr';
  else if (lang.startsWith('zh')) target = 'zh';
  else target = 'en';

  if (target === current) return;

  const roots = { en: '/grimasso/', de: '/grimasso/de/', fr: '/grimasso/fr/', zh: '/grimasso/zh/' };
  window.location.replace(roots[target]);
})();

// Compact language selector for mobile — replaces pills with a <select> on narrow screens
(function () {
    function buildLangSelect() {
        const switcher = document.querySelector('.grimasso-lang-switcher');
        if (!switcher || switcher.querySelector('.lang-select-mobile')) return;

        const links = switcher.querySelectorAll('.lang-switch');
        if (links.length < 2) return;

        const select = document.createElement('select');
        select.className = 'lang-select-mobile';
        select.setAttribute('aria-label', 'Select language');

        links.forEach(link => {
            const opt = document.createElement('option');
            opt.value = link.href;
            opt.textContent = (link.getAttribute('title') || link.textContent.trim());
            if (link.classList.contains('active')) opt.selected = true;
            select.appendChild(opt);
        });

        select.addEventListener('change', () => {
            if (select.value) {
                localStorage.setItem('langChosen', '1');
                window.location.href = select.value;
            }
        });

        switcher.appendChild(select);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildLangSelect);
    } else {
        buildLangSelect();
    }
})();

document.addEventListener('DOMContentLoaded', () => {

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Force light theme as default for Grimasso if no preference saved
    const html = document.documentElement;
    const savedTheme = localStorage.getItem('theme');
    if (!savedTheme) {
        html.setAttribute('data-theme', 'light');
    }

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
            const hasSuffix = targetText.includes('+');
            const duration = 1500; // 1.5 seconds
            const startTime = performance.now();

            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Ease out cubic for smooth deceleration
                const easeOutCubic = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(easeOutCubic * targetNum);

                numberEl.textContent = current + (hasSuffix ? '+' : '');

                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    numberEl.textContent = targetText;
                    numberEl.dataset.animated = 'true';
                }
            };

            if (!prefersReducedMotion) {
                numberEl.textContent = '0' + (hasSuffix ? '+' : '');
                requestAnimationFrame(animate);
            }
        });
    };

    // ============================================
    // 2. CONFETTI ON CTA BUTTON CLICK
    // ============================================
    const createConfetti = (button) => {
        const colors = ['#33C759', '#FFD933', '#FF9933', '#FF8099', '#66B3FF', '#B380FF'];
        const particleCount = 40;
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'grimasso-confetti';
            particle.style.left = centerX + 'px';
            particle.style.top = centerY + 'px';
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

            // Random angle and velocity
            const angle = (Math.PI * 2 * i) / particleCount + (Math.random() - 0.5) * 0.5;
            const velocity = 150 + Math.random() * 100;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;

            particle.style.setProperty('--vx', vx + 'px');
            particle.style.setProperty('--vy', vy + 'px');
            particle.style.setProperty('--rotation', Math.random() * 720 + 'deg');

            document.body.appendChild(particle);

            // Remove after animation
            setTimeout(() => particle.remove(), 1000);
        }
    };

    // Attach confetti to all CTA buttons
    const ctaButtons = document.querySelectorAll('.btn-grimasso-primary');
    ctaButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!prefersReducedMotion) {
                createConfetti(button);
            }
        });
    });

    // ============================================
    // 3. CARD TILT/3D EFFECT ON HOVER
    // ============================================
    const setupCardTilt = () => {
        // Only enable on non-touch devices
        if ('ontouchstart' in window) return;

        const cards = document.querySelectorAll('.feature-card, .benefit-card, .app-feature-item');

        cards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                if (prefersReducedMotion) return;

                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = (y - centerY) / centerY * -5; // Max 5deg
                const rotateY = (x - centerX) / centerX * 5;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    };

    if (!prefersReducedMotion) {
        setupCardTilt();
    }

    // ============================================
    // 4. BOUNCE/SPRING SCROLL ANIMATIONS
    // ============================================
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

    // Observe Grimasso cards and sections for animation with spring effect
    document.querySelectorAll('.feature-card, .step-card, .benefit-card, .app-feature-item').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px) scale(0.95)';
        el.style.transition = prefersReducedMotion
            ? 'opacity 0.3s ease, transform 0.3s ease'
            : 'opacity 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
        el.style.transitionDelay = `${index * 0.08}s`;
        grimassoObserver.observe(el);
    });

    // Stats section observer for count-up
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                animateStatNumbers();
            }
        });
    }, {
        threshold: 0.3
    });

    const statsSection = document.querySelector('.grimasso-stats-section');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    // Add animate-in style with spring effect
    if (!document.querySelector('#grimasso-animate-style')) {
        const style = document.createElement('style');
        style.id = 'grimasso-animate-style';
        style.textContent = `
            .animate-in {
                opacity: 1 !important;
                transform: translateY(0) scale(1) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // ============================================
    // 5. APP ICON INTERACTION
    // ============================================
    const setupAppIconInteraction = () => {
        const appIcon = document.querySelector('.hero-app-icon img');
        if (!appIcon) return;

        const emojis = ['😛', '⭐', '✨', '🌟', '💫', '🎉'];

        appIcon.addEventListener('click', (e) => {
            if (prefersReducedMotion) return;

            e.preventDefault();

            // Wobble effect
            appIcon.classList.add('grimasso-wobble');
            setTimeout(() => appIcon.classList.remove('grimasso-wobble'), 600);

            // Emoji burst
            const rect = appIcon.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            for (let i = 0; i < 8; i++) {
                const emoji = document.createElement('div');
                emoji.className = 'grimasso-emoji-burst';
                emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                emoji.style.left = centerX + 'px';
                emoji.style.top = centerY + 'px';

                const angle = (Math.PI * 2 * i) / 8;
                const distance = 120 + Math.random() * 40;
                const tx = Math.cos(angle) * distance;
                const ty = Math.sin(angle) * distance;

                emoji.style.setProperty('--tx', tx + 'px');
                emoji.style.setProperty('--ty', ty + 'px');

                document.body.appendChild(emoji);

                setTimeout(() => emoji.remove(), 1000);
            }
        });
    };

    setupAppIconInteraction();

    // ============================================
    // 6. SMOOTH SCROLL PROGRESS INDICATOR
    // ============================================
    const createScrollProgress = () => {
        const progressBar = document.createElement('div');
        progressBar.className = 'grimasso-scroll-progress';
        document.body.prepend(progressBar);

        const updateProgress = () => {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const progress = (scrollTop / scrollHeight) * 100;

            progressBar.style.width = progress + '%';
        };

        window.addEventListener('scroll', () => {
            if (!prefersReducedMotion) {
                requestAnimationFrame(updateProgress);
            }
        }, { passive: true });

        updateProgress();
    };

    createScrollProgress();

});

// ============================================
// FAQ ACCORDION
// ============================================
(function() {
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.faq-question').forEach(btn => {
            btn.addEventListener('click', () => {
                const isOpen = btn.getAttribute('aria-expanded') === 'true';
                const answer = btn.nextElementSibling;

                // Close all others
                document.querySelectorAll('.faq-question').forEach(b => {
                    b.setAttribute('aria-expanded', 'false');
                    if (b.nextElementSibling) b.nextElementSibling.classList.remove('open');
                });

                // Toggle current
                if (!isOpen) {
                    btn.setAttribute('aria-expanded', 'true');
                    answer.classList.add('open');
                }
            });
        });
    });
})();

// ============================================
// EMAIL CAPTURE FORM
// ============================================
function handleEmailSubmit(event) {
    event.preventDefault();
    const form = document.getElementById('emailCaptureForm');
    const successMsg = document.getElementById('emailSuccessMsg');
    if (form && successMsg) {
        form.style.display = 'none';
        successMsg.style.display = 'block';
    }
}

// Screenshot device tab switcher
(function() {
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

// ============================================
// EMAIL CAPTURE FORM - GERMAN
// ============================================
function handleEmailSubmitDE(event) {
    event.preventDefault();
    const form = document.getElementById('emailCaptureFormDE');
    const successMsg = document.getElementById('emailSuccessMsgDE');
    if (form && successMsg) {
        form.style.display = 'none';
        successMsg.style.display = 'block';
    }
}

// ============================================
// Email obfuscation - reconstruct mailto links from data attributes
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.email-link').forEach(el => {
        const addr = el.dataset.user + '@' + el.dataset.domain;
        el.href = 'mailto:' + addr;
        if (el.dataset.showaddr === 'true') el.textContent = addr;
    });
});

// ANALYTICS - Plausible (GDPR-friendly, no cookies)
// ============================================
(function() {
    var s = document.createElement('script');
    s.defer = true;
    s.setAttribute('data-domain', 'lorenzmaierhofer.com');
    s.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(s);
})();
