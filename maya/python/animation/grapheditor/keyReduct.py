
# -*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True

from functools import partial
from maya import cmds

class windowClass(object):
    def __init__(self):
        self.wName  = 'keyReductWindow'
        self.wTitle = 'Key Reductor'

    def paddingFrame(self,padding=4):
        __max = int(cmds.playbackOptions(q=True,max=True))
        __min = int(cmds.playbackOptions(q=True,min=True))
        frames = [float(i+__min) for i in range(__max-__min+1)]
        paddingFrames = frames[::padding]
        if not __max in paddingFrames:
            paddingFrames.insert(len(paddingFrames),__max)
        removeFrames = list(set(frames)-set(paddingFrames))
        return [removeFrames,paddingFrames]

    def keyReduction(self,padding=0):
        if not padding or padding == 1:
            return
        selected = cmds.ls(sl=True,l=True)
        if not selected:
            return
        removeFrames, paddingFrames = self.paddingFrame(padding=padding)

        animationCurves = cmds.keyframe(selected,q=True,n=True)
        if not animationCurves:
            print 'Animation was not found.'
            return
        command = [eval('(%s,)'%removeFrames[i]) for i in xrange(len(removeFrames))]
        cmds.cutKey(cl=True,t=command)
        cmds.keyTangent(animationCurves,itt='auto', ott='auto')
        print "Keyframe reduct is done."

    def doIt(self,*args):
        padding = cmds.intFieldGrp(self.padding,q=True,v1=True)
        self.keyReduction(padding=padding)

    def buildUI(self):
        if cmds.window(self.wName,ex=True):
            cmds.deleteUI(self.wName)
        cmds.window(self.wName,t=self.wTitle)
        cmds.columnLayout(adj=True)
        self.padding = cmds.intFieldGrp(l='Padding',v1=5)
        cmds.button(l='Reduct',c=partial(self.doIt))
        cmds.setParent('..')
        cmds.showWindow(self.wName)

def main():
    windowClass().buildUI()