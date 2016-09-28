#!/usr/bin/python
#module:
#author: jzhao019

from procparse import tparser
from procparse import mparser
from msgHandle import msgDecoder
from filterEng import query_filter
from common import debug_print
from xml.dom import minidom
import versionHandle
import time

class ajaxSet(object):
    def __init__(self):
        pass

    def do_error(self, param1, param2):
        constr = param2.replace('\n', '<p>')
        doc = minidom.Document()
        rootNode = doc.createElement('Tag_ajax')
        content = '<p>' + param1 + '</p><p>' + constr + '</p>'
        content += '<p>Please contract author: <a href="mailto:Jun.J.Zhao@alcatel-sbell.com.cn">Zhao Jun</a></p>'
        text = doc.createTextNode(content)
        rootNode.appendChild(text)
        doc.appendChild(rootNode)
        xmlStr = doc.toxml()
        self.show(xmlStr)

    def do_normal(self, param):
        self.show(param)

    def show(self, param, Cookies=[]):
        if len(Cookies) > 0:
            print "SetCookie"
        # print maybe has a enter line, but it is error for chrome and error as following:
        # error on line 1 at column 6: XML declaration allowed only at the start of the document
        print "Content-type:text/xml\r\n\r\n", param

    def do_showbuffer(self, param):
        if len(param)  == 1:
            md = msgDecoder(param[0])
            if not md.prepare_template():
                self.do_error("Show Buffer Error", "Prepare template Error!\n" + md.dumpError())
                return
            tp = md.query_buffer(param[0])
            if tp[0] == False:
                self.do_error("Get Buffer Error", tp[1])
                return
            self.do_normal(tp[1])
        else:
            self.do_error("Get Buffer Error ", " parameter number error!")

    def do_listbuffer(self, param):
        if len(param)  == 1:
            md = msgDecoder(param[0])
            if not md.prepare_template():
                self.do_error("List Buffer Error", "Prepare template Error!\n" + md.dumpError())
                return
            tp = md.list_buffer(param[0])
            if tp[0] == False:
                self.do_error("List Buffer Error", tp[1])
                return
            self.do_normal(tp[1])
        else:
            self.do_error("List Buffer Error ", " parameter number error!")

    def do_setbuffer(self, param):
        if len(param)  == 3:
            md = msgDecoder(param[2])
            if not md.prepare_template():
                self.do_error("Set Buffer Error", "Prepare template Error!\n" + md.dumpError())
                return
            tp = md.set_buffer(param)
            if tp[0] == False:
                self.do_error("Set Buffer Error", tp[1])
                return
            self.do_normal(tp[1])
        else:
            self.do_error("Set Buffer Error ", " parameter number error!")

    def do_getfilter(self, param):
        if len(param)  == 1:
            tp = query_filter(param)
            if tp[0] == False:
                self.do_error("Get Filter Error", tp[1])
                return
            self.do_normal(tp[1])
        else:
            self.do_error("Get Filter Error ", " parameter number error!")

    def do_parsetrace(self, param):
        if len(param)  == 4:
            tp = tparser(param[0], param[1], param[2], param[3])
            if tp[0] == False:
                self.do_error("ParseTrace Error", tp[1])
                return
            self.do_normal(tp[1])
        else:
            self.do_error("ParseTrace Error ", " parameter number error!")

    def do_decodemsg(self, param):
        if len(param)  == 2:
            md = msgDecoder(param[1])
            if not md.prepare_template():
                self.do_error("DecodMsg Error", "Prepare template Error!\n" + md.dumpError())
                return
            rt = md.getMsg(param[0])
            if not rt[0]:
                self.do_error("DecodMsg Error", "Wrong ram message content!\n" + rt[1])
                return
            mdd = md.decode()
            if mdd[0]:
                self.do_normal(mdd[1])
            else:
                self.do_error("DecodMsg Error ", mdd[1])
        else:
            self.do_error("DecodMsg Error ", "Wrong ram message length!")

    def do_decodesinglemsg(self, param):
        timestat = "";
        start = time.time();
        if len(param) == 6:
           msg_new = mparser(param[0], param[1], param[2])
           end = time.time();
           timestat = timestat + "mparser:%d s\n"%(end - start);
           start = end;
           if msg_new[0]:
               md = msgDecoder(param[2])
               if not md.prepare_template():
                   self.do_error("DecodMsg Error", "Prepare template Error!\n" + md.dumpError())
                   return
               rt = md.getMsg(msg_new[1])
               end = time.time();
               timestat = timestat + "getMsg:%d s\n"%(end - start);
               if not rt[0]:
                   self.do_error("DecodeSingleMsg Error", "Wrong ram message content!\n" + rt[1])
                   return
               md.set_param(param);
               mdd = md.decode()
               end = time.time();
               timestat = timestat + "decode:%d s\n"%(end - start);
               debug_print(timestat);
               if mdd[0]:
                   #self.do_error("test", "")
                   self.do_normal(mdd[1])
               else:
                  # self.do_error("DecodSingleMsg Error ", mdd[1])
                  errorMsg = mdd[1];
                  errorMsg += param[1] + "|" + param[2];
                  errorMsg += "|" + (param[3] or "None");
                  errorMsg += "|" + (param[4] or "None");
                  errorMsg += "|" + (param[5] or "None");
                  self.do_error("DecodSingleMsg Error ", errorMsg);
           else:
              self.do_error("DecodSingleMsg Error ", msg_new[1])
        else:
            self.do_error("DecodSingleMsg Error ", "Wrong ram parameter number!")

    def do_listbscversion(self, param):
        if len(param) == 0:
            ret_vl = versionHandle.get_bsc_ver_list()
            if ret_vl[0] == False:
                self.do_error("List BSC Version Error", ret_vl[1])
            else:
                self.do_normal(ret_vl[1])
        else:
            self.do_error("List BSC Version Error ", " parameter number error!")
