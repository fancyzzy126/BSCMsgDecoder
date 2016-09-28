#!/usr/bin/python
#module:
#author jzhao019

from filter_inv import filterDBFile
from fileHandler import traceFilter, convert
import os
from xml.dom import minidom

from svgGenerator import svgGenerator
from common import debug_print

def tparser(filename, uname, fname, version):
    if filename and len(filename.strip()):
        return parser_assist(filename, uname, fname, version)
    else:
        return [False, 'trace file name is empty']

def mparser(msg_str, uname, version):
    if msg_str and len(msg_str.strip()):
        return prepare_single_msg(msg_str, uname, version)
    else:
        return [False, 'message is empty']

def prepare_single_msg(msg_str, uname, version):
    ct = convert('','', msg_str);
    ctl = ct.toList()
    fto = traceFilter({}, version)
    if ctl:
        if fto.loadList(ctl, '.fmmlist', 't_msgFile') == False:
            return [False, fto.dumpError()]
    else:
        return [False, ct.dumpError()]
    msg = fto.showTrace()
    if msg and len(msg) == 1:
        msg = msg[0]
        # [ True, 'msg', '00:15:42:004', '0336886848', 'vostask.c', '1100', ['124', '0124_READ_REC_CNF','IMRV', 
        #   ['4', 'ME_TWIN_FILE'], ['62', 'ROLL_BACK_HDLR'], '14 00 ... msgFields', 'msgUBuffer or no buffer'] ]
        # msg_new = __msgId$__msgTime$__msgSeq$__msgFields$__msgUBuffer
        msg_new = msg[-1][0] + "$" + msg[2] + "$" + msg[3] + "$" + msg[-1][-2] + "$" +msg[-1][-1]
        debug_print("procparse:prepare_single_msg, " + msg_new);
        return [True, msg_new]
    else:
        return [False, fto.dumpError()]
    

def parser_assist(filename, uname, fname, version):
    #cgi and html(temp) do not same direction, so the file name is different
    html_filename = "../trace/" + filename.split("/")[-1]
    max_record = 250
    file_num = 0
    f = filterDBFile()
    res = f.get_exact(uname, fname)
    if res[0] == False:
        return [False, f.dumperror()]
    fdict = {}
    for it in res[1]:
        if it[2] == 'msg':
            msglist = it[3].split(',')
            msglist = [it for it in msglist if len(it) > 0]
            fdict['msg'] = {}
            for item in msglist:
                if not fdict['msg'].has_key('msg ' + item):
                    fdict['msg']['msg ' + item] = 1
        elif it[2] == 'fmm':
            fmmlist = it[3].split(',')
            fmmlist = [it for it in fmmlist if len(it) > 0]
            fdict['fmm'] = {}
            for item in fmmlist:
                if not fdict['fmm'].has_key(item):
                    fdict['fmm'][item] = 1
##    # for test
##    fdict = {}
    ct = convert(filename, filename+'.tmp')
    fto = traceFilter(fdict, version)
##    if ct.toFile() == False:
##        return [False, ct.dumpError()]
    ctl = ct.toList()
    if not ctl:
        return [False, ct.dumpError()]
    if fto.loadList(ctl, '.fmmlist', 't_msgFile') == False:
        return [False, fto.dumpError()]
    sg = svgGenerator()    
    out = fto.showTrace()
##    #for test
    svg_file_num = 0
    svg_file_list = []
    if out and len(out) > max_record:
        num_record = len(out)
        i = 0
        curr = 0
        while curr < num_record:
            tmp_out = []
            if curr+max_record < num_record:
                end_index = curr + int(max_record)
                tmp_out = out[curr:end_index]
            else:
                tmp_out = out[curr:]
            if sg.loadTrace(tmp_out):
                if sg.drawContent(filename+"_"+str(i)+'.svg') == False:
                    return [False, sg.dumpError()]
            else:
                return [False, sg.dumpError()]
            svg_width = sg.getWidth()
            svg_height = sg.getHeight()
            svg_file_list.append([i, html_filename+"_"+str(i)+'.svg', svg_width, svg_height])
            i += 1
            curr += int(max_record)
            svg_file_num += 1
    else:
        if sg.loadTrace(out):
            if sg.drawContent(filename+'_0.svg') == False:
                return [False, sg.dumpError()]
        else:
            return [False, sg.dumpError()]
        svg_width = sg.getWidth()
        svg_height = sg.getHeight()
        svg_file_list.append([0, html_filename+'_0.svg', svg_width, svg_height])
        svg_file_num = 1
        
    doc = minidom.Document()
    rootNode = doc.createElement('svg_trace')
    doc.appendChild(rootNode)

    fnumNode = doc.createElement('svg_file_num')
    fnumNode.setAttribute('value', str(svg_file_num))
    rootNode.appendChild(fnumNode)

    flistNode = doc.createElement('svg_file_list')
    rootNode.appendChild(flistNode)

    for it in svg_file_list:
        fblockNode = doc.createElement('svg_file_'+str(it[0]))
        flistNode.appendChild(fblockNode)
        
        fnameNode = doc.createElement('svg_file_name')
        fnameNode.setAttribute('value', it[1])
        fblockNode.appendChild(fnameNode)   
        
        widthNode = doc.createElement('svg_width')
        widthNode.setAttribute('value', str(it[2]))
        fblockNode.appendChild(widthNode)
        
        heightNode = doc.createElement('svg_height')
        heightNode.setAttribute('value', str(it[3]))
        fblockNode.appendChild(heightNode)
    
    xmlStr = doc.toxml()
    return [True, xmlStr]



