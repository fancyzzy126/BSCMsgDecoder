#!/usr/bin/python
#author: jzhao019
#module:

import os, re
from versionHandle import check_bsc_ver_exist
from versionHandle import get_ver_template_path
_debug = False
#if _debug:
from time import *
from common import debug_print
from common import is_debug
_debug = is_debug();

class convert(object):
    def __init__(self, inputfile='', outputfile='', tracestr=''):
        self.__errorContent = ""
        self.__maxline = 1024
        self.__contentList = [] # line string
        self.__traceStr = tracestr.strip()
        self.__fileName = inputfile.strip()
        self.__outputName = outputfile.strip()
        self.__lineHeader = re.compile(r"^\d{9,10} \d{2}:\d{2}:\d{2}:\d{3}")
        self.__cmwLineHeader = re.compile(r"^ {4,47}\d{1,4}:")
        #self.__cmwLineHeaderTab = re.compile(r"^\t{5} {3,7}\d{1,4}:")
        self.__cmwLineHeaderTab = re.compile(r"^[\s]*\d{1,4}:")
        self.__invalidLine_ticks_udp = re.compile(r"^\d{9} ticks upd,")
        self.__invalidLine_tradeb_ast = re.compile(r"^\d{10} \d{2}:\d{2}:\d{2}:\d{3} tradeb_ast.c")

    def toFile(self):
        if len(self.__outputName) == 0:
            self.__errorContent = "convert: No output file name!"
            return False
        else:
            if self.getTrace():
                if _debug:
                    print(asctime() + ' compactTrace');
                self.compactTrace()
                if _debug:
                    print asctime() + ' parseContent'
                self.parseContent()
##                print "true"
                if _debug:
                    print asctime() + ' writeFile'
                out = file(self.__outputName, "w")
                for it in self.__contentList:
                    items = it[0] + " " + it[1] + " " + it[2] + ' ' + it[3] + ' ' + it[4]
                    out.write(items + "\n")
                out.close()
                return True
            else:
                return False

    def toList(self):
        if self.getTrace():
            debug_print('compactTrace' + str(self.__contentList));
            self.compactTrace()
            debug_print('parseContent' + str(self.__contentList));
            self.parseContent()
            debug_print('toList return __contentList: ' + str(self.__contentList));
            return self.__contentList
        else:
            debug_print('toList failed:');
            return None

    def getTrace(self):
        if self.__fileName and len(self.__fileName) > 0:
            try:
                if os.path.isfile(self.__fileName.strip()):
                    traceFile = file(self.__fileName.strip())
                    contents = traceFile.readlines(self.__maxline)
                    while contents != []:
                        contents = [it[:-1] for it in contents if self.valid(it)]
                        self.__contentList += contents
                        contents = traceFile.readlines(self.__maxline)
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "File: " + self.__fileName + " does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        elif self.__traceStr and len(self.__traceStr) > 0:
            contents = self.__traceStr.split('\n')
            contents = [it for it in contents if self.valid(it)]
            self.__contentList = contents
            return True
	else:
            self.__errorContent += "Both Input File name and Trace string are empty!\n"
            return False
    def getMsg(self):
        pass
    def valid(self, parastr):
        return len(parastr.strip()) > 0 and \
		self.__invalidLine_ticks_udp.match(parastr) == None and \
		self.__invalidLine_tradeb_ast.match(parastr) == None

    def checkSeqTime(self, parastr):
        return self.__lineHeader.match(parastr) != None
		
    def do_filter(self, line):
	    return True

    # compact the multi-line trace for EMSD/EMRV
    def compactTrace(self, filter=True):
        index = 0
        pos = -1
        while index < len(self.__contentList):
            if self.checkSeqTime(self.__contentList[index]):
                pos = index
            else :
                app_ret = self.processAppendLine(self.__contentList[pos],
                                              self.__contentList[index])
                if app_ret[0]:
                    self.__contentList[pos] += " " + app_ret[1]
