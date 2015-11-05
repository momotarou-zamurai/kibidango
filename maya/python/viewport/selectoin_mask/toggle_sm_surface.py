#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: Masahiro Ohmomo
# 
# Description.
# In this script, you can toggle the selection mask of objects .
#
# Run command.
# import toggle_sm_surface
# toggle_sm_surface.main()
#

from maya import cmds, mel

dcc_ver = cmds.about(v=True)

def main():
	# The nurbs.
	isNs   = False if cmds.selectType(q=True, ns=True) else True
	# The poly.
	isPoly = False if cmds.selectType(q=True, p=True) else True
	# The subdiv.
	isSd   = False if cmds.selectType(q=True, sd=True) else True
	# The plane.
	isPln  = False if cmds.selectType(q=True, pl=True) else True
	# The gpu chache.
	isGPU  = 0
	if '2013' in dcc_ver:
		isGPU = 0 if mel.eval('selectType -q -byName "gpuCache";') else 1
	
	cmds.selectType(ns=isNs)
	cmds.selectType(p=isPoly)
	cmds.selectType(sd=isSd)
	cmds.selectType(pl=isPln)
	if '2013' in dcc_ver:
		mel.eval('selectType -byName "gpuCache" %i;'%isGPU)