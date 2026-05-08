# Check API Usage

See how many forecast calls you've used and how many remain in the current billing period.

!!! info "How it works"
    A minimal request is sent to `0,0` (Gulf of Guinea) using your key. The API response headers report your current usage. Your key is sent **directly from your browser** to the Pirate Weather API — it is never forwarded to any other server.

---

<div class="pw-try-card" markdown="0">

  <form id="pw-usage-form" autocomplete="off" novalidate>

    <div class="pw-field-group">
      <label for="pw-usage-key">API Key</label>
      <input
        id="pw-usage-key"
        type="text"
        placeholder="Your Pirate Weather API key"
        spellcheck="false"
        autocomplete="off"
      />
      <span class="pw-hint">
        Don't have a key? <a href="https://pirateweather.net/" target="_blank" rel="noopener">Sign up free</a>.
      </span>
    </div>

    <button id="pw-usage-submit" type="submit" class="pw-btn-primary">Check Usage</button>

  </form>

  <div id="pw-usage-result" style="display:none;">
    <hr class="pw-divider" />
    <div id="pw-usage-error" class="pw-error-box" style="display:none;"></div>
    <div id="pw-usage-dashboard" class="pw-usage-dashboard" style="display:none;"></div>
  </div>

</div>
