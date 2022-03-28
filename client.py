import os
import pika

def publish_pip(pip):
    """
    publish a message to MQ server
    """

    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='pb_control')

        channel.basic_publish(exchange='', routing_key='pb_control', body=pip)
        print(" [x] "+pip)
        connection.close()
    except Exception as e:
        print(e)
        print("MQ failed, saved locally")

if True:

    RABBITMQ_SERVER=os.getenv("RABBITMQ_SERVER")
    RABBITMQ_USER=os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        service_check(body.decode("utf-8"))


    if RABBITMQ_PASSWORD is None or RABBITMQ_USER is None or RABBITMQ_SERVER is None:
        print("no config, using localhost and guest/guest")
        RABBITMQ_SERVER='localhost'
        RABBITMQ_USER='guest'
        RABBITMQ_PASSWORD='guest'
    else:
        print ("aceepted rabbit, mode RABBITMQ")
    publish_pip("test")
