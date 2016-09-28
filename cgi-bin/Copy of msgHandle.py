#!/usr/bin/python
#module: msgHandle
#author: jzhao019

import os
from xml.dom import minidom

class msgDecoder(object):
    def __init__(self):
        self.__errorContent = 'class msgDecoder \n'
        self.__msgId = ''
        self.__msgTime = ''
        self.__msgSeq = ''
        self.__msgFields = []
        self.__msgUBuffer = []
        self.__msgType = ''
        self.__msgFieldsType = ''
        self.__msgBufferType = ''
        self.__synDict = {}
        self.__msgXml = ''
        self.__fieldsName = 't_fieldsFile'
        self.__modeName = 't_modeFile'
        self.__synName = 't_synFile'
        self.__nodeName = 't_leafFile'
        self.__defName = 't_msgFile'
        self.__content = []
        self.__bufferMode = 'unknown'
        
        self.__header = ''
        self.__pathid = ''
        self.__bufferpointer = ''
        self.__bufferlength = ''
        self.__fields = 'unknown' 

    def getMsg(self, strMsg):
        if len(strMsg) == 0 or strMsg.count('$') != 4:
            self.__errorContent += 'msg input error\n'
            return [False, self.__errorContent]
        if strMsg[-1] == '\n':
            strMsg = strMsg[:-1]
        msgContent = strMsg.split('$')
        self.__msgId = str(int(msgContent[0]))
        self.__msgTime = msgContent[1]
        self.__msgSeq = msgContent[2]
        self.__msgFields = msgContent[3].split()
        self.__msgUBuffer = msgContent[4].split()
        md = self.loadmsgDefFFile(True)
        if not md[0]:
            return [False, self.__errorContent]
        msgDef = md[1]
        if int(msgDef[1]):
            self.__msgFieldsType = 'withfields'
        else:
            self.__msgFieldsType = 'nofields'
        if int(msgDef[2]):
            self.__msgBufferType = 'withbuffer'
            self.__msgType = 'withbuffer'
        else:
            self.__msgBufferType = 'nobuffer'
            self.__msgType = 'nobuffer'
        if len(msgDef) > 3:
            self.__bufferMode = msgDef[3]
            if self.__bufferMode[-1] == '\n':
                self.__bufferMode = self.__bufferMode[:-1]
        if self.__msgUBuffer[0] in ['nobuffer', 'EMSD']:
            self.__msgType = self.__msgUBuffer[0]
        else:
            self.__msgType = 'withbuffer'
        if self.__msgUBuffer[0] == 'EMSD':
            if self.__msgFieldsType == 'withfields':
                self.__msgFields = self.__msgFields[20:]
            elif self.__msgBufferType == 'withbuffer':
                self.__msgUBuffer = self.__msgFields[18:]
            else:
                # Both fields and buffer not exist, impossible.
                pass
        else:
            self.__msgFields = self.__msgFields[16:]
        return [True]

    def decode(self):
        xmlStr = ''
        if self.__msgType in ['withbuffer', 'nobuffer', 'EMSD']:
            doc = minidom.Document()
            rootNode = doc.createElement('msg_' + self.__msgId)
            doc.appendChild(rootNode)
            seqNode = doc.createElement('Trace_sequence')
            seqNode.setAttribute('value', str(self.__msgSeq))
            rootNode.appendChild(seqNode)
            doc.appendChild(rootNode)
            timeNode = doc.createElement('Trace_time')
            timeNode.setAttribute('value', str(self.__msgTime))
            rootNode.appendChild(timeNode)
##            if self.__msgType != 'EMSD':
            rt = self.handleFields()
            if not rt[0]:
                return rt
            rootNode.appendChild(rt[1])
            rt = self.handleUBffer()
            if not rt[0]:
                return rt
            rootNode.appendChild(rt[1])
            xmlStr = doc.toxml()
            return [True,xmlStr]
