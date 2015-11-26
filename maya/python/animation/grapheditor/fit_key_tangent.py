#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
Copyright (c) 2015 Masahiro Ohmomo



Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:



The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.



THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# Author   : Masahiro Ohmomo
# DCC      : Maya
# Version  : 2013 - Latest
# Recommend: 2013
# 
# Description.
# In this script, do the fitting.
# The target is keyframe's tangent.
# You should be selected keyframe's of least two index.
#
# Run command.
# import fit_key_tangent
# fit_key_tangent.main()
#

from maya import cmds, mel
import math

def rad_deg(value=0.0, rd=False):
	if rd:
		return 180.0*value/3.141592
	else:
		return 3.141592*value/180.0

def main():
	names = cmds.keyframe(q=True, n=True)
	for n in names:
		frames  = cmds.keyframe(n,q=True,sl=True)
		values  = cmds.keyframe(n,q=True,vc=True,sl=True)
		countup = 0
		for i in range(len(values)):
			isLast = False
			if len(values)-1 == countup:
				x1,y1,x2,y2 = frames[i],values[i],frames[i-1],values[i-1]
				isLast=True
			else:
				x1,y1,x2,y2 = frames[i],values[i],frames[i+1],values[i+1]
			c_tan = rad_deg(math.atan((y2-y1)/(x2-x1)),True)
			if not isLast:
				cmds.keyTangent(n,e=True,a=True,t=(frames[i],frames[i]),oa=c_tan)
			else:
				cmds.keyTangent(n,e=True,a=True,t=(frames[i],frames[i]),ia=c_tan,oa=c_tan)
			countup += 1