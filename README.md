# Connector's Guardian

Guardian you need for your Kafka Connect connectors.

## How It work

Connector's Guardian interact with Kafka Connect cluster using its [rest api](https://docs.confluent.io/platform/current/connect/references/restapi.html) and parse returned json with [jq](https://github.com/jqlang/jq) (in version [0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)) and with json library in python (from version[0.2.0](https://github.com/anvaari/connector-guardian/releases/tag/0.2.0)).

## Features

* **Auto Connector Restart**: It check status of connectors and tasks and restart if they are failed. **Available from [V0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)**

* **Restart Back Off**: The restarts will happen always after an increasing time period. The first restart will happen immediately at first run. If it does not help, the next restart will happen only after `EXPONENTIAL_RATIO ^ 1` run. If even the second restart doesn’t help, the next restart will be done only after another `EXPONENTIAL_RATIO ^ 1` run. And so on. This leaves more time for the root cause of the failure to be resolved. Thanks to this back-off mechanism, even if the network outage takes over these minutes, the auto-restart will help your connectors to recover from it. The last Restart (= `MAX_RESTART`) restart will happen after `EXPONENTIAL_RATIO ^ 1` run from the initial failure. But if the issue is not resolved even after the last restart, the Guardian will stop restarting and it is up to you to solve it manually.

## Usage

### Container image

You can pull image from Docker hub:

* [https://hub.docker.com/r/anvaari/connector-guardian](https://hub.docker.com/r/anvaari/connector-guardian)

### Non Cloud Environments

You can use provided [docker-compose](./deploy/docker-compose.yaml) to deploy connector guardian in your server

Before deploying image, make sure to set appropriate environment variables in [docker-compose.yaml](./deploy/docker-compose.yaml)

```bash
cd deploy
docker compose up -d
```

### Kubernetes or Open Shift

You can use provided helm chart: (You can see guid for install helm [here](https://helm.sh/docs/intro/install/))

Before deploying chart, make sure to set appropriate environment variables in [values.yaml](./deploy/chart/values.yaml)

```bash
helm upgrade connector-guardian --install -n {your_namespace_name} -f deploy/chart/values.yaml deploy/chart
```

After deploying, it creates 1 pod which run a `connector_guardian.py` every 5 minutes.

### Environment variables

In order to use Docker image, [docker-compose](./deploy/docker-compose.yaml) or [helm chart](./deploy/chart/),  you need to set some environment variables:

* `KAFKA_CONNECT_HOST`: Default = `localhost`
  * Host of your kafka connect cluster (without `http` or `https` and any `/` at the end and also port)
* `KAFKA_CONNECT_PORT`: Default = `8083`
  * Port of kafka connect cluster for rest api
* `KAFKA_CONNECT_PROTO`: Default = `http`
  * Protocol for kafka connect host. Should be `http` and `https`
* `KAFKA_CONNECT_USER`: Default = `''`
* `KAFKA_CONNECT_PASS`: Default = `''`
* `MAX_RESTART` : Default = `7`
  * Maximum number of continuouse restart for each connector
* `EXPONENTIAL_RATIO`: Default = `1`
  * Exponential ratio to increase sleep between each connector restart.

**Note:** Set values for `KAFKA_CONNECT_USER` and `KAFKA_CONNECT_PASS` only if Kafka Connect cluster need basic authentication otherwise don't set them.

## Change Log

### [0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)
  
First version of connector guardian which use simple bash script which restart failed connector and task in each run

### [0.2.0](https://github.com/anvaari/connector-guardian/releases/tag/0.2.0)

* Migrate to python
* Add helm chart thanks to [Amin](https://github.com/alashti)
* Add `docker-compose.yaml` so connector guardian can be used for non-cloud environment
* `KAFKA_CONNECT_PROTO` changed to `KAFKA_CONNECT_PROTOCOL`

### [0.3.0](https://github.com/anvaari/connector-guardian/releases/tag/0.3.0)
* Add restart back off mechanism. Read more [here](#features)
* Some enhancement on helm chart