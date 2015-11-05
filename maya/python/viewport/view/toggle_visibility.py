#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: Masahiro Ohmomo
# 
# Description.
# In this script, you can toggle the visibility of objects .
#
# Run command.
# import toggle_visibility
# toggle_visibility.main()
#

from maya import cmds

def main():
	selected = cmds.ls(sl=True)
	if selected:
		for sel in selected:
			b_v = False if cmds.getAttr('%s.v'%sel) else True
			cmds.setAttr('%s.v'%sel, b_v)