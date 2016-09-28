#!/usr/bin/python
#module:
#author: jzhao019

import os

recfilename = ".rttpaccount"
def recaccount(userid, username, email, phone, team):
    try:
        acfile = file(recfilename, "aw")
        record = userid + "$$$"
        record += username + "$$$"
        record += email + "$$$"
        record += phone + "$$$"
        record += team + "\n"
        acfile.write(record)
        acfile.close()
        return [True, 'succ']
    except Exception, ex:
        return [False, "record account:\n" + str(ex)]

def getaccount(userid):
    if os.path.isfile(recfilename):
        try:
            acfile = file(recfilename)
            contents = acfile.readlines()
            contents = [it.strip().split("$$$") for it in contents
                        if len(it) > 0]
            for it in contents:
                if it[0].strip() == userid.strip():
                    result = []
                    for item in it:
                        result.append(item.strip())
                    return result
        except Exception, ex:
            print str(ex)
            return []
    else:
        return []

def Test():
##    if recaccount("test", "wuhan", "wuhan@alcatel-sbell.com.cn", "36054510", "FM"):
    print getaccount("test")

if __name__ == '__main__':
    Test()
