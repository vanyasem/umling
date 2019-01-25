#!/usr/bin/env python3

import cgi

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
text = form.getvalue('text')

print('Content-type: text/html')
print()
print("hi " + text)
