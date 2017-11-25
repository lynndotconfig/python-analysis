import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)

conn_broker = pika.BlockingConnection(conn_params)  # connect to server
channel = conn_broker.channel()  # get channel

channel.queue_declare(queue="rpc_server")

# summary = {
# 	'0': 0,
# 	'1': 1,
# }

# def fib(n):
# 	if not isinstance(n, int):
# 		raise ValueError('n must be int.')
# 	global summary
# 	if n < 0:
# 		raise ValueError("n must be non-negative.")
# 	for i in range(n + 1):
# 		if str(i) in summary.keys():
# 			continue
# 		s = summary.get(str(i-2)) + summary.get(str(i - 1))
# 		summary[str(i)] = s
# 	return summary.get(str(n))

def mem_cache(func):
	memory = {
		"0": 0,
		"1": 1
		}
	def wrap(n):
		if str(n) in memory:
			return memory.get(str(n))
		result = func(n)
		memory[str(n)] = result
		return result
	return wrap

@mem_cache
def fib(n):
	return fib(n - 1) + fib(n - 2)

def on_proccess(channel, method, headers, body):
	n = int(body)
	print "[.] fib(%s)" % n
	result = fib(n)
	channel.basic_publish(
		exchange="",
		routing_key=headers.reply_to,
		body=str(result),
		properties=pika.BasicProperties(
			correlation_id=headers.correlation_id))
	channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
	on_proccess,
	queue="rpc_server")

print "[x] Awaiting RPC Request"
channel.start_consuming()