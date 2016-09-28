#!/usr/bin/python
#module:
#author: jzhao019

import os
from xml.dom import minidom

class msg_template:
    def __init__(self):
        self.__errorContent = 'class msg_template\n'
        self.__msgFieldsDict = {}
        self.__modeDict = {}
        self.__templateFileName = 'msg_mode_template'
        self.__leafNodesDict = {}
        self.__msgFieldsTree = {}
        self.__modeTree = {}
        self.__modeTempDB = {}
        self.__synDict = {}
        self.__msgDefDict = {}
        self.__nodeDict = {}

    def loadDefFile(self):
        self.__errorContent += 'loadDefFile\n'
        fileName = self.__templateFileName
        if fileName and len(fileName.strip()) > 0:
##            try:
            if os.path.isfile(fileName.strip()):
                traceFile = file(fileName.strip())
                contents = traceFile.readlines()
##                contents = [it[:-2] for it in contents]#for linux
                contents = [it[:-1] for it in contents]#for windows
                msg_fields_index = contents.index("#msg_fields") + 1
                mode_index = contents.index("#mode") + 1
                msgList = contents[1:msg_fields_index-1]
                msgFieldsList = contents[msg_fields_index:mode_index-1]
                modeList = contents[mode_index:]
                self.__msgDefDict = self.getMDEFList(msgList)
                self.__msgFieldsDict = self.getMFDict(msgFieldsList)
                self.__modeDict = self.getMDict(modeList)
                traceFile.close()
                return True
            else:
                self.__errorContent += "File: " + fileName + " does not exist!\n"
                return False
##            except Exception, ex:
##                self.__errorContent += str(ex) + "\n"
##                return False
        else:
            self.__errorContent += "File name is empty!\n"
            return False


    def getMDEFList(self, tmpList):
        newDict = {}
        newList = [it.split(',')[:-1] for it in tmpList]
        for it in newList:
            newDict[int(it[0])] = [it[1], 0, 0]
            if int(it[3]) == 1:
                newDict[int(it[0])][1] = 1
            if int(it[5]) == 1:
                newDict[int(it[0])][2] = 1
        return newDict


    def getMFDict(self, tmpList):
        newDict = {}
        newList = [it.split(',')[:-1] for it in tmpList]
        for it in newList:
            newDict[int(it[0])] = [int(it[1]), int(it[2]),[]]
            for item in it[-1].split(';')[:-1]:
                eleList = item.split('.')[:-1]
                eleList[2] = int(eleList[2])
                eleList[3] = int(eleList[3])
                newDict[int(it[0])][-1].append(eleList)
##            print int(it[0]), newDict[int(it[0])]
        return newDict


    def getMDict(self, tmpList):
        newDict = {}
        newList = [it.split(',')[:-1] for it in tmpList]
        for it in newList:
            newDict[it[0]] = [int(it[1]), it[2], bool(int(it[3])), []]
            if bool(int(it[3])):
                for item in it[-1].split(';')[:-1]:
                    if item.count('.') > 0:
                        eleList = item.split('.')[:-1]
                        eleList[2] = int(eleList[2])
                        eleList[3] = int(eleList[3])
                        newDict[it[0]][-1].append(eleList)
                    else:
                        newDict[it[0]][-1].append(int(item))
            else:
                newDict[it[0]][-1] = it[-1].split(';')[:-1]
