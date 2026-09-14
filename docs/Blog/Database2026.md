# Databases for days

Databases have always been one of the parts of Pirate Weather's infrastructure that I try not to touch unless I absolutely have to. There's plenty of weater data to worry about without adding user data on top of it, and user data is much higher stakes to make sure it's handlled correctly. Weather data is relatively straightforward: download some files, process them, save them somewhere fast, and read them when someone makes an API request. User accounts, API keys, rate limits, subscriptions, and authentication state are a little different.

Those need a database; however, the good news is that Kong and Apibale do all of this for me, happily interfacing with PostgreSQL to keep track of everything. Until August 27, when several long-time Pirate Weather users suddenly started receiving `403 Unauthorized` responses from the API. Their Apibale subscriptions were showing as expired and, more concerningly, their API keys had been revoked.

This ultimately turned into one of the stranger Pirate Weather incidents in a while. After checking with Apiable, around 140 subscriptions had unexpectedly been removed due to a glitch in how their cleanup scripts responded to manual actions I had taken, requiring me to recover their Kong consumers, API keys, access-control settings, and rate limits from a backup database without overwriting anything that had legitimately changed in production (mostly new signups).

The good news is that I had backup, so the underlying data was there. The slightly less good news is that restoring everything turned out to be considerably more complicated than I initially expected.

## Some database background

As described in my previous [Kong infrastructure post](KongGatewayInfrastructure.md), Pirate Weather uses Kong Gateway to handle authentication and rate limiting.

Behind Kong is a PostgreSQL database running on Amazon RDS. This database stores most of the persistent state associated with the API gateway. Conceptually, an API user isn't represented by just an API key. Kong has a **consumer** object, with other records connected to it for things like:

* API key credentials;
* Access Control Lists (ACLs);
* Rate-limit configuration; and
* Other gateway metadata.

Apibale sits on top of this and handles the user-facing registration and subscription process. When someone signs up, the relevant configuration goes into Kong, and Kong uses that information to decide whether an incoming request should be allowed.

### RDS

Pirate Weather’s Kong database runs on Amazon Aurora PostgreSQL through RDS, using an Aurora Serverless v2 writer instance. Aurora separates the logical database cluster from the underlying database instance, so Kong connects to the cluster while AWS manages the actual compute and storage underneath it. For Pirate Weather, I just use a single writer instance rather than a larger multi-instance or read-replica setup, since Kong’s database load is relatively small and there isn’t much benefit to adding additional database capacity just for the sake of it. Kong also continues if there's a hiccup in the database connection, so it's not a mission critical part of the stack.

The database instance itself uses Aurora Serverless v2, configured to scale between 0.5 and 3 Aurora Capacity Units (ACUs). AWS roughly maps that to about 1–6 GB of memory, along with proportional CPU and networking capacity. This is a particularly good fit for Pirate Weather because the database is important, but it is not continuously busy. Most API requests are handled by Kong and the weather API containers without generating heavy database activity, while things like user registrations, subscription changes, API-key management, and administrative operations create comparatively short bursts of work. Serverless v2 means I can keep the baseline database very small (and cost effective) most of the time, while still allowing it to scale automatically if there is suddenly more activity. It also avoids me having to pick a fixed EC2-style database instance size and then either pay for unused capacity or discover at an inconvenient time that I picked something too small.

On the storage side, Aurora takes care of the details almost entirely for me. The cluster uses Aurora’s managed storage layer rather than storage attached directly to the database instance, so I don’t need to provision disks, choose IOPS, or manually expand the volume as the database grows. The database is encrypted at rest using an AWS-managed KMS key, and RDS manages the underlying database infrastructure, backups, maintenance, and recovery mechanisms. This is exactly the kind of thing I want from a database service: PostgreSQL behaves like PostgreSQL, while most of the systems-administration work disappears into AWS.

