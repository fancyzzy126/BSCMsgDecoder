#!/usr/bin/python
#module:
#author: jzhao019

# Import modules for CGI handling 
import cgi, cgitb
from ajaxprocess import handle
from common import set_debug

cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FieldStorage()

# Get data from fields
action = form.getvalue('action')
set_debug(False);
if action == 'decodesinglemsg':
    msg_content = form.getvalue('msgcontent')
    uname = form.getvalue('uname')
    version = form.getvalue('version')
    objname = form.getvalue('objname')
    buffermode = form.getvalue('buffermode')
    fieldmode = form.getvalue('fieldmode')
    handle(action, [msg_content, uname, version, objname, buffermode, fieldmode])
elif action == 'decodemsg':
    msg_content = form.getvalue('msg')
    version = form.getvalue('version')
    handle(action, [msg_content, version])
elif action == 'parsetrace':
    filename = form.getvalue('filename')
    uname = form.getvalue('uname')
    fname = form.getvalue('fname')
    version = form.getvalue('version')
    handle(action, [filename, uname, fname, version])
elif action == 'getfilter':
    uname = form.getvalue('uname')
    handle(action, [uname])
elif action == 'showbuffer':
    version = form.getvalue('version')
    handle(action, [version])
elif action == 'listbuffer':
    version = form.getvalue('version')
    handle(action, [version])
elif action == 'setbuffer':
    msg_id = form.getvalue('msgid')
    mode = form.getvalue('mode')
    version = form.getvalue('version')
    handle(action, [msg_id, mode,version])
elif action == 'listbscversion':
    handle(action, [])
else:
    handle(action,[])
