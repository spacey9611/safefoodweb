/**
 * Cookie consent — Accept / Reject, scroll lock until choice is made.
 */
(function () {
    const KEY = 'fs_cookie_consent_v2';
    const LEGACY_KEY = 'fs_cookie_accepted_v1';

    function updateConsent(granted) {
        if (typeof gtag !== 'function') return;
        gtag('consent', 'update', granted ? {
            ad_storage: 'granted',
            ad_user_data: 'granted',
            ad_personalization: 'granted',
            analytics_storage: 'granted',
        } : {
            ad_storage: 'denied',
            ad_user_data: 'denied',
            ad_personalization: 'denied',
            analytics_storage: 'denied',
        });
        if (window.dataLayer) {
            window.dataLayer.push({ event: 'consent_update', consent_granted: granted });
        }
    }

    function unlockPage(accepted) {
        document.documentElement.classList.remove('cookie-banner-open');
        document.documentElement.classList.add('cookies-resolved');
        document.documentElement.classList.toggle('cookies-accepted', accepted);
    }

    function lockPage() {
        document.documentElement.classList.add('cookie-banner-open');
        document.documentElement.classList.remove('cookies-resolved', 'cookies-accepted');
    }

    function getStoredChoice() {
        try {
            const c = localStorage.getItem(KEY);
            if (c === 'accepted' || c === 'denied') return c;
            if (localStorage.getItem(LEGACY_KEY) === 'true') return 'accepted';
        } catch (e) {}
        return null;
    }

    function saveChoice(accepted) {
        try {
            localStorage.setItem(KEY, accepted ? 'accepted' : 'denied');
            if (accepted) localStorage.setItem(LEGACY_KEY, 'true');
        } catch (e) {}
        updateConsent(accepted);
        unlockPage(accepted);
    }

    function preventScroll(e) {
        if (document.documentElement.classList.contains('cookie-banner-open')) {
            e.preventDefault();
        }
    }

    function init() {
        const stored = getStoredChoice();
        if (stored === 'accepted') {
            updateConsent(true);
            unlockPage(true);
            return;
        }
        if (stored === 'denied') {
            updateConsent(false);
            unlockPage(false);
            return;
        }

        lockPage();
        document.addEventListener('wheel', preventScroll, { passive: false });
        document.addEventListener('touchmove', preventScroll, { passive: false });
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.documentElement.classList.contains('cookie-banner-open')) {
                e.preventDefault();
            }
        });

        const accept = document.getElementById('cookie-accept');
        const deny = document.getElementById('cookie-deny');
        if (!accept || !deny) return;

        accept.addEventListener('click', () => saveChoice(true));
        deny.addEventListener('click', () => saveChoice(false));
        window.setTimeout(() => { try { accept.focus(); } catch (e) {} }, 100);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
