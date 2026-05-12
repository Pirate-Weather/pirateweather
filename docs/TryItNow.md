# Try It Now

Make a live forecast request straight from your browser.

!!! info "Privacy notice"
    Your key is sent **directly from your browser** to the Pirate Weather API — it is never forwarded to any other server.
    Only use an API key you are comfortable entering in a browser context.
    Do not use production or high-privilege keys on shared or public computers.

---

<div class="pw-try-card" markdown="0">

  <form id="pw-try-form" autocomplete="off" novalidate>

    <!-- Required fields -->
    <div class="pw-section-label">Required</div>

    <div class="pw-field-group">
      <label for="pw-api-key">API Key</label>
      <input
        id="pw-api-key"
        type="text"
        placeholder="Your Pirate Weather API key"
        spellcheck="false"
        autocomplete="off"
      />
      <span class="pw-hint">
        Don't have a key? <a href="https://pirateweather.net/" target="_blank" rel="noopener">Sign up free</a>.
      </span>
    </div>

    <div class="pw-field-row">
      <div class="pw-field-group">
        <label for="pw-lat">Latitude</label>
        <input
          id="pw-lat"
          type="number"
          step="any"
          placeholder="e.g. 45.42"
          inputmode="decimal"
        />
      </div>
      <div class="pw-field-group">
        <label for="pw-lon">Longitude</label>
        <input
          id="pw-lon"
          type="number"
          step="any"
          placeholder="e.g. -75.69"
          inputmode="decimal"
        />
      </div>
    </div>

    <!-- Optional fields -->
    <details class="pw-optional-block">
      <summary class="pw-section-label">Optional parameters <span class="pw-caret">▸</span></summary>

      <div class="pw-field-row">
        <div class="pw-field-group">
          <label for="pw-endpoint">Endpoint</label>
          <select id="pw-endpoint">
            <option value="api" selected>Production (api.pirateweather.net)</option>
            <option value="dev">Development (dev.pirateweather.net)</option>
          </select>
        </div>
        <div class="pw-field-group">
          <label for="pw-units">Units</label>
          <select id="pw-units">
            <option value="">Default (us)</option>
            <option value="si">si – SI / metric</option>
            <option value="ca">ca – SI, km/h wind</option>
            <option value="uk">uk – SI, mph wind</option>
            <option value="us">us – Imperial</option>
          </select>
        </div>
        <div class="pw-field-group">
          <label for="pw-version">Version</label>
          <select id="pw-version">
            <option value="">Default (v1)</option>
            <option value="2" selected>2</option>
          </select>
        </div>
      </div>

      <div class="pw-field-group">
        <label for="pw-lang">Language (lang)</label>
        <input
          id="pw-lang"
          type="text"
          placeholder="e.g. en, fr, de"
          maxlength="10"
        />
      </div>

      <div class="pw-field-group">
        <label>Exclude blocks</label>
        <div class="pw-checkbox-row">
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="currently"> currently</label>
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="minutely"> minutely</label>
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="hourly"> hourly</label>
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="daily"> daily</label>
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="alerts"> alerts</label>
          <label class="pw-check"><input class="pw-exclude" type="checkbox" value="flags"> flags</label>
        </div>
      </div>

      <div class="pw-field-group">
        <label class="pw-check">
          <input id="pw-extend" type="checkbox">
          Extend hourly forecast (<code>extend=hourly</code>)
        </label>
      </div>

    </details>

    <!-- Submit -->
    <button id="pw-submit" type="submit" class="pw-btn-primary">Send Request</button>

  </form>

  <!-- Result area -->
  <div id="pw-result-section" style="display:none;">
    <hr class="pw-divider" />

    <div class="pw-result-header">
      <span class="pw-result-label">Request URL</span>
      <button id="pw-copy-url" class="pw-btn-secondary" style="display:none;" type="button">Copy URL</button>
    </div>
    <div id="pw-request-url" class="pw-url-display"></div>

    <div style="margin-top:0.75rem;">
      <span id="pw-status" class="pw-status"></span>
    </div>

    <div id="pw-error" class="pw-error-box" style="display:none;"></div>

    <!-- Current conditions card -->
    <div id="pw-weather-card" class="pw-weather-card" style="display:none;"></div>

    <!-- 3-day forecast -->
    <div id="pw-forecast-card" class="pw-forecast-card" style="display:none;"></div>

    <!-- Raw JSON (collapsible) -->
    <details id="pw-json-details" style="display:none; margin-top:1rem;">
      <summary class="pw-section-label" style="cursor:pointer; user-select:none;">
        Raw JSON response <span class="pw-caret">▸</span>
      </summary>
      <div class="pw-result-header" style="margin-top:0.5rem;">
        <span></span>
        <button id="pw-copy-json" class="pw-btn-secondary" style="display:none;" type="button">Copy JSON</button>
      </div>
      <pre id="pw-response" class="pw-response-box" style="display:none;"></pre>
    </details>

  </div>

</div>
