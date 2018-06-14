import os
import re
import sys
import glob
import datetime
from maya import cmds, mel

def editShaderValue():
    # 
    # Input your target attribute.
    # 
    attributes = [
        'diffuse',
        'colorR',
    ]
    
    anisotropicList = cmds.ls(typ='anisotropic') or []
    for asl in anisotropicList:
        print '[ %s ]' % asl
        for attr in attributes:
            if cmds.attributeQuery(attr, n=asl, ex=True):
                cmds.setAttr('%s.%s' % (asl, attr), .0)
                print '\t%s >>> .0' % attr

def getLatestFile(dirPath='F:/', fileFilter='', fileExt='.mb'):
    if not os.path.isdir(dirPath):
        return ''
    dirPath = dirPath.replace(os.sep, '/')
    searchPath = '%s%s*%s' % (dirPath, fileFilter, fileExt)
    files = glob.glob(searchPath)
    if not files:
        return []
    latestFile = max(files, key=os.path.getctime)
    latestFile = latestFile.replace(os.sep, '/')
    return latestFile

# 
# Input your root folder.
# 
rootPath = r'F:\aaa\bbb\ccc'

# Get target folder.
elements = glob.glob('%s/*' % rootPath)

# 
# If you have subfolders, edit here.
# 
subFolderPath = r'hoge\scenes'

# Get the date of today.
today = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

for element in elements:
    targetFolderPath = '/'.join([element, subFolderPath])
    targetFolderPath = '%s/' % targetFolderPath

    # Get the latest file.
    latestFile = getLatestFile(
        dirPath=targetFolderPath,
        fileFilter='',
        fileExt='.mb'
    )
    
    # File open.
    cmds.file(
        latestFile,
        f=True,
        o=True
    )

    # Edit the material.
    editShaderValue()
    
    # File save.
    basename = os.path.basename(latestFile)
    temps = basename.split('.')
    extension = temps[-1]
    fileName = basename.replace('.%s' % extension, '')
    if re.search('editAMat', fileName):
        fileName = fileName.split('_editAMat')[0]
    newName = '_'.join([fileName, 'editAMat%s' % today])
    newFilePath = '%s%s.%s' % (targetFolderPath, newName, extension)
    
    cmds.file(rename=newFilePath)
    cmds.file(save=True, type="mayaBinary")
