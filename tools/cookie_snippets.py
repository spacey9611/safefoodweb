"""Shared head/footer snippets for HTML builders."""

GA4_ID = "G-N69BCEQGQ2"

CONSENT_HEAD = '''    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag("consent", "default", {
        "ad_storage": "denied",
        "ad_user_data": "denied",
        "ad_personalization": "denied",
        "analytics_storage": "denied",
        "wait_for_update": 500
      });
      dataLayer.push({ "event": "default_consent_set" });
    </script>'''

GA4_TAG = f'''    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      gtag('js', new Date());
      gtag('config', '{GA4_ID}');
    </script>'''

COOKIE_HEAD = '''    <script>
      (function () {
        try {
          var c = localStorage.getItem("fs_cookie_consent_v2");
          if (c === "accepted" || c === "denied") {
            document.documentElement.classList.add("cookies-resolved");
            if (c === "accepted") document.documentElement.classList.add("cookies-accepted");
            return;
          }
          if (localStorage.getItem("fs_cookie_accepted_v1") === "true") {
            document.documentElement.classList.add("cookies-resolved", "cookies-accepted");
            return;
          }
          document.documentElement.classList.add("cookie-banner-open");
        } catch (e) {
          document.documentElement.classList.add("cookie-banner-open");
        }
      })();
    </script>'''

def cookie_banner_html(legal_href="/legal.html#privacy"):
    return f'''    <div id="cookie-banner-backdrop" class="cookie-banner-backdrop" aria-hidden="true"></div>
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-modal="true" aria-labelledby="cookie-banner-title" aria-live="polite">
        <div class="cookie-banner__content">
            <div class="cookie-banner__copy">
                <p id="cookie-banner-title"><strong>Accept cookies to continue</strong></p>
                <p class="cookie-banner__sub">We use cookies to keep the site running and to understand how people use our free practice tests. Tap accept to start studying. <a href="{legal_href}">Privacy Policy</a></p>
            </div>
            <div class="cookie-banner__actions">
                <button type="button" id="cookie-accept" class="btn btn-primary cookie-btn cookie-btn--accept">Accept &amp; continue</button>
                <button type="button" id="cookie-deny" class="cookie-banner__reject">Essential cookies only</button>
            </div>
        </div>
    </div>'''

COOKIE_BANNER = cookie_banner_html()

COOKIE_SCRIPT = '<script src="{src}" defer></script>'
