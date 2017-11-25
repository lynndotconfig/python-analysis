import sys
import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.exchange_declare(
	exchange="topic_logs",
	exchange_type="topic")

severity = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"

message = "".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(
	exchange="topic_logs",
	routing_key=severity,
	body=message)

print "[x] Send %s: %s" % (severity, message)

conn_broker.close()
