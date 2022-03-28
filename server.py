import os
import pika

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
        RABBITMQ_PASSWORD='guest*'
    else:
        print ("aceepted rabbit, mode RABBITMQ")

while True:
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
#        channel.basic_qos(prefetch_count=1, global_qos=False)
        channel.queue_declare(queue='pb_control')
        channel.basic_consume(queue='pb_control', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
#    except pika.exceptions.AMQPConnectionError:
#        print ("retry connecting to rabbit")
#        time.sleep(6)
    except Exception as e1:
        print (e1)
        print ("retry connecting to rabbit")
        time.sleep(6)
