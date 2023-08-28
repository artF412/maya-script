from PySide2 import QtWidgets , QtGui , QtCore
import maya.cmds as cmds
import maya.api.OpenMaya as om2

list_widget = None

def create_ui():
    global list_widget , label   #global variable
    dialog = QtWidgets.QDialog(parent=QtWidgets.QApplication.activeWindow())
    dialog.setWindowTitle('Checker UVs')
    dialog.setFixedSize(600, 800)

    layout = QtWidgets.QHBoxLayout()

    left_layout = QtWidgets.QVBoxLayout()

    label = QtWidgets.QLabel('Select Group Object')
    left_layout.addWidget(label)

    list_widget = QtWidgets.QListWidget()
    left_layout.addWidget(list_widget)

    left_widget = QtWidgets.QWidget()
    left_widget.setLayout(left_layout)
    layout.addWidget(left_widget, stretch=2)

    right_layout = QtWidgets.QVBoxLayout()
    
    button_delete_history = QtWidgets.QPushButton("Delete History")
    right_layout.addWidget(button_delete_history)
    button_delete_history.clicked.connect(on_button_delete_history)
    
    button_check_uv = QtWidgets.QPushButton("Check UVs")
    right_layout.addWidget(button_check_uv)
    button_check_uv.clicked.connect(on_button_check_uvs)
    
    button_check_overlapping = QtWidgets.QPushButton("Check Overlapping UVs")
    right_layout.addWidget(button_check_overlapping)
    button_check_overlapping.clicked.connect(on_button_check_overlapping)
    
    button_check_udim = QtWidgets.QPushButton("Check UDIM")
    right_layout.addWidget(button_check_udim)
    button_check_udim.clicked.connect(on_button_check_udim)
    
    button_check_flip = QtWidgets.QPushButton("Check Flip UVs")
    right_layout.addWidget(button_check_flip)
    button_check_flip.clicked.connect(on_button_check_flip)
    
    button_check_uv_map = QtWidgets.QPushButton("Check UV Map")
    right_layout.addWidget(button_check_uv_map)
    button_check_uv_map.clicked.connect(on_button_check_uv_map)
    
    button_freeze_transformations = QtWidgets.QPushButton("Freeze Transformations")
    right_layout.addWidget(button_freeze_transformations)
    button_freeze_transformations.clicked.connect(on_button_freeze_transformations)
    
    button_clear = QtWidgets.QPushButton("Clear")
    right_layout.addWidget(button_clear)
    button_clear.clicked.connect(on_button_clear)

    right_widget = QtWidgets.QWidget()
    right_widget.setLayout(right_layout)
    layout.addWidget(right_widget, stretch=1)

    dialog.setLayout(layout)
    dialog.show()

def on_button_delete_history():
    list_widget.clear()
    select_group = cmds.ls(selection=True, dag=True, long=True)
    if not select_group:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        cmds.delete(select_group,constructionHistory = True)
        
    cmds.select(d=True)
    label.setText('Delete history success')
        
def on_button_check_uvs():
    list_widget.clear()
    objects_with_uv = []
    objects_without_uv = []
    
    all = cmds.listRelatives(allDescendents=True, fullPath=True)
    if not all:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for obj in all:
            shape = cmds.listRelatives(obj, type='mesh', fullPath=True)
            if shape:
                try:
                    check_uv_count = int(cmds.polyEvaluate(shape, uv=True))
                except:
                    pass
                result = check_uv_count > 0
                if result:
                    objects_with_uv.append(obj)
                else:
                    objects_without_uv.append(obj)
                    cmds.select(cl=True)
                    
    cmds.select(objects_without_uv, add=True)

    display_results(objects_without_uv=objects_without_uv)
    label.setText("Objects without UVs: " + str(len(objects_without_uv)))

def on_button_check_overlapping():
    list_widget.clear()
    overLapping = []
    all = cmds.listRelatives(allDescendents=True, fullPath=True)
    if not all:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for obj in all:
            shape = cmds.listRelatives(obj, shapes=True, fullPath=True)
            toFace = cmds.polyListComponentConversion(shape, tf=True)
            overLap = cmds.polyUVOverlap(toFace, oc=True)
            if not overLap == None:
                overLapping.append(obj)
                cmds.select(cl=True)
                cmds.select(overLapping, add=True)

    display_results(overLapping=overLapping)
    label.setText("UV Overlapping: " + str(len(overLapping)))

def on_button_check_udim():
    list_widget.clear()
    udim_Crossing = []
    udimNegative = []
    select_group = cmds.ls(selection=True, dag=True ,long=True)
    if not select_group:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for list in select_group:
            obj = cmds.listRelatives(list, type='mesh', fullPath=True)
            #print(obj)
            if not obj == None:
                obj = obj[0]
                border_uv = cmds.polyEvaluate(obj,b2=True)
                #print(border_uv)
                x_min , x_max = border_uv[0]
                y_min , y_max = border_uv[1]
                #print(x_min,x_max,y_min,y_max)
                if x_min < 0 or y_min < 0:
                    udimNegative.append(obj)
                else:
                    uv_shell = {}
                    uv_components = cmds.ls(obj+'.f[*]', flatten=True)
                    for uv_compo in uv_components:
                        uv_coords = cmds.polyEvaluate(uv_compo, bc2=True)
                        udim_x_min , udim_x_max = uv_coords[0]
                        udim_y_min , udim_y_max = uv_coords[1]
                        udim_x_minInt = int(udim_x_min)
                        udim_x_maxInt = int(udim_x_max)
                        udim_y_minInt = int(udim_y_min)
                        udim_y_maxInt = int(udim_y_max)
                        if not (udim_x_minInt == udim_x_maxInt and udim_y_minInt == udim_y_maxInt):
                            if not obj in udim_Crossing:
                                udim_Crossing.append(obj)

    cmds.select(cl=True)                    
    cmds.select(udimNegative, add=True)
    cmds.select(udim_Crossing, add=True)

    display_results(udimNegative=udimNegative, udim_Crossing=udim_Crossing)
    label.setText("UV Over UDIM: " + str(len(udim_Crossing)) + " - " + "UV Error Negative Over UDIM: " + str(len(udimNegative)))
    
    
