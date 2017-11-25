import sys
import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.exchange_declare(
	exchange="direct_logs",
	exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else "info"

message = "".join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(
	exchange="direct_logs",
	routing_key=severity,
	body=message)

print "[x] Send %s: %s" % (severity, message)

conn_broker.close()
