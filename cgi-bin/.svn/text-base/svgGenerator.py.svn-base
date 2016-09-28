#!/usr/bin/python
#author: jzhao019
#module:

from fileHandler import traceFilter, convert
import os

class svgGenerator:
    def __init__(self):
        self.__fmmPosX = None
        self.__fmmPoxY = None
        self.__content = ''
        self.__traceList = []
        self.__fmmList = []        
        self.__fmmPos = {}        
        self.__errorContent = ''
        self.__svgWidth = 0
        self.__svgHeight = 0

    def svgHeader(self):
        self.__content += '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-flat-20030114.dtd">
<svg width="100%" height="100%"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink">
   <title>Drag And Drop</title>
   <script xlink:href="../temp/mainSvg.js" type="text/javascript"/>
   <desc>
      SVG for RTTP created by MJ.
   </desc>'''
        self.__content += '\n'

    def svgTail(self):
        self.__content += '</svg>'

    def startDraw(self):
        self.svgHeader()
        if len(self.__traceList):
            self.drawBg()
            self.drawTrace()
        self.svgTail()

    def drawBg(self):
        self.checkFmm()
        if len(self.__fmmList):
            fmmX = 50
            for it in self.__fmmList:
                self.drawFmm(it, fmmX)
                fmmX += 200
        self.__svgWidth = fmmX + 20

    def drawTrace(self):
        if len(self.__fmmList):
            traceY = 200
            for it in self.__traceList:
                if it[1] == 'msg':
                    self.drawMsg(it, traceY)
                    traceY += 50
            self.__svgHeight = traceY + 20
                    

    def drawContent(self, svgName):        
        if svgName and len(svgName.strip()) > 0:
            try:
                self.__content = ''
                self.startDraw()
                svgFile = file(svgName.strip(), 'w')
                svgFile.write(self.__content)
                svgFile.close()
                return True
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                raise ex
                return False
        else:
            self.__errorContent += "SVG output file name is empty!\n"
            return False

    def loadTrace(self, trace):
        if trace and len(trace) > 0:
            self.__traceList = trace
            #print len(trace),trace
            return True
        else:
            #trace == null
            #print len(trace)
            self.__errorContent += "Trace list is empty!\n"
            return False

    def loadFile(self, traceFile):
        if traceFile and len(traceFile.strip()) > 0:
            try:
                if os.path.isfile(self.__fileName.strip()):
                    traceFile = file(traceFile.strip())
                    contents = traceFile.readlines()
                    self.__traceList = contents
                    traceFile.close()
                    return True
                else:
                    self.__errorContent += "File: " + traceFile.strip() + "does not exist!\n"
                    return False
            except Exception, ex:
                self.__errorContent += str(ex) + "\n"
                return False
        else:
            self.__errorContent += "Trace file name is empty!\n"
            return False

    def drawFmm(self, fmm, fmmX):
        fmmStr = '''<a id="fmm''' + fmm[0] + '''" onmouseover="showFmm(''' + "'fmm" + fmm[0] + " " + fmm[1] + "'" + ''')">'''
        fmmStr += '''<rect id="Rectangle''' + fmm[0] + '''" x="'''
        fmmStr += str(fmmX) + '''" y="70" width="100" height="50" style="fill:red; stroke:brown; stroke-width:1;"/>
   <text id="DraggableText'''
        fmmStr += fmm[0] + '''" x="''' + str(fmmX) + '''" y="100" style="fill:black; font-size:15px; font-weight:bold;">'''
        self.__fmmPos[fmm[0]] = fmmX
        fmmStr += fmm[1] + '''</text>'''
        fmmStr += '''<line id="FmmLine''' + fmm[0]
        fmmStr += '''" x1="''' + str(fmmX + 50) + '''" y1="120" x2="''' + str(fmmX + 50) + '''" y2="100000" stroke-width="2" style="stroke:rgb(99,99,99)" /></a>'''
        fmmStr += '\n'
        self.__content += fmmStr

    def drawLeftArrow(self, posX, posY):
        self.drawArrow('left', posX, posY)

    def drawRightArrow(self, posX, posY):
        self.drawArrow('right', posX, posY)

    def drawArrow(self, direction, posX, posY):
        if direction == 'left':
            upPosX = posX + 10
            upPosY = posY - 5
            downPosX = posX + 10
            downPosY = posY + 5
        elif direction == 'right':        
            upPosX = posX - 10
            upPosY = posY - 5
            downPosX = posX - 10
            downPosY = posY + 5
        else:
            upPosX = posX
            upPosY = posY
            downPosX = posX
            downPosY = posY
        
        arrowStr = '''<line x1="''' + str(posX)
        arrowStr += '''" y1="''' + str(posY)
        arrowStr += '''" x2="''' + str(upPosX)
        arrowStr += '''" y2="''' + str(upPosY)
        arrowStr += '''" stroke-width="2" style="stroke:rgb(99,99,99)" />'''

        arrowStr += '\n'

        arrowStr += '''<line x1="''' + str(posX)
        arrowStr += '''" y1="''' + str(posY)
        arrowStr += '''" x2="''' + str(downPosX)
        arrowStr += '''" y2="''' + str(downPosY)
        arrowStr += '''" stroke-width="2" style="stroke:rgb(99,99,99)" />'''

        arrowStr += '\n'
        self.__content += arrowStr

    def drawMsg(self, msg, traceY):
        fromId = msg[-1][3][0]
        toId = msg[-1][4][0]
        fromX = self.__fmmPos[fromId] + 50
        toX = self.__fmmPos[toId] + 50
        testX = 0
