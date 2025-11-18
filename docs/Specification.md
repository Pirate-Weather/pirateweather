# OpenAPI Specification

<div class="swagger-container-wrapper">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css" />
	<div id="swagger-ui"></div>
	<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js"></script>
	<script>
		window.onload = function() {
			const ui = SwaggerUIBundle({
				url: "https://raw.githubusercontent.com/alexander0042/pirateweather/main/PW_OpenAPI.yaml",
				dom_id: "#swagger-ui",
				presets: [SwaggerUIBundle.presets.apis],
				layout: "BaseLayout",
				tryItOutEnabled: true
			});
			window.ui = ui;
		};
	</script>
</div>