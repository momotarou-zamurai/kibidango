import os
import re
import sys
import glob
import datetime
from maya import cmds, mel

def editShaderValue(attributes=[]):
    # 
    # Input your target attribute.
    # 
    # attributes = [
    #     'diffuse',
    #     'colorR',
    # ]
    
    materials = cmds.ls(mat=True) or []
    for mat in materials:
        print '[ %s ]' % mat
        for attr in attributes:
            if cmds.attributeQuery(attr, n=mat, ex=True):
                cmds.setAttr('%s.%s' % (mat, attr), .0)
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

def doIt(
    rootPath = r'F:\aaa\bbb\ccc',
    subFolderPath=r'hoge\scenes',
    searchFileType='.mb',
    editAttributes=['diffuse', 'colorR',],
    saveFileType='.ma'
):
    # 
    # Input your root folder.
    # 
    rootPath = rootPath

    # Get target folder.
    elements = glob.glob('%s/*' % rootPath)

    # 
    # If you have subfolders, edit here.
    # 
    subFolderPath = subFolderPath

    # Get the date of today.
    today = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

    for element in elements:
        targetFolderPath = '/'.join([element, subFolderPath])
        targetFolderPath = '%s/' % targetFolderPath

        # Get the latest file.
        latestFile = getLatestFile(
            dirPath=targetFolderPath,
            fileFilter='',
            fileExt=searchFileType
        )
        
        # File open.
        cmds.file(
            latestFile,
            f=True,
            o=True
        )

        # Edit the material.
        editShaderValue(attributes=editAttributes)
        
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
        fileType = 'mayaAscii'
        if saveFileType == '.mb':
            fileType = 'mayaBinary'
        cmds.file(save=True, type=fileType)

# 
# Edit
# 
rootPath       = r'F:\ohmomo\project\tempProjectA'
subFolderPath  = r'hoge\scenes'
editAttributes = [
    'specularAnisotropy',
]
searchFileType = '.mb'
saveFileType   = '.ma'

# Batch mode. Auto save.
doIt(
    rootPath = rootPath,
    subFolderPath=subFolderPath,
    searchFileType=searchFileType,
    editAttributes=editAttributes,
    saveFileType='.ma'
)


#
# Single Command.
#
attributes = [
    'specularAnisotropy',
]
editShaderValue(attributes=attributes)