def on_button_check_flip():
    list_widget.clear()
    select_group = cmds.ls(selection=True, dag=True ,long=True)
    flippedUVList = []
    if not select_group:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for list in select_group:
            shapes = cmds.listRelatives(list, shapes=True, fullPath=True)
            if shapes:
                for shape in shapes:
                    faces = cmds.ls(cmds.polyListComponentConversion(shape + '.f[*]', tf=True), fl=True)
                    for face in faces:
                        uvs = []
                        vtxFaces = cmds.ls(cmds.polyListComponentConversion(face, toVertexFace=True), flatten=True)
                        for vtxFace in vtxFaces:
                            uv = cmds.polyListComponentConversion(vtxFace, fromVertexFace=True, toUV=True)
                            uvs.extend(uv)
                        if len(uvs) >= 3:
                            uvAPos = cmds.polyEditUV(uvs[0], query=True)
                            uvBPos = cmds.polyEditUV(uvs[1], query=True)
                            uvCPos = cmds.polyEditUV(uvs[2], query=True)
                            uvAB = om2.MVector([uvBPos[0] - uvAPos[0], uvBPos[1] - uvAPos[1]])
                            uvBC = om2.MVector([uvCPos[0] - uvBPos[0], uvCPos[1] - uvBPos[1]])
                            #print(uvs,uvAB, uvBC)
                            crose_vector = (uvAB ^ uvBC) * (om2.MVector([0, 0, 1]))
                            #print(crose_vector)
                            if crose_vector < 0:
                                flippedUVList.append(shape)
    cmds.select(cl=True)                    
    cmds.select(flippedUVList, add=True)
    
    flippedUVs = set(flippedUVList)
    
    display_results(flippedUVList=flippedUVs)
    label.setText("UV Flip: " + str(len(flippedUVList)))
    
def on_button_check_uv_map():
    list_widget.clear()
    all_objects = cmds.ls(sl=True, dag=True, long=True)
    uv_map = []
    if not all_objects:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for all_path in all_objects:
            obj = cmds.listRelatives(all_path, type="mesh", fullPath=True)
            if not obj == None:
                obj = obj[0]
                uv_sets = cmds.polyUVSet(obj, query=True, allUVSets=True)
                for uv_set in uv_sets:
                    if ' ' in uv_set:
                        uv_map.append(obj)

    cmds.select(uv_map, add=True)
    display_results(uv_map=uv_map)
    label.setText("UV Map have space : " + str(len(uv_map)))
    
def on_button_freeze_transformations():
    list_widget.clear()
    selection = cmds.ls(sl=True, dag=True, long=True)
    if not selection:
        cmds.confirmDialog(title='Error', message='You not select Group Object ', button=['OK'], defaultButton='OK')
    else:
        for select in selection:
            cmds.makeIdentity(select , apply=True)
    label.setText("Freeze transformations is success")

def on_button_clear():
    list_widget.clear()
    cmds.select(d=True)
    label.setText('Select Group Object')

def display_results(objects_without_uv=None, overLapping=None, udimNegative=None, udim_Crossing=None , flippedUVList=None, uv_map=None):
    list_widget.clear()
    red_color = QtGui.QColor(255, 0, 0)
    white_color = QtGui.QColor(255, 255, 255)

    if objects_without_uv!=None:
        for obj in objects_without_uv:
            obj_withOut_uv = QtWidgets.QListWidgetItem(obj)
            obj_withOut_uv.setForeground(white_color)
            list_widget.addItem(obj_withOut_uv)
    
    if overLapping!=None:
        for obj in overLapping:
            overlap = QtWidgets.QListWidgetItem(obj)
            overlap.setForeground(white_color)
            list_widget.addItem(overlap)
            
    if udimNegative!=None:
        for obj in udimNegative:
            error_message = "UV Error Negative Over UDIM : "+obj
            negative = QtWidgets.QListWidgetItem(error_message)
            negative.setForeground(red_color)
            list_widget.addItem(negative)

    if udim_Crossing!=None:
        for obj in udim_Crossing:
            udims_Crossing = QtWidgets.QListWidgetItem(obj)
            udims_Crossing.setForeground(white_color)
            list_widget.addItem(udims_Crossing)
            

    if flippedUVList!=None:
        for obj in flippedUVList:
            flip = QtWidgets.QListWidgetItem(obj)
            flip.setForeground(white_color)
            list_widget.addItem(flip)
    
    if uv_map!=None:
        for obj in uv_map:
            uv_maps = QtWidgets.QListWidgetItem(obj)
            uv_maps.setForeground(white_color)
            list_widget.addItem(uv_maps)

create_ui()