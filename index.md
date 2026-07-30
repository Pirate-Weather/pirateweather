---
layout: splash
title: Pirate Weather
permalink: /
classes:
  - landing
  - wide
header:
  overlay_color: "#071521"
  overlay_filter: "0.18"
  actions:
    - label: "Get an API key"
      url: "https://pirate-weather.apiable.io/products/weatherdata/plans"
    - label: "Try the API"
      url: "https://pirateweather.net/en/latest/TryItNow/"
  caption: "Open source · Developer focused · Weather without the black box"
excerpt: >-
  Forecast data you can inspect, integrate, and trust. Pirate Weather turns
  public weather-model data into a fast, documented API with familiar
  Dark Sky-compatible responses and modern REST and MCP access.
feature_row:
  - icon: "fas fa-code"
    title: "Familiar API"
    excerpt: "A practical Dark Sky-compatible JSON interface for existing applications and new integrations."
    url: "https://pirateweather.net/en/latest/API/"
    btn_label: "Explore the API"
    btn_class: "btn--primary"
  - icon: "fas fa-eye"
    title: "Transparent forecasts"
    excerpt: "Public model data, documented processing, and open-source code make it possible to see how forecasts are built."
    url: "https://pirateweather.net/en/latest/DataSources/"
    btn_label: "View data sources"
    btn_class: "btn--primary"
  - icon: "fas fa-cloud"
    title: "Built to scale"
    excerpt: "Hosted infrastructure provides dependable access for apps, dashboards, automations, and community projects."
    url: "https://pirateweather.xitoring.io/"
    btn_label: "Check status"
    btn_class: "btn--primary"
feature_row_mcp:
  - image_path: https://raw.githubusercontent.com/Pirate-Weather/pirateweather/main/docs/images/pw_favicon.png
    image_caption: "REST and MCP access from one weather platform"
    alt: "Pirate Weather logo"
    title: "Weather data for developers—and agents"
    excerpt: >-
      Use Pirate Weather through the REST API or connect applications and AI
      agents to the hosted MCP server. Forecast, current, hourly, minutely,
      daily, alert, historical, summary, and subscription tools are available
      through a remote streamable HTTP endpoint.
    url: "https://pirateweather.net/en/latest/#mcp-server"
    btn_label: "Connect the MCP server"
    btn_class: "btn--primary"
feature_row_ecosystem:
  - title: "MerrySky"
    excerpt: "A clean, Dark Sky-style forecast experience for the web."
    url: "https://merrysky.net/"
    btn_label: "Visit MerrySky"
    btn_class: "btn--inverse"
  - title: "Breezy Weather"
    excerpt: "A feature-rich, open-source Android weather application."
    url: "https://github.com/breezy-weather/breezy-weather"
    btn_label: "View project"
    btn_class: "btn--inverse"
  - title: "Weathergraph"
    excerpt: "Graphical forecasts for iPhone, iPad, Apple Watch, and Mac."
    url: "https://weathergraph.app/"
    btn_label: "Visit Weathergraph"
    btn_class: "btn--inverse"
---

<div class="pw-proof" aria-label="Pirate Weather platform highlights">
  <div><strong>REST API</strong><span>Forecast and historical weather</span></div>
  <div><strong>MCP Server</strong><span>Tools for applications and agents</span></div>
  <div><strong>10,000</strong><span>Free calls each month</span></div>
  <div><strong>Open Source</strong><span>Documented processing pipeline</span></div>
</div>

<section id="features" class="pw-section">
  <p class="pw-kicker">Built for practical integration</p>
  <h2>A weather API that shows its work.</h2>
  <p class="pw-lede">Pirate Weather combines a familiar developer experience with transparent data sources and community-led improvement.</p>
</section>

{% include feature_row %}

<section class="pw-code-showcase" aria-label="Example Pirate Weather API request">
  <div>
    <p class="pw-kicker">Straightforward by design</p>
    <h2>One request. A complete forecast.</h2>
    <p>Request current conditions plus minutely, hourly, and daily forecasts through a predictable JSON response.</p>
    <a href="https://pirateweather.net/en/latest/TryItNow/" class="btn btn--primary">Make a test request</a>
  </div>
  <pre><code>GET /forecast/&lt;API_KEY&gt;/45.42,-75.69

{
  "timezone": "America/Toronto",
  "currently": {
    "summary": "Partly Cloudy",
    "temperature": 23.4,
    "windSpeed": 11.2
  },
  "hourly": { ... },
  "daily": { ... }
}</code></pre>
</section>

<section id="mcp" class="pw-section pw-section--accent">
{% include feature_row id="feature_row_mcp" type="left" %}
<div class="pw-endpoint"><code>https://mcp.pirateweather.net/mcp?apikey=&lt;APIKEY&gt;</code></div>
</section>

<section id="ecosystem" class="pw-section">
  <p class="pw-kicker">A growing ecosystem</p>
  <h2>Powering weather apps, dashboards, and automations.</h2>
  <p class="pw-lede">Pirate Weather already supports projects across mobile, desktop, browser extensions, Home Assistant, and custom workflows.</p>
</section>

{% include feature_row id="feature_row_ecosystem" %}

<section class="pw-final-cta">
  <p class="pw-kicker">Start building</p>
  <h2>Open weather data with familiar interfaces.</h2>
  <p>Build with the hosted API, review the source, or support the free tier.</p>
  <p>
    <a href="https://pirate-weather.apiable.io/products/weatherdata/plans" class="btn btn--primary btn--large">Create an API key</a>
    <a href="https://github.com/Pirate-Weather/pirate-weather-code" class="btn btn--inverse btn--large">View the source</a>
  </p>
</section>
