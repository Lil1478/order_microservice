import pika
import configparser
import json

config = configparser.ConfigParser()
config.read("configuration.ini")

rabbit_config = config["rabbit"]

rabbit_host = rabbit_config["host"]
rabbit_user = rabbit_config["user"]
rabbit_password = rabbit_config["password"]

credentials = pika.PlainCredentials(rabbit_user, rabbit_password)


def publish_message(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="is_queue")

    channel.basic_publish(exchange="", routing_key="is_queue", body=json.dumps(body))
    connection.close()
