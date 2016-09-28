#!/usr/bin/python
#module:
#author: jzhao019

import os

class filterDB(object):
    '''
       user_name
       filter_name
       filter_type-->msg/fmm/msg-fmm
       content
       descripton
    '''
    def __init__(self):
        self.__

    def loadDB(self):
        pass

    def saveDB(self):
        pass

    def get_exact(self, uname, fname):
        pass

    def get_list(self, uname):
        pass

    def add(self, filter_list):
        print 'filterdb'

    def delete(self, uname, fname):
        pass

    def update(self, filter_list):
        pass

    def dumperror(self):
        pass

class filterDBFile(object):
    '''
       user_name
       filter_name
       filter_type-->msg/fmm/msg-fmm
       content
       descripton
    '''
    def __init__(self):
        self.__errorContent = 'filterDBFile\n'
        self.__fileName = '.filterDB'
        self.__contentList = []
        self.__sepFlag = '&^&'

    def loadDB(self):
        if self.__fileName and len(self.__fileName.strip()) > 0:
            try:
                if os.path.isfile(self.__fileName.strip()):
                    traceFile = file(self.__fileName.strip())
                    contents = traceFile.readlines()
                    contents = [it[:-1].split(self.__sepFlag) for it in contents if len(self.__fileName.strip()) > 0]
                    self.__contentList = contents
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "File: " + self.__fileName + " does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"
            return False

    def saveDB(self):
        if len(self.__fileName) == 0:
            self.__errorContent += "No filter file name!"
            return False
        else:
            out = file(self.__fileName, "w")
            for it in self.__contentList:
                items  = it[0] + self.__sepFlag
                items += it[1] + self.__sepFlag
                items += it[2] + self.__sepFlag
                items += it[3] + self.__sepFlag
                items += it[4]
                out.write(items + "\n")
            out.close()
            return True

    def get_exact(self, uname=None, fname=None):
        flag = False
        res = []
        if self.loadDB() == False:
            return [False, res]
        if uname and fname:
            for it in self.__contentList:
                if uname == it[0] and fname == it[1]:
                    res.append(it)
                    flag = True
        elif uname:
            for it in self.__contentList:
                if uname == it[0]:
                    res.append(it)
                    flag = True
        elif len(self.__contentList):
            res = self.__contentList
            flag = True
        else:
            self.__errorContent += 'get_exact: filter empty\n'
        if flag == False:
            self.__errorContent += 'get_exact: filter does not exist\n'
        return [flag, res]

    def get_list(self, uname=None):
        if uname == '':
            uname = None
        return self.get_exact(uname)

    def checkexist(self, uname, fname, ftype):
        '''
            exist          --> True
            does not exist --> False
        '''
        for it in self.__contentList:
            if uname == it[0] and fname == it[1] and ftype == it[2]:
                return True
        return False

    def add(self, filter_list):
        flag = False
        if self.loadDB() == False:
            return False
        if len(filter_list) == 5:
            if self.checkexist(filter_list[0], filter_list[1], filter_list[2]) == False:
                if filter_list[3] == None:
                    filter_list[3] = ''
                if filter_list[4] == None:
                    filter_list[4] = ''
                self.__contentList.append(filter_list)
                flag = True
            else:
                self.__errorContent += 'add: filter already exist\n'
        else:
            self.__errorContent += 'filter list should contain 5 parameters\n'
        if flag:
            flag = self.saveDB()
        return flag

    def delete(self, uname, fname):
        flag = False
        if self.loadDB() == False:
            return False
        for it in self.__contentList:
            if uname == it[0] and fname == it[1]:
                self.__contentList.remove(it)
                flag = True
        if flag == False:
            self.__errorContent += 'delete: filter does not exist\n'
        if flag:
            flag = self.saveDB()
        return flag

    def update(self, filter_list):
        flag = False
        uname = filter_list[0]
        fname = filter_list[1]
        ftype = filter_list[2]
        if self.loadDB() == False:
            return False
        for it in self.__contentList:
            if uname == it[0] and fname == it[1] and ftype == it[2]:
                it[3] = filter_list[3]
                it[4] = filter_list[4]
                flag = True
                break
        if flag == False:
            self.__errorContent += 'update: filter does not exist\n'
        if flag:
            flag = self.saveDB()
        return flag

    def dumperror(self):
        return self.__errorContent

def test():
    f = filterDBFile()

    res = f.get_list('123')
    if res[0] == False:
        print f.dumperror()
    print res[1]


if __name__ == '__main__':
    test()
