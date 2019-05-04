import requests
from bs4 import BeautifulSoup
import re
import time

def main():
	startTime = time.time()
	totalPageNumber, soup = getTotalPageNumber()
	print("This is first page: ", getInfoFromSoup(soup)) #printing out the first page seperatly
	for i in range (2,totalPageNumber):
		time.sleep(0.1)
		print("preparing page: " + str(i))
		soup = rerest(i)
		print("This is " + str(i) + " page: ", getInfoFromSoup(soup))
	endTime = time.time()
	print("Total time consume: ", endTime - startTime)

# get data from specific page number
# return soup object
def rerest(pageNum):
	start = "https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=" + str(pageNum) + "&coinId=2&tradeType=sell&blockType=general&online=1"
	soup = BeautifulSoup(requests.get(start).content, features = "lxml")
	return soup

# get total  page number from first page for itteration
def getTotalPageNumber():
	soup = rerest(1)
	p = soup.select('p')
	#matchObj = re.search( r'totalPage\W\W(.*)\W\WcurrPage', str(p)) --------also works
	matchObj = re.search(r'totalPage":(.*),"currPage', str(p))
	if matchObj:
		return int(matchObj.group(1)), soup

	else:
		print("Page number No Found!")
		return 1, soup

# Get information from soup from each page.
# Return a list of list which contain all the necessary numbers in the order of (UID, MIN, MAX, PRICE, AMOUNT)
def getInfoFromSoup(soup):
	matchObj = re.findall(r'"uid":(.*?),"userName"|minTradeLimit":(.*?),"isOnline"', str(soup.select('p')))
	temp = 1
	holder = []
	for item in matchObj:
		if(temp == 1):
			holder.append(list(item[0].split(' ')))
			temp *= -1
		else:
			holder[-1].extend(re.findall(r'[-+]?\d*\.\d+|\d+', item[1]))
			temp *= -1
	return holder
main()