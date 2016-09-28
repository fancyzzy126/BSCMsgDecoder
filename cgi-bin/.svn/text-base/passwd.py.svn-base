#!/usr/bin/python
#author: jzhao019

import hashlib 
from base64 import b64decode, b64encode 
def utf16tobin(s): 
  return s.encode('hex')[4:].decode('hex') 
b64salt = "kDP0Py2QwEdJYtUX9cJABg==" 
b64hash = "OJF6H4KdxFLgLu+oTDNFodCEfMA=" 
binsalt = b64decode(b64salt) 
password_string = 'password'.encode("utf16") 
password_string = utf16tobin(password_string) 
m1 = hashlib.sha1() 
 
m1.update(binsalt + password_string) 

if b64encode(m1.digest()) == b64hash: 
    print "Logged in!" 
else: 
    print "Didn't match" 
    print b64hash 
    print b64encode(m1.digest()) 
