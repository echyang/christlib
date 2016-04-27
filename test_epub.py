#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Chyang Wong'


import os

os.mkdir('test')
f = open('test/01.html', 'ab')
text_start = '''
<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
	        <title>__TITLE__</title>
			    </head>
				    <body>
'''
text_end = '''
    </body>
	</html>
'''

text_content = '''
<h2>tst/h2>
<p>dfdksjfkdsfjds</p>
'''

f.write(text_start+text_content+text_end)
f.close()
