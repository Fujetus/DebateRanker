#!/usr/bin/env python
# save as cgi-bin/index.py
# Python 2.7
import cgi
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
html = """
<html>
<head>
</head>
<body>
<form action="index.py" name="myform" method="GET">
	    Enter length:  <input type="text" name="length"><br />
	    Enter width: <input type="text" name="width"><br />
	    <input type="submit" value="submit">
</form>
</body>
</html>
"""


try:
    length = int(form['length'].value)
    width = int(form['width'].value)
    area = length * width
    print ("Content-Type: text/html")

    print ("<p>The area is:  " + str(area) + "</p>")
except KeyError:
    print (html)