import maya.cmds as cmds

def keyFullRotation( pObjectName, pStartTime, pEndTime, pTargetAttribute ):
    cmds.cutKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute )
    
    cmds.setKeyframe( pObjectName, time=pStartTime, attribute=pTargetAttribute, value=0 )
    
    cmds.setKeyframe( pObjectName, time=pEndTime, attribute=pTargetAttribute, value=360 )
    
    cmds.selectKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute, keyframe=True )
    
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )


selected = cmds.ls(sl=True, type='transform')

if not selected:
    cmds.confirmDialog(title='Error', message='You not select Object ', button=['OK'], defaultButton='OK')
else:
    
    startTime = cmds.playbackOptions(q=True, minTime=True)
    endTime = cmds.playbackOptions(q=True, maxTime=True)
    
    for objectName in selected:
        keyFullRotation(objectName, startTime, endTime, 'rotateY')