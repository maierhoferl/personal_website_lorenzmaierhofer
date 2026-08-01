/* ============================================
   OFFGRID MEDIA — subsite interactions
   Loaded after ../script.js (shared nav + theme)
   ============================================ */

/* The listing will live at https://apps.apple.com/us/app/offgrid-media
   Set APP_STORE_URL to that address once it is published and every
   "coming soon" badge on the page turns into a real App Store button.
   Left null until then so the badge never links to a 404. */
const APP_STORE_URL = null;

/* ---- Language auto-redirect (first visit, English page only) ---- */
(function () {
    if (localStorage.getItem('langChosen')) return;
    if (window.location.pathname !== '/offgridmedia/' && window.location.pathname !== '/offgridmedia/index.html') return;

    const localeMap = {
        ar: 'ar', de: 'de', es: 'es', fr: 'fr', hi: 'hi',
        id: 'id', in: 'id', pt: 'pt', ru: 'ru', zh: 'zh'
    };
    const lang = ((navigator.languages && navigator.languages[0]) || navigator.language || 'en').toLowerCase();
    const target = localeMap[lang.split('-')[0]];
    if (target) window.location.replace('/offgridmedia/' + target + '/');
})();

document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---- The offline switch: the page's one big idea ---- */
    const sw = document.getElementById('ogmSwitch');
    if (sw) {
        const hint = document.getElementById('ogmSwitchHint');
        sw.addEventListener('click', () => {
            const online = document.body.classList.toggle('is-online');
            sw.setAttribute('aria-pressed', String(!online));
            sw.querySelector('.ogm-switch-text').textContent =
                online ? sw.dataset.labelOnline : sw.dataset.labelOffline;
            if (hint) hint.textContent = online ? hint.dataset.hintOnline : hint.dataset.hintOffline;
        });
    }

    /* ---- FAQ accordion (one open at a time) ---- */
    document.querySelectorAll('.ogm-faq-q').forEach((btn) => {
        btn.addEventListener('click', () => {
            const open = btn.getAttribute('aria-expanded') === 'true';
            document.querySelectorAll('.ogm-faq-q').forEach((other) => {
                other.setAttribute('aria-expanded', 'false');
                other.nextElementSibling.classList.remove('open');
            });
            if (!open) {
                btn.setAttribute('aria-expanded', 'true');
                btn.nextElementSibling.classList.add('open');
            }
        });
    });

    /* ---- iPhone / iPad screenshot tabs ---- */
    const tabs = document.querySelectorAll('.ogm-device-tab');
    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            tabs.forEach((t) => {
                t.classList.toggle('active', t === tab);
                t.setAttribute('aria-selected', String(t === tab));
            });
            document.querySelectorAll('.ogm-shots').forEach((row) => {
                row.classList.toggle('hidden', row.dataset.device !== tab.dataset.device);
            });
        });
    });

    /* ---- Scroll reveal + stat count-up ---- */
    document.body.classList.add('ogm-anim');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('is-in');
            if (entry.target.dataset.count && !reduceMotion) countUp(entry.target);
            observer.unobserve(entry.target);
        });
    }, { threshold: 0.2, rootMargin: '0px 0px -60px 0px' });

    document.querySelectorAll('.ogm-reveal, [data-count]').forEach((el) => observer.observe(el));

    function countUp(el) {
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1100;
        const start = performance.now();
        function frame(now) {
            const p = Math.min((now - start) / duration, 1);
            el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
            if (p < 1) requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
    }

    /* ---- Scroll progress ---- */
    const bar = document.createElement('div');
    bar.className = 'ogm-progress';
    document.body.prepend(bar);
    window.addEventListener('scroll', () => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }, { passive: true });

    /* ---- Hero preview video: play only when it is worth it ---- */
    const video = document.querySelector('.ogm-phone video');
    if (video) {
        if (reduceMotion || !window.matchMedia('(min-width: 1024px)').matches) {
            video.removeAttribute('autoplay');
            video.pause();
            video.controls = true;
        }
        // Stop burning cycles while the hero is off screen.
        new IntersectionObserver((entries) => {
            entries.forEach((e) => {
                if (e.isIntersecting) {
                    if (video.hasAttribute('autoplay')) video.play().catch(() => {});
                } else {
                    video.pause();
                }
            });
        }, { threshold: 0.2 }).observe(video);
    }

    /* ---- Flip "coming soon" badges once the app is listed ---- */
    if (APP_STORE_URL) {
        document.querySelectorAll('.ogm-soon').forEach((badge) => {
            const a = document.createElement('a');
            a.className = 'ogm-btn ogm-btn-primary';
            a.href = APP_STORE_URL;
            a.target = '_blank';
            a.rel = 'noopener';
            a.innerHTML = badge.dataset.liveLabel || 'Download on the App Store';
            badge.replaceWith(a);
        });
    }
});

/* ---- Plausible (site analytics, not app analytics) ---- */
(function () {
    const s = document.createElement('script');
    s.defer = true;
    s.setAttribute('data-domain', 'lorenzmaierhofer.com');
    s.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(s);
})();
