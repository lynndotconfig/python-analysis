import sys
import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.exchange_declare(
	exchange="logs",
	exchange_type="fanout")


message = "".join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
	exchange="logs",
	routing_key="",
	body=message)

print "[x] Send Message: %s" % message

conn_broker.close()