##        msgContent = "'" + msg[2] + "$" + msg[3] + "'"
        msgContent = "'" + msg[-1][0] + "$" + msg[2] + "$" + msg[3] + "$" + msg[-1][-2] + "$" +msg[-1][-1] +"'"
        msgStr = '''<a id="msg''' + msg[-1][0]
        msgStr += '''" onmouseover="showRaw(''' + msgContent
        msgStr += ''')" onmouseout="clearMsg()" onclick="showDetailedMsg(''' + msgContent + ''')">
   <line id="BlueLine" x1="'''
        msgStr += str(fromX) + '''" y1="''' + str(traceY) + '''" x2="''' + str(toX)
        msgStr += '''" y2="''' + str(traceY) + '''" stroke-width="2" style="stroke:rgb(99,99,99)"  />'''
        msgStr += '\n'
        self.__content += msgStr
        if fromX <= toX:
            self.drawRightArrow(toX, traceY)
            textX = fromX + 50
        else:
            self.drawLeftArrow(toX, traceY)
            textX = toX + 50
        msgStr = '''<text x="''' + str(textX) + '''" y="''' + str(traceY)
        if msg[-1][1] == 'dummy':
            msgStr += '''" style="fill:black; font-size:15px; font-weight:bold;">''' + msg[-1][0]
        else:
            msgStr += '''" style="fill:black; font-size:15px; font-weight:bold;">''' + msg[-1][1]
        msgStr += '''</text>
   </a>'''
        msgStr += '\n'
        self.__content += msgStr

    def checkFmm(self):
        for it in self.__traceList:
            if it[1] == 'Inside Function':
                pass
            elif it[1] == 'msg':
                fromFmm = it[-1][3]
                if fromFmm not in self.__fmmList:
                    self.__fmmList.append(fromFmm)
                toFmm = it[-1][4]
                if toFmm not in self.__fmmList:
                    self.__fmmList.append(toFmm)

    def getWidth(self):
        return self.__svgWidth

    def getHeight(self):
        return self.__svgHeight

    def dumpError(self):
        return self.__errorContent

def loadFilter():
    fileName = 'g.txt'
    svgName = 'g.svg'
    inputfile = '20100421_074648_20100421_075432_1.3.6_SCPR_[1]_1014.rtrc_backup.out'
##    inputfile = '20100901_001446_20100901_003037_1.3.6_SCPR_[1]_1014.rtrc_backup.out'
    ct = convert(inputfile, fileName)
    if ct.toFile() == False:
        print ct.dumpError()
    ft = {'inside':{'fmm 19':1}
          ,'msg':{
      'msg 411':1,
      'msg 412':1,
      'msg 121':1,
      'msg 122':1,
      'msg 123':1,
      'msg 124':1,
      'msg 125':1,
      'msg 126':1,
      'msg 127':1,
      'msg 128':1,
      'msg 136':1,
      'msg 135':1},
          'fmm':{
              '11':1
              }
          }
    fto = traceFilter(ft)
    if fto.loadFile(fileName, '.fmmlist', '.BSC_Messages') == False:
        print fto.dumpError()

    sg = svgGenerator()
    out = fto.showTrace()
    if sg.loadTrace(out):
        if sg.drawContent(svgName) == False:
            print sg.dumpError()
    else:
        print sg.dumpError()
    print sg.getWidth()
    print sg.getHeight()

def trace2svg():
   ## filename = '20100901_001446_20100901_003037_1.3.6_SCPR_[1]_1014.rtrc_backup.out'
    filename = '20121022_030208_20121022_031920_1.3.6_SCPR_[1]_1019.rtrc_backup.out'
    svgName = filename + '.svg'
    fto = traceFilter({})
    ct = convert(filename, filename+'.tmp')
    ctl = ct.toList()
    if not ctl:
        print ct.dumpError()
    if fto.loadList(ctl, '.fmmlist', 't_msgFile') == False:
        print fto.dumpError()

    sg = svgGenerator()
    out = fto.showTrace()
    if sg.loadTrace(out):
        if sg.drawContent(svgName) == False:
            print sg.dumpError()
    else:
        print sg.dumpError()
    print sg.getWidth()
    print sg.getHeight()


def Test():
    sg = svgGenerator()
    sg.drawFmm('19', 250)

if __name__ == '__main__':
    trace2svg()
##    Test()