##                print index, pos, app_ret[1]
##                print self.__contentList[pos]
                self.__contentList[index] = ''
            index += 1
        self.__contentList = [it.split(" ",4) for it in self.__contentList if len(it) > 0 and filter and self.do_filter(it)]
##        self.__contentList = [it for it in self.__contentList if len(it) > 0]

    def processAppendLine(self, refLine, curLine):
        newLine = ''
        flag = False
        # Find by index directly for performance. May need be enhanced for some abnormal cases.
        # refLine[41:50]
        temp = refLine.split();
        if len(temp) > 4 and temp[4][:9] == "DBUG:Hdr:" and (self.__cmwLineHeader.match(curLine) != None or self.__cmwLineHeaderTab.match(curLine) != None):
            pos = curLine.find(':')
            newLine = curLine[pos+1:].strip()
            flag = True
##            print newLine
        return (flag, newLine)

    def parseContent(self):
        self.assembleMsg()

    def assembleMsg(self):
        '''
        EMSD
        IMRV
        ...
        '''
        index = 0
        #debug_print( "__contentList length:%d"%(len(self.__contentList)) );
        debug_print( "__contentList length:%d, %s\n"%(len(self.__contentList), self.__contentList) );
        while index < len(self.__contentList): 
            traceType = self.__contentList[index][-1][:4].strip()
            processFunction = getattr(self, "process%s" % traceType, self.processOTHER)
            index_bak = index;
            len_bak = len(self.__contentList);
            index = processFunction(index);
            if (index <= index_bak and len_bak == len(self.__contentList)):
                self.__errorContent += "Error, maybe enter endless loop! current index: %s" % str(index_bak)
                print "Content-type:text/xml\r\n\r\n", "<Tag_ajax>", self.dumpError(), \
                    self.__contentList[index], "</Tag_ajax>";
                exit(-1);

            if _debug:
                if index % 10000 == 0:
                    print asctime() + ' assemble ', index

    def processEMRV(self, index):
        return self.EMRV_EMSD_handler('EMRV', index)
		
    def processEMSD(self, index):
	    return self.EMRV_EMSD_handler('EMSD', index)
		
    def EMRV_EMSD_handler(self, msg_type, index):
        result = index
        len_cont = len(self.__contentList)
        msg_flag = msg_type + ':msg'
        # bug for parse error for end line
        msgid = ''
        # self.__contentList[index] = ['0336886848', '00:15:42:004', 'cmw-api.c', '1085', 'EMRV:msg 103 Prio 2 VCE1002 FMM40 -> VCE235 FMM25']
        if self.__contentList[index][-1][:8] == msg_flag and (index+1) < len_cont:
            msgid = self.__contentList[index][-1].split(' ', 2)[1]
            # self.__contentList[index + 1] = ['0336886848', '00:15:42:004', 'cmw-common.c', '558', 'DBUG:Hdr: 2A 00 00 00 EB 00 00 00 ...']
            if self.__contentList[index+1][-1][:8] == 'DBUG:Hdr':
                self.__contentList[index] = self.__contentList[index+1]
                msg_str = self.__contentList[index][-1]
                msg_str = msg_str.replace('DBUG', msg_type)
                msg_str = msg_str.replace('Hdr', msgid)
                self.__contentList[index][-1] = msg_str
                # self.__contentList[index] = ['0336886848', '00:15:42:004', 'cmw-common.c', '558', 'EMRV:103: 2A 00 00 00 EB 00 00 00 ...']
                del self.__contentList[index+1]
                result += 1
            # bug for error EMSD trace: 
            # 0009790777 03:04:01:225 cmw-api.c 950 EMSD:msgsnd(163845,,58,IPC_NOWAIT) returns 0 for vce=9
            else:
                del self.__contentList[index]
        else:
            del self.__contentList[index]
        return result            

    def IMRV_IMSD_handler(self, index, msg_type, msg_send_flag):
        # bug for parse error for end line
        result = index
        cont_len = len(self.__contentList)
        # ['0000502487', '11:48:33:012', 'vostask.c', '1100', 'IMRV:FA 03 03 08 20 2D 39 08 ...'] 
        if self.__contentList[index][-1].count(msg_send_flag) == 0 and (index+1) < cont_len:
            if self.__contentList[index+1][-1][:4] == msg_type:
                msg_send_flag_count1 = self.__contentList[index+1][-1].count(msg_send_flag)
                if msg_send_flag_count1 == 1:
                    # handle the last line of IMRV msg.
                    # self.__contentList[index + 1] = ['0000502489', '11:48:33:012', 'vostask.c', '1145', 'IMRV:VCE 209 msg 2105 ->FMM219']
                    self.__contentList[index][-1] += self.__contentList[index+1][-1][4:]
                    del self.__contentList[index+1]
                    result += 1
                elif msg_send_flag_count1 == 0 and (index + 2) < cont_len:
                    # self.__contentList[index + 1] = ['0000502488', '11:48:33:012', 'vostask.c', '1103', 'IMRV:07 40 FF FF FF FF FA 01 ...']
                    # self.__contentList[index + 2] = ['0000502489', '11:48:33:012', 'vostask.c', '1145', 'IMRV:VCE 209 msg 2105 ->FMM219']
                    msg_send_flag_count2 = self.__contentList[index+2][-1].count(msg_send_flag)
                    if self.__contentList[index+2][-1][:4] == msg_type and msg_send_flag_count2 == 1:
                        self.__contentList[index][-1] += self.__contentList[index+1][-1][4:]
                        self.__contentList[index][-1] += self.__contentList[index+2][-1][4:]
                        # self.__contentList[index] = ['0000502487', '11:48:33:012', 'vostask.c', '1100', 
                        # 'IMRV:FA 03 03 08 20 2D 39 08 ... :07 40 FF FF FF FF FA 01 ... :VCE 209 msg 2105 ->FMM219'] 
                        del self.__contentList[index+2]
                        del self.__contentList[index+1]
                        result += 1
                    elif msg_send_flag_count2 != 1:
                        del self.__contentList[index+1]
                        del self.__contentList[index]
                    else:
                        del self.__contentList[index+1]
                        del self.__contentList[index]
                else:
                    del self.__contentList[index+1]
                    del self.__contentList[index]
            else:
                del self.__contentList[index]
        else:
            del self.__contentList[index]
        return result

    def processIMRV(self, index):
        return self.IMRV_IMSD_handler(index, 'IMRV', '->')

    def processIMSD(self, index):
        return self.IMRV_IMSD_handler(index, 'IMSD', '->')

    def processOTHER(self, index):
        return index + 1

    def dumpError(self):
        return self.__errorContent