##            else:
##                xmlStr = 'EMSD not implemented...'
##                return [False,xmlStr]
        else:
            return [False, 'wrong in message user buffer!']

    def handleUBffer(self,):
        if self.__msgBufferType == 'nobuffer':
            doc = minidom.Document()
            rootNode = doc.createElement('msg_buffer')
            rootNode.setAttribute('value', 'No User Buffer!')
            doc.appendChild(rootNode)
            return [True, doc.documentElement]
        if self.__bufferMode == 'unknown':
            doc = minidom.Document()
            rootNode = doc.createElement('msg_buffer')
            rootNode.setAttribute('value', 'Not Select Buffer Mode!')
            doc.appendChild(rootNode)
            return [True, doc.documentElement]
        mf = self.loadModeFFile(True)
        if not mf[0]:
            return [False, self.__errorContent]
        msgBuffer = mf[1]
        nd = self.loadNodeFFile(False)
        if not nd[0]:
            return [False, self.__errorContent]
        sd = self.loadSynFFile()
        #todo
        doc = minidom.parseString(msgBuffer)
        ndl = nd[1].split(',')[1].split(';')[:-1]
        for it in ndl:
            nodeContent = it.split('$')
            nodeName = nodeContent[0]
            nodeMode = nodeContent[1]
            nodeSize = int(nodeContent[2])
            nodeOffset = int(nodeContent[3])
            if nodeSize % 8 != 0:
                nodeSize = nodeSize/8 +1
            else:
                nodeSize = nodeSize/8
            if len(self.__msgUBuffer) >= (nodeOffset + nodeSize):
                data = ''
                for item in self.__msgUBuffer[nodeOffset:(nodeOffset+nodeSize)]:
                    data += item + ' '
                data = data[:-1]
                for node in doc.getElementsByTagName(nodeName):
                    node.setAttribute("value",data)
        return [True, doc.documentElement]

    def handleFields(self):
        if self.__msgFieldsType == 'nofields':
            doc = minidom.Document()
            rootNode = doc.createElement('msg_fields')
            rootNode.setAttribute('value', 'No Fields!')
            doc.appendChild(rootNode)
            return [True, doc.documentElement]
        mf = self.loadmsgFieldsFFile()
        if not mf[0]:
            return [False, self.__errorContent]
        msgFields = mf[1]
        nd = self.loadNodeFFile(True)
        if not nd[0]:
            return [False, self.__errorContent]
        sd = self.loadSynFFile()
        #todo
        doc = minidom.parseString(msgFields)
        ndl = nd[1].split(',')[1].split(';')[:-1]
        for it in ndl:
            nodeContent = it.split('$')
            nodeName = nodeContent[0]
            nodeMode = nodeContent[1]
            nodeSize = int(nodeContent[2])
            nodeOffset = int(nodeContent[3])
            if nodeSize % 8 != 0:
                nodeSize = nodeSize/8 +1
            else:
                nodeSize = nodeSize/8
            if len(self.__msgFields) >= (nodeOffset + nodeSize):
                data = ''
                for item in self.__msgFields[nodeOffset:(nodeOffset+nodeSize)]:
                    data += item + ' '
                data = data[:-1]
                for node in doc.getElementsByTagName(nodeName):
                    node.setAttribute("value",data)
        return [True, doc.documentElement]
            

    def preProcessMsg(self):
        pass

    def loadmsgFieldsFFile(self):
        self.__errorContent += 'loadmsgFieldsFFile\n'
        if self.loadFile(self.__fieldsName):
            for it in self.__content:
                if it.startswith(self.__msgId + ','):
                    return [True, it.split(',')[1]]
            self.__errorContent += 'no msg' + self.__msgId + 'fields defined!\n'
            return [False]
        else:
            return [False]

    def loadmsgDefFFile(self, flag):
        '''
            flag True --> get special msg
                 False--> get all msg
        '''
        self.__errorContent += 'loadmsgDefFFile\n'
        if self.loadFile(self.__defName):
            if flag:
                for it in self.__content:
                    if it.startswith(self.__msgId + ','):                        
                        return [True, it.split(',')[1:]]
                self.__errorContent += 'no msg' + self.__msgId + 'structure defined!\n'
                return [False]
            else:
                try:
                    items = [it[:-1].split(',') for it in self.__content]
                    items = [it for it in items if int(it[3])]
                    return [True, items]
                except Exception, ex:
                    self.__errorContent += str(ex) + "\n"
                    return False
        else:
            return [False]

    def loadFile(self, fileName):
        self.__errorContent += 'loadFile\n'
        if fileName and len(fileName.strip()) > 0:
            try:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    contents = traceFile.readlines()
                    self.__content = [it for it in contents if len(it.strip())]
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

    def loadModeFFile(self, param):
        '''
           param: True --> buffer mode for special msgid
                  False--> all buffer mode
        '''
        self.__errorContent += 'loadModeFFile\n'
        if self.loadFile(self.__modeName):
            if param:
                for it in self.__content:
                    if it.startswith(self.__bufferMode + ','):
                        return [True, it.split(',')[1]]
                self.__errorContent += 'no mode ' + self.__msgId + ' defined!\n'
                return [False]
            else:                
                items = [it.split(',', 1)[0] for it in self.__content]
                return [True, items]
        else:
            return [False]

    def loadSynFFile(self):
        pass

    def loadNodeFFile(self, param):
        '''
           param: True --> msg
                  False--> mode
        '''
        self.__errorContent += 'loadModeFFile\n'
        if self.loadFile(self.__nodeName):
            if param:
                    start = self.__msgId + ','
            else:
                start = self.__bufferMode + ','
            for it in self.__content:
                if it.startswith(start):
                    nodeDef = it
                    return [True, nodeDef]
            self.__errorContent += 'no node ' + start + ' defined!\n'
            return [False]
        else:
            return [False]

    def query_buffer(self, param):
        md = self.loadmsgDefFFile(False)
        if not md[0]:
            return [False, self.__errorContent]
        doc = minidom.Document()
        rootNode = doc.createElement('buffer_list')
        doc.appendChild(rootNode)    
        msgDef = md[1]
        for it in msgDef:
            bufferNode = doc.createElement('msg_' + it[0])                        
            if len(it) > 4:
                bufferNode.setAttribute('value', it[4])
            rootNode.appendChild(bufferNode)
        return [True, doc.toxml()]

    def list_buffer(self, param):
        md = self.loadModeFFile(False)
        if not md[0]:
            return [False, self.__errorContent]
        doc = minidom.Document()
        rootNode = doc.createElement('buffer_list')
        doc.appendChild(rootNode)    
        msgDef = md[1]
        msgDef.sort()
        for it in msgDef:
            bufferNode = doc.createElement(it)     
            rootNode.appendChild(bufferNode)
        return [True, doc.toxml()]

    def set_buffer(self, param):
        self.__msgId = param[0]
        md = self.loadmsgDefFFile(True)
        if not md[0]:
            return [False, self.__errorContent]
        for it in self.__content:
            if it.startswith(self.__msgId + ','):
                index = self.__content.index(it)
                it = it[:-1].split(',')[:4]
                item = it[0] + ','
                item += it[1] + ','
                item += it[2] + ','
                item += it[3] + ','
                self.__content[index] = item + param[1]
        if not self.savemsgDef2File():
            return [False, self.__errorContent]
        doc = minidom.Document()
        rootNode = doc.createElement('set_buffer')
        doc.appendChild(rootNode)
        bufferNode = doc.createElement('success')
        rootNode.appendChild(bufferNode)
        return [True, doc.toxml()]

    def savemsgDef2File(self):
        self.__errorContent += 'savemsgDef2File'
        fileName = self.__defName
        if fileName and len(fileName.strip()) > 0:
            try:
                traceFile = open(fileName.strip(),'w')
                for it in self.__content:
                    traceFile.write(it + '\n')
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
    print 'test'
    md = msgDecoder()
    nb8 = '276$07:46:35:501$009500848$56 00 00 00 02 00 00 00 4E 00 00 00 20 3D 14 01 02 00 04 00 01 00 13 00 01 00 13 00 05 00 40 00 07 01 00 00 01 00 B8 10 02 43 1B 00 02 00 02 00 04 00 04 00 00 05 01 00 00 2C 00 00 00 02 00 01 00 2F 00 00 02 00 FC 00 FD 00 00 02 00 01 00 01 20 4E 0E 00 01 00$EMSD'
    nb7 = '471$07:47:30:371$009509141$61 00 00 00 03 00 00 00 59 00 00 20 20 4E D7 01 03 00 0E 00 01 00 0B 00 6F 81 0C 0B 04 00 00 00 29 00 01 00 0B 00 02 00 02 00 00 00 98 3A 01 00 03 00 EA 00 01 00 01 00 30 80 A2 03 02 01 00 A3 05 A1 03 02 01 00 AA 05 03 03 02 30 0C 00 00 40 00 01 00 03 00 05 00 00 02 00 02 00 02 00 00 00 00$EMSD'
    nb6 = '234$07:46:48:321$009502971$00 00 00 0E 20 4D EA 00 00 00 10 00 01 00 38 00 00 00 58 43 0F 09 D0 03 01 00 38 00 01 00$7A 00 01 01 01 01 00 00 00 00 00 00 00 01 01 00 00 00 00 00 00 00 00 00 00 00 36 01 01 00 03 01 01 01 01 01 96 00 01 00 FF 00 00 00 00 00 D1 00 3C 00 04 01 06 00 07 00 80 77 06 00 0A 00 0A 00 0A 00 00 00 00 00 00 00 00 00 00 00 00 13 14 07 00 00 2A 00 00 00 00 00 00 00 00 00 D2 00 98 67 23 01 68 00 07 00 E0 77 06 00 FF 00 FF 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 13 15 07 00 00 35 34 00 00 00 00 00 00 C6 00 D3 00 F6 09 0A 01 0A 00 07 00 50 E0 06 00 FF 00 FF 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 13 83 07 00 00 19 05 00 00 00 00 00 00 00 00 D4 00 F0 55 20 01 2C 00 07 00 90 EA 06 00 F4 01 F4 01 F4 01 00 00 00 00 DA 07 04 15 07 2E 30 03 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 66 00 07 00 40 41 07 00 F4 01 F4 01 F4 01 00 00 00 00 00 00 00 00 0C 00 25 00 01 02 F4 00 D4 21 00 00 00 00 00 13 E9 07 00 00 A4 64 00 00 00 00 00 00 AC 00 D6 00 08 52 1D 01 2A 00 07 00 90 0A 08 00 F4 01 F4 01 F4 01 00 00 00 00 00 00 00 00 00 00 00 13 BD 08 00 00 5B 29 00 00 00 00 00 00 47 00 D7 00 60 6D 11 01 1C 00 07 00 50 5D 08 00 E8 03 E8 03 E8 03 00 00 00 00 00 00 00 00 00 00 00 13 14 09 00 00 E3 36 00 00 00 00 00 00 D8 02 D9 00 F0 B9 15 01 22 00 07 00 20 CB 08 00 78 05 78 05 78 05 00 00 00 00 00 00 00 00 00 00 00 13 88 09 00 00 37 5D 01 00 00 00 00 00 9C 00 DB 00 DE 21 14 01 22 00 07 00 90 85 09 00 FF 00 FF 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 13 4D 0A 00 00 2B 11 01 00 00 00 00 00 0B 00 DD 00 A0 8C 06 01 24 00 07 00 F0 A7 09 00 E8 03 E8 03 E8 03 00 00 00 00 00 00 00 00 00 00 00 13 72 0A 00 00 62 46 00 00 00 00 FE 00 AC 03 05 07 00 03 B6 03 E6 00 04 00 04 00 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 00 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 FE 00 A8 03 05 07 00 03 B6 03 E6 00 04 00 04 00 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 FE 00 A4 03 05 07 00 03 B6 03 E6 00 04 00 04 00 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FE 00 A0 03 05 07 00 03 B6 03 E6 00 04 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FE 00 AD 03 05 07 00 03 B6 03 F0 00 04 00 01 00 08 00 01 01 01 01 00 00 00 00 00 01 01 01 00 00 00 00 00 00 00 00 00 00 00 00 60 00 01 00 03 02 00 01 00 01 38 00 07 00 FF 00 00 00 60 00 01 00 03 02 00 01 00 01 38 00 05 00 FF 00 00 00 60 00 01 00 03 02 00 01 00 01 38 00 03 00 FF 00 00 00 60 00 01 00 03 02 00 01 00 01 38 00 01 00 FF 80 00 00 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80 80'
    nb5 = '334$07:46:06:305$009498618$00 00 00 08 00 3E 4E 01 01 00 73 00 01 00 26 00 A2 7D 54 08 01 00 02 00$nobuffer'
    nb4 = '278$00:14:44:749$0009275026$40 00 03 08 20 3D 16 01 01 00 02 00 01 00 1F 00 00 00 38 83 06 09 32 00$07 40 01 00 1F 00 00 0E 2C 4A 07 00 00 00 01 00 B8 10 1C 41 61 01 02 00 01 00 14 00 A7 13 06 00 FF FF 01 00 00 01 0C 00 7A 2B 00 00 02 00 B8 04 B9 04'
    nb3 = '6$07:46:06:305$009498603$24 00 00 08 20 4E 06 00 01 00 1F 00 DB 05 00 00 00 0C 38 83 06 09 16 00$07 40 82 05 00 00 00 00 01 00 01 00 03 00 01 00 03 00 01 00 7D 00'
    nb = '121$07:46:06:305$009498603$00 00 00 08 00 38 79 00 00 00 26 00 01 00 02 00 A2 7D 54 08 01 00 02 00$nobuffer'
    nb2 = '126$07:46:06:327$009498762$04 00 00 0A 00 3E 7E 00 01 00 73 00 01 00 17 00 A2 7D 54 08 01 00 17 00 00 01$nobuffer'
    emsd = '411$07:46:06:329$009499057$28 00 00 00 EB 00 00 00 20 00 00 00 20 4D 9B 01 EB 00 12 00 01 00 13 00 00 00 01 00 00 01 2A 01 00 00 5D 01 01 00 80 40$EMSD'
    wb = ''
    emsd1 = '239$12:03:22:453$0000509221$02 00 00 00 11 00 00 01  00 2D EF 00 02 00 0A 00  01 00 07 00 00 0A 56 43 45$EMSD'
    rt = md.getMsg(emsd1)
    if not rt[0]:
        print 'wrong', rt[1]
    else:
        print 'process...'
        rt = md.decode()
        if rt[0]:
            print rt[1]
        else:
            print 'failed'
            print rt[1]

def test_querybuffer():
    print 'test_querybuffer'
    md = msgDecoder()
    rt = md.query_buffer([])
    if not rt[0]:
        print rt[1]
    else:
        print rt[1]

def test_list_buffer():
    print 'test_querybuffer'
    md = msgDecoder()
    rt = md.list_buffer([])
    if not rt[0]:
        print rt[1]
    else:
        print rt[1]

def test_set_buffer():
    print 'test_set_buffer'
    md = msgDecoder()
    rt = md.set_buffer(['6', 'M_LOCAL_REPORTING'])
    if not rt[0]:
        print rt[1]
    else:
        print rt[1]

if __name__ == '__main__':
    test()
