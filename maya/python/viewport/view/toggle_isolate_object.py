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
# toggle_isolate_object()
# 
# Run extra command.
# toggle_isolate_object(False)
# 

from maya import cmds, mel

def toggle_isolate_object(b_isolate=True):
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
				cmds.isolateSelect(src_panel, state=True)
			selected = cmds.ls(sl=True)
			if selected:
				view_object = cmds.isolateSelect(src_panel, q=True, vo=True)
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