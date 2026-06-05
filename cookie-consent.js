/**
 * Cookie consent banner — load on every page (before or alongside site-ui.js / script.js).
 */
(function () {
    const KEY = 'fs_cookie_accepted_v1';

    function applyGrantedConsent() {
        document.documentElement.classList.add('cookies-accepted');
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

    function init() {
        const banner = document.getElementById('cookie-banner');
        const accept = document.getElementById('cookie-accept');

        try {
            if (localStorage.getItem(KEY) === 'true') {
                applyGrantedConsent();
                return;
            }
        } catch (e) {}

        if (!banner || !accept) return;

        accept.addEventListener('click', () => {
            try {
                localStorage.setItem(KEY, 'true');
            } catch (e) {}
            applyGrantedConsent();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
