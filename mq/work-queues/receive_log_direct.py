import sys
import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

queue = channel.queue_declare(exclusive=True)

severities = sys.argv[1:] if len(sys.argv) > 2 else ["info"]

for severity in severities:
	channel.queue_bind(
		queue=queue.method.queue,
		exchange="direct_logs",
		routing_key=severity)
print "[*] Waiting for logs. To exit press CTRL+C"

def process_log(channel, method, header, body):
	print "[x] Received: %r: %r" % (method.routing_key, body)
	channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
	process_log,
	queue=queue.method.queue)

channel.start_consuming()