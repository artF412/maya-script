import maya.cmds as cmds
import random


# fix random
random.seed(1234)

# create polyCube width = 1 , height = 1 , depth = 1, name=set the name
create_cube = cmds.polyCube(w=1,h=1,d=1, name='cube#')

# get value transform node
transformName = create_cube[0]

# create group
groupName = cmds.group(empty=True, name=transformName+'_grp#')

# Create cube by number range
for i in range(50):
    # Duplicate objects from transformName
    createCube = cmds.instance(transformName, name=transformName+'_#')
    
    # Set child and parent
    cmds.parent(createCube, groupName)
    
    x = random.uniform(-10,10)
    y = random.uniform(0,20)
    z = random.uniform(-10,10)
    cmds.move(x, y, z, createCube)
    
    xRot = random.uniform(0, 360)
    yRot = random.uniform(0, 360)
    zRot = random.uniform(0, 360)
    cmds.rotate(xRot, yRot, zRot, createCube)
    
    scalingXYZ = random.uniform(0.3, 1.5)
    cmds.scale(scalingXYZ, scalingXYZ, scalingXYZ, createCube)
    
# set Pivot center in groupName
cmds.xform(groupName, centerPivots=True)

# hide transformName
cmds.hide(transformName)