One important architectural detail is that the Kong database is persistent state in a way that most of Pirate Weather’s other infrastructure is not. If an ECS container disappears, I can start another one. If an EC2 instance disappears, autoscaling can replace it. Weather model data can be downloaded and regenerated. The PostgreSQL database is different: it contains the relationships between Kong consumers, API credentials, ACLs, rate limits, and the rest of the gateway configuration. That makes the database both relatively small and disproportionately important, hence the benefit to having AWS handle it. 

## The incident

The first report came through [GitHub issue #675](https://github.com/Pirate-Weather/pirateweather/issues/675), when a user reported that an API key they had been using for several years had suddenly stopped working. Their subscription appeared as expired in Apiable and requests were returning `403 Unauthorized`.

Shortly afterwards, another user reported the same thing.

At first I was worried that this was a much larger failure involving all Apiable-managed subscriptions. However, Apiable quickly tracked the problem down to a rogue cleanup job that had incorrectly removed approximately **140 subscriptions**, which also explained why none of my existing monitoring had noticed anything.

From the API's perspective, everything was healthy. Containers were running, requests were being served, Kong was responding normally, and the overwhelming majority of API keys continued to work. Losing 140 subscriptions was extremely significant for the people affected, but relatively small compared with the total number of users, so it didn't cross any of the thresholds I had configured.

### Why I couldn't just restore the backup

If I simply replaced the production database with an older copy, the deleted users would come back, but anything legitimately created or modified since that backup could disappear.

For example, imagine the backup looked like this:

```text
Backup:
User A
User B
User C
User D
```

And production now looked like:

```text
Production:
User A
User C
User D
User E
```

In this example, `User B` was accidentally deleted, while `User E` legitimately registered after the backup was taken. 

Restoring the backup fixes User B but deletes User E, so this was more off a diff and merge operation than restore. So the backup was still required, but not in a "restore the backup" sort of way.

### Comparing production against the backup

The first step was to bring up the backup database separately and connect directly to both PostgreSQL databases. I'd never had to do this before, since it's always been managed by Kong, but it turns out AWS makes it pretty straightforward. I took the most recent backup that had the missing keys, hit restore, and spun it up as a new cluster with its own endpoint. From there, I could compare the consumer records in the backup against production and identify objects that existed in the backup but no longer existed in the live database.

This worked well and produced roughly the number of missing records I expected based on Apiable's investigation.

My initial assumption was that only the API key credentials had been removed. That would have made the recovery relatively straightforward: find the missing credentials and recreate them through the Kong Admin API. However, after a bit of searching it turned out that the entire consumer object was gone, not just the keys, so there was nothing to attach the recovered API keys to.

And since ACL memberships and rate-limit configuration are also associated with those consumers, simply putting the key-auth credentials back wouldn't restore the account to its previous state.

So the recovery process expanded to:

1. Identify consumers present in the backup but missing from production.
2. Recreate those consumers through the Kong Admin API.
3. Restore their ACL memberships.
4. Restore their rate-limit configuration.
5. Restore their key-auth credentials.

Importantly, this was all additive. Existing production consumers weren't overwritten or recreated. so no risk to expanding the outage. A dozen lines of Python later and all the consumers and keys were back, I could spin down the backup database, and things returned more or less to normal.

## Lessons learned 

Three high level takeaways from this incident:

1. There's room for improvement on my monitoring front. I don't have a good plan for this yet, but I'd like some way to detect and catch these localized incidents. 
2. Database backups are important- I was very happy that RDS managed all of it and I had a week of daily backups, but I've expanded that to keep backups around for longer in case something needs to be restored from a different point. 
3. I've added a fallback network pathway I can use if something like this happens again or in case of a different issue with Kong. Using AWS API Gateway, I can proxy requests directly to the production servers, allowing data to keep flowing in the case of an issue with the auth. It has the capacity for basic rate limits to ensure nothing gets overloaded, buying time for the main server to come back up again.