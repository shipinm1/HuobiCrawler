from web import web
import time

def main():
	print("Web Started!")
	while True:
		starttime = time.time()
		web()
		for i in range (1,60):
			print("sleeping: ", i, "- 60.", end='\r')
			time.sleep(1)
		print()
		print("Total time consumed: ", time.time() - starttime)
main()