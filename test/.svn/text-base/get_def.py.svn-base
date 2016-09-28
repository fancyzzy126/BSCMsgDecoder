#!/usr/bin/python
#module:
#author: jzhao019


import os

_debug = True

class GetDef:
    def __init__(self):
        self.__errorContent = 'class GetDef.\n'
        self.__content = []
        self.__msgDefFile = 'msg_mode/msg_def'
        self.__modeDefFile = 'msg_mode/mode_def'
        self.__msgfieldsDefFile = 'msg_mode/msg_fields_def'
        self.__msgDict = {}
        self.__msgFieldDict = {}
        self.__modeDict = {}
        self.__msgDictLoc = {}
        self.__msgFiledDictLoc = {}
        self.__modeDictLoc = {}
        self.__destPath = 'listing/'
        self.__current_msgDef_file = None
        self.__current_modeDef_file = None
        self.__current_fieldsDef_file = None
        self.__current_msgDef_fileName = ''
        self.__current_modeDef_fileName = ''
        self.__current_fieldsDef_fileName = ''
        self.__current_msgDef_lineNo = 0
        self.__current_modeDef_lineNo = 0
        self.__current_fieldsDef_lineNo = 0
        self.__current_msgDef_line = ''
        self.__current_modeDef_line = ''
        self.__current_modeDef_line = ''

    def loadFile(self, fileName):
        self.__content = []
        if fileName and len(fileName.strip()) > 0:
            try:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    contents = traceFile.readlines()
                    contents = [it.split(':') for it in contents if len(it.strip())>0]
                    self.__content = contents
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "File: " + fileName + " does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"
            return False

    def loadMsg(self, msgid, fileName, lineno_param):
        msgFieldsUBuffer = ['T_B_ELMT_STRUCT','T_B_BUFFER_LEN']
        continue_in_exist_file = False
        if _debug:
            debug_str = 'msgid: ' + msgid  + ', lineno: ' + str(lineno_param) + ', curr-lineno: ' + str(self.__current_msgDef_lineNo) + '\n'
        try:
            if len(self.__current_msgDef_fileName) == 0:
                self.__current_msgDef_fileName = fileName
                self.__current_msgDef_lineNo = 0
            elif self.__current_msgDef_fileName != fileName:
                # still find in the same file.
                if self.__current_msgDef_file != None and (not self.__current_msgDef_file.closed):
                    self.__current_msgDef_file.close()
                self.__current_msgDef_fileName = fileName
                self.__current_msgDef_lineNo = 0
            else:
                continue_in_exist_file = True
            if not continue_in_exist_file:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    self.__current_msgDef_file = traceFile
                else:
                    self.__errorContent += "File: " + fileName + " does not exist!\n"
                    return False
            else:
                traceFile = self.__current_msgDef_file   
            msgLine = ''
            lineno = lineno_param - self.__current_msgDef_lineNo
            while lineno > 0:
                msgLine = traceFile.readline()
                lineno -= 1
            self.__current_msgDef_lineNo = lineno_param
            if len(msgLine) == 0:
                msgLine = self.__current_msgDef_line
            msgName = msgLine.split()[0]
            if _debug:
                debug_str += msgLine+'-'
            if msgLine[71:77] != 'STRUCT':
                msgLine = traceFile.readline()
                self.__current_msgDef_lineNo += 1
            msgSize = msgLine[35:54].split()[1]
            #  False  ---->  0
            #  True   ---->  1
            self.__msgDict[msgid] = [msgName, msgSize, '0', [], '0', []]
            msgLine = traceFile.readline()
            self.__current_msgDef_lineNo += 1
            while not msgLine.startswith('T_MSG_'):
                if len(msgLine) > 35:
                    if msgLine[35:40] == 'Field':
                        lineField = msgLine[2:].split()[0]
                        if lineField in msgFieldsUBuffer:
                            if lineField == msgFieldsUBuffer[0]:
                                self.__msgDict[msgid][2] = '1'
                                FieldsList = msgLine[35:71].strip().split()[1:]
                                FieldsList[0] = FieldsList[0]
                                FieldsList[1] = str(int(FieldsList[1][:8], 16))
                                self.__msgDict[msgid][3] = FieldsList
                            elif lineField == msgFieldsUBuffer[1]:
                                self.__msgDict[msgid][4] = '1'
                                BufferList = msgLine[35:71].strip().split()[1:]
                                BufferList[0] = BufferList[0]
                                BufferList[1] = str(int(BufferList[1][:8], 16))
                                self.__msgDict[msgid][5] = BufferList
                msgLine = traceFile.readline()
                self.__current_msgDef_lineNo += 1
            self.__current_msgDef_line = msgLine
