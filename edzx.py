# -*- coding: utf-8 -*-
from crab import crab
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

params = {
		'url':'http://books.edzx.com/html/book/0382/Index.html',
		'fields':[
			{'name':'author', 'select':'div#TextInfo a', 'regex':''},	
			{'name':'title', 'select':'div#TextTitle', 'regex':''},	
			{'name':'pages', 'select':'div#BookText ul li a', 'regex':'', 'url':True, 'multi':True}	
		],
		'charset':'utf8'
	}	

child_params = {
		'url':'',
		'fields':[
			{'name':'content', 'select':'div#BookText', 'regex':'', 'number':0, 'content':True}	
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
