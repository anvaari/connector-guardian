# Connector's Guardian

Guardian you need for your Kafka Connect connectors. It check status of connectors and tasks and restart if they are failed.

## How It work

Connector's Guardian interact with Kafka Connect cluster using its [rest api](https://docs.confluent.io/platform/current/connect/references/restapi.html) and parse returned json with [jq](https://github.com/jqlang/jq).

## Container image

You can pull image from Docker hub:

* [https://hub.docker.com/r/anvaari/connector-guardian](https://hub.docker.com/r/anvaari/connector-guardian)

## Usage

The image is optimized to use in k8s/okd4 environments. You can simply deploy provided [deployment.yaml](./deploy/deployment.yaml) with `kubectl` (on k8s) or `oc` (on okd):

**Important:** Change [environment](#environment-variables) variables to match your Kafka Connect cluster before deploying.

```bash
oc apply -f deploy/deployment.yaml -n {your_namespace_name}
```

```bash
kubectl apply -f deploy/deployment.yaml -n {your_namespace_name}
```

After deploying, it creates 1 pod which run a bash script every 5 minutes. So all failed connectors and tasks will restart.

**Note:** It ignore `PAUSED` connector so it don't restart failed task of `PAUSED` connectors.

### Environment variables

In order to use Docker image you need to set some environment variables:

* `KAFKA_CONNECT_HOST`: Default = `localhost`
* `KAFKA_CONNECT_PORT`: Default = `8083`
* `KAFKA_CONNECT_PROTO`: Default = `http`
* `KAFKA_CONNECT_USER`: Default = `''`
* `KAFKA_CONNECT_PASS`: Default = `''`

**Note:** Set values for `KAFKA_CONNECT_USER` and `KAFKA_CONNECT_PASS` only if Kafka Connect cluster need basic authentication otherwise don't set them.

## To Do

* Make Docker Image usable in non ks8 environments.
