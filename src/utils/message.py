import os
import pika

# Get RabbitMQ environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "0.0.0.0")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))


def send_message(key: str, message: str, host: str=RABBITMQ_HOST, port: int=RABBITMQ_PORT):
    """
    Sends a message to the RabbitMQ server

    Parameters
    ----------
    key : str
        The key of the message
    message : str
        The message to send
    host : str, optional
        The address to connect to, by default RABBITMQ_HOST
    port : int, optional
        The port to connect to, by default RABBITMQ_PORT

    Raises
    ------
    Exception
        This exception is raised if the RabbitMQ connection fails
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()
    channel.queue_declare(queue=key, durable=True)
    channel.confirm_delivery()

    try:
        channel.basic_publish(exchange="", routing_key=key, body=message,
                                properties=pika.BasicProperties(
                                    content_type="application/json",
                                    delivery_mode=2
                              ), mandatory=True)
    except:
        raise Exception("Failed to send message!")

    connection.close()
