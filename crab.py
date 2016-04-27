# -*- coding: utf-8 -*-
import urllib2
import urllib
from  bs4 import BeautifulSoup
import re
import urlparse
import time
import os
import sys
import copy
#import pdb


def get_realurl(cur_url='', rel_url=''):
	url = ''	
	o =  urlparse.urlparse(url)
	if not o.netloc:
		cur_url = url_encode(cur_url)
		if cur_url and rel_url:
			url = urlparse.urljoin(cur_url, rel_url)
			url = reduce(lambda r,x:r.replace(x[0], x[1]), [('/../', '/')], url)	
	else:
		url = rel_url
	url = url.replace("../", '')
	url = url.replace("./", '')
	return url

def url_encode(url):
	o =  urlparse.urlparse(url)
	params = {}
	query = ''
	if o.query:
		for query_i in o.query.split('&'):
			params[query_i.split('=')[0]] =  urllib.quote(query_i.split('=')[1].decode('utf-8').encode('gb2312'))
		query = "&".join([k+'='+params[k] for k in params])
	return urlparse.urlunparse((o.scheme, o.netloc, o.path, '', query, ''))

def url_decode(url):
	o =  urlparse.urlparse(url)
	params = {}
	query = ''
	if o.query:
		for query_i in o.query.split('&'):
			params[query_i.split('=')[0]] =  urllib.unquote(query_i.split('=')[1]).decode('gb2312').encode('utf-8')
		query = "&".join([k+'='+params[k] for k in params])
	return urlparse.urlunparse((o.scheme, o.netloc, o.path, '', query, ''))

def recive_file(name='', url=''):
	try:
		conn = Connection()
		db = conn['crab']
		collection = db['recive_file']
		row = collection.find_one({"url":url})
		if row:
			new_filename =  row['file_path'] 
		else:
			cur_dir = './images/'+name+'/'
			if not os.path.exists(cur_dir):
				os.makedirs(cur_dir)
			ext = os.path.basename(urlparse.urlsplit(url)[2]).split('.')[1]
			new_filename = cur_dir + time.strftime('%Y%m%d%H%M%S', time.localtime()) +'.'+ ext
			urllib.urlretrieve(url, new_filename)[0]
			
			collection.insert({'url':url, 'file_path':new_filename})
		db.logout()
	except:
		#print'Export Data Failed.'
		pass
	return new_filename

	cur_dir = './images/'+name+'/'
	if not os.path.exists(cur_dir):
		os.makedirs(cur_dir)
	ext = os.path.basename(urlparse.urlsplit(url)[2]).split('.')[1]
	new_filename = cur_dir + time.strftime('%Y%m%d%H%M%S', time.localtime()) +'.'+ ext 
	return  urllib.urlretrieve(url, new_filename)[0]