class traceFilter:
    def __init__(self, filterTemplate, version):
        self.__typeDict = {}
        self.__fmmDict = {}
        self.__msgDict = {}
        # self.__content[index] = ['0000502487', '11:48:33:012', 'vostask.c', '1100', 
        # 'IMRV:FA 03 03 08 20 2D 39 08 ... :07 40 FF FF FF FF FA 01 ... :VCE 209 msg 2105 ->FMM219']
        # self.__content[index] = ['0336886848', '00:15:42:004', 'cmw-common.c', '558', 'EMRV:103: 2A 00 00 00 EB 00 00 00 ...']
        self.__content = []
        self.__outList = []
        self.__filterTemplate = filterTemplate
        self.__version = version
        self.__template_dir = ''
        self.__errorContent = 'traceFilter: \n'

    def loadFile(self, fileName, fmmlist, msglist, ):
        ver_ret = check_bsc_ver_exist(self.__version)
        if not ver_ret[0]:
            self.__errorContent += ver_ret[1] + '\n'
            return False
        ver_ret = get_ver_template_path(self.__version)
        if not ver_ret[0]:
            self.__errorContent += ver_ret[1] + '\n'
            return False
        self.__template_dir = ver_ret[1]
        if self.loadFmmList(fmmlist) == False:
            return False
        if self.loadMsgList(msglist) == False:
            return False
        if fileName and len(fileName.strip()) > 0:
            try:
                if os.path.isfile(fileName.strip()):
                    traceFile = file(fileName.strip())
                    contents = traceFile.readlines()
                    contents = [it.split(' ', 4) for it in contents]
                    self.__content = contents
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "File: " + fileName + "does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "File name is empty!\n"
            return False

    def loadList(self, content, fmmlist, msglist):
        ver_ret = check_bsc_ver_exist(self.__version)
        if not ver_ret[0]:
            self.__errorContent += ver_ret[1] + '\n'
            return False
        ver_ret = get_ver_template_path(self.__version)
        if not ver_ret[0]:
            self.__errorContent += ver_ret[1] + '\n'
            return False
        self.__template_dir = ver_ret[1]
        if self.loadFmmList(fmmlist) == False:
            return False
        if self.loadMsgList(msglist) == False:
            return False
        self.__content = content
        return True

    def loadMsgList(self, msglist):
        self.__errorContent += 'loadMsgList\n'
        if msglist and len(msglist.strip()) > 0:
            try:
                if os.path.isfile(self.__template_dir+msglist.strip()):
                    traceFile = file(self.__template_dir+msglist.strip())
                    contents = traceFile.readlines()
                    for it in contents:
                        if len(it.strip()):
                            msg = it.split(',')
                            self.__msgDict[str(int(msg[0]))] = msg[1][6:]