##                print msgid,self.__msgDict[msgid] 
            return True
        except Exception, ex:
            if _debug:
                self.__errorContent += debug_str + '\n'
            self.__errorContent += str(ex) + "\n"
            return False

    def msg_def(self):
        self.__errorContent += 'msg_def\n'
        if self.loadFile(self.__msgDefFile):
##            os.chdir('listing')
            self.__errorContent += 'loadMsg\n'
            for it in self.__content:
                msg_id = str(int(it[2].split()[0][6:10]))
                if not self.__msgDictLoc.has_key(msg_id):
                    self.__msgDictLoc[msg_id] = [it[0],int(it[1])]
                    if not self.loadMsg(msg_id, self.__destPath+self.__msgDictLoc[msg_id][0], self.__msgDictLoc[msg_id][1]):
                        return False
            if self.__current_msgDef_file != None and (not self.__current_msgDef_file.closed):
                self.__current_msgDef_file.close()
##            os.chdir('..')
            self.__msgDictLoc.clear()
            return True
        else:
            return False

    def loadMsgField(self, msgid, fileName, lineno_param):
        continue_in_exist_file = False
        try:
            if len(self.__current_fieldsDef_fileName) == 0:
                self.__current_fieldsDef_fileName = fileName
                self.__current_fieldsDef_lineNo = 0
            elif self.__current_fieldsDef_fileName != fileName:
                # still find in the same file.
                if self.__current_fieldsDef_file != None and (not self.__current_fieldsDef_file.closed):
                    self.__current_fieldsDef_file.close()
                self.__current_fieldsDef_fileName = fileName
                self.__current_fieldsDef_lineNo = 0
            else:
                continue_in_exist_file = True
            if not continue_in_exist_file:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    self.__current_fieldsDef_file = traceFile
                else:
                    self.__errorContent += "File: " + fileName + " does not exist!\n"
                    return False
            else:
                traceFile = self.__current_fieldsDef_file
            msgFieldLine = ''
            lineno = lineno_param - self.__current_fieldsDef_lineNo
            while lineno > 0:
                msgFieldLine = traceFile.readline()
                lineno -= 1
            self.__current_fieldsDef_lineNo = lineno_param
            if len(msgFieldLine) == 0:
                msgFieldLine = self.__current_fieldsDef_line
            msgFieldSize = msgFieldLine[35:54].split()[1]
            self.__msgFieldDict[msgid] = [msgFieldSize, '0', []]
            msgFieldLine = traceFile.readline()
            self.__current_fieldsDef_lineNo += 1
            while not msgFieldLine.startswith('T_MSG_'):
                if len(msgFieldLine) > 35:
                    if msgFieldLine[35:40] == 'Field':
                        lineElement = msgFieldLine[2:].split()[0]
                        lineFields = msgFieldLine[35:98].strip().split()[1:]
                        lineFields[1] = str(int(lineFields[1][:8], 16))
                        self.__msgFieldDict[msgid][-1].append([lineElement,lineFields[2], lineFields[0], lineFields[1]])        
                msgFieldLine = traceFile.readline()
                self.__current_fieldsDef_lineNo += 1
            self.__current_fieldsDef_line = msgFieldLine
            self.__msgFieldDict[msgid][1] = str(len(self.__msgFieldDict[msgid][-1]))
