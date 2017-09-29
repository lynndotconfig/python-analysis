import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

# declare exchange, if not exist, then create it, else go on;
channel.exchange_declare(
    exchange="hello-exchange",
    type="direct",
    passive=False,
    durable=True,
    auto_delete=False
)

channel.queue_declare(queue="hello-queue")  # declare queue
channel.queue_bind(
    queue="hello-queue",
    exchange="hello-exchange",
    routing_key="hola"
)


def msg_consumer(channel, method, header, body):  # function for consumer
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == 'quit':
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_comsuming()
    else:
        print body
    return

channel.basic_consume(  # subscribe consumer
    msg_consumer,
    queue="hello-queue",
    consumer_tag="hello-consumer"
)

channel.start_consuming()  # start to comsume