##                            print msg[0], msg[1]
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "Msglist file: " + self.__template_dir+msglist.strip() + " does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "Msglist file name is empty!\n"
            return False

    def loadFmmList(self, fmmlist):
        self.__errorContent += 'loadFmmList\n'
        if fmmlist and len(fmmlist.strip()) > 0:
            try:
                if os.path.isfile(fmmlist.strip()):
                    traceFile = file(fmmlist.strip())
                    contents = traceFile.readlines()
                    for it in contents:
                        fmm = it.split()
                        self.__fmmDict[fmm[1]] = fmm[2].split('_', 3)[3]
##                        print fmm[1], fmm[2].split('_', 3)[3]
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "Fmmlist file: " + fmmlist.strip() + " does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "Fmmlist file name is empty!\n"
            return False

    def checkType(self):
        index = 0
        while index < len(self.__content):
##            print self.__content[index][4][:4].strip()
            traceType = self.__content[index][4][:4].strip()
            if traceType in ('IMRV', 'IMSD', 'EMSD', 'EMRV'):
                self.msgTrace(index, traceType)
            else:
                pass
            index += 1

    def condCheck(self):
        pass            

    def showTrace(self):
        if len(self.__content):
            self.checkType()
            if len(self.__outList):
                return self.__outList
        else:
            self.__errorContent = 'traceFilter: no trace input for filter'
        return None

    def convRev2Int(self, low, high):
        Id_low = int(low, 16)
        Id_high = int(high, 16)
        Id = Id_high * 16 * 16 + Id_low
        return Id

    def msgTrace(self, index, traceType):

        traceContent = [True, 'msg']
        traceContent.append(self.__content[index][1]) # date & time
        traceContent.append(self.__content[index][0]) # sequence
        traceContent.append(self.__content[index][2]) # file name
        traceContent.append(self.__content[index][3]) # line number
        msgContent = []
        if traceType in ['EMSD', 'EMRV']:
            '''
            EMSD_EMRV_MIN_LEN = 21
            EMSD_EMRV_PREFIX = 4 # CmwMsgQueue_t.mtype length
            EMSD_EMRV_PREFIX_BYTE = 12
            min_len = EMSD_EMRV_MIN_LEN
            offset = 0
            # self.__content[index][4] = 'EMRV:103: 2A 00 00 00 EB ...'
            tmp = self.__content[index][4].split(':')
            msgStr = tmp[2].strip();
            msgId_actual = tmp[1]
            msgStr_sec = msgStr.split()
##            print len(msgStr_sec),  self.__content[index], index
            msgId = self.convRev2Int(msgStr_sec[10], msgStr_sec[11])
            msgId =  str(msgId)
            if msgId != msgId_actual:
                offset = EMSD_EMRV_PREFIX
                min_len += EMSD_EMRV_PREFIX
                msgId = self.convRev2Int(msgStr_sec[offset+10], msgStr_sec[offset+11])
                msgId =  str(msgId)
                msgStr = msgStr[EMSD_EMRV_PREFIX_BYTE:]
            if len(msgStr_sec) < min_len:
                return
            '''
            EMSD_EMRV_PREFIX = 8 # CMW trace fields length
            # self.__content[index][4] = 'EMRV:103: 2A 00 00 00 EB ...'
            tmp = self.__content[index][4].split(':')
            msgStr = tmp[2].strip();
            msgId_actual = tmp[1]
            msgStr_sec = msgStr.split()
            msgId = self.convRev2Int(msgStr_sec[6], msgStr_sec[7])
            msgId = str(msgId)
            if msgId != msgId_actual:
                offset = EMSD_EMRV_PREFIX
                msgId = self.convRev2Int(msgStr_sec[offset + 6], msgStr_sec[offset + 7])
                msgId = str(msgId)

