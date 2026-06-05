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
      try {
        if (localStorage.getItem("fs_cookie_accepted_v1") === "true") {
          document.documentElement.classList.add("cookies-accepted");
        }
      } catch (e) {}
    </script>'''

COOKIE_BANNER = '''    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-live="polite" aria-label="Cookie notice">
        <div class="cookie-banner__content">
            <p>We use cookies for analytics and advertising. See our <a href="{legal}">Privacy Policy</a>.</p>
            <div class="cookie-banner__actions">
                <button type="button" id="cookie-accept" class="btn btn-primary cookie-btn">Accept</button>
            </div>
        </div>
    </div>'''

COOKIE_SCRIPT = '<script src="{src}" defer></script>'
