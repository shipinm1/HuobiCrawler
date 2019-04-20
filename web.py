import requests
from bs4 import BeautifulSoup
import re
import time

def main():
	totalPageNumber, soup = getTotalPageNumber()
	getInfoFromSoup(soup)
	for i in range (2,totalPageNumber):
		time.sleep(3)
		print("preparing page: " + str(i))
		soup = rerest(i)
		getInfoFromSoup(soup)
		print("========================page: " + str(i) + "==========================")

# get data from specific page number
# return soup object
def rerest(pageNum):
	start = "https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=" + str(pageNum) + "&coinId=2&tradeType=sell&blockType=general&online=1"
	soup = BeautifulSoup(requests.get(start).content, features = "lxml")
	return soup

# get total  page number for itteration
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
# get information from soup from each page.(minTradeLimit, maxTradeLimit, Price, )
def getInfoFromSoup(soup):
	matchObj = re.findall(r'minTradeLimit":(.*?),"maxTradeLimit', str(soup.select('p')))
	for item in matchObj:
		print(float(item))
main()