##                print msgid,self.__msgFieldDict[msgid] 
            return True
        except Exception, ex:
            self.__errorContent += str(ex) + "\n"
            return False

    def msg_fields_def(self):
        self.__errorContent += 'msg_fields_def\n'
        if self.loadFile(self.__msgfieldsDefFile):
##            os.chdir('listing')
            self.__errorContent += 'loadMsgField\n'
            for it in self.__content:
                msg_id = str(int(it[2].split()[0][6:10]))
                if not self.__msgFiledDictLoc.has_key(msg_id):
                    self.__msgFiledDictLoc[msg_id] = [it[0],int(it[1])]
                    if not self.loadMsgField(msg_id, self.__destPath+self.__msgFiledDictLoc[msg_id][0], self.__msgFiledDictLoc[msg_id][1]):
                        return False
            if self.__current_fieldsDef_file != None and (not self.__current_fieldsDef_file.closed):
                self.__current_fieldsDef_file.close()
##            os.chdir('..')
            self.__msgFiledDictLoc.clear()
            return True
        else:
            return False

    def loadMode(self, modeName, fileName, lineno_param):
        continue_in_exist_file = False
        try:
            if len(self.__current_modeDef_fileName) == 0:
                self.__current_modeDef_fileName = fileName
                self.__current_modeDef_lineNo = 0
            elif self.__current_modeDef_fileName != fileName:
                # still find in the same file.
                if self.__current_modeDef_file != None and (not self.__current_modeDef_file.closed):
                    self.__current_modeDef_file.close()
                self.__current_modeDef_fileName = fileName
                self.__current_modeDef_lineNo = 0
            else:
                continue_in_exist_file = True
            if not continue_in_exist_file:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    self.__current_modeDef_file = traceFile
                else:
                    self.__errorContent += "File: " + fileName + " does not exist!\n"
                    return False
            else:
                traceFile = self.__current_modeDef_file
            ModeLine = ''
            lineno = lineno_param - self.__current_modeDef_lineNo
            while lineno > 0:
                ModeLine = traceFile.readline()
                lineno -= 1
            self.__current_modeDef_lineNo = lineno_param
            if len(ModeLine) == 0:
                ModeLine = self.__current_modeDef_line
            modeList = ModeLine.split()
            if len(modeList) == 1:
                ModeLine = traceFile.readline()
                self.__current_modeDef_lineNo += 1
            modeList = ModeLine[35:71].split()
            modeType = ModeLine[71:77]
            defType = modeList[0]
            if len(modeList) > 1 and modeList[1].isdigit():
                modeSize = modeList[1]
            else:
                modeSize = '0'
            #  False  ---->  0
            #  True   ---->  1
            #[modeValue, SYN, False, [mode]]
            #[modeSize, NEWMODE/SYNMODE, False, [mode]]
            #struct:[modeSize, NEWMODE/SYNMODE, True,[num,[element, mode, size, offset],...]]
            self.__modeDict[modeName] = [modeSize, defType, '0', []]
            if modeType == 'STRUCT':
                self.__modeDict[modeName][2] = '1'
                self.__modeDict[modeName][-1].append('0')
                ModeLine = traceFile.readline()
                self.__current_modeDef_lineNo += 1
                while not ModeLine.startswith('M_'):
                    if len(ModeLine) > 35:
                        if ModeLine[35:40] == 'Field':
                            lineElement = ModeLine[2:].split()[0]
                            lineFields = ModeLine[35:71].strip().split()[1:]
                            lineFields[1] = str(int(lineFields[1][:8], 16))
                            modeType = ''
                            if self.checkTypePos(ModeLine):
                                modeType = ModeLine[71:].rstrip()
                            else:
                                modeType = ModeLine[71:98].rstrip()
                            self.__modeDict[modeName][-1].append([lineElement,modeType, lineFields[0], lineFields[1]])
                    ModeLine = traceFile.readline()
                    self.__current_modeDef_lineNo += 1
                self.__current_modeDef_line = ModeLine
                self.__modeDict[modeName][-1][0] = str(len(self.__modeDict[modeName][-1])-1)
            else:
                if self.checkTypePos(ModeLine):
                    self.__modeDict[modeName][-1].append(ModeLine[71:].rstrip())
                else:
                    self.__modeDict[modeName][-1].append(ModeLine[71:98].rstrip())
