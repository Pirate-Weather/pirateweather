# Incident Reports

Weather data is critical for many applications, and accordingly, Pirate Weather takes uptime very seriously. This page will be updated with details on any outage, along with lessons learned and next steps.


???+ note "December 24, 2025"

	* Unfortunately, this was the most significant outage in several years, with a four hour prod outage. To explain the root cause, a bit of background on Pirate Weather's AWS infrastructure is required, and is all detailed in a new blog post here: <a href="/Infrastructure2026/#december-24-2025-downtime-incident">December 24, 2025 downtime incident</a>.



???+ note "November 28, 2025"

	* The production file synchronization location was not defined in the zip_sync script, resulting in the transfer failing on new EC2 instances. 
	* Fixed in [PR #425](https://github.com/Pirate-Weather/pirate-weather-code/pull/425).
	* This was quickly identified and corrected using the new notification process.

???+ note "November 17, 2025"

	* An AWS Load Balancer Target Group configuration error, pushed as part of the new container required by the 2.8.2 update, meant that new EC2 instances were not registered. This was compounded by an earlier configuration error that meant an incorrect port was being used for health checks, which prevented automated monitoring from noticing the issue.
	* The issue was resolved by manually adding the EC2 instances back to the target group, and updating the deployment template configuration to ensure that they are automatically added going forward.
	* Moreover, the automatic restart (lifecycle) policy for the EC2 instances was changed to ensure that they had a one week staggered restart. This will allow any issues to be identified before both production instances are restarted, instead of the previous 2-hour window.
	* Going forward, Pirate Weather will move to a Terraform defined Kubernetes setup, which will allow any infrastructure changes to be noticed and corrected immediately.
