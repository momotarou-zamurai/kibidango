#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: Masahiro Ohmomo
# 
# Description.
# In this script, you can toggle the isolate of objects .
# Run Select the object.
# 
# Extra command to disable the isolate.
# 
# 
# Run command. -Defult
# import toggle_isolate_object
# toggle_isolate_object.main()
# 
# Run extra command.
# import toggle_isolate_object
# toggle_isolate_object.main(False)
# 

from maya import cmds, mel

def main(b_isolate=True):
	active_panel = cmds.getPanel(wf=True)
	model_panel  = cmds.getPanel(typ='modelPanel')
	src_panel    = None
	if active_panel and active_panel in model_panel:
		src_panel = active_panel
	
	if src_panel:
		iso_state = cmds.isolateSelect(src_panel, q=True, state=True)
		isExist   = True
		if b_isolate:
			if iso_state == False:
				isExist = False
				mel.eval('enableIsolateSelect "%s" 1;'%src_panel)
			selected = cmds.ls(sl=True)
			if selected:
				view_object = cmds.isolateSelect(src_panel, q=True, vo=True)
				if view_object:
					set_members = cmds.sets(view_object, q=True)
					if set_members == None:
						set_members = []
					for sel in selected:
						cmds.select(sel,r=True)
						if sel in set_members and isExist == True:
							cmds.isolateSelect(src_panel, rs=True)
						else:
							cmds.isolateSelect(src_panel, addSelected=True)
					cmds.isolateSelect(src_panel,u=True)
					cmds.select(selected, r=True)
		elif b_isolate == False and iso_state:
			cmds.isolateSelect(src_panel, state=False)