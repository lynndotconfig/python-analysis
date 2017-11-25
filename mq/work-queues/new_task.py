import sys

import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.queue_declare(queue="task_queue", durable=True)

message = "".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
	exchange="",
	routing_key="task_queue",
	body=message,
	properties=pika.BasicProperties(
		delivery_mode=2, # make message persisten
		))

print "[x] Send %r" % message

conn_broker.close()