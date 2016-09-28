#!/usr/bin/python
#module:
#author: jzhao019

# Import modules for CGI handling 
import cgi, cgitb, normalpage_win
from accountvalid import process

cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FieldStorage()

# Get data from fields
action = form.getvalue('action')
if action == "login":
    username = form.getvalue('cname')
    passwd = form.getvalue('cpassword')
    process(action, [username, passwd])
elif action == "reg":
    username = form.getvalue("logonid")
    truename = form.getvalue("name")
    email = form.getvalue("mailid")
    phone = form.getvalue("phone")
    team = form.getvalue("team")
    passwd = form.getvalue("pwd1")
    process(action, [username, truename, email, phone, team, passwd])
else:
    process(action, [])

       
