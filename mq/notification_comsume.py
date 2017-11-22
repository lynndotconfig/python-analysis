import pika, json

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.exchange_declare(
    exchange="trove",
    exchange_type="topic",
    auto_delete=False
)

channel.queue_declare(queue="notifications.info", auto_delete=False)
channel.queue_bind(
    queue="notifications.info",
    exchange="trove",
    routing_key="notifications.info"
)


def api_ping(channel, method, header, body):
    """ping API call."""
    channel.basic_ack(delivery_tag=method.delivery_tag)
    msg_dict = json.loads(body)
    print "Recive API call----------------------", msg_dict


channel.basic_consume(
    api_ping,
    queue="notifications.info",
    consumer_tag="notifications.info"
)
print "Waiting for RPC call..."
channel.start_consuming()
