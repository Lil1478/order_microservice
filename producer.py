import pika, json

params = pika.ConnectionParameters(host='localhost')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='order', body=json.dumps(body), properties=properties)