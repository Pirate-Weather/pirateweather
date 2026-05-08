/**
 * Try It Now – Pirate Weather interactive API demo
 * Vanilla JS, no external dependencies.
 * Works with MkDocs Material's SPA-style navigation via document$.subscribe.
 */

(function () {
  "use strict";

  // Emoji icon map for weather conditions
  var WEATHER_ICONS = {
    "clear-day":           "☀️",
    "clear-night":         "🌙",
    "rain":                "🌧️",
    "snow":                "❄️",
    "sleet":               "🌨️",
    "wind":                "💨",
    "fog":                 "🌫️",
    "cloudy":              "☁️",
    "partly-cloudy-day":   "⛅",
    "partly-cloudy-night": "🌙",
    "hail":                "🌨️",
    "thunderstorm":        "⛈️",
    "tornado":             "🌪️"
  };

  function weatherIcon(icon) {
    return WEATHER_ICONS[icon] || "🌡️";
  }

  function tempUnit(units) {
    return (units === "si" || units === "ca" || units === "uk") ? "°C" : "°F";
  }

  function windUnit(units) {
    if (units === "si") return "m/s";
    if (units === "ca") return "km/h";
    return "mph";
  }

  function pct(val) {
    return typeof val === "number" ? Math.round(val * 100) + "%" : "—";
  }

  function wStat(label, value) {
    return (
      '<div class="pw-wcard-stat">' +
        '<span class="pw-wcard-stat-value">' + value + '</span>' +
        '<span class="pw-wcard-stat-label">' + label + '</span>' +
      '</div>'
    );
  }

  function renderWeatherCard(card, data, units) {
    var curr = data && data.currently;
    if (!curr) {
      card.style.display = "none";
      return;
    }

    var tu = tempUnit(units);
    var wu = windUnit(units);

    var icon    = weatherIcon(curr.icon);
    var summary = curr.summary || "—";
    var temp    = curr.temperature         != null ? Math.round(curr.temperature)         + tu : "—";
    var feels   = curr.apparentTemperature != null ? Math.round(curr.apparentTemperature) + tu : "—";
    var humidity  = pct(curr.humidity);
    var wind      = curr.windSpeed  != null ? (Math.round(curr.windSpeed * 10) / 10) + " " + wu : "—";
    var uv        = curr.uvIndex    != null ? String(curr.uvIndex) : "—";
    var precip    = pct(curr.precipProbability);
    var cloud     = pct(curr.cloudCover);
    var dewPoint  = curr.dewPoint  != null ? Math.round(curr.dewPoint)  + tu      : "—";
    var pressure  = curr.pressure  != null ? Math.round(curr.pressure)  + " hPa"  : "—";

    card.innerHTML =
      '<div class="pw-wcard-main">' +
        '<span class="pw-wcard-icon" aria-hidden="true">' + icon + '</span>' +
        '<div class="pw-wcard-temp">' + temp + '</div>' +
        '<div class="pw-wcard-summary">' + summary + '</div>' +
      '</div>' +
      '<div class="pw-wcard-grid">' +
        wStat("Feels Like",   feels)    +
        wStat("Humidity",     humidity) +
        wStat("Wind",         wind)     +
        wStat("UV Index",     uv)       +
        wStat("Precip. Prob.", precip)  +
        wStat("Cloud Cover",  cloud)    +
        wStat("Dew Point",    dewPoint) +
        wStat("Pressure",     pressure) +
      '</div>';

    card.style.display = "block";
  }

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
    var weatherCard   = document.getElementById("pw-weather-card");
    var jsonDetails   = document.getElementById("pw-json-details");
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
      errorBox.textContent   = msg;
      errorBox.style.display = "block";
      weatherCard.style.display = "none";
      if (jsonDetails) jsonDetails.style.display = "none";
      responseBox.style.display = "none";
      statusDisplay.textContent = "";
    }

    function hideError() {
      errorBox.style.display = "none";
    }

    function setLoading(loading) {
      submitBtn.disabled    = loading;
      submitBtn.textContent = loading ? "Sending…" : "Send Request";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      hideError();
      weatherCard.style.display = "none";
      if (jsonDetails) {
        jsonDetails.removeAttribute("open");
        jsonDetails.style.display = "none";
      }
      responseBox.style.display = "none";
      statusDisplay.textContent = "";
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
          statusDisplay.className   = "pw-status " + (status === 200 ? "pw-status-ok" : "pw-status-err");
          return resp.text().then(function (body) {
            return { status: status, body: body };
          });
        })
        .then(function (result) {
          setLoading(false);
          if (result.status === 200) {
            try {
              var parsed = JSON.parse(result.body);
              var units  = unitsSelect ? unitsSelect.value : "";
              renderWeatherCard(weatherCard, parsed, units);
              responseBox.textContent = JSON.stringify(parsed, null, 2);
            } catch (_) {
              responseBox.textContent = result.body;
            }
            responseBox.style.display = "block";
            if (jsonDetails) jsonDetails.style.display = "block";
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
        ta.style.opacity  = "0";
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
