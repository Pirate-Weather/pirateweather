/**
 * Try It Now – Pirate Weather interactive API demo
 * Vanilla JS, no external dependencies.
 * Works with MkDocs Material's SPA-style navigation via document$.subscribe.
 */

(function () {
  "use strict";
  var SECONDS_PER_DAY = 86400;

  function init() {
    var form = document.getElementById("pw-try-form");
    if (!form) return; // not on the Try It Now page

    var apiKeyInput   = document.getElementById("pw-api-key");
    var latInput      = document.getElementById("pw-lat");
    var lonInput      = document.getElementById("pw-lon");
    var unitsSelect   = document.getElementById("pw-units");
    var langInput     = document.getElementById("pw-lang");
    var excludeInputs = document.querySelectorAll(".pw-exclude");
    var extendCheck   = document.getElementById("pw-extend");
    var versionSelect = document.getElementById("pw-version");

    var urlDisplay    = document.getElementById("pw-request-url");
    var statusDisplay = document.getElementById("pw-status");
    var responseBox   = document.getElementById("pw-response");
    var rateLimitsBox = document.getElementById("pw-rate-limits");
    var errorBox      = document.getElementById("pw-error");
    var submitBtn     = document.getElementById("pw-submit");
    var copyUrlBtn    = document.getElementById("pw-copy-url");
    var copyJsonBtn   = document.getElementById("pw-copy-json");
    var resultSection = document.getElementById("pw-result-section");

    function buildUrl() {
      var key  = (apiKeyInput.value || "").trim();
      var lat  = (latInput.value  || "").trim();
      var lon  = (lonInput.value  || "").trim();
      if (!key || !lat || !lon) return null;

      var base = "https://api.pirateweather.net/forecast/" + key + "/" + lat + "," + lon;

      var params = [];
      var units = unitsSelect.value;
      if (units) params.push("units=" + encodeURIComponent(units));

      var lang = (langInput.value || "").trim();
      if (lang) params.push("lang=" + encodeURIComponent(lang));

      var excluded = [];
      excludeInputs.forEach(function (cb) {
        if (cb.checked) excluded.push(cb.value);
      });
      if (excluded.length) params.push("exclude=" + encodeURIComponent(excluded.join(",")));

      if (extendCheck && extendCheck.checked) params.push("extend=hourly");

      var version = versionSelect ? versionSelect.value : "";
      if (version) params.push("version=" + encodeURIComponent(version));

      return base + (params.length ? "?" + params.join("&") : "");
    }

    function showError(msg) {
      errorBox.textContent  = msg;
      errorBox.style.display = "block";
      responseBox.style.display = "none";
      statusDisplay.textContent = "";
    }

    function formatRateLimitDisplay(limit, remaining, resetSeconds) {
      var resetDays = "n/a";
      if (resetSeconds !== null && resetSeconds !== "") {
        var parsedReset = Number(resetSeconds);
        if (isFinite(parsedReset)) {
          resetDays = (parsedReset / SECONDS_PER_DAY).toFixed(4);
        }
      }

      return [
        "ratelimit-limit: " + (limit || "n/a"),
        "ratelimit-remaining: " + (remaining || "n/a"),
        "ratelimit-reset: " + resetDays + " days"
      ].join("\n");
    }

    function getHeaderValue(headers, headerName) {
      var normalizedTarget = (headerName || "").toLowerCase();
      var candidates = [
        normalizedTarget,
        "x-" + normalizedTarget,
        normalizedTarget.replace(/-/g, "_"),
        "x_" + normalizedTarget.replace(/-/g, "_")
      ];

      for (var i = 0; i < candidates.length; i += 1) {
        var value = headers.get(candidates[i]);
        if (value !== null) return value;
      }

      var iterator = headers.entries();
      var next = iterator.next();
      while (!next.done) {
        var key = next.value[0];
        var value = next.value[1];
        var normalizedKey = String(key || "")
          .toLowerCase()
          .replace(/^x[-_]/, "")
          .replace(/_/g, "-");
        if (normalizedKey === normalizedTarget) return value;
        next = iterator.next();
      }
      return null;
    }

    function hideError() {
      errorBox.style.display = "none";
    }

    function setLoading(loading) {
      submitBtn.disabled = loading;
      submitBtn.textContent = loading ? "Sending…" : "Send Request";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      hideError();
      responseBox.style.display = "none";
      statusDisplay.textContent = "";
      rateLimitsBox.style.display = "none";
      rateLimitsBox.textContent = "";
      copyJsonBtn.style.display = "none";

      var url = buildUrl();
      if (!url) {
        showError("Please fill in all required fields (API key, latitude, longitude).");
        return;
      }

      // Show the URL before sending
      urlDisplay.textContent = url;
      resultSection.style.display = "block";
      copyUrlBtn.style.display = "inline-block";

      setLoading(true);

      fetch(url)
        .then(function (resp) {
          var status = resp.status;
          statusDisplay.textContent = "HTTP " + status + " " + (resp.statusText || "");
          statusDisplay.className = "pw-status " + (status === 200 ? "pw-status-ok" : "pw-status-err");
          var rateLimitLimit = getHeaderValue(resp.headers, "ratelimit-limit");
          var rateLimitRemaining = getHeaderValue(resp.headers, "ratelimit-remaining");
          var rateLimitReset = getHeaderValue(resp.headers, "ratelimit-reset");
          return resp.text().then(function (body) {
            return {
              status: status,
              body: body,
              rateLimitLimit: rateLimitLimit,
              rateLimitRemaining: rateLimitRemaining,
              rateLimitReset: rateLimitReset
            };
          });
        })
        .then(function (result) {
          setLoading(false);
          rateLimitsBox.textContent = formatRateLimitDisplay(
            result.rateLimitLimit,
            result.rateLimitRemaining,
            result.rateLimitReset
          );
          rateLimitsBox.style.display = "block";
          if (result.status === 200) {
            try {
              var parsed = JSON.parse(result.body);
              responseBox.textContent = JSON.stringify(parsed, null, 2);
            } catch (_) {
              responseBox.textContent = result.body;
            }
            responseBox.style.display = "block";
            copyJsonBtn.style.display = "inline-block";
          } else {
            showError("Request failed with status " + result.status + ".\n" + result.body);
          }
        })
        .catch(function (err) {
          setLoading(false);
          showError(
            "Request could not be completed.\n" +
            (err && err.message ? err.message : String(err)) +
            "\n\nThis may be a network error or a CORS issue. " +
            "Check your browser console for details."
          );
        });
    });

    copyUrlBtn.addEventListener("click", function () {
      var text = urlDisplay.textContent;
      if (!text) return;
      copyToClipboard(text, copyUrlBtn);
    });

    copyJsonBtn.addEventListener("click", function () {
      var text = responseBox.textContent;
      if (!text) return;
      copyToClipboard(text, copyJsonBtn);
    });

    function copyToClipboard(text, btn) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          flashBtn(btn);
        });
      } else {
        // Fallback for older browsers
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); flashBtn(btn); } catch (_) {}
        document.body.removeChild(ta);
      }
    }

    function flashBtn(btn) {
      var orig = btn.textContent;
      btn.textContent = "Copied!";
      setTimeout(function () { btn.textContent = orig; }, 1500);
    }
  }

  // MkDocs Material SPA lifecycle hook
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(init);
  } else {
    // Fallback for standard page load
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", init);
    } else {
      init();
    }
  }
})();
