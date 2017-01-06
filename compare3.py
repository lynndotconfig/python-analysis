base = 1
def get_compare(base):
	def real_compare(value, base=base):
		return value > base
	return real_compare

compare_with_10 = get_compare(10)
print compare_with_10(5)
print compare_with_10(20)
print compare_with_10(5, 1)
print compare_with_10(25, 30)