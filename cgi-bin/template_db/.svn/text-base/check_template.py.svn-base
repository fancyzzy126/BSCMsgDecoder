#!/usr/bin/python
#author: Jun Zhao

import os, sys

def Get_list_from_file(filename):
    if filename and len(filename.strip()) > 0:
        try:
            if os.path.isfile(filename.strip()):
                traceFile = file(filename.strip())
                contents = traceFile.readlines()
                contents = [it.strip() for it in contents if len(it.strip()) > 1]
                traceFile.close()
                return contents
            else:
                print "File: " + filename.strip() + " does not exist!\n"
                return None
        except Exception, ex:
            print str(ex)
            return None
    else:
        print "File name is empty!\n"
        return None 

def Get_msg_base(msg_list):
    new_list = [int(it.split()[1].strip()) for it in msg_list]
    return new_list

def Get_msg_template(msg_list):
    new_list = [int(it.split(',')[0].strip()) for it in msg_list]
    return new_list

def Msg_template_verify(base_file, msg_template):
    base_list = Get_list_from_file(base_file)
    if base_list == None:
        print 'Cannot get base for msgs.'
        return
    msg_list = Get_list_from_file(msg_template)
    if msg_list == None:
        print 'Cannot get template for msgs'
        return
    base_list = Get_msg_base(base_list)
    msg_list = Get_msg_template(msg_list)
    print 'Based on base:'
    print base_list
    print msg_list
    for it in base_list:
        if not (it in msg_list):
            print it
    print 'Based on template:'
    for it in msg_list:
        if it in base_list:
            pass
        else:
            print it
    print 'Msg verification finished.'

def test(param):
    if len(param) != 3:
        print 'Parameter number is wrong!'
    else:
        Msg_template_verify(param[1], param[2])

if __name__ == '__main__':
    test(sys.argv)
