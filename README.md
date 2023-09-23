# Connector's Guardian

Guardian you need for your Kafka Connect connectors.

## How It work

Connector's Guardian interact with Kafka Connect cluster using its [rest api](https://docs.confluent.io/platform/current/connect/references/restapi.html) and parse returned json with [jq](https://github.com/jqlang/jq) (in version [0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)) and with json library in python (from version[0.2.0](https://github.com/anvaari/connector-guardian/releases/tag/0.2.0)).

## Features

* **Auto Connector Restart**: It check status of connectors and tasks and restart if they are failed. **Available from [V0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)**

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

In order to use Docker image you need to set some environment variables:

* `KAFKA_CONNECT_HOST`: Default = `localhost`
  * Host of your kafka connect cluster (without `http` or `https` and any `/` at the end and also port)
* `KAFKA_CONNECT_PORT`: Default = `8083`
  * Port of kafka connect cluster for rest api
* `KAFKA_CONNECT_PROTO`: Default = `http`
  * Protocol for kafka connect host. Should be `http` and `https`
* `KAFKA_CONNECT_USER`: Default = `''`
* `KAFKA_CONNECT_PASS`: Default = `''`

**Note:** Set values for `KAFKA_CONNECT_USER` and `KAFKA_CONNECT_PASS` only if Kafka Connect cluster need basic authentication otherwise don't set them.

## Change Log

### [0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)
  
First version of connector guardian which use simple bash script which restart failed connector and task in each run

### [0.2.0](https://github.com/anvaari/connector-guardian/releases/tag/0.2.0)

* Migrate to python
* Add helm chart thanks to [Amin](https://github.com/alashti)
* Add `docker-compose.yaml` so connector guardian can be used for non-cloud environment
* `KAFKA_CONNECT_PROTO` changed to `KAFKA_CONNECT_PROTOCOL`
