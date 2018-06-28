# -*- coding: utf-8 -*-
#
# Installation:
# Add this file to your script path.
# Mac
# /Users/Shared/Autodesk/Maya
# Windows
# <user directory>/My Documents/Maya/scripts
# Linux
# /usr/autodesk/userconfig/Maya/scripts
#
#
# Usage:
# Select the target, and execute the following python command:
#
# import fitViewToObject
# fitViewToObject.fitView()
#

import math
import sys
from maya import OpenMaya, OpenMayaUI, cmds

sys.dont_write_bytecode = True


def getActiveView():
    view = OpenMayaUI.M3dView.active3dView()
    return view


def getDagPath(name=''):
    sl = OpenMaya.MSelectionList()
    dagPath = OpenMaya.MDagPath()
    sl.add(name)
    sl.getDagPath(0, dagPath)
    return dagPath


def fitView():
    objects = cmds.ls(sl=True)
    if not objects:
        return

    # View
    view = getActiveView()

    # Camera.
    cam = OpenMaya.MDagPath()
    view.getCamera(cam)
    camPath = cam.fullPathName()
    camDag = getDagPath(name=camPath)
    camFn = OpenMaya.MFnCamera(camDag)
    camTransform = cmds.listRelatives(camPath, p=True, typ='transform')[0]
    hFov = camFn.horizontalFieldOfView()

    # Create data.
    boundsArray = []
    centerArray = []
    for obj in objects:
        objPath = getDagPath(name=obj)
        try:
            objPath.extendToShape()
        except:
            pass
        objDagFn = OpenMaya.MFnDagNode(objPath)

        # Bounds.
        bBox = objDagFn.boundingBox()
        bBox.transformUsing(objPath.exclusiveMatrix())
        bbCenter = bBox.center()
        bbMin = bBox.min()
        bbMax = bBox.max()

        centerArray.append(OpenMaya.MVector(
            bbCenter.x,
            bbCenter.y,
            bbCenter.z
        ))

        temp = [
            OpenMaya.MPoint(bbMin[0], bbMin[1], bbMin[2]),
            OpenMaya.MPoint(bbMin[0], bbMin[1], bbMax[2]),
            OpenMaya.MPoint(bbMin[0], bbMax[1], bbMin[2]),
            OpenMaya.MPoint(bbMin[0], bbMax[1], bbMax[2]),

            OpenMaya.MPoint(bbMax[0], bbMin[1], bbMin[2]),
            OpenMaya.MPoint(bbMax[0], bbMin[1], bbMax[2]),
            OpenMaya.MPoint(bbMax[0], bbMax[1], bbMin[2]),
            OpenMaya.MPoint(bbMax[0], bbMax[1], bbMax[2])
        ]
        boundsArray += temp

    camCenter = OpenMaya.MVector(0, 0, 0)
    for center in centerArray:
        camCenter += center
    camCenter /= len(centerArray)

    boundingSphere = .0
    temp = []
    for pIndecs in xrange(len(boundsArray)):
        pp = boundsArray[pIndecs]
        v = bbCenter - pp
        temp.append(v.length())
    boundingSphere = max(temp) * 2.

    camDepth = boundingSphere / math.tan(hFov / 2.0)
    camDepth = OpenMaya.MPoint(0, 0, camDepth)
    if camDepth.z == 0:
        camDepth = OpenMaya.MPoint(0, 0, 5.)

    # Calc start.
    mMatrix = OpenMaya.MMatrix()
    __matrix = cmds.getAttr('%s.worldMatrix' % camTransform)
    OpenMaya.MScriptUtil.createMatrixFromList(__matrix, mMatrix)
    transformMatrix = OpenMaya.MTransformationMatrix(mMatrix)
    transformMatrix.setTranslation(
        OpenMaya.MVector(camCenter.x, camCenter.y, camCenter.z),
        OpenMaya.MSpace.kWorld
    )
    camMatrix = transformMatrix.asMatrix()
    camPos = camDepth * camMatrix

    cmds.setAttr(
        '%s.t' % camTransform,
        camPos.x,
        camPos.y,
        camPos.z
    )

    pA = cmds.xform(objects[0], q=True, ws=True, rp=True)
    vA = OpenMaya.MVector(pA[0], pA[1], pA[2])
    pB = cmds.xform(camTransform, q=True, ws=True, rp=True)
    vB = OpenMaya.MVector(pB[0], pB[1], pB[2])
    vAB = vA - vB
    coi = vAB.length()

    cmds.setAttr("%s.coi" % camPath, coi)
    cmds.setAttr(
        "%s.tumblePivot" % camPath,
        camCenter.x,
        camCenter.y,
        camCenter.z
    )
