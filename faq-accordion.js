/**
 * FAQ accordion, standalone (no module import) so it always runs after DOM ready.
 */
(function () {
    'use strict';

    let listenersAttached = false;

    function toggleFaqItem(dt) {
        const answer = dt.nextElementSibling;
        if (!answer || answer.tagName !== 'DD') return;
        const nextExpanded = dt.getAttribute('aria-expanded') !== 'true';
        dt.setAttribute('aria-expanded', String(nextExpanded));
        answer.hidden = !nextExpanded;
    }

    function prepareFaqItem(dt) {
        if (dt.dataset.faqInit) return;
        const answer = dt.nextElementSibling;
        if (!answer || answer.tagName !== 'DD') return;
        dt.dataset.faqInit = '1';

        if (dt.classList.contains('blog-faq-q')) {
            dt.classList.add('faq-question');
            answer.classList.add('faq-answer');
        }
        if (!dt.hasAttribute('aria-expanded')) {
            dt.setAttribute('aria-expanded', 'false');
        }
        if (!dt.hasAttribute('tabindex')) {
            dt.setAttribute('tabindex', '0');
        }

        if (!dt.querySelector('.faq-toggle')) {
            const toggle = document.createElement('span');
            toggle.className = 'faq-toggle';
            toggle.setAttribute('aria-hidden', 'true');
            dt.appendChild(toggle);
        }

        if (dt.getAttribute('aria-expanded') !== 'true') {
            answer.hidden = true;
        }
    }

    function initFaq() {
        document.querySelectorAll('.faq-question, .blog-faq-q').forEach(prepareFaqItem);

        if (listenersAttached) return;
        listenersAttached = true;

        document.addEventListener('click', (e) => {
            const dt = e.target.closest('.faq-question, .blog-faq-q');
            if (!dt) return;
            prepareFaqItem(dt);
            toggleFaqItem(dt);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            const dt = e.target.closest('.faq-question, .blog-faq-q');
            if (!dt) return;
            e.preventDefault();
            prepareFaqItem(dt);
            toggleFaqItem(dt);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFaq);
    } else {
        initFaq();
    }
})();
