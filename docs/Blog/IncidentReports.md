# Incident Reports

Weather data is critical for many applications, and accordingly, Pirate Weather takes uptime very seriously. This page will be updated with details on any outage, along with lessons learned and next steps.


???+ note "November 17, 2025"

	* An AWS Load Balancer Target Group configuration error, pushed as part of the new container required by the 2.8.2 update, meant that new EC2 instances were not registered. This was compounded by an earlier configuration error that meant an incorrect port was being used for health checks, which prevented automated monitoring from noticing the issue.
	* The issue was resolved by manually adding the EC2 instances back  to the target group, and updating the deployment template configuration to ensure that they are automatically added going forward.
	* Moreover, the automatic restart (lifecycle) policy for the EC2 instances was changed to ensure that they had a one week staggered restart. This will allow any issues to be identified before both production instances are restarted, instead of the previous 2-hour window.
	* Going forward, Pirate Weather will move to a Terraform defined Kubernities setup, which will allow any infrastructure changes to be noticed and corrected immediately.
