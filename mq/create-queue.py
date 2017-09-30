import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

# declare exchange, if not exist, then create it, else go on;
channel.exchange_declare(
    exchange="logs-exchange",
    exchange_type="topic",
    passive=False,
    durable=True,
    auto_delete=False
)

channel.queue_declare(queue="msg-inbox-errors")  # declare queue
channel.queue_declare(queue="msg-inbox-logs")  # declare queue
channel.queue_declare(queue="all-logs")  # declare queue

channel.queue_bind(
    queue="msg-inbox-errors",
    exchange="logs-exchange",
    routing_key="error.msg-inbox"
)
channel.queue_bind(
    queue="msg-inbox-logs",
    exchange="logs-exchange",
    routing_key="*.msg-inbox"
)
