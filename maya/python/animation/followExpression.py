# -*- coding: utf-8 -*-
from maya import cmds

ctrlShape = cmds.createNode('locator')
ctrlTransform = cmds.listRelatives(ctrlShape,p=True,f=True)
if isinstance(ctrlTransform,list):
    ctrlTransform = ctrlTransform[0]
jt = cmds.createNode('joint',n='followJoint')

attrName = 'follow'
if not cmds.attributeQuery(attrName,n=ctrlTransform,ex=True):
    cmds.addAttr(ctrlTransform,ln=attrName,at='double',min=0.0,max=1.0,dv=0.1)
    cmds.setAttr('%s.%s'%(ctrlTransform,attrName),e=True,k=True)

exp  = '{\n\t$tx1 = %s.translateX;\n'%ctrlTransform
exp += '\t$ty1 = %s.translateY;\n'%ctrlTransform
exp += '\t$tz1 = %s.translateZ;\n'%ctrlTransform
exp += '\t$tx2 = %s.translateX;\n'%jt
exp += '\t$ty2 = %s.translateY;\n'%jt
exp += '\t$tz2 = %s.translateZ;\n'%jt
exp += '\t\n\t$f  = %s.follow;\n'%ctrlTransform
exp += '\t$dx = $tx1;\n'
exp += '\t$dy = $ty1;\n'
exp += '\t$dz = $tz1;\n'
exp += '\tif ($f > 0.0)\n\t{\n\t\t$dx = ($tx1-$tx2)*$f;\n'
exp += '\t\t$dy = ($ty1-$ty2)*$f;\n'
exp += '\t\t$dz = ($tz1-$tz2)*$f;\n'
exp += '\t}\n\t%s.translateX += $dx;\n'%jt
exp += '\t%s.translateY += $dy;\n'%jt
exp += '\t%s.translateZ += $dz;\n'%jt
exp += '}'
cmds.expression(s=exp)
