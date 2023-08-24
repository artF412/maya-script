import maya.cmds as cmds

def show_group_names():
    # Get the selected group
    select_GRP = cmds.ls(selection=True)
    if not select_GRP:
        cmds.warning('No Group Selected')
        return

    # Get the children of the selected group
    children = cmds.listRelatives(select_GRP, allDescendents=True, fullPath=True, type='transform')
    if not children:
        cmds.warning('No children found!')
        return

    all_names = select_GRP + children
    for path_check in all_names:
        path = path_check.split("|")[-1]
        if path.endswith(("GRP","GEO","SUBD")):
            s_path = path.split("_")[:-1]
            side = ['L','R','C']
            material = ['CERAMIC','GLASS','LEATHER','METAL','ORGANIC','PAPER','PLASTIC','RUBBER','TEXTILE','WOOD']
            if s_path[0] in side:
                s_path.remove(s_path[0])
            for s in s_path:
                if s in material:
                    s_path.remove(s)
            check_name_is_lower(s_path, path)
        else:
            cmds.warning('Object Name Incorrect: {}'.format(path))
            cmds.select(path, add=True)

def check_name_is_lower(s_path, path):
    check_name = ' '.join(s_path)
    if not check_name.islower():
        cmds.warning('Object Name Incorrect: {}'.format(check_name))
        cmds.select(path, add=True)

# Call the function
show_group_names()
