from web import web
import time

def main():
	print("Web Started!")
	while True:
		starttime = time.time()
		web()
		# for i in range (1,2):
		# 	print("sleeping: ", i, "- 5.", end='\r')
		# 	time.sleep(1)
		print()
		print("Total time consumed: ", time.time() - starttime)
main()