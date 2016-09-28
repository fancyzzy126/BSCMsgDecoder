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
    if path.count('/') > 3:#back
        thirdslash = path.index('/', 7) + 1
        path = path[:thirdslash]
    result = ''
    result += '<HTML><HEAD><SCRIPT Language="Javascript">' + '\n'
    result += "self.location='" + path + targ + "'\n"
    result += "</SCRIPT>\n"
    result += "</HEAD></HTML>"
    print 'Content-Type: text/html\r\n\r\n'
    print 'HTTP/1.1 200 OK'
    print 'Server: RTTP server'
    print result

def sendTopRedirect(targ=''):
    '''
       redirect from the root, target is top, used for frame
    '''
    path = os.environ['HTTP_REFERER'].strip()
    if not path.endswith('/'):
        path = path + '/'
    if path.count('/') > 3:#back
        thirdslash = path.index('/', 7) + 1
        path = path[:thirdslash]

    print "Content-type:text/html\r\n\r\n"
    print "<html>"
    print "<head>"
    print "<title>"
    print "test</title>"
    print "</head>"
    print "<body>"
    print "<h2>Create new filter successfully.<p>"
    print """<a href="#" LANGUAGE=javascript onclick="{href='""" + path + targ + """';target='_top';}">back</a></h2>"""
    print "</body>"
    print "</html>"

def test():
    sendTopRedirect("http://warts2.vz.cit.alcatel.fr")

if __name__ == '__main__':
    test()
        
    
