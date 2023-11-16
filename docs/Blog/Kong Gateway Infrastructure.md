# Deploying Kong Gateway (OSS) in Production on AWS Using serverless Tools
## You can bring a data scientist to a database, but you can’t make them an administrator

Weather APIs are complicated things, with lot of different data flowing in and out. At [Pirate Weather](https://pirateweather.net), my background in data processing means that while I'm comfortable using Python to work with files, cloud infrastructure was a whole new world for me. I'm familier enough a command line and know the basics, but I went into this without any background in networking or databases, and didn't really want to have to learn. So it was great when I realized I could use serverless tools to abstract away the infrastructure and focus on building.

In the beginning, AWS API Gateway was an incredible tool, full stop. It let me rapidly deploy Pirate Weather as a functioning API using little more than a Lambda function and a URL, which was exactly what I was looking for at the time. It was easy to set up, very high performant, and allowed just the right amount of customization. However, two years post-launch, Pirate Weather started to come up against the API key limit imposed by AWS API Gateway, and the developer portal I was using had been depreciated. This meant that it was time to find a new solution, and Kong Gateway was exactly what I was looking for!

### Why Kong?
Why Kong Gateway (OSS)? Five main reasons:

1. Cloud native. Kong is designed to run in containers and has built in support for AWS Lambda, which meant it fit right in with my existing infrastructure.
2. Scalable. Running in containers, Kong is more than capable of handling as many requests as I could throw at it and doesn’t have any key limitations.
3. Compatible. My awesome registration provider ([Apiable](https://www.apiable.io/)) already supported it as a backend, and the API is very straightforward.
4. Customization. Kong supports custom plug-ins, which let me use a URL based API Key as authentication.
5. Open Source! It felt wrong to put an open weather API behind a proprietary gateway, so this was an added plus.

### Overview
Implementing this was a significant undertaking, and I relied heavily on other published walkthroughs, so I wanted to take the time to explain the process here. At a high level, the architecture is straightforward: a network load balancer in front of a containerized Fargate service interacting with a cache, database, and Lambda function.

<img src="https://github.com/Pirate-Weather/pirateweather/blob/main/docs/Pirate%20Kong.png?raw=true">

### Image
The system starts with a lightly customized [Kong OSS image](https://gallery.ecr.aws/j9v4j3c7/pirate-kong), which is build using Docker on an EC2 ARM instant and a very simple dockerfile:

```
FROM kong:3.2-ubuntu
USER root
COPY kong-plugin-request-transformer_1251-0.4-1.all.rock /tmp/kong-plugin-request-transformer_1251-0.4-1.all.rock
WORKDIR /tmp
RUN luarocks install kong-plugin-request-transformer_1251-0.4-1.all.rock
USER kong
```

Why the custom image? By default, the “Request Transformer” plugin runs after authentication; however, I needed it to run beforehand to extract the API key from a URL string. Specifically, the plugin adds a header from a URI capture: apikey:$(uri_captures['apikey']). This required that I create a ever so slightly modified version of the built in transformer [built in transformer](https://github.com/Kong/kong/tree/a382576530b7ddd57898c9ce917343bddeaf93f4/kong/plugins/request-transformer) with a [priority of 1251](https://docs.konghq.com/gateway/latest/plugin-development/custom-logic/#handlerlua-specifications) so it would run beforehand. By downloading the request transformer files, I could adjust the priority and [build a new rock](https://github.com/luarocks/luarocks/wiki/Creating-a-rock). The created the file that gets copied over and installed in the dockerfile.

### Database
Now that I had a functioning image, the AWS infrastructure falls into place around it. Kong stores everything in a Postgres database, and while I could have spun up my own, it was easier to rely on the AWS option, Aurora Postgres. Since the load is relatively small, I’m using the smallest Serverless v2 option, which uses 0.5 Aurora Capacity Units. By running this on RDS, it means I don’t have to worry about database updates, maintenance, or backups, and it will scale if there’s ever a wave of traffic.

Kong can also rely on Redis for caching API calls or authentication. While I’m not caching any data yet, caching authentication quotas did produce a slight performance improvement, and allow for quotas to stay in sync when multiple instances of the Kong instance are running or if it gets restarted. For this, I spun up a simple, single node t4g instance, which provides a primary endpoint that Kong uses.

### Container
With the AWS infrastructure in place, it was time to get to Kong. At the core, it is a ECS service calls a task definition that looks like this:

<details> 
  <summary> ECS Task JSON </summary>
  
```
		{
		    "taskDefinitionArn": "<AWS TASK ARN>",
		    "containerDefinitions": [
		        {
		            "name": "pirate-kong",
		            "image": "public.ecr.aws/j9v4j3c7/pirate-kong:latest",
		            "cpu": 0,
		            "portMappings": [
		                {
		                    "name": "pirate-kong-8000-tcp",
		                    "containerPort": 8000,
		                    "hostPort": 8000,
		                    "protocol": "tcp",
		                    "appProtocol": "http"
		                },
		                {
		                    "name": "pirate-kong-8001-tcp",
		                    "containerPort": 8001,
		                    "hostPort": 8001,
		                    "protocol": "tcp",
		                    "appProtocol": "http"
		                },
		                {
		                    "name": "pirate-kong-8443-tcp",
		                    "containerPort": 8443,
		                    "hostPort": 8443,
		                    "protocol": "tcp",
		                    "appProtocol": "http"
		                },
		                {
		                    "name": "pirate-kong-8444-tcp",
		                    "containerPort": 8444,
		                    "hostPort": 8444,
		                    "protocol": "tcp",
		                    "appProtocol": "http"
		                }
		            ],
		            "essential": true,
		            "environment": [
		                {
		                    "name": "KONG_NGINX_HTTP_GZIP_PROXIED",
		                    "value": "any"
		                },
		                {
		                    "name": "KONG_NGINX_HTTP_GZIP_COMP_LEVEL",
		                    "value": "6"
		                },
		                {
		                    "name": "KONG_PLUGINS",
		                    "value": "bundled,request-transformer_1251"
		                },
		                {
		                    "name": "KONG_DATABASE",
		                    "value": "postgres"
		                },
		                {
		                    "name": "KONG_LOG_LEVEL",
		                    "value": "warn"
		                },
		                {
		                    "name": "KONG_PROXY_STREAM_ACCESS_LOG",
		                    "value": "off"
		                },
		                {
		                    "name": "KONG_PG_HOST",
		                    "value": "<pg_rds_host>"
		                },
		                {
		                    "name": "KONG_NGINX_HTTP_GZIP_VARY",
		                    "value": "on"
		                },
		                {
		                    "name": "KONG_PG_PASSWORD",
		                    "value": "<pg_db_password>"
		                },
		                {
		                    "name": "KONG_PG_DATABASE",
		                    "value": "<pg_db_name>"
		                },
		                {
		                    "name": "KONG_PROXY_ACCESS_LOG",
		                    "value": "off"
		                },
		                {
		                    "name": "KONG_NGINX_HTTP_GZIP_TYPES",
		                    "value": "application/json"
		                },
		                {
		                    "name": "KONG_PG_USER",
		                    "value": "<pg_username>"
		                },
		                {
		                    "name": "KONG_ADMIN_LISTEN",
		                    "value": "0.0.0.0:8001, 0.0.0.0:8444 ssl"
		                },
		                {
		                    "name": "KONG_NGINX_HTTP_GZIP",
		                    "value": "on"
		                }
		            ],
		            "mountPoints": [],
		            "volumesFrom": [],
		            "logConfiguration": {
		                "logDriver": "awslogs",
		                "options": {
		                    "awslogs-create-group": "true",
		                    "awslogs-group": "/ecs/pirate-kong",
		                    "awslogs-region": "us-east-1",
		                    "awslogs-stream-prefix": "ecs"
		                },
		                "secretOptions": []
		            },
		            "healthCheck": {
		                "command": [
		                    "CMD-SHELL",
		                    "kong health"
		                ],
		                "interval": 30,
		                "timeout": 5,
		                "retries": 3,
		                "startPeriod": 120
		            }
		        }
		    ],
		    "family": "pirate-kong",
		    "executionRoleArn": "<AWS ROLE>",
		    "networkMode": "awsvpc",
		    "revision": 20,
		    "volumes": [],
		    "status": "ACTIVE",
		    "requiresAttributes": [
		        {
		            "name": "com.amazonaws.ecs.capability.logging-driver.awslogs"
		        },
		        {
		            "name": "ecs.capability.execution-role-awslogs"
		        },
		        {
		            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.19"
		        },
		        {
		            "name": "ecs.capability.container-health-check"
		        },
		        {
		            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"
		        },
		        {
		            "name": "ecs.capability.task-eni"
		        },
		        {
		            "name": "com.amazonaws.ecs.capability.docker-remote-api.1.29"
		        }
		    ],
		    "placementConstraints": [],
		    "compatibilities": [
		        "EC2",
		        "FARGATE"
		    ],
		    "requiresCompatibilities": [
		        "FARGATE"
		    ],
		    "cpu": "1024",
		    "memory": "2048",
		    "runtimePlatform": {
		        "cpuArchitecture": "ARM64",
		        "operatingSystemFamily": "LINUX"
		    },
		    "registeredAt": "2023-08-29T13:50:15.622Z",
		    "registeredBy": "<AWS ROLE>",
		    "tags": []
		}
```
</details>

This calls the public image with a few environmental variables referencing the database and cache. The service is designed to run as many copies of this task as required, scaling them up and down as needed. In terms of networking, the containers are assigned a public IP address, which allows the image to be pulled, and are otherwise attached to a private subnet. I also had to configure security groups to allow access to the database, cache, and Lambda function.

With the basic Kong container in place, it was time to get traffic two and from it! At the front end, a Network Load Balancer interfaces between the broader internet and however many Kong containers are currently running. It’s configured to distribute traffic evenly between functioning containers, and Route53 is used to set the DNS for api.pirateweather.net to this load balancer or a fallback (more on that in a minute). For the back-end, I configured Kong to pass requests to a Lambda function using their built in plugin and a [Lambda endpoint](https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc-endpoints.html) in my VPC. I did all the Kong setup using the wonderful [Konga](https://github.com/pantsel/konga) running in a docker container on a management EC2 VM.

### Fallback
While this setup is designed to be resilient and reliable, I’m always thinking about possible failures, and Route53 has a tool built specifically for this! By adding in a healthcheck, Route53 will either return the DNS for the Elastic Load Balancer, or in case there’s an issue with my Konga setup, fall back to AWS API HTTP Gateway. This does not provide quota management or allow for new registrations but keeps things running at a baseline level.

Compared to the regular AWS API Gateway, this setup has advantages and disadvantages. The always on database, container, and cache result in a slightly higher bill than before; however, this should remain relatively flat with increased usage. It’s equally fast, provides a wider range of customisation options, and scaled past the 10,000th key without missing a beat! In six months of production this setup has been rock solid, easily handling more than 20 million requests per month.

### Apiable
Sitting alongside all of it is [Apiable](https://www.apiable.io/). This service was exactly what I was looking for to replace my depreciated AWS developer portal, handling registration, signups, and quota plans. Their service interfaces with my Kong admin API via the same port/ load balancer but a [different endpoint within Kong](https://docs.konghq.com/gateway/latest/admin-api/), so all I had to do to connect the two was create an admin consumer API key and point the URL to the correct place.