##            print 'msgId', msgId
            if msgId in self.__msgDict:
                msgContent = [msgId, self.__msgDict[msgId], 'EMSD']
            else:
                msgContent = [msgId, 'dummy', 'EMSD']
            fromFmm = self.convRev2Int(msgStr_sec[offset+14], msgStr_sec[offset+15])
            fromFmm = str(fromFmm)
##            print 'fromFmm ', fromFmm
            fromVce = self.convRev2Int(msgStr_sec[offset+12], msgStr_sec[offset+13])
            fromVce = str(fromVce)
##            print 'fromVce', fromVce
            toFmm = self.convRev2Int(msgStr_sec[offset+10], msgStr_sec[offset+11])
            toFmm = str(toFmm)
##            print 'toFmm', toFmm
            toVce = self.convRev2Int(msgStr_sec[offset+8], msgStr_sec[offset+9])
            toVce = str(toVce)
##            print 'toVce', toVce
            if fromFmm in self.__fmmDict:
                msgContent.append([fromVce, fromFmm, self.__fmmDict[fromFmm]])
            else:
                msgContent.append([fromVce, fromFmm, 'unknown'])
            if toFmm in self.__fmmDict:
                msgContent.append([toVce, toFmm, self.__fmmDict[toFmm]])
            else:
                msgContent.append([toVce, toFmm, 'unknown'])
            #msgContent.append(msgStr)
            msgContent.append(" ".join(msgStr_sec[offset:]));
            msgContent.append('EMSD')
##            print 'msgContent', msgContent
        elif traceType in ('IMRV', 'IMSD'):
            if not self.__content[index][4].count('msg'):
                return
            tmp = self.__content[index][4].split(':') # tmp[-1] = 'VCE 1 msg 124 FMM4->FMM62'
            msgTitle = tmp[-1].split('->'); # msgTitle[0] = 'VCE 1 msg 124 FMM4' msgTitle[1] = 'FMM62'
            fromPart = msgTitle[0].split(); # fromPart = ['VCE', '1', 'msg', '124', 'FMM4']
            msgIndex = fromPart.index('msg')
            msgId = fromPart[msgIndex + 1]
            if msgId in self.__msgDict:
                msgContent = [msgId, self.__msgDict[msgId], traceType]
            else:
                msgContent = [msgId, 'dummy', traceType]
            if tmp[-1].count('FMM') == 1:
                msgContent.append(['0', 'dummy'])
            else:
                fromFmm = msgTitle[0].split()[-1][3:]
                if fromFmm in self.__fmmDict:
                    msgContent.append([fromFmm, self.__fmmDict[fromFmm]])
                else:
                    msgContent.append([fromFmm, 'unknown'])
            toFmm = msgTitle[1][3:].strip()
            if toFmm in self.__fmmDict:
                msgContent.append([toFmm, self.__fmmDict[toFmm]])
            else:
                msgContent.append([toFmm, 'unknown'])            
            msgContent.append(tmp[1].strip()) # first line: message head and content, buffer pointer
            if len(tmp) == 4:
                msgContent.append(tmp[2].strip()) # second line: buffer content
            else:
                msgContent.append('nobuffer') 
        traceContent.append(msgContent)
        msgKey = 'msg ' + msgContent[0]
        msgFlag = False
        if self.__filterTemplate.has_key('fmm') or self.__filterTemplate.has_key('msg'):
            if self.__filterTemplate.has_key('msg') and self.__filterTemplate['msg'].has_key(msgKey):
                msgFlag = True
            if self.__filterTemplate.has_key('fmm') and (self.__filterTemplate['fmm'].has_key(msgContent[3][0]) or self.__filterTemplate['fmm'].has_key(msgContent[4][0])):
                msgFlag = True
        else:
            msgFlag = True
        if msgFlag == True:
            self.__outList.append(traceContent)

    def insideTrace(self):
        pass

    def dbTrace(self):
        pass

    def otherTrace(self):
        pass

    def dumpError(self):
        return self.__errorContent


