# daas-api
The Diastema DaaS API. This is an oversimplified API which simply acts as a mediator between external services and the internal DaaS service.

## How to Use
This project is inteded to by used by [the Diastema orchestrator](https://github.com/DIASTEMA-UPRC/orchestrator). If you need information on how to use it alongside other components, please refer to that documentation. If you need information on how to run this in isolation, follow the steps described below:

### Prerequisites
+ Docker
+ RabbitMQ
+ Mongo
+ Kafka

### How to Build
```bash
docker build -t daas-api:latest .
```

### How to Run
The dev Docker-compose creates an isolated environment and I leave it up to you to figure out how you want to access RabbitMQ to check the messages. Other than that you can simply run the service exactly how its described below and perform your requests

```bash
docker-compose up
```

### Routes

| Route | Method |
| ----- | ------ |
| /data-ingesting | POST |
| /data-cleaning | POST |
| /data-sink | POST |
| /join | POST |

#### Subroutes
These subroutes exist on the queue-based processes. These processes are:
+ Data Ingesting
+ Data Cleaning
+ Join
For these you can use the following subroutes to check the status of the process:

| Route | Method | Argument | Description |
| ----- | ------ | -------- | ----------- |
| /progress | GET | ?id | Returns the progress of the process based on the ID argument |
| /job | GET | job | Returns the result of the process based on the ID on the route |

## License
Licensed under the [Apache License Version 2.0](README) by [Konstantinos Voulgaris](https://github.com/konvoulgaris) for the research project Diastema
