
# [0.1.0](https://github.com/anvaari/connector-guardian/releases/tag/0.1.0)
  
First version of connector guardian which use simple bash script which restart failed connector and task in each run

# [0.2.0](https://github.com/anvaari/connector-guardian/releases/tag/0.2.0)

* Migrate to python
* Add helm chart thanks to [Amin](https://github.com/alashti)
* Add `docker-compose.yaml` so connector guardian can be used for non-cloud environment
* `KAFKA_CONNECT_PROTO` changed to `KAFKA_CONNECT_PROTOCOL`

# [0.3.0](https://github.com/anvaari/connector-guardian/releases/tag/0.3.0)

* Add restart back off mechanism. Read more [here](./README.md#features)
* Some enhancement on helm chart
* Solve [#11](https://github.com/anvaari/connector-guardian/issues/11) and [#12](https://github.com/anvaari/connector-guardian/issues/12)

# [0.3.1](https://github.com/anvaari/connector-guardian/releases/tag/0.3.1)

* Fix some bugs
  * Change default value of `EXPONENTIAL_RATIO` to 2
  * Add config validator to prevent connector guardian to run when invalid configs provided
  * Handle error prone situation in math.log in [connector_restart](https://github.com/anvaari/connector-guardian/blob/4b54e8ba34d7f102029904375f185e56a62bc1d6/functionalities/connector_restart.py#L58)
  