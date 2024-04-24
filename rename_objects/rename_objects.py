import maya.cmds as cmds

def list_objects():

    # List transform objects
    transformObjs = cmds.ls(transforms=True)

    # Take out camera viewport from transform objects
    items_names = [obj for obj in transformObjs if obj not in ['persp', 'top', 'front', 'side']]

    # Create list of objects mesh and group
    mesh = []
    grp = []

    # Check if object is mesh or group
    for items_name in items_names:
        shapes = cmds.listRelatives(items_name, shapes=True)
        if shapes:
            mesh.append(items_name)
        else:
            grp.append(items_name)

    # Return list of group and mesh
    return grp, mesh

# Testing
items = list_objects()
grp, mesh = items
print("Groups :", grp)
print("\nMeshes :", mesh)