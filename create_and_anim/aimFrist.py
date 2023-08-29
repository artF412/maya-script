# aim first

import maya.cmds as cmds

selectionList = cmds.ls( orderedSelection = True)

if len(selectionList) >= 2:
    
    print('Selection item : {selectionList}')
    
    tragetName = selectionList[0]
    
    selectionList.remove (tragetName)
    
    for objectName in selectionList:
        
        print(f'Constraining {objectName} towards {tragetName}')
        
        cmds.aimConstraint(tragetName, objectName, aimVector=[0,1,0])
    
else:
    
    print('Please selected two or more objects')