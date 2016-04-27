#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Chyang Wong'


from bs4 import BeautifulSoup

def get_page(url):
	import urllib2
	if url != '' :
		headers = {
			'User-Agent':'Mozilla/5.0(Windows;U;WindowsNT 6.1;en-us;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
		}
		req = urllib2.Request(url, headers=headers)
		fails = 0
		while True:
			try:
				if fails >= 3:
					print 'Load URL Failed.'
					break
				page = urllib2.urlopen(req, timeout=20)
			except:
				fails += 1 
			else:
				break
	return page




if __name__ == "__main__":
	'''
	html = get_page('http://www.usebible.com/cbook/html/809/index.htm')
	soup = BeautifulSoup(html, 'html.parser')
	#print soup.select('table span:nth-of-type(1)')[0].get_text().strip()
	#print soup.select('table td:nth-of-type(12)')[0].get_text().strip()
	#print [{'url':str(x['href']),'text':x.get_text()} for x in soup.select('table table a[href^="Z"]')]
	print [{'url':str(x['href']),'text':x.get_text()} for x in soup.select('table table a[href^=19]')]

	'''
	html = get_page('http://books.edzx.com/html/book/0382/Index.html')
	soup = BeautifulSoup(html, 'lxml')
	
	print soup.select('#BookText ul li a')[0]
	#print "".join([unicode(x) for x in soup.select('div#content')[0].contents])
	#print soup.select('td.ccss a')[0]

	html2 = get_page('http://books.edzx.com/html/book/0382/1915.html')
	soup2 = BeautifulSoup(html2, 'lxml')
	#print soup2.select('#BookText')
	print "".join([unicode(x) for x in soup2.select('#BookText')[0].contents])