##            print it[0], newDict[it[0]]
        return newDict

    def loadDefDict(self):
        pass

    def update_node_pos(tree):
        pass

    def createMsgFieldsTree(self):
        for it in self.__msgFieldsDict.keys():
            self.__msgFieldsTree[it] = []
            if int(self.__msgFieldsDict[it][1]) > 0:
                for item in self.__msgFieldsDict[it][-1]:
                    newItem = [item[0], item[1], item[2], item[3]]
                    newItem.append(self.parseMode(str(it), item[0], item[1], item[2], item[3]))
                    self.__msgFieldsTree[it].append(newItem)
                self.update_node_pos(self.__msgFieldsTree[it])
                self.__msgFieldsTree[it] = self.list2XML('msg', str(it), self.__msgFieldsTree[it])
            else:
                self.__errorContent += 'msg' + it + 'has no fields!\n'
                return False
        return True

    def createModeTree(self):
        for it in self.__modeDict.keys():
            modeList = self.__modeDict[it]
            size = 0
            if modeList[1] != 'SYN':
                size = modeList[0]
            else:
                #create SYN dict
                #cannot handle SYN INT!
                if self.__synDict.has_key(modeList[-1][0]):
                    self.__synDict[modeList[-1][0]][modeList[0]] = it
                else:
                    self.__synDict[modeList[-1][0]] = {}
                    self.__synDict[modeList[-1][0]][modeList[0]] = it
            self.__modeTree[it] = self.parseMode(it, it, it, size, 0)
            self.update_node_pos(self.__modeTree[it])
            self.__modeTree[it] = self.list2XML('mode', it, self.__modeTree[it])

    def found_same_offset_in_rest(item_list, index, total):
        if total > 0 and (index + 1) < total:
            if item_list[index][3] == item_list[index+1][3]:
                return True
        return False

    def updateTreeOffset(self, tree, offset):
        pass

    def parseMode(self, msg_mode, element, modeName, size, offset):
        '''
            msg_mode: msg_id or mode_name, str
        '''
        if self.__modeDict.has_key(modeName):
            # find in the TempDB to reduce the repeated caculate.
            if self.__modeTempDB.has_key(modeName):
                temp_subtree = deepcopy(self.__modeTempDB[modeName])
                self.updateTreeOffset(temp_subtree, offset)
                return temp_subtree
            modeContent = self.__modeDict[modeName]
            newList = []
            if modeContent[2]:
                preOffset = -1
                firstFlag = False
                in_case_of = False
                case_of_pos = 0
                index = 0
                total_element = len(modeContent[-1][1:])
                caseofList = []
                caseofElement = []
                for it in modeContent[-1][1:]:
                    if found_same_offset_in_rest(modeContent[-1], index, total_element):
                        if not firstFlag and not in_case_of:
                            firstFlag = True
                        in_case_of = True
                        case_of_pos = it[3]
                    else:
                        in_case_of = False
                    if in_case_of:
                        if firstFlag:
                            firstFlag = False
                            newElement = element + '.' + it[0] + '_case'
                            newOffset = it[3] + offset
                            caseofElement = [newElement, 'case_of', it[2], newOffset, []]
                            subElement = element + '.' + it[0] + '_case.' + it[0]
                            subOffset = newOffset
                            subItem = [subElement, it[1], it[2], newOffset]
                            subItem.append(self.parseMode(msg_mode, subItem[0], subItem[1], subItem[2], subItem[3]))
                            caseofElement[-1].append(subItem)
                        else:
                            newElement = caseofElement[0] + '.' + it[0]
                            newOffset = it[3] + offset
                            newItem = [newElement, it[1], it[2], newOffset]
                            newItem.append(self.parseMode(msg_mode, newItem[0], newItem[1], newItem[2], newItem[3]))
                            caseofElement[-1].append(newItem)
                            caseofElement[2] += it[2]
                    else:
                        newElement = element + '.' + it[0]
                        newOffset = it[3] + offset
                        newItem = [newElement, it[1], it[2], newOffset]
                        newItem.append(self.parseMode(msg_mode, newItem[0], newItem[1], newItem[2], newItem[3]))
                        newList.append(newItem)
            else:
                newElement = element + '.NULL'
                childList = [newElement, modeContent[-1][0], 0, offset]
                if modeContent[1] == 'SYN':
                    childList[2] = size
                    childList.append('SYN')
                else:
                    childList[2] = modeContent[0]                
                childList.append(self.parseMode(msg_mode, childList[0], childList[1], childList[2], childList[3]))
                newList.append(childList)
            # save this subtree in DB for further use.
            self.__modeTempDB[modeName] = newList
            return newList
        else:
            if self.__leafNodesDict.has_key(msg_mode):
                self.__leafNodesDict[msg_mode].append([element, modeName, size, offset])
            else:
                self.__leafNodesDict[msg_mode] = [[element, modeName, size, offset]]
            return []

    def list2XML(self, msg_mode, name, contentList):
        doc = minidom.Document()
        rootNode = None
        if msg_mode == 'msg':
            rootNode = doc.createElement('msg_' + name + '_fields')
        else:
            rootNode = doc.createElement(name)
        for it in contentList:
            rootNode.appendChild(self.element2Node(doc, it))
        doc.appendChild(rootNode)
        return rootNode.toxml()
  
    def element2Node(self, doc, element):
        newNode = doc.createElement(element[0])
        newNode.setAttribute('type', element[1])
        newNode.setAttribute('size', str(element[2]))
        newNode.setAttribute('offset', str(element[3]))
        if len(element) == 6:
            newNode.setAttribute('nodemode', element[4])
        for it in element[-1]:
            newNode.appendChild(self.element2Node(doc, it))
        return newNode

    def generate2DB(self):
        if not self.loadDefFile():
            return False
        self.createMsgFieldsTree()
        self.createModeTree()
        #TODO: save to DB

    def generate2File(self, fieldsFile, modeFile, synFile, leafFile, msgFile):
        self.__errorContent += 'dictToFile \n'
        if not self.loadDefFile():
            return False
        if not self.createMsgFieldsTree():
            return False
        self.createModeTree()
        #TODO: save to files
        
        self.__errorContent += 'save msg fields to file \n'
        if not self.saveFieldMode(fieldsFile, self.__msgFieldsTree):
            return False
        
        self.__errorContent += 'save mode to file \n'
        if not self.saveFieldMode(modeFile, self.__modeTree):
            return False

        self.__errorContent += 'save syn definition to file \n'
        if not self.saveSynDef(synFile, self.__synDict):
            return False

        self.__errorContent += 'save leaf nodes to file \n'
        if not self.saveLeafNode(leafFile, self.__leafNodesDict):
            return False

        self.__errorContent += 'save msg def to file \n'
        if not self.saveMsgDef(msgFile, self.__msgDefDict):
            return False
        return True

    def saveMsgDef(self, fileName, contentDict):
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')
                for it in contentDict.keys():
                    linestr = str(it) + ','
                    linestr += contentDict[it][0] + ','
                    linestr += str(contentDict[it][1]) + ','
                    linestr += str(contentDict[it][2])
                    traceFile.write(linestr + '\n')
                traceFile.close()
                return True
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"

    def saveFieldMode(self, fileName, contentDict):
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')
                for it in contentDict.keys():
                    linestr = str(it) + ','
                    linestr += contentDict[it]
                    traceFile.write(linestr + '\n')
                traceFile.close()
                return True
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"

    def saveSynDef(self, fileName, contentDict):
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')
                for it in contentDict.keys():
                    linestr = str(it) + ','
                    for item in contentDict[it].keys():
                        linestr += str(item)
                        linestr += '.'
                        linestr += contentDict[it][item]
                        linestr += ';'
                    traceFile.write(linestr + '\n')
                traceFile.close()
                return True
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"

    def saveLeafNode(self, fileName, contentDict):
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')
                for it in contentDict.keys():
                    linestr = it + ','
                    for item1 in contentDict[it]:
                        for item2 in item1:
                            linestr += str(item2) + '$'
                        linestr += ';'
                    linestr += ','
                    traceFile.write(linestr + '\n')
                traceFile.close()
                return True
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"
            return False

    def dumpError(self):
        return self.__errorContent

    def dumpDict(self):
        print self.__msgDefDict
        print
        print self.__msgFieldsDict
        print
        print self.__modeDict 

def test():
    print 'test'
    mt = msg_template()
    if not mt.generate2File('t_fieldsFile', 't_modeFile', 't_synFile', 't_leafFile', 't_msgFile'):
        print mt.dumpError()

def miniTest():
    mt = msg_template()
    if not mt.loadDefFile():
        print mt.dumpError()
##    mt.createMsgFieldsTree()
    mt.dumpDict()
    

if __name__ == '__main__':
##    miniTest()
    test()
