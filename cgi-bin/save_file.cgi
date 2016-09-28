#!/usr/bin/python
#author: jzhao019

import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid 
   # directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   lfn = fn.split("\\")
   fn = lfn[-1]
   trace_file = open('../trace/' + fn, 'wb')
   trace_file.write(fileitem.file.read())
   trace_file.close()

   message = 'The file "' + fn + '" was uploaded successfully'
   
else:
   message = 'No file was uploaded'
   
print """\
Content-Type: text/html\n
<html>
<head>
<script language="javascript" src="../common.js">
</script>
<script language="javascript" src="../temp/center.js">
</script>
</head>
<body>
   <p>%s</p>
   <p><a href="javascript:showprogress('%s');">parse trace</a></p>
   <div id="prog">dynamic progress</div>
</body>
</html>
""" % (message,'../trace/'+fn)
