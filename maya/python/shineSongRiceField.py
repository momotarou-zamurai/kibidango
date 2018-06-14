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

#
# Single Command.
#
attributes = [
    'specularAnisotropy',
]
editShaderValue(attributes=attributes)
