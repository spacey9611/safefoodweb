/* ==========================================================================
   AdSense activation — ONE-LINE SWITCH
   --------------------------------------------------------------------------
   You have NOT applied yet, so this is currently OFF and all ad placeholders
   are hidden (the site looks clean).

   TO TURN ON after you are approved:
   1. Replace the CLIENT value below with your real publisher ID
      (looks like "ca-pub-1234567890123456").
   2. Create /ads.txt at the site root (see ads.txt for the line to uncomment).
   3. That's it. This enables Google Auto Ads site-wide, and also fills any
      manual <div class="ad-slot" data-ad-slot-id="NNNN"> units you add later
      with real ad slot IDs from your AdSense dashboard.
   ========================================================================== */
(function () {
  var CLIENT = "ca-pub-XXXXXXXXXXXXXXXX";      // <-- paste your publisher ID here
  var PLACEHOLDER = "ca-pub-XXXXXXXXXXXXXXXX";

  function hidePlaceholders() {
    document.querySelectorAll(".ad-slot").forEach(function (el) {
      el.style.display = "none";
    });
  }

  // Not configured yet → keep the site clean, no empty ad boxes.
  if (!CLIENT || CLIENT === PLACEHOLDER) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", hidePlaceholders);
    } else {
      hidePlaceholders();
    }
    return;
  }

  // Load the AdSense library.
  var s = document.createElement("script");
  s.async = true;
  s.crossOrigin = "anonymous";
  s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + CLIENT;
  document.head.appendChild(s);

  // Enable Auto Ads (page-level) — no per-slot IDs needed.
  (window.adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: CLIENT,
    enable_page_level_ads: true
  });

  // Fill any manual reinforcement slots that carry a real slot ID.
  function fillManualSlots() {
    document.querySelectorAll(".ad-slot[data-ad-slot-id]").forEach(function (el) {
      el.innerHTML = "";
      var ins = document.createElement("ins");
      ins.className = "adsbygoogle";
      ins.style.display = "block";
      ins.setAttribute("data-ad-client", CLIENT);
      ins.setAttribute("data-ad-slot", el.getAttribute("data-ad-slot-id"));
      ins.setAttribute("data-ad-format", "auto");
      ins.setAttribute("data-full-width-responsive", "true");
      el.appendChild(ins);
      try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fillManualSlots);
  } else {
    fillManualSlots();
  }
})();