def showTraceType(inputfile):
    rfile = file(inputfile)
    content = rfile.readlines()

    typeDict = {}
    for it in content:
        traceType = it.split(" ",4)[-1][:4]
        if traceType in typeDict:
            pass
        else:
            typeDict[traceType] = 1

    items = typeDict.keys()
    print items


def testConvert():
    ct = convert("tcu.txt", "h.txt")
##    ct.toXML()
    tl = ct.toList()
    temp = file('temp.txt', 'w')
    if tl:
        for it in tl:
            temp.write(it[0] + " " + it[1] + " " + it[2] + ' ' + it[3] + ' ' + it[4] + '\n')
    temp.close()

def showMsg():
##      ct = convert("20100421_074648_20100421_075432_1.3.6_SCPR_[1]_1014.rtrc_backup.out", "h.txt")
##    ct = convert("20100916_113845_20100916_122751_1.3.6_SCPR_[1]_1025.rtrc_backup.out","g.txt")
      ct = convert('../trace/20100805_120211_20100805_131742_1.3.6_SCPR_[1]_1014.rtrc_backup.out','g.txt')
##    ct = convert('20100901_001446_20100901_003037_1.3.6_SCPR_[1]_1014.rtrc_backup.out','g.txt')
##      ct = convert('../trace/20120613_193840_20120614_071822_1.4.4_TCU_[235]_335.rtrc_backup.out', 'h.txt')
##      ct = convert('test.out', 'h.txt')
      ft = {'msg':{'msg 6':1,
                   'msg 234':1,
                   'msg 1458':1},
            'fmm':{'11':1}}
      fto = traceFilter(ft, 'B11_MX_MR1_ED2')
      if ct.toFile() == False:
          print ct.dumpError()
      else:
          if fto.loadFile('g.txt', '.fmmlist', 't_msgFile') == False:
              print '123' +fto.dumpError()  
    ##    fto.loadList(ct.toList())
      out = fto.showTrace()
      print out
      if out:
          for it in out:
              print it
    
def Test():
    showMsg()
##    showTraceType("g.txt")