class crab:
	
	soup = None


	PAGE_CHARSET_LIST = {'utf8':'UTF-8', 'gb2312':'GB2312', 'gbk':'GB18030'}
	PAGE_CHARSET_DEFAULT = PAGE_CHARSET_LIST['utf8']
	#PAGE_CHARSET_DEFAULT = PAGE_CHARSET_LIST['gbk']
	debug = True
	debug = False
	
	field_template = {'name':'', 'select':'', 'regex':'', 'number':0, 'url':False, 'multi':False, 'image':False, 'content':False}	

	def __init__(self, params):
		self.url = unicode(params['url'])
		self.fields = params['fields']
		self.set_charset(params['charset'])
		self.get_url()

	def debug(self):
		if self.debug:
			print 'Debug now openned .'
		else:
			print 'Debug now  closed .'
		return debug

	def set_debug(self, is_debug):
		self.debug = is_debug
		self.debug()
		
	def get_charset(self):
		return self.PAGE_CHARSET_DEFAULT


	def set_charset(self, charset='utf8'):
		b_charset = False
		if self.PAGE_CHARSET_LIST.has_key(charset):
			self.PAGE_CHARSET_DEFAULT = self.PAGE_CHARSET_LIST[charset]	
			b_charset = True
			print 'Charset has changed:'+self.PAGE_CHARSET_DEFAULT
		else:
			print 'Charset can not support your charset.'
		return b_charset


	def get_url(self):
		url = url_encode(self.url)
		if self.debug:
			print 'Load URL: ' + url
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
					#print self.PAGE_CHARSET_DEFAULT
					self.soup = BeautifulSoup(page.read(), 'lxml')
				except:
					fails += 1 
				else:
					break

	def get_fields(self):
		fields = {} 
		for field in self.fields:
			fields.update(self.get_field(field))
		return fields
	
	def get_field(self, field_params):
		field = copy.copy(self.field_template)
		field.update(field_params)
		if self.debug:
			print field
		value = None
		#pdb.set_trace()
		if field['select']:
			if field['multi']:
				if field['image']:
					images = [get_realurl(url, str(x['src'])) for x in self.soup.select(field['select'])] 
					value = [recive_file(self.name, x) for x in images]
				elif field['url']:
					value = [{'url':get_realurl(self.url, x.get('href')), 'file':x.get('href'), 'text':x.get_text()} for x in self.soup.select(field['select'])] 
				else:
					value = [str(x) for x in self.soup.select(field['select'])[0].contents] 
			else:
				if field['content']:
					content = "".join([unicode(x) for x in self.soup.select(field['select'])[0].contents])
					value = unicode(content) 
				else:
					number = 0
					if field['number']:
						number = int(field['number'])
						if number < 0:
							number = 0
					if field['image']:
						if not number:
							value  = recive_file(self.name, get_realurl(url, self.soup.select(field['select'])[0]['src']))
						else:
							value  = recive_file(self.name, get_realurl(url, self.soup.select(field['select'])[0].contents[number-1]['src']))
					else:
						if not number:
							value  = self.soup.select(field['select'])[0].get_text().strip()
						else:
							value = self.soup.select(field['select'])[0].contents[number-1].get_text().strip()


		if self.debug:
			print value
		field_new = {field['name']: value}
		return field_new

	

if __name__ == "__main__":

	reload(sys)
	sys.setdefaultencoding("utf-8")

	params = {
			'url':'http://www.usebible.com/cbook/html/746/index.htm',
			'fields':[
				{'name':'author', 'select':'table td:nth-of-type(12)', 'regex':''},	
				{'name':'title', 'select':'table td span:nth-of-type(1)', 'regex':''},	
				{'name':'pages', 'select':'table table a[href^=1]', 'regex':'', 'url':True, 'multi':True}	
			],
			'charset':'utf8'
		}	
	
	child_params = {
			'url':'',
			'fields':[
				{'name':'content', 'select':'div#content', 'regex':'', 'number':0, 'content':True}	
			],
			'charset':'utf8'
		}	

	book_index = crab(params) 
	index_data = book_index.get_fields()
	#print index_data

	pages_data = [] 
	for page in index_data['pages']:
		page_params = child_params
		page_params.update({'url':page['url']})
		page_index = crab(page_params)
		page_data = page_index.get_fields()
		page_data.update({'file':page['file'],'title':page['text']})
		pages_data.append(page_data)


	text_start = '''
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
			<title>__TITLE__</title>
				</head>
					<body>
'''
	text_start = text_start.replace('__TITLE__', index_data['title'])
	#print text_start

	text_end = '''
	</body>
</html>
'''
	if not os.path.exists(index_data['title']):
		os.makedirs(index_data['title'])

	text_content = """
	<h1>__TITLE__</h1>
	<p>__AUTHOR__</p>
	"""

	text_content = text_content.replace('__TITLE__', index_data['title']).replace('__AUTHOR__', index_data['author'])
	#print text_content
	text_content = text_content + ''.join(['<a href="'+page['file']+'">'+page['text']+'</a><br />'+"\n" for page in index_data['pages']])


	f = open(index_data['title']+'/index.html', 'w')
	f.write(text_start+text_content+text_end)
	f.close()

	for page_data in pages_data:	
		text_content = """
		<h2>__TITLE__</h2>
		<p>__CONTENT__</p>
		"""
		text_content = text_content.replace('__TITLE__', page_data['title']).replace('__CONTENT__', page_data['content']).replace('<br/><br/><br/><br/>', '<br />')

		f = open(index_data['title']+'/'+page_data['file'], 'w')
		f.write(text_start+text_content+text_end)
		f.close()