##                print modeName,self.__modeDict[modeName] 
            return True
        except Exception, ex:
            self.__errorContent += str(ex) + "\n"
            return False

    def mode_def(self):
        self.__errorContent += 'mode_def\n'
        if self.loadFile(self.__modeDefFile):
##            os.chdir('listing')
            self.__errorContent += 'loadMode\n'
            for it in self.__content:
                mode_name = it[2].split()[0]
                if not self.__modeDictLoc.has_key(mode_name):
                    self.__modeDictLoc[mode_name] = [it[0],int(it[1])]
                    if not self.loadMode(mode_name, self.__destPath+self.__modeDictLoc[mode_name][0], self.__modeDictLoc[mode_name][1]):
                        return False
            if self.__current_modeDef_file != None and (not self.__current_modeDef_file.closed):
                self.__current_modeDef_file.close()
##            os.chdir('..')
            self.__modeDictLoc.clear()
            return True
        else:
            return False

    def checkTypePos(self, linestr):
        '''
        '''
        packIndex = linestr.find(' PACK', 71)
        if packIndex > 0 and linestr.find(' ', packIndex+4) > 96:
            return True
        if linestr.find('ARRAY(', 71) > 0:
            rightIndex = linestr.find(')', 71)
            if linestr.find(' ', rightIndex+2) > 96:
                return True
        if linestr.find(' ', 71) > 96:
                return True
        return False

    def dictToDB(self):
        pass

    def dictToFile(self, fileName):
        self.__errorContent += 'dictToFile \n'
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')

                traceFile.write('#msg\n')
                for it in self.__msgDict.keys():
                    linestr = it + ','
                    linestr += self.__msgDict[it][0] + ','
                    linestr += self.__msgDict[it][1] + ','
                    linestr += self.__msgDict[it][2] + ','
                    for item1 in self.__msgDict[it][3]:
                        linestr += item1 + ';'
                    linestr += ','
                    linestr += self.__msgDict[it][4] + ','
                    for item2 in self.__msgDict[it][5]:
                        linestr += item2 + ';'
                    linestr += ','
                    traceFile.write(linestr + '\n')
                self.__msgDict.clear()
                traceFile.write('#msg_fields\n')
                for it in self.__msgFieldDict.keys():
                    linestr = it + ','
                    linestr += self.__msgFieldDict[it][0] + ','
                    linestr += self.__msgFieldDict[it][1] + ','
                    for item1 in self.__msgFieldDict[it][2]:
                        for item2 in item1:
                            linestr += item2 + '.'
                        linestr += ';'
                    linestr += ','
                    traceFile.write(linestr + '\n')
                self.__msgFieldDict.clear()
                traceFile.write('#mode\n')
                for it in self.__modeDict.keys():
                    linestr = it + ','
                    linestr += self.__modeDict[it][0] + ','
                    linestr += self.__modeDict[it][1] + ','
                    linestr += self.__modeDict[it][2] + ','
                    linestr += self.__modeDict[it][3][0] + ';'
                    if len(self.__modeDict[it][3]) > 1:
                        tmplist = self.__modeDict[it][3][1:]
                        for item1 in tmplist:
                            for item2 in item1:
                                linestr += item2 + '.'
                            linestr += ';'
                    linestr += ','
                    traceFile.write(linestr + '\n')
                self.__modeDict.clear()
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

def test():
    gd = GetDef()
    if gd.msg_def() and gd.msg_fields_def() and gd.mode_def() and gd.dictToFile('msg_mode_template'):
        pass
    else:
        print gd.dumpError()
##    if not gd.msg_def():
##        print gd.dumpError()
##    if not gd.msg_fields_def():
##        print gd.dumpError()
##    if not gd.mode_def():
##        print gd.dumpError()
##    print '------------------------------------------------------------------'
##    if not gd.dictToFile('msg_mode_template'):
##        print gd.dumpError()

if __name__ == '__main__':
    test()
