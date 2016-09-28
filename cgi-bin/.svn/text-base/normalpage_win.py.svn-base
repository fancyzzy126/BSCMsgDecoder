#!/usr/bin/python
#module:
#author: jzhao019

import os, cgi

def sendCont():
    print 'HTTP/1.1 100 Continue'

def sendRedirect(targ=''):
    path = os.environ['HTTP_REFERER'].strip()
    if not path.endswith('/'):
        path = path + '/'
    if path.count('/') > 3:
        thirdslash = path.index('/', 7) + 1
        path = path[:thirdslash]
    result = '\r\n'
    result += '<HTML><SCRIPT Language="Javascript">' + '\n'
    result += "self.location='" + path + targ + "'\n"
    result += "</SCRIPT>\n"
    result += "</HTML>"
    print
    print 'Status: 200 OK'
    print 'Transfer-Encoding: chunked'
    print 'Allow: GET, HEAD'
    print 'Server: RTTP server'
    print 'Content-Type: text/html'
    print result


def test():
    sendRedirect("http://warts2.vz.cit.alcatel.fr")

if __name__ == '__main__':
    test()
        
    
