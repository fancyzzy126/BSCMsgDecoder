#!/usr/bin/python
#module:
#author: jzhao019

import os, errorpage, normalpage
from filter_inv import filterDBFile
from xml.dom import minidom

class filterEng(object):
    def __init__(self):
        self.__fdf = filterDBFile()
    def fileexist(self):
        return os.path.isfile(self.__filename.strip())
        
    def do_error(self, param1, param2):
        errorpage.showerror(param1, param2)

    def do_rediret(self, targ):
        normalpage.sendRedirect(targ)

    def do_toprediret(self, targ):
        normalpage.sendTopRedirect(targ)

    def listfilter(self, fl):
        self.do_rediret("temp/mainframe.html")
        

    def do_delete(self, param):
        self.do_rediret("temp/mainframe.html")

    def do_modify(self, param):
        self.do_rediret("temp/mainframe.html")

    def do_query(self, param):
        err = ''
        fl = []
        if len(param) == 1:
            ckp = self.__fdf.get_list(param[0])
            if ckp[0]:
                fl = ckp[1]
            else:
                err = self.__fdf.dumperror()
        else:
            err = "Query Filter Error", "parameter error"
        if err == '':
            self.listfilter(fl)
        else:
            err += '<a href="../temp/mainframe.html">back</a>'
            self.do_error("create filter error", err)

    def do_create(self, param):
        err = ''
        if len(param) == 5:
            if param[0] and param[1]:
                if param[2] and param[2] != '':
                    if self.__fdf.add([param[0],param[1],'msg',param[2],param[4]]) == False:
                        err = self.__fdf.dumperror()
                        err += '''<p><a href="#" LANGUAGE=javascript onclick="{href='../temp/mainframe.html';target='_top';}">back</a>'''
                if param[3] and param[3] != '':
                    if self.__fdf.add([param[0],param[1],'fmm',param[3],param[4]]) == False:
                        err = self.__fdf.dumperror()
                        err += '''<p><a href="#" LANGUAGE=javascript onclick="{href='../temp/mainframe.html';target='_top';}">back</a>'''
            else:
                err += '''please <a href="#" LANGUAGE=javascript onclick="{href='../index.html';target='_top';}">login</a>'''
        else:
            err = "Create filter Error1, Parameters are not sufficient!"
            err += '''<p><a href="#" LANGUAGE=javascript onclick="{href='../temp/mainframe.html';target='_top';}">back</a>'''
        if err != '':
            self.do_error("create filter error", err)
        else:
            self.do_toprediret("temp/mainframe.html")

def process(action, param):
    fe = filterEng()
    if hasattr(fe, "do_%s" % action):
        actual_func = getattr(fe, "do_%s" % action)
        actual_func(param)
    else:
        errorpage.showerror("Unknow Action: " + action, "Filter: Invalid Access!")

def query_filter(param):
    err = ''
    fl = []
    fdf = filterDBFile()
    uname = ''
    if len(param) > 0:
        uname = param[0]
    ckp = fdf.get_list(uname)
    if ckp[0]:
        fl = ckp[1]
    else:
        err = fdf.dumperror()
    if err == '':
        return [True, assemble(fl)]
    else:
        err += '<a href="../temp/mainframe.html">back</a>'
        return [False, err]

def assemble(fl):
    fd = {}
    for it in fl:
        if fd.has_key((it[0], it[1])):
            if it[2] == 'msg':
                fd[(it[0], it[1])][0] = it[3]
            elif it[2] == 'fmm':
                fd[(it[0], it[1])][1] = it[3]
        else:
            if it[2] == 'msg':
                fd[(it[0], it[1])] = [it[3], '', it[4]]
            elif it[2] == 'fmm':
                fd[(it[0], it[1])] = ['', it[3], it[4]]
    doc = minidom.Document()
    rootNode = doc.createElement('filter_list')
    doc.appendChild(rootNode)
    
    i = 1;
    for it in fd.keys():
        filterNode = doc.createElement('filter_record' + str(i))
        rootNode.appendChild(filterNode)

        filter_id = doc.createElement('filter_id')
        filter_id.setAttribute('value', str(i))
        filterNode.appendChild(filter_id)

        uname = doc.createElement('uname')
        uname.setAttribute('value', it[0])
        filterNode.appendChild(uname)

        fname = doc.createElement('fname')
        fname.setAttribute('value', it[1])
        filterNode.appendChild(fname)

        elem = fd[it]
        msgids = doc.createElement('msgids')
        msgids.setAttribute('value', elem[0])
        filterNode.appendChild(msgids)

        fmms = doc.createElement('fmms')
        fmms.setAttribute('value', elem[1])
        filterNode.appendChild(fmms)

        desc = doc.createElement('description')
        desc.setAttribute('value', elem[2])
        filterNode.appendChild(desc)
        i += 1;
    content = doc.toxml()
    return content
        

def Test():
    print 'Test'

    func = process('create',['jma007','bts41', 'msg', '123,345', 'bts'])

if __name__ == '__main__':
    Test()
