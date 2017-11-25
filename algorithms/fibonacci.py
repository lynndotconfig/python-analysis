#########################################################

summary = {
	'0': 0,
	'1': 1,
}

def fib(n):
	if not isinstance(n, int):
		raise ValueError('n must be int.')
	global summary
	if n < 0:
		raise ValueError("n must be non-negative.")
	for i in range(n + 1):
		if str(i) in summary.keys():
			continue
		s = summary.get(str(i-2)) + summary.get(str(i - 1))
		summary[str(i)] = s
	return summary.get(str(n))


# #################################################
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
