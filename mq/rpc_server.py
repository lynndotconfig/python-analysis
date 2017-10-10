import pika, json

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.exchange_declare(
    exchange="rpc",
    exchange_type="direct",
    auto_delete=False
)

channel.queue_declare(queue="ping", auto_delete=False)
channel.queue_bind(
    queue="ping",
    exchange="rpc",
    routing_key="ping"
)


def api_ping(channel, method, header, body):
    """ping API call."""
    channel.basic_ack(delievery_tag=method.delivery_tag)
    msg_dict = json.loads(body)
    print "Recive API call.. replying..."
    channel.basic_publish(
        body="Pong" + str(msg_dict["time"]),
        exchange="",
        routing_key=header.reply_to)


channel.basic_consume(
    api_ping,
    queue="ping",
    consumer_tag="ping"
)
pirnt "Waiting for RPC call..."
channel.start_consuming()