def test_tparser():
    print 'test'
##    filename = '../trace/20150617_030437_1.3.5_DTC_[9]_9_884.rtrc.out'
    filename = '../htdocs/trace/20150617_030519_1.3.5_DTC_[514]_514_593.rtrc.out'
##    filename = '../trace/test.out'
    uname = 'chasond'
    fname = '214FMM'
    version = 'B11_MX_MR1_ED2'
    rt = tparser(filename, uname, fname, version)
    if not rt[0]:
        print rt[1]
    else:
        print rt[1]

def test_mparser():
    msg = '''0076492894 07:02:50:874 cmw-api.c 870 EMSD:msg 1979 Prio 4 VCE1 FMM11 -> VCE1001 FMM0
0076492895 07:02:50:874 cmw-common.c 563 DBUG:Hdr: 1E 00 00 00 E9 03 00 00 
					       0: 16 00 00 06 00 4D BB 07  E9 03 00 00 01 00 0B 00 
					      16: FF FF FF 00 FF FF '''
    msg_imrv = ''' 0015999986 17:43:08:852 vostask.c 1100 IMRV:56 01 00 0C 20 4D 20 06 01 00 1F 00 01 00 05 00 BA AC D8 4C 15 09 44 01 13 00 00 00 
0015999987 17:43:08:852 vostask.c 1103 IMRV:07 40 FA 01 16 02 16 02 92 00 7A 00 02 02 12 02 2E 02 56 02 8E 00 8E 00 2A 02 26 02 22 02 06 02 12 02 02 02 2E 02 3E 02 7A 00 3E 02 26 02 FA 01 22 02 3E 02 36 02 36 02 62 00 7A 00 52 02 FE 01 56 02 9E 00 92 00 1E 02 92 00 62 00 0E 02 7A 00 7A 00 FF FF 0E 02 32 02 FF FF 62 00 2E 02 56 02 26 02 7A 00 3A 02 3E 02 8E 00 32 02 3A 02 FF FF 22 02 32 02 FF FF FF FF FF FF FF FF 0E 02 0A 02 FF FF FF FF FE 01 FF FF FF FF FF FF 9E 00 7A 00 1E 02 FF FF FF FF 62 00 FF FF 62 00 62 00 62 00 FF FF 00 00 FF FF FF FF 56 02 26 02 62 00 FF FF FF FF FF FF FF FF FF FF 56 02 92 00 2E 02 36 02 9E 00 9E 00 FF FF FF FF 9E 00 92 00 FF FF FF FF FA 01 12 02 06 02 FF FF 62 00 62 00 1E 02 92 00 1E 02 FF FF FF FF FF FF 9E 00 62 00 8E 00 7A 00 FF FF 26 02 2A 02 FF FF FF FF 3A 02 FF FF FF FF 32 02 36 02 2A 02 2A 02 FF FF FF FF FF FF FF FF FF FF 7A 00 22 02 92 00 FF FF FF FF FF FF FF FF FF FF FF FF 7A 00 FF FF FF FF FF FF FF FF 92 00 1E 02 2E 02 2E 02 36 02 FF FF FF FF 2A 02 16 02 56 02 92 00 
0015999988 17:43:08:852 vostask.c 1140 IMRV:VCE 1 msg 1568 FMM302->FMM11
'''
    msg_emsd1 = '''0338470693 03:24:24:960 cmw-api.c 870 EMSD:msg 239 Prio 2 VCE1 FMM7 -> VCE2 FMM10
0338470694 03:24:24:960 cmw-common.c 563 DBUG:Hdr: 02 00 00 00 11 00 00 01
                                               0: 00 2D EF 00 02 00 0A 00  01 00 07 00 00 0A 56 43
                                              16: 45'''
    msg_emsd2 = '''386122182 08:30:20:598 cmw-api.c 1085 EMRV:msg 685 Prio 3 VCE3 FMM49 -> VCE1 FMM4
386122183 08:30:20:598 cmw-common.c 558 DBUG:Hdr: AA 00 00 00 01 00 00 00 
					       0: A2 00 03 00 20 3D AD 02  01 00 04 00 03 00 31 00 
					      16: 01 00 03 00 31 00 00 00  CC 00 00 00 00 00 00 00 
					      32: 1E 00 00 00 76 00 00 00  94 00 00 00 46 00 30 00 
					      48: 00 00 00 00 00 00 0F 00  0C 00 00 00 03 00 00 01 
					      64: FF FF FF FF 00 00 00 00  06 00 00 00 00 01 21 00 
					      80: 9B 00 FF 0F 02 FF 1B 02  00 00 D2 00 FF FF 00 00 
					      96: 00 01 C0 00 04 00 FF 00  FF FF 00 00 FF 00 FF FF 
					     112: FF FF FF 00 FF FF 00 00  FF FF 00 00 FF FF 00 00 '''
    uname = 'tester'
    version = 'B11_MX_MR1_ED2'
    rt = mparser(msg_emsd2, uname, version)
    if not rt[0]:
        print rt[1]
    else:
        print rt[1]

if __name__ == '__main__':
    test_mparser()
    #test_tparser()