def convertSingleMsg():
    msg_imrv = ''' 0336886848 00:15:42:004 vostask.c 1100 IMRV:14 00 00 0A 00 3E 7C 00 01 00 2D 00 01 00 1D 01 98 A8 62 08 01 00 1D 01 00 00 
0336886849 00:15:42:004 vostask.c 1140 IMRV:VCE 1 msg 124 FMM4->FMM62
'''
    msg_imrv1 = ''' 0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03 
0000502488 11:48:33:012 vostask.c 1103 IMRV:07 40 FF FF FF FF FA 01
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
'''
    msg_imrv2 = ''' 0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03 
0000502488 11:48:33:012 vostask.c 1103 IMRV:07 40 FF FF FF FF FA 01
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
'''
    msg_imrv3 = ''' 0015736949 17:34:54:755 vostask.c 1100 IMRV:1C 00 00 0E 20 48 B5 05 01 00 1F 00 01 00 1C 00 AA 68 18 85 14 09 24 03 02 00 13 09 FF FF 
0015736950 17:34:54:755 vostask.c 1103 IMRV:15 00 0A 00 04 00 00 07 D2 00 00 02 E6 01 00 00 E8 01 00 00 EA 01 00 07 EC 01 00 22 EE 01 00 01 F0 01 00 00 F2 01 00 00 F4 01 00 07 0B 17 11 22 2C 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FE 00 61 01 05 07 01 03 78 02 F0 00 03 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FE 00 62 01 05 07 01 03 78 02 98 00 03 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
0015736951 17:34:54:755 vostask.c 1140 IMRV:VCE 1 msg 1461 FMM21->FMM11
'''
    msg_imrv4 = ''' 0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03 
0000502488 11:48:33:012 vostask.c 1103 IMRV:07 40 FF FF FF FF FA 01
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03 
0000502488 11:48:33:012 vostask.c 1103 IMRV:07 40 FF FF FF FF FA 01
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
0000502487 11:48:33:012 vostask.c 1100 IMRV:FA 03 03 08 20 2D 39 08 01 00 3B 00 D1 00 17 00 00 00 F8 0F 11 09 EC 03 
0000502488 11:48:33:012 vostask.c 1103 IMRV:07 40 FF FF FF FF FA 01
0000502489 11:48:33:012 vostask.c 1145 IMRV:VCE 209 msg 2105 ->FMM219
'''
    msg_emsd = '''0000509209 12:03:21:143 cmw-api.c 870 EMSD:msg 276 Prio 3 VCE1 FMM53 -> VCE2 FMM4
0000509210 12:03:21:143 cmw-common.c 563 DBUG:Hdr: 02 00 00 00 31 00 00 00 
					       0: 20 3D 14 01 02 00 04 00  01 00 35 00 01 00 35 00 
					      16: 05 00 23 00 01 00 00 00  01 00 B8 10 16 41 A3 00 
					      32: 01 00 01 00 54 00 0F 00  FF FF 01 00 03 0A 6B 54 
					      48: 75
'''
    msg_emsd1 = '''0000509220 12:03:22:453 cmw-api.c 870 EMSD:msg 239 Prio 2 VCE1 FMM7 -> VCE2 FMM10
0000509221 12:03:22:453 cmw-common.c 563 DBUG:Hdr: 00 00 00 00 02 00 00 00 11 00 00 01 
					       0: 00 2D EF 00 02 00 0A 00  01 00 07 00 00 0A 56 43 
					      16: 45
'''
    msg_imsd = '''0183334107 03:19:06:795 voscomm.c 182 IMSD:4C 00 03 08 20 3D 16 01 02 00 3C 00 02 00 09 00 00 00 98 D7 40 09 3E 00 
0183334108 03:19:06:795 voscomm.c 185 IMSD:07 40 02 00 09 00 03 13 06 4F 07 00 00 00 02 00 A0 14 07 41 64 01 03 00 03 00 1C 00 7B 22 52 00 FF FF 01 00 02 00 0D 00 9A 34 00 00 02 00 F6 03 F7 03 0D 00 98 34 03 00 02 00 F8 03 F7 03 
0183334109 03:19:06:795 voscomm.c 264 IMSD:msg 278 FMM232->FMM60
'''
    msg_emrv = '''0000019674 07:09:21:064 cmw-api.c 1079 EMRV:blocking msgrcv(1474605,85a2924,8286) call returns size=42
CmwLen=42, MsgLen=34, CtxLen = 0
0000019675 07:09:21:064 cmw-api.c 1085 EMRV:msg 103 Prio 2 VCE1002 FMM40 -> VCE235 FMM25
0000019676 07:09:21:064 cmw-common.c 558 DBUG:Hdr: 2A 00 00 00 EB 00 00 00 
					       0: 22 00 03 00 20 AD 67 00  EB 00 19 00 EA 03 28 00 
					      16: 00 00 00 00 00 00 00 00  00 00 00 01 04 00 FA 03 
					      32: 01 08  
0000019677 07:09:21:064 vos.c 120 ITFP:GET_MSG_BUF called by BackgroundTask.'''
    msg_imrv8 = '''0001048739 13:23:54:499 vostask.c 1100 IMRV:46 00 00 28 20 4D 9C 01 02 00 13 00 1D 01 08 00 00 00 58 4E 42 09 18 00 00 00 00 00 00 00 00 00 D3 24 01 BB 63 01 2B 2B 2B 2B 2B 2B 2B 00 00 00 00 00 00 00 00 00 00 00 
0001048740 13:23:54:499 vostask.c 1103 IMRV:07 40 1D 01 08 00 1D 01 35 03 00 00 C1 01 01 01 00 00 00 00 00 00 00 00 
0001048741 13:23:54:499 vostask.c 1145 IMRV:VCE 285 msg 412 ->FMM19'''
    msg_emsd2 = '''0002880880 04:41:40:489 cmw-api.c 870 EMSD:msg 137 Prio 4 VCE1 FMM260 -> VCE1309 FMM0
0002880881 04:41:40:489 cmw-common.c 563 DBUG:Hdr: 1D 05 00 00 22 00 00 12 
            0: 00 4D 89 00 1D 05 00 00  01 00 04 01 04 00 00 00 
           16: 01 00 29 00 01 00 FF 00  06 00 01 00 0E 00 0A 6D 
           32: 5F 53'''
    msg_emsd3 = '''0338431136 03:24:16:882 cmw-api.c 870 EMSD:msg 239 Prio 2 VCE1 FMM7 -> VCE2 FMM10
0338431137 03:24:16:882 cmw-common.c 563 DBUG:Hdr: 02 00 00 00 11 00 00 01
                                               0: 00 2D EF 00 02 00 0A 00  01 00 07 00 00 0A 56 43
                                              16: 45'''
    msg_emsd4 = '''0031026714 05:09:54:567 cmw-api.c 870 EMSD:msg 276 Prio 3 VCE1 FMM59 -> VCE2 FMM4
0031026715 05:09:54:567 cmw-common.c 563 DBUG:Hdr: 02 00 00 00 63 00 00 00 
					       0: 20 3D 14 01 02 00 04 00  01 00 3B 00 01 00 3B 00 
					      16: 05 00 55 00 01 00 00 00  01 00 A0 14 0A 41 34 01 
					      32: 05 00 01 00 36 00 02 00  00 00 FF FF FF FF 01 00 
					      48: 00 06 00 00 00 FF FF FF  FF 01 00 00 07 00 00 00 
					      64: FF FF FF FF 01 00 07 08  00 00 00 FF FF FF FF 02 
					      80: 00 02 00 30 00 00 00 03  00 00 00 02 00 CC 01 0A 
					      96: 54 75 70  '''
    msg_emsd5 = '''0031026714 05:09:54:567 cmw-api.c 870 EMSD:msg 1273 Prio 2 VCE1 FMM59 -> VCE505 FMM239
0031026715 05:09:54:567 cmw-common.c 563 DBUG:Hdr: f9 01 00 00 12 00 00 02
                                               0: 00 2d f9 04 f9 01 ef 00  01 00 3b 00 02 00 0a 20 
                                              16: 56 43'''
    ct = convert('','', msg_emrv)
    ctl = ct.toList()
    fto = traceFilter({}, 'B11_MX_MR1_ED2')
    if ctl:
        if fto.loadList(ctl, '.fmmlist', 't_msgFile') == False:
            print fto.dumpError()
    else:
        ct.dumpError()
    out = fto.showTrace()
    if out:
        for it in out:
            msg = it
            print 'msg2', msg
            #print msg[-1][0] + "$" + msg[2] + "$" + msg[3] + "$" + msg[-1][-2] + "$" +msg[-1][-1]

if __name__ == '__main__':
#    showMsg()
    convertSingleMsg()
