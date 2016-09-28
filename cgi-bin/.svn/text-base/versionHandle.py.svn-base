#!/usr/bin/python
#author: jzhao019

import os
from xml.dom import minidom

bsc_version_file_name = 'bsc_version'

def get_bsc_ver_list():
    if os.path.isfile(bsc_version_file_name):
        ver_file = file(bsc_version_file_name)
        contents = ver_file.readlines()
        contents = [it.split()[0] for it in contents]
        contents = [it.strip() for it in contents]
        return (True, show_bsc_ver_xml(contents))
    else:
        return (False, 'bsc_version does not exist!')

def show_bsc_ver_xml(ver_list):
    doc = minidom.Document()
    rootNode = doc.createElement('BSC_VER')
    for it in ver_list:
        text = doc.createElement(it)
        rootNode.appendChild(text)
    doc.appendChild(rootNode)
    xmlStr = doc.toxml()
    return xmlStr

def check_bsc_ver_exist(ver):
    if os.path.isfile(bsc_version_file_name):
        ver_file = file(bsc_version_file_name)
        contents = ver_file.readlines()
        contents = [it.split()[0] for it in contents]
        contents = [it.strip() for it in contents]
        if ver in contents:
            return (True, '')
        else:
            return (False, 'Version ' + ver + ' does not exist!')
    else:
        return (False, 'bsc_version does not exist!')

def get_ver_template_path(ver):
    if os.path.isdir('template_db/' + ver):
        return [True, 'template_db/'+ver+'/']
    else:
        #for chill_list, default parse configuration direction
        return [True, 'template_db/B12_MR2_ED2/']
        #return [False, 'Template for version ' + ver + ' does not exist!']

def get_ver_obj_path(ver):
    #make sure the version is exist
    #read version config
    ver_file = file(bsc_version_file_name)
    contents = ver_file.readlines()
    ver_list = [it.split()[0] for it in contents]
    ver_list = [it.strip() for it in ver_list]
    path_list = []; #version object path list
    for it in contents:
        items = it.split();
        if len(items)>=3: 
            path_list.append(items[2])
        else:
            path_list.append('template_db/default_obj/');#default path
    path_list = [it.strip() for it in path_list]
    #get object path
    i = ver_list.index(ver)
    if os.path.isdir(path_list[i]):
        return [True, path_list[i]]
    else:
        return [False, 'object path for version ' + ver + ' does not exist!']

def test():
    ret = get_bsc_ver_list()
    if ret[0]:
        print 'True ', ret[1]
    else:
        print 'False ', ret[1]
    ret = check_bsc_ver_exist('B11_MX_MR3_ED1')
    print ret
    ret = get_ver_template_path('B11_MX_MR3_ED1')
    print ret
    ret = get_ver_obj_path('B12_MR2_ED2')
    print ret

if __name__ == '__main__':
    test()
