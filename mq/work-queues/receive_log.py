import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

queue = channel.queue_declare(exclusive=True)

channel.queue_bind(
	queue=queue.method.queue,
	exchange="logs"
	)


def process_log(channel, method, header, body):
	print "[x] Received: %s" % (body)
	channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
	process_log,
	queue=queue.method.queue)

channel.start_consuming()