def handle(action, param):
    ajs = ajaxSet()
    if hasattr(ajs, "do_%s" % action):
        actual_func = getattr(ajs, "do_%s" % action)
        actual_func(param)
    else:
        ajs.do_error("Unknow Action: (" + action, ") Invalid Ajax Req!")
    

def test():
    print 'test'
##    handle('decodemsg', ['121$07:46:06:305$009498603$24 00 00 08 20 4E 06 00 01 00 1F 00 DB 05 00 00 00 0C 38 83 06 09 16 00$07 40 82 05 00 00 00 00 01 00 01 00 03 00 01 00 03 00 01 00 7D 00'])
##    handle('showbuffer', ['B11_MX_MR1_ED2'])
    handle('decodesinglemsg', ["123"])
    msg = '''0055247522 10:50:53:991 cmw-api.c 870 EMSD:msg 560 Prio 2 VCE210 FMM23 -> VCE149 FMM29
0055247523 10:50:53:991 cmw-common.c 563 DBUG:Hdr: 95 00 00 00 26 00 00 16 
                 0: 00 2D 30 02 95 00 1D 00 D2 00 17 00 D1 00 77 1A 
                16: 4A 01 07 0A 71 00 8D 01 01 00 00 01 01 00 00 00 
                32: FF 30 0A 6C 61 67''';
    handle('decodesinglemsg', [msg, "root", "B12_MX_MR2_ED4(AL31)", "", "", ""])
    return
    msg = '''0693078211 03:01:13:421 vostask.c 1100 IMRV:14 00 03 04 00 2D 63 06 01 00 32 00 16 05 00 00 00 00 00 00 
0693078212 03:01:13:421 vostask.c 1145 IMRV:VCE 1302 msg 1635 ->FMM321''';
    handle('decodesinglemsg', [msg, "root", "B12_MX_MR2_ED4(AL31)", "", "", ""])
    msg = '''1490095668 23:30:01:541 voscomm.c 182 IMSD:6B 00 00 28 20 4E 5F 02 03 00 26 00 03 00 12 00 03 02 08 2E CD 08 24 07 01 00 4A 03 08 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3D 00 1C 02 
1490095669 23:30:01:541 voscomm.c 185 IMSD:57 00 4A 03 00 00 AF 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 71 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DF 08 00 00 01 82 3F 03 81 01 00 DF 82 3E 01 00 DF 82 4C 01 1D 00 00 21 10 32 30 31 36 30 32 30 36 32 33 33 30 30 30 2E 30 00 00 00 00 00 00 00 00 F5 07 01 01 00 00 00 00 0F 02 01 02 01 01 81 04 01 02 03 04 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 
1490095670 23:30:01:541 voscomm.c 264 IMSD:msg 607 FMM87->FMM156''';
    handle('decodesinglemsg', [msg, "root", "B12_MX_MR2_ED4(AL31)", "", "", ""])

##    handle('listbuffer', ['B11_MX_MR1_ED2'])
##    handle('parsetrace', ['../trace/test.out','123','maint'])
##    handle('decodemsg', ['276$07:46:35:501$009500848$56 00 00 00 02 00 00 00 4E 00 00 00 20 3D 14 01 02 00 04 00 01 00 13 00 01 00 13 00 05 00 40 00 07 01 00 00 01 00 B8 10 02 43 1B 00 02 00 02 00 04 00 04 00 00 05 01 00 00 2C 00 00 00 02 00 01 00 2F 00 00 02 00 FC 00 FD 00 00 02 00 01 00 01 20 4E 0E 00 01 00$EMSD'])
##    handle('setbuffer', ['1', 'M_FI_DTC_LAPD_L2_FMM', 'B11_MX_MR1_ED2'])
##    handle('decodemsg1', ['685$07:46:06:305$009498557$BA 00 03 08 20 3D AD 02 01 00 2A 00 03 00 1D 00 00 00 D8 18 05 09 AC 00$07 40 01 00 03 00 1D 00 02 00 D2 00 00 00 00 00 00 00 04 00 04 00 A4 00 00 00 A8 00 00 00 74 00 30 00 00 00 00 00 00 00 23 00 0C 00 00 00 03 00 00 01 00 00 00 00 00 00 00 00 01 00 FF FF FF FF 01 00 05 FF 00 09 FF 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 06 00 FF FF 01 00 FF 00 01 02 0C 0C 00 1F FF FF FF FF 00 01 00 00 00 00 00 08 00 00 00 0A 00 00 00 00 31 30 30 30 38 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 00 00 00 01 00 00 01 1A 00 00 40'])
    handle('listbscversion', [])

if __name__ == '__main__':
    test()
