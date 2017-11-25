import pika
import uuid

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

class FibonacciRpcClient(object):

	def __init__(self):
		self.conn = conn_broker
		self.channel = self.conn.channel()
		self.callback_queue = self.channel.queue_declare(exclusive=True)
		self.channel.basic_consume(
			self.on_response,
			queue=self.callback_queue.method.queue)

	def on_response(self, channel, method, props, body):
		if self.correlation_id == props.correlation_id:
			self.response = body

	def call(self, n):
		self.response = None
		self.correlation_id = str(uuid.uuid4())
		self.channel.basic_publish(
			exchange="",
			routing_key="rpc_server",
			body=str(n),
			properties=pika.BasicProperties(
				correlation_id=self.correlation_id,
				reply_to=self.callback_queue.method.queue))
		while self.response is None:
			self.conn.process_data_events()
		return int(self.response)


fibonacci_rpc = FibonacciRpcClient()
result = fibonacci_rpc.call(9)
print "fib(9) is %s" % result
