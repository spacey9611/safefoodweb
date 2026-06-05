/**
 * Shared UI for content pages (blog, guide, topics), no quiz bundle.
 */
(function () {
    const COOKIE_KEY = 'fs_cookie_accepted_v1';
    const FONT_KEY = 'fs_font_size_v1';
    const FONT_SIZES = [14, 16, 18, 20, 22];
    const FONT_DEFAULT_IDX = 1;
    const THEME_KEY = 'fs_theme_v1';

    function applyTheme(theme) {
        if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
        else document.documentElement.removeAttribute('data-theme');
        document.querySelectorAll('.theme-toggle').forEach((btn) => {
            btn.textContent = theme === 'dark' ? '☀️' : '🌙';
            btn.setAttribute('aria-pressed', String(theme === 'dark'));
        });
    }

    function initTheme() {
        let theme = 'light';
        try { theme = localStorage.getItem(THEME_KEY) || 'light'; } catch (e) {}
        const tools = document.querySelector('.site-header__tools') || document.querySelector('.site-header__top');
        if (tools && !document.querySelector('.theme-toggle')) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'theme-toggle';
            btn.setAttribute('aria-label', 'Toggle dark mode');
            btn.title = 'Toggle dark mode';
            btn.addEventListener('click', () => {
                const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                const next = isDark ? 'light' : 'dark';
                applyTheme(next);
                try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
            });
            tools.appendChild(btn);
        }
        applyTheme(theme);
    }

    function onUserAcceptsCookies() {
        if (typeof gtag === 'function') {
            gtag('consent', 'update', {
                ad_storage: 'granted',
                ad_user_data: 'granted',
                ad_personalization: 'granted',
                analytics_storage: 'granted',
            });
        }
        if (window.dataLayer) {
            window.dataLayer.push({ event: 'consent_update' });
        }
    }

    function initCookies() {
        /* Handled by cookie-consent.js sitewide */
    }

    function applyFontSize(idx) {
        document.documentElement.style.fontSize = FONT_SIZES[idx] + 'px';
        try {
            localStorage.setItem(FONT_KEY, String(idx));
        } catch (e) {}
    }

    function initFontResize() {
        let idx;
        try {
            idx = parseInt(localStorage.getItem(FONT_KEY) ?? '', 10);
        } catch (e) {}
        if (isNaN(idx) || idx < 0 || idx >= FONT_SIZES.length) idx = FONT_DEFAULT_IDX;
        applyFontSize(idx);

        const dec = document.getElementById('font-decrease');
        const inc = document.getElementById('font-increase');
        if (!dec || !inc) return;
        if (dec.dataset.fontBound) return; // guard: avoid double-binding when script.js also loads
        dec.dataset.fontBound = '1';

        dec.addEventListener('click', () => {
            let i = FONT_SIZES.indexOf(parseInt(document.documentElement.style.fontSize, 10));
            if (i < 0) i = FONT_DEFAULT_IDX;
            applyFontSize(Math.max(0, i - 1));
        });
        inc.addEventListener('click', () => {
            let i = FONT_SIZES.indexOf(parseInt(document.documentElement.style.fontSize, 10));
            if (i < 0) i = FONT_DEFAULT_IDX;
            applyFontSize(Math.min(FONT_SIZES.length - 1, i + 1));
        });
    }

    function closeSiteNav(header) {
        header.classList.remove('nav-open');
        document.body.classList.remove('nav-menu-open');
        const toggle = header.querySelector('.nav-toggle');
        if (toggle) {
            toggle.setAttribute('aria-expanded', 'false');
            toggle.textContent = 'Menu';
        }
    }

    function bindSiteNav(header) {
        const toggle = header.querySelector('.nav-toggle');
        if (!toggle || toggle.dataset.bound) return;
        toggle.dataset.bound = '1';

        toggle.addEventListener('click', () => {
            if (header.classList.contains('nav-open')) {
                closeSiteNav(header);
            } else {
                header.classList.add('nav-open');
                document.body.classList.add('nav-menu-open');
                toggle.setAttribute('aria-expanded', 'true');
                toggle.textContent = 'Close';
            }
        });

        header.querySelectorAll('.secondary-nav a').forEach((link) => {
            link.addEventListener('click', () => closeSiteNav(header));
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && header.classList.contains('nav-open')) {
                closeSiteNav(header);
            }
        });
    }

    function initNav() {
        const header = document.querySelector('body > header');
        if (!header) return;
        const secondary = header.querySelector('.secondary-nav');

        if (secondary && !secondary.querySelector('a[href="/"], a[href="index.html"]')) {
            const home = document.createElement('a');
            home.href = '/';
            home.className = 'nav-link';
            home.textContent = 'Practice Test';
            secondary.insertBefore(home, secondary.firstChild);
        }

        const path = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '') || '/';
        header.querySelectorAll('.secondary-nav .nav-link, .state-link').forEach((a) => {
            const href = a.getAttribute('href');
            if (!href) return;
            let norm = href.replace(/index\.html$/, '');
            if (norm.endsWith('/')) norm = norm.slice(0, -1) || '/';
            if (norm === path || (path.endsWith('.html') && norm === path)) {
                a.setAttribute('aria-current', 'page');
            } else {
                a.removeAttribute('aria-current');
            }
        });

        bindSiteNav(header);
    }

    function boot() {
        initTheme();
        initNav();
        initFontResize();
        initCookies();
    }

    function onReady(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    onReady(boot);
})();
