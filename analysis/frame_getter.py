import sys

# def get_current_frame():
# 	try:
# 		1/0
# 	except Exception as e:
# 		type, value, traceback = sys.exc_info()
# 		return traceback.tb_frame.f_back

# get_current_frame()

try:
	1/0
except Exception as e:
	type, value, traceback = sys.exc_info()
	print traceback.tb_frame.f_back