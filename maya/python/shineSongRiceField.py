from maya import cmds, mel

def editShaderValue(attributes=[], value=.0):
    # 
    # Input your target attribute.
    # 
    # attributes = [
    #     'diffuse',
    #     'colorR',
    # ]
    
    materials = cmds.ls(mat=True) or []
    selected = cmds.ls(sl=True) or []
    for mat in materials:
        if selected:
            if not mat in selected:
                continue
        print '[ %s ]' % mat
        for attr in attributes:
            if cmds.attributeQuery(attr, n=mat, ex=True):
                cmds.setAttr('%s.%s' % (mat, attr), value)
                print '\t%s >>> %s' % (attr, value)

#
# Command.
#
attributes = [
    'specularAnisotropy',
]
value = .0
editShaderValue(attributes=attributes, value=value)
