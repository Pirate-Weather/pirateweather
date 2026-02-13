# AWS Infrastructure, 2026 Edition 

Since it's been a while since I last covered Pirate Weather's AWS infrastructure, I thought it was time to write a short update on how everything fits together, and also explain where things have gone wrong. At a high level, Pirate Weather is a Python script that reads Zarr files. These files are created from a series of scripts that run on a schedule, download the data, perform some light processing, and save .zip files for the response script. 


* **Ingestion & Processing:** A suite of Python scripts runs on a precise schedule, triggered by **Amazon EventBridge**. These scripts are orchestrated by **AWS Step Functions**, which manage **AWS Fargate** containers (using our [custom ARM-based image](https://gallery.ecr.aws/j9v4j3c7/pirate-wgrib-python-arm)). These containers download raw data, perform light processing, and "chunk" the data into Zarr format for lightning-fast retrieval.
* **Storage Strategy:** The processed Zarr data is initially persisted as zip files on **Amazon S3**. To minimize latency, an **rclone** container syncs these files to **autoscaled EC2 NVMe instances**. 
	* By serving data from local NVMe storage rather than directly from S3, we achieve the IOPS necessary for real-time weather requests.
	* Using zip files avoids the having a ton of S3 objects and the associated transaction costs.
	* Notably, the time for each model forecast is included in every chunk, which avoids having to rely on metadata. 
* **ECS service:** An ECS service coordinates four containers running on the EC2 instances: rclone for syncing, the [production FastAPI container](https://gallery.ecr.aws/j9v4j3c7/pirate-alpine-zarr), the development container, the historic data (Time Machine) container, and Kong.
	* This ensures that things are restarted if there are issues, handles placement on the instances, and container updates.
* **Traffic Management & Security:** Inbound requests are routed through **Amazon CloudFront** to a **Network Load Balancer (NLB)**, which passes it to the EC2 instances. From there, traffic hits a **Kong Gateway** container, which manages authentication and rate limiting.
* **Data Persistence:** The gateway and API layers are supported by **Amazon ElastiCache (Redis)** for rapid session/rate-limit caching and an **Amazon RDS** database for persistent metadata and user information.

![](https://github.com/Pirate-Weather/pirateweather/blob/main/docs/images/Arch_Diagram_2026.png)

There's quite a few nuances to the various pieces; however, this is "meat and potatoes" of it. 

#### December 24, 2025 downtime incident

The four hour production downtime had two root causes. The first was traced to a configuration conflict between our AWS Step Function definitions and the underlying ECS cluster strategy. While our ECS cluster is architected to run a resilient 50:50 mix of Fargate Spot and Fargate On-Demand instances, the Step Function definition responsible for triggering the ingestion tasks contained an explicit override. As seen in the configuration snippet below, the task was hardcoded to rely exclusively on `FARGATE_SPOT`. During a period of high Spot instance reclamation in our availability zone, these ingestion containers were repeatedly terminated by AWS before completion, halting the data pipeline.

```json
  "CapacityProviderStrategy": [
    {
      "CapacityProvider": "FARGATE_SPOT",
      "Weight": 1
    }
  ],

```

This is an issue on it's own; however, should have been recoverable; however, the ingestion failure was amplified by a logic error in the processing scripts, which lacked a fallback mechanism for missing GFS data when the two day buffer was exceeded, causing the forecast generation to fail entirely rather than serving stale or partial data. To resolve this, I have updated all Step Function task definitions to remove the explicit `CapacityProviderStrategy` override. The tasks now defer to the ECS cluster’s default capacity provider strategy, ensuring a stable 50:50 distribution between Spot and On-Demand instances. This change guarantees that even if Spot capacity is volatile, the On-Demand instances will ensure the ingestion process completes successfully. I've also added additional logging on when ingest tasks fail, which will avoid missing failures in the underlying data, as well as a check to avoid serving stale model results ([PR #542](https://github.com/Pirate-Weather/pirate-weather-code/pull/542)). 