import time, json, pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

msg = json.dumps({
    "client_name": "RPC Client 1.0",
    "time": time.time()
})

result = channel.queue_declare(exclusive=True, auto_delete=True)
msg_props = pika.BasicProperties()
msg_props.reply_to = result.method.queue
channel.basic_publish(
    body=msg, 
    exchange="rpc",
    properties=msg_props,
    routing_key="ping"
)

print "Sent 'ping' RPC call. Waiting for reply..."

def reply_call(channel, method, header, body):
    """Receives RPC Server replies."""
    print "RPC Relpy ---- %s" %(body)
    channel.stop_consuming()

channel.basic_consume(
    reply_call,
    queue=result.method.queue,
    consumer_tag=result.method.queue
)

channel.start_consuming()
