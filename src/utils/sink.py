import os
import json

from kafka import KafkaProducer

# Get Kafka environment variables
KAFKA_HOST = os.getenv("KAFKA_HOST", "0.0.0.0")
KAFKA_PORT = int(os.getenv("KAFKA_PORT", "9092"))
KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"


def sink_data(key: str, message: str):
    """
    Sinks data to the Kafka server

    Parameters
    ----------
    key : str
        The key of the message
    message : str
        The message to send, in JSON format
    """
    prod = KafkaProducer(bootstrap_servers=[KAFKA_SERVER], value_serializer=lambda x: json.dumps(x).encode("utf-8"))
    prod.send(key, value=message)
