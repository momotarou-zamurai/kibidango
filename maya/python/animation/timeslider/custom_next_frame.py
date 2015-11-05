#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: Masahiro Ohmomo
# 
# Description.
# In this script, you can go to next frame.
# And not save of undo history.
# If you go to than the maximum frame, it will jump to the minimum frame.
#
# Run command.
# import custom_next_frame
# custom_next_frame.main()
#

from maya import cmds

def main():
	current  = cmds.currentTime(q=True)
	min, max = cmds.playbackOptions(q=True,min=True), cmds.playbackOptions(q=True,max=True)
	cmds.undoInfo(stateWithoutFlush=False)
	if current == max:
		cmds.currentTime(min)
	else:
		cmds.currentTime(current+1)
	cmds.undoInfo(stateWithoutFlush=True)