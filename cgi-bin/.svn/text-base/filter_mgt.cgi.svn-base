#!/usr/bin/python
#module:
#author: jzhao019

# Import modules for CGI handling 
import cgi, cgitb
from filterEng import process

cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FieldStorage()

# Get data from fields
action = form.getvalue('action')
paralist = []
if action == "create":
    uname = form.getvalue('uname')
    fname = form.getvalue('fname')
    msgids = form.getvalue('msgids')
    fmmids = form.getvalue('fmmids')
    desc = form.getvalue('desc')
    paralist = [uname, fname, msgids, fmmids, desc]
elif action == "delete":
    uname = form.getvalue('uname')
    fname = form.getvalue('fname')
    paralist = [uname, fname, msgids, fmmids, desc]
elif action == "modify":
    uname = form.getvalue('uname')
    fname = form.getvalue('fname')
    msgids = form.getvalue('msgids')
    fmmids = form.getvalue('fmmids')
    desc = form.getvalue('desc')
    paralist = [uname, fname, msgids, fmmids, desc]
elif action == "query":
    uname = form.getvalue('uname')
    paralist = [uname]
else:
    action = 'Unknow action'

process(action, paralist)

       
