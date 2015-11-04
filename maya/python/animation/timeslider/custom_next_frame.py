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
# custom_previous_frame()
#

def custom_next_frame():
	current  = cmds.currentTime(q=True)
	min, max = cmds.playbackOptions(q=True,min=True), cmds.playbackOptions(q=True,max=True)
	min     = cmds.playbackOptions(q=True,min=True)
	cmds.undoInfo(stateWithoutFlush=False)
	if current == max:
		cmds.currentTime(min)
	else:
		cmds.currentTime(current+1)
	cmds.undoInfo(stateWithoutFlush=True)