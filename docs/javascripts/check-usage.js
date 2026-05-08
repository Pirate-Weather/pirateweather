/**
 * Check API Usage – Pirate Weather usage dashboard
 * Vanilla JS, no external dependencies.
 * Works with MkDocs Material's SPA-style navigation via document$.subscribe.
 */

(function () {
  "use strict";

  var SECONDS_PER_DAY  = 86400;
  var SECONDS_PER_HOUR = 3600;

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
      var k  = next.value[0];
      var v  = next.value[1];
      var nk = String(k || "").toLowerCase().replace(/^x[-_]/, "").replace(/_/g, "-");
      if (nk === normalizedTarget) return v;
      next = iterator.next();
    }
    return null;
  }

  function usageStat(label, value, valueClass) {
    return (
      '<div class="pw-usage-stat">' +
        '<span class="pw-usage-stat-value' + (valueClass ? ' ' + valueClass : '') + '">' + value + '</span>' +
        '<span class="pw-usage-stat-label">' + label + '</span>' +
      '</div>'
    );
  }

  function init() {
    var form      = document.getElementById("pw-usage-form");
    if (!form) return; // not on the Check Usage page

    var keyInput   = document.getElementById("pw-usage-key");
    var submitBtn  = document.getElementById("pw-usage-submit");
    var resultDiv  = document.getElementById("pw-usage-result");
    var errorBox   = document.getElementById("pw-usage-error");
    var dashboard  = document.getElementById("pw-usage-dashboard");

    function showError(msg) {
      errorBox.textContent   = msg;
      errorBox.style.display = "block";
      dashboard.style.display = "none";
    }

    function setLoading(loading) {
      submitBtn.disabled    = loading;
      submitBtn.textContent = loading ? "Checking…" : "Check Usage";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var key = (keyInput.value || "").trim();
      if (!key) {
        errorBox.textContent   = "Please enter your API key.";
        errorBox.style.display = "block";
        return;
      }

      errorBox.style.display  = "none";
      dashboard.style.display = "none";
      resultDiv.style.display = "block";
      setLoading(true);

      var url = "https://api.pirateweather.net/forecast/" + key +
                "/0,0?exclude=minutely,hourly,daily,alerts,flags";

      fetch(url)
        .then(function (resp) {
          var status    = resp.status;
          var limit     = getHeaderValue(resp.headers, "ratelimit-limit");
          var remaining = getHeaderValue(resp.headers, "ratelimit-remaining");
          var reset     = getHeaderValue(resp.headers, "ratelimit-reset");
          return resp.text().then(function (body) {
            return { status: status, limit: limit, remaining: remaining, reset: reset, body: body };
          });
        })
        .then(function (result) {
          setLoading(false);

          if (result.status !== 200) {
            var msg = "Request failed with status " + result.status + ".";
            try {
              var p = JSON.parse(result.body);
              if (p && p.detail) msg += "\n" + p.detail;
            } catch (parseError) {}
            showError(msg);
            return;
          }

          var limitNum     = result.limit     !== null ? Number(result.limit)     : null;
          var remainingNum = result.remaining !== null ? Number(result.remaining) : null;
          var resetNum     = result.reset     !== null ? Number(result.reset)     : null;

          var usedNum = (limitNum !== null && remainingNum !== null)
            ? limitNum - remainingNum
            : null;

          var pct = (limitNum && usedNum !== null)
            ? Math.min(100, Math.round((usedNum / limitNum) * 100))
            : null;

          var resetText = "n/a";
          if (resetNum !== null && isFinite(resetNum)) {
            var resetDays = resetNum / SECONDS_PER_DAY;
            resetText = resetDays >= 1
              ? resetDays.toFixed(1) + " days"
              : Math.round(resetNum / SECONDS_PER_HOUR) + " hours";
          }

          var html = "";

          // If headers weren't exposed, fall back gracefully
          if (limitNum === null && remainingNum === null) {
            html =
              '<div class="pw-usage-note">' +
                '⚠️ Rate-limit headers were not returned. Your key is valid (HTTP 200), ' +
                'but usage data requires <code>Access-Control-Expose-Headers</code> to be ' +
                'configured on the API gateway.' +
              '</div>';
          } else {
            var barPct   = pct !== null ? pct : 0;
            var barClass = barPct < 75 ? "pw-bar-ok" : (barPct < 90 ? "pw-bar-warn" : "pw-bar-crit");

            html =
              '<div class="pw-usage-title">API Usage This Period</div>' +
              (pct !== null
                ? '<div class="pw-usage-bar-wrap">' +
                    '<div class="pw-usage-bar ' + barClass + '" style="width:' + barPct + '%"></div>' +
                  '</div>' +
                  '<div class="pw-usage-bar-label">' + barPct + '% used</div>'
                : '') +
              '<div class="pw-usage-stats">' +
                usageStat("Calls Remaining", remainingNum !== null ? remainingNum.toLocaleString() : "n/a", "pw-stat-remaining") +
                usageStat("Calls Used",      usedNum      !== null ? usedNum.toLocaleString()      : "n/a", "") +
                usageStat("Monthly Limit",   limitNum     !== null ? limitNum.toLocaleString()     : "n/a", "") +
                usageStat("Resets In",       resetText,                                                      "") +
              '</div>';
          }

          dashboard.innerHTML = html;
          dashboard.style.display = "block";
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
