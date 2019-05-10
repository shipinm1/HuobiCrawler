import requests
from bs4 import BeautifulSoup
import re
import time
import sqlite3
import math


def web():

	tokens = ['buy', 'sell']
	for token in tokens:
		stackHolder = []
		totalPageNumber, soup = getTotalPageNumber(token)
		stackHolder.extend(getInfoFromSoup(soup))
		totalPageNumber = math.ceil(totalPageNumber * 0.7) #only interested in the upper 70% of the output(estimated)
		for i in range (2, totalPageNumber):
			time.sleep(0.1)
			soup = makeSoup(i, token)
			stackHolder.extend(getInfoFromSoup(soup))
			print("Compeletion: ", i, "-", totalPageNumber,", Token=",token ,end='\r' )
		print()
		#database operation---------------
		sendToDatabase(stackHolder, token)
		#---------------------------------

# get data from specific page number
# return soup object
def makeSoup(pageNum, token):
	start = "https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=" + str(pageNum) + "&coinId=2&tradeType=" + token + "&blockType=general&online=1"
	soup = BeautifulSoup(requests.get(start).content, features = "lxml")
	return soup

# get total  page number from first page for itteration
def getTotalPageNumber(token):
	soup = makeSoup(1, token)
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

#sending data to the database
def sendToDatabase(info, table):
	conn = sqlite3.connect('huobidata.db')
	print("Database connected")
	c = conn.cursor()
	c.execute("DELETE FROM '%s'" % table)
	for item in info:
		#print("INSERT INTO sell VALUES (?,?,?,?,?)", item)
		#c.execute("INSERT OR REPLACE INTO sell VALUES(12367, 2, 3, 4, 5)")
		c.execute("INSERT OR REPLACE INTO '%s' VALUES (?,?,?,?,?)" % table ,item)
	conn.commit()
	print("Database closed")
	conn.close()		
	pass