Running applications in containers provides numerous benefits—easy deployments, rapid scaling, streamlined updates, and more. However, troubleshooting and maintaining observability can become challenging, especially when containers run in cloud environments. Issues that didn't surface during testing might appear suddenly in production, and without direct access to underlying processes, diagnosing root causes can quickly become complex. This exact scenario happened to us recently at Pirate Weather, where unexpected container failures led to brief and seemingly random downtime incidents.

As outlined previously in our infrastructure overview, Pirate Weather’s production stack is hosted on Amazon Elastic Container Service (Amazon ECS), utilizing a series of ECS tasks managed by a single ECS service. Our service ensures high availability by maintaining at least two tasks running at all times, each task consisting of three distinct containers. Behind these tasks, we leverage auto-scaling EC2 instances to handle dynamic workloads.

When we began experiencing intermittent downtime, our initial investigation revealed ECS tasks failing with the infamous "Error 137," indicating that containers were terminated due to exceeding memory limits. Although this was a helpful clue, we still didn't know which specific container was responsible or whether the issue stemmed from sudden memory spikes or gradual leaks.

Initially, our monitoring setup involved using the Kong Prometheus plugin, but this provided insights only at the API gateway level, not deep within our ECS infrastructure. Seeking a more comprehensive solution, we discovered [AWS Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html), a built-in feature of Amazon CloudWatch that offers detailed metrics and logs for containers running on Amazon ECS.

Enabling AWS Container Insights was incredibly straightforward—just a single click in our ECS task definition settings, a quick update to our ECS service, and within minutes, we had detailed container-level metrics on CPU utilization, storage I/O, and crucially, memory usage available directly in CloudWatch. Arguably one of the easiest yet most impactful updates we’ve ever made!

After collecting data for a couple of days (and observing several more restarts), we revisited CloudWatch. The depth of data was impressive—almost overwhelming at first glance—but by filtering on key parameters like ClusterName, ContainerName, and ServiceName, we quickly identified the culprit. Our "TimeMachine" container, responsible for handling historical data requests, was steadily leaking memory and occasionally experiencing significant spikes. These spikes caused it to exceed its allocated memory, resulting in container termination and subsequent stack downtime.

<img src="https://github.com/Pirate-Weather/pirateweather/raw/main/docs/images/CloudWatch.png" width="325">

While a complete, permanent solution requires deeper investigation into the memory leak, AWS Container Insights provided immediate actionable insights, enabling us to implement two effective short-term solutions:

We modified our task definition to include the --limit-max-requests=25 flag in our Uvicorn Docker command, automatically restarting worker processes within the container to mitigate the slow memory leak.

We leveraged ECS's newly available container [restart policy](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-restart-policy.html), enabling graceful restarts of our TimeMachine container upon memory overload events. This ensured only the problematic container restarted rather than impacting the entire ECS task.

Though further work is needed for a long-term fix, activating AWS Container Insights significantly streamlined our troubleshooting process, demonstrating the immense value this tool offers for quickly diagnosing and resolving container-related issues.