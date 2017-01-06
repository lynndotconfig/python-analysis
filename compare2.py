base = 1
def get_compare(base):
	def real_compare(value):
		return value < base

compare_with_10 = get_compare(10)
print compare_with_10(5)
print compare_with_10(20)