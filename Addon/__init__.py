import bpy
import random
from datetime import datetime
import numpy as np
import sys
import json
import base64
import math

bl_info = {
    "name": "Customized Tree Generator",
    "author": "Fabian Mieg <fabian.alexander.mieg@hs-furtwangen.de>, Felix Poenitzsch <felix.poenitzsch@hs-furtwangen.de>",
    "version": (1, 1),
    "blender": (3, 3, 1),
    "location": "View3D > Sidepanel > TreeGen",
    "description": "Create Awesome Trees",
    "category": "Mesh-Generation",
    "support": "TESTING",
}

PROPS = [
    ('max_height', bpy.props.FloatProperty(name='Max Height',default=4.0,min=1.0, max=100.0, soft_max=20.0, soft_min=4.0, step=0.1 ,precision=3, unit='LENGTH')),
    ('path_length', bpy.props.FloatProperty(name='Path Lenght', default=1.0,min=0.1, max=100.0, soft_max=2.0, soft_min=0.01, step=0.01 ,precision=3 , unit='LENGTH')),
    ('radius', bpy.props.FloatProperty(name='Stem Radius',default=0.5,min=0.1, max=2.0, step=0.01 ,precision=3, unit='LENGTH')),
    ('straightness', bpy.props.IntProperty(name='Straightness', subtype="PERCENTAGE",default = 60, min=50, max=90, step=1)),
    ('branch_chance', bpy.props.IntProperty(name='Branch Spread', subtype="PERCENTAGE",default = 10, min=1, max=100, step=1)),
    ('branch_change', bpy.props.FloatProperty(name='Branch Radius Change',default = 0.8, min=0, max=1, step=0.01)),
    ('max_distance_from_middle', bpy.props.FloatProperty(name='Max Distance From Middle', default = 5, min = 0.5, max = 10, step=0.5)),
    ('texture_quality', bpy.props.FloatProperty(name='Texture Quality', default=1.0,min=0.1, max=15.0, soft_max=15.0, soft_min=0.01, step=0.01 ,precision=3)),
    ('leaf_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Leaf Object')),
    ('bark_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Bark Object')),
    ('base_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Base Object')),
    ('leaf_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Leaf Material')),
    ('bark_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Bark Material')),
    ('primary_seed', bpy.props.StringProperty(name='Primary Seed', default = "0")),
    ('secondary_seed', bpy.props.StringProperty(name='Secondary Seed', default = "0")),
    ('tertiary_seed', bpy.props.StringProperty(name='Tertiary Seed', default = "0")),
    ('bool_detail_bark', bpy.props.BoolProperty(name='Enable Bark Detail')),
    ('bool_detail_leaf', bpy.props.BoolProperty(name='Enable Leaf Detail')),
    ('exchange_string',bpy.props.StringProperty(name='Exchange String', ))
]

class TestOperator(bpy.types.Operator):
    bl_idname = "object.testoperator"
    bl_label = "Simple Test Operator "

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        print("Start Testing")
        ResetSeed()
        s = bpy.context.scene
        if(s.base_object == None):
            s.base_object = make_empty("Generated Tree Base", bpy.context.scene.cursor.location,0)
        Generator.generateForm()
        Generator.generateStem(s.max_height,(s.max_height/s.path_length), s.path_length,s.radius ,0.2,s.branch_change,s.branch_chance,s.max_distance_from_middle,(0,0,0))
        Generator.mergePaths()
        Generator.generateLeavesBall()
        return {'FINISHED'}

class Generator():
    
    TreePartsList = []
    LeavesSpawnPosList = []
    Tree: bpy.types.Object = None
    Leaves: bpy.types.Object = None
    Form = None
    
    def generateForm ():
        bpy.ops.curve.primitive_nurbs_circle_add(radius=1, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        FormSpline = bpy.context.object.data.splines[0]
        FormLen = len(bpy.context.object.data.splines[0].points)
        i = 0
        while (i<FormLen):
            newX = 0
            newY = 0
            OldCo = FormSpline.points[i].co
            if (OldCo[0] < 0):
                newX = (0.5+GetRand(3))*-1
            if (OldCo[0] > 0):
                newX = 0.5+GetRand(3)
            if (OldCo[1] < 0):
                newY = (0.5+GetRand(3))*-1
            if (OldCo[1] > 0):
                newY = 0.5+GetRand(3)
            FormSpline.points[i].co = (newX,newY,0,1)
            i = i+1
        bpy.ops.object.editmode_toggle()
        Generator.Form = bpy.context.object


    def generateStem (height, segments, streightness, stemRadius, stemRadiusChangeFactor, BranchRadiusFactor, twigPercentage, maxStemOutbreak, StartingPoint):
        
        if (Generator.Tree != None):
            try:
                bpy.data.objects.remove(Generator.Tree, do_unlink=True)
            except:
                Generator.Tree = None

        if (Generator.Leaves != None):
            try:
                bpy.data.objects.remove(Generator.Leaves, do_unlink=True)
            except:
                Generator.Leaves = None

        TPLLength = len(Generator.TreePartsList)
        k = 0
        while (k<TPLLength):
            Generator.TreePartsList[k]
            k = k+1

        Generator.TreePartsList = []
        Generator.LeavesSpawnPosList = []
        
        #base
        bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=True, align='WORLD', location=StartingPoint, scale=(1, 1, 1))
        bpy.context.object.data.bevel_mode = 'OBJECT'
        bpy.context.object.data.bevel_object = Generator.Form
        bpy.ops.curve.select_all(action='TOGGLE')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 1), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":False, "use_snap_edit":False, "use_snap_nonedit":False, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.context.object.data.use_fill_caps = True
        bpy.context.object.data.splines[0].points[0].radius = stemRadius
        bpy.context.object.data.splines[0].points[1].radius = stemRadius
        
        #stem loop
        EndPoint = (StartingPoint[0],StartingPoint[1],StartingPoint[2]+1)
        actHeight = 1
        heightRangeMin = height/segments*0.9
        heightRangeMax = height/segments*1.1
        splinePoint = 2
        i = 0
        while i < segments:
            i += 1
            addHeight = heightRangeMin+GetRand(1)*(heightRangeMax-heightRangeMin)
            actHeight += addHeight
            def StemInRadius(radius):
                newX = (GetRand(1)*maxStemOutbreak*2-maxStemOutbreak)/2
                newY = (GetRand(1)*maxStemOutbreak*2-maxStemOutbreak)/2
                spline = bpy.context.object.data.splines[0]
                point = spline.points[splinePoint].co
                newPath = (newX, newY, addHeight)
                a2 = (point[0]+newX)*(point[0]+newX)
                b2 = (point[1]+newY)*(point[1]+newY)
                c2 = radius*radius
                if ((a2+b2)>c2):
                    return StemInRadius(radius)
                else:
                    return newPath
            newPath = StemInRadius(maxStemOutbreak)
            EndPoint = (EndPoint[0]+newPath[0],EndPoint[1]+newPath[1],EndPoint[2]+newPath[2])
            bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":newPath, "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":False, "use_snap_edit":False, "use_snap_nonedit":False, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            splinePoint += 1
            nextRadius = stemRadius*(1-(actHeight/height))
            bpy.context.object.data.splines[0].points[splinePoint].radius = nextRadius + ((1-nextRadius)*stemRadiusChangeFactor)
        bpy.context.object.data.splines[0].points[splinePoint].radius = 0
        branch = bpy.context.object.data.splines[0].points[splinePoint]
        actualPath = (branch.co[0] + StartingPoint[0],branch.co[1] + StartingPoint[1],branch.co[2] + StartingPoint[2])
        Generator.LeavesSpawnPosList.append((actualPath[0],actualPath[1],actualPath[2]))
        
        
        #cleanup
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.object.editmode_toggle()
        
        part = bpy.context.object
        Generator.TreePartsList.append(part)
        
        stem = bpy.context.active_object.data.splines[0]        
        stemLength = len(stem.points)
        j = 1
        while (j<stemLength-2):
            j = j+1
            if ((GetRand(1)*(10-j))<(0.4*10)):
                branchPoint = stem.points[j]
                branchStart = (StartingPoint[0] + branchPoint.co[0], StartingPoint[1] + branchPoint.co[1], StartingPoint[2] + branchPoint.co[2])
                branchRootPoint = stem.points[j-1]
                branchRoot = (StartingPoint[0] + branchRootPoint.co[0], StartingPoint[1] + branchRootPoint.co[1], StartingPoint[2] + branchRootPoint.co[2])
                RootToStart = ((branchStart[0] - branchRoot[0])*0.5,(branchStart[1] - branchRoot[1])*0.5,(branchStart[2] - branchRoot[2])*0.5)
                fixedRoot = (branchRoot[0] + RootToStart[0],branchRoot[1] + RootToStart[1],branchRoot[2] + RootToStart[2])
                Generator.generateBranch(height-j,segments-j,twigPercentage/10,branchRootPoint.radius*BranchRadiusFactor,stemRadiusChangeFactor, maxStemOutbreak, twigPercentage, 1, fixedRoot, RootToStart)
        TPLLength = len(Generator.TreePartsList)
        print (TPLLength)

    def generateBranch (height, segments, streightness, stemRadius, stemRadiusChangeFactor, maxStemOutbreak , twigPercentage, depth, branchRoot, StartingPoint):
        
        #base
        bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=True, align='WORLD', location=branchRoot, scale=(1, 1, 1))
        bpy.context.object.data.bevel_mode = 'OBJECT'
        bpy.context.object.data.bevel_object = Generator.Form
        bpy.ops.curve.select_all(action='TOGGLE')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":StartingPoint, "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":False, "use_snap_edit":False, "use_snap_nonedit":False, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.context.object.data.use_fill_caps = True
        
        #stem loop
        EndPoint = (StartingPoint[0],StartingPoint[1],StartingPoint[2]+1)
        actHeight = StartingPoint[2]
        heightRangeMin = height/segments*0.9
        heightRangeMax = height/segments*1.1
        splinePoint = 2
        i = 0
        while i < segments:
            newPath = (0,0,0)
            s = bpy.context.scene
            if (splinePoint>2):
                def BranchInDirection(diversion):
                    newX = GetRand(1)*streightness*2-streightness
                    newY = GetRand(1)*streightness*2-streightness
                    addHeight = heightRangeMin+GetRand(1)*(heightRangeMax-heightRangeMin)
                    newVector = (newX, newY, addHeight)
                    spline = bpy.context.object.data.splines[0]
                    point = spline.points[splinePoint].co
                    prevPoint = spline.points[splinePoint-1].co
                    prevVector = (point[0]-prevPoint[0],point[1]-prevPoint[1],point[2]-prevPoint[2])
                    scalar = prevVector[0]*newVector[0]+prevVector[1]*newVector[1]+prevVector[2]*newVector[2]
                    ALen = math.sqrt(prevVector[0]*prevVector[0]+prevVector[1]*prevVector[1]+prevVector[2]*prevVector[2])
                    BLen = math.sqrt(newVector[0]*newVector[0]+newVector[1]*newVector[1]+newVector[2]*newVector[2])
                    cosy = scalar/(ALen*BLen)
                    print(cosy)
                    if (cosy<diversion):
                        return BranchInDirection(diversion)
                    else:
                        return newVector
                newPath = BranchInDirection(s.straightness/100)
                actHeight += newPath[2]
            else:
                addHeight = heightRangeMin+GetRand(1)*(heightRangeMax-heightRangeMin)
                actHeight += addHeight
                newX = GetRand(1)*streightness*2-streightness
                newY = GetRand(1)*streightness*2-streightness
                newPath = (newX, newY, addHeight)
            EndPoint = (EndPoint[0]+newPath[0],EndPoint[1]+newPath[1],EndPoint[2]+newPath[2])
            bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":newPath, "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":False, "use_snap_edit":False, "use_snap_nonedit":False, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            splinePoint += 1
            nextRadius = stemRadius*(segments-i-1)/segments*0.8
            bpy.context.object.data.splines[0].points[splinePoint].radius = nextRadius + ((1-nextRadius)*stemRadiusChangeFactor)
            i += 1
        bpy.context.object.data.splines[0].points[splinePoint].radius = 0
        branch = bpy.context.object.data.splines[0].points[splinePoint]
        actualPath = (branch.co[0] + branchRoot[0],branch.co[1] + branchRoot[1],branch.co[2] + branchRoot[2])
        Generator.LeavesSpawnPosList.append((actualPath[0],actualPath[1],actualPath[2]))
        
        
        #cleanup
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.object.editmode_toggle()

        part = bpy.context.object
        bpy.context.object.data.splines[0].points[0].radius = 0
        Generator.TreePartsList.append(part)

        if (depth > 0):
            stem = bpy.context.active_object.data.splines[0]
            stemLength = len(stem.points)
            j = 1
            while (j<stemLength-2):
                j = j+1
                if ((GetRand(1)*(segments-j))<(0.4*segments)):
                    branchPoint = stem.points[j]
                    branchStart = (branchPoint.co[0], branchPoint.co[1], branchPoint.co[2])
                    branchRootPoint = stem.points[j-1]
                    branchRootStart = (branchRootPoint.co[0], branchRootPoint.co[1], branchRootPoint.co[2])
                    newBranchRoot = (branchRoot[0] + branchRootStart[0],branchRoot[1] + branchRootStart[1],branchRoot[2] + branchRootStart[2])
                    newBranchStart = (branchRoot[0] + branchStart[0],branchRoot[1] + branchStart[1],branchRoot[2] + branchStart[2])
                    RootToStart = ((newBranchStart[0] - newBranchRoot[0])*0.5,(newBranchStart[1] - newBranchRoot[1])*0.5,(newBranchStart[2] - newBranchRoot[2])*0.5)
                    fixedRoot = (newBranchRoot[0] + RootToStart[0],newBranchRoot[1] + RootToStart[1],newBranchRoot[2] + RootToStart[2])
                    Generator.generateBranch(height*(1-j/stemLength)*0.5,segments,streightness/2,branchPoint.radius,stemRadiusChangeFactor*0.3, maxStemOutbreak, twigPercentage, depth-1, fixedRoot, RootToStart)

    def mergePaths ():
        TPLLength = len(Generator.TreePartsList)
        print (TPLLength)
        k = 0
        while (k<TPLLength):
            print(Generator.TreePartsList[k])
            Generator.TreePartsList[k].select_set(True)
            print(Generator.LeavesSpawnPosList[k])
            k = k+1
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.join()
        Generator.Tree = bpy.context.object
        Generator.Tree.parent = bpy.context.scene.base_object
        bpy.context.scene.bark_object = bpy.context.object
        bpy.context.object.name = "Generated Tree"
        bpy.data.objects.remove(Generator.Form)

    def generateLeavesBall ():
        leavesLen = len(Generator.LeavesSpawnPosList)
        leaves = []
        i = 0
        while (i<leavesLen):
            x = 1.5+GetRand(1)*0.5
            y = 1.5+GetRand(1)*0.5
            z = 0.8+GetRand(1)*0.4
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=Generator.LeavesSpawnPosList[i], scale=(x, y, z))
            leaves.append(bpy.context.object)
            i = i+1
        leavesLen = len(leaves)
        i = 0
        while (i<leavesLen):
            leaves[i].select_set(True)
            i = i+1
        bpy.ops.object.booltool_auto_union()
        Generator.Leaves = bpy.context.active_object
        Generator.Leaves.parent = bpy.context.scene.base_object
        bpy.context.scene.leaf_object = bpy.context.object
        bpy.context.object.name = "Generated Leaves"

class GenExchangeString(bpy.types.Operator):
    bl_idname = "object.genexchangestring"
    bl_label = "Generates Exchange String"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        exchangeJson = {
            "max_height": bpy.context.scene.max_height,
            "path_length": bpy.context.scene.path_length,
            "branch_chance": bpy.context.scene.branch_chance,
            "branch_change": bpy.context.scene.branch_change,
            "straightness": bpy.context.scene.straightness,
            "radius": bpy.context.scene.radius,
            "max_distance_from_middle": bpy.context.scene.max_distance_from_middle,
            "primary_seed": bpy.context.scene.primary_seed,
            "secondary_seed": bpy.context.scene.secondary_seed,
            "tertiary_seed": bpy.context.scene.secondary_seed,
            "bool_detail_bark": bpy.context.scene.bool_detail_bark,
            "bool_detail_leaf": bpy.context.scene.bool_detail_leaf,
            "texture_quality": bpy.context.scene.texture_quality,
        }
        jsonstring = json.dumps(exchangeJson)
        b64_exchange_string = base64.b64encode(jsonstring.encode('utf-8'))
        bpy.context.scene.exchange_string = b64_exchange_string.decode('utf-8')
        print(b64_exchange_string)
        return {'FINISHED'}

class UseExchangeString(bpy.types.Operator):
    bl_idname = "object.useexchangestring"
    bl_label = "Use Exchange String"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        print("Start Testing")

        b64_exchange_string = bpy.context.scene.exchange_string
        jsonString = base64.b64decode(b64_exchange_string).decode('utf-8')
        exchangeJson = json.loads(jsonString)
        bpy.context.scene.max_height = exchangeJson["max_height"]
        bpy.context.scene.path_length = exchangeJson["path_length"]
        bpy.context.scene.branch_chance = exchangeJson["branch_chance"]
        bpy.context.scene.branch_change = exchangeJson["branch_change"]
        bpy.context.scene.straightness = exchangeJson["straightness"]
        bpy.context.scene.radius = exchangeJson["radius"]
        bpy.context.scene.max_distance_from_middle = exchangeJson["max_distance_from_middle"]
        bpy.context.scene.primary_seed = exchangeJson["primary_seed"]
        bpy.context.scene.secondary_seed = exchangeJson["secondary_seed"]
        bpy.context.scene.tertiary_seed = exchangeJson["tertiary_seed"]
        bpy.context.scene.bool_detail_bark = exchangeJson["bool_detail_bark"]
        bpy.context.scene.bool_detail_leaf = exchangeJson["bool_detail_leaf"]
        bpy.context.scene.texture_quality = exchangeJson["texture_quality"]
        
        return {'FINISHED'}

class GenNewBark(bpy.types.Operator):
    bl_idname = "object.gennewbark"
    bl_label = "Genenate Bark Material"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        if(bpy.data.materials.find("bark_material") != -1):
            bpy.data.materials.remove(bpy.data.materials["bark_material"])
        material =bpy.data.materials.new(name="bark_material")
        bpy.context.scene.bark_mat = material
        material.use_nodes = True

    # Node Creation
        material_output: bpy.types.ShaderNodeOutputMaterial = material.node_tree.nodes.get('Material Output')
        material_shader: bpy.types.ShaderNodeBsdfPrincipled = material.node_tree.nodes.get('Principled BSDF')
        texture_coor: bpy.types.ShaderNodeTexCoord = material.node_tree.nodes.new("ShaderNodeTexCoord")
        noise_tex_1: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        noise_tex_2: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        noise_tex_3: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        noise_tex_4: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        color_ramp_1: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp_2: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp_3: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp_4: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        bump_1: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        bump_2: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        bump_3: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        linear_light: bpy.types.ShaderNodeMixRGB = material.node_tree.nodes.new("ShaderNodeMixRGB")
        mix_rgb: bpy.types.ShaderNodeMixRGB = material.node_tree.nodes.new("ShaderNodeMixRGB")
        mapping: bpy.types.ShaderNodeMapping = material.node_tree.nodes.new("ShaderNodeMapping")
        voronoi_tex: bpy.types.ShaderNodeTexVoronoi = material.node_tree.nodes.new("ShaderNodeTexVoronoi")
        displacement: bpy.types.ShaderNodeDisplacement = material.node_tree.nodes.new("ShaderNodeDisplacement")
       
    # Node Position
        material_output.location = (2600,1000)
        material_shader.location = (2300,800)
        texture_coor.location = (0,1000)
        noise_tex_1.location = (400,1000)
        noise_tex_2.location = (400,500)
        noise_tex_3.location = (900,500)
        noise_tex_4.location = (400,0)
        color_ramp_1.location = (600,1000)
        color_ramp_2.location = (600,500)
        color_ramp_3.location = (1700,500)
        color_ramp_4.location = (1700,200)
        bump_1.location = (1700,-100)
        bump_2.location = (1900,-100)
        bump_3.location = (2100,-100)
        linear_light.location = (1100,500)
        mix_rgb.location = (2000,800)
        mapping.location = (1300,500)
        voronoi_tex.location = (1500,500)
        displacement.location = (1700,1000)

    # Node Settings
        # Noise-Texture
        noise_tex_1.inputs["Scale"].default_value = 1 + GetRand(1)*2
        noise_tex_1.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_1.inputs["Roughness"].default_value = 0.65
        noise_tex_1.inputs["Distortion"].default_value = 0.3
        
        noise_tex_2.inputs["Scale"].default_value = 2 + GetRand(1)*2
        noise_tex_2.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_2.inputs["Roughness"].default_value = 0.5
        noise_tex_2.inputs["Distortion"].default_value = 0.0

        noise_tex_3.inputs["Scale"].default_value = 7 + GetRand(1)*2
        noise_tex_3.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_3.inputs["Distortion"].default_value = 0.0

        noise_tex_4.inputs["Scale"].default_value = 3 + GetRand(1)*2
        noise_tex_4.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_4.inputs["Roughness"].default_value = 0.60
        noise_tex_4.inputs["Distortion"].default_value = 0.0
        
        # Voronoi-Texture
        voronoi_tex.inputs["Scale"].default_value = 8.0
        voronoi_tex.inputs["Randomness"].default_value = 1.0

        # Color-Ramp
        color_ramp_1.color_ramp.elements[0].position = 0.53
        color_ramp_1.color_ramp.elements[0].color = (0,0,0,1)
        color_ramp_1.color_ramp.elements[1].position = 0.71
        color_ramp_1.color_ramp.elements[1].color = (1,1,1,1)

        color_ramp_2.color_ramp.elements[0].position = 0.373
        color_ramp_2.color_ramp.elements[0].color = (0.44,0.44,0.44,1)
        color_ramp_2.color_ramp.elements[1].position = 0.627
        color_ramp_2.color_ramp.elements[1].color = (0.617,0.617,0.617,1)

        color_ramp_3.color_ramp.elements[0].position = 0.0
        color_ramp_3.color_ramp.elements[0].color = (0.305,0.184,0.1,1)
        color_ramp_3.color_ramp.elements[1].position = 0.264
        color_ramp_3.color_ramp.elements[1].color = (0.1,0.05,0.022,1)
        color_ramp_3.color_ramp.elements.new(2)
        color_ramp_3.color_ramp.elements[2].position = 0.891
        color_ramp_3.color_ramp.elements[2].color = (0.004,0.003,0.002,1)

        color_ramp_4.color_ramp.elements[0].position = 0.0
        color_ramp_4.color_ramp.elements[0].color = (0.451,0.451,0.451,1)
        color_ramp_4.color_ramp.elements[1].position = 0.0
        color_ramp_4.color_ramp.elements[1].color = (0.847,0.847,0.847,1)

        # Bump
        bump_1.inputs["Strength"].default_value = 0.35
        bump_2.inputs["Strength"].default_value = 0.4
        bump_3.inputs["Strength"].default_value = 1.0

        # Mapping
        mapping.inputs["Scale"].default_value[2] = 0.3
        mapping.inputs["Location"].default_value[0] = 5*GetRand(2)
        mapping.inputs["Location"].default_value[1] = 5*GetRand(2)
        mapping.inputs["Location"].default_value[2] = 5*GetRand(2)

        #Rest  (Mapping, Displacement, MixRGB, Linear-Light)
        linear_light.blend_type = "LINEAR_LIGHT"
        linear_light.inputs["Fac"].default_value = 0.08
        mix_rgb.inputs["Color2"].default_value = (0.0561284, 0.14996, 0.0241577, 1)
        displacement.inputs["Scale"].default_value = 0.140
        material_shader.inputs["Specular"].default_value = 0.5


    # Node Linking
        # Texture Coordinate
        material.node_tree.links.new(noise_tex_1.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(noise_tex_2.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(noise_tex_3.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(noise_tex_4.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(linear_light.inputs[1], texture_coor.outputs[3])
            
        # Noise Texture
        material.node_tree.links.new(color_ramp_1.inputs[0], noise_tex_1.outputs[1])
        material.node_tree.links.new(color_ramp_2.inputs[0], noise_tex_2.outputs[1])
        material.node_tree.links.new(linear_light.inputs[2], noise_tex_3.outputs[1])
        material.node_tree.links.new(bump_2.inputs[2], noise_tex_4.outputs[0])
            
        # Voronoi texture
        material.node_tree.links.new(color_ramp_3.inputs[0], voronoi_tex.outputs[0])
        material.node_tree.links.new(color_ramp_4.inputs[0], voronoi_tex.outputs[0])
        material.node_tree.links.new(displacement.inputs[0], voronoi_tex.outputs[0])
        material.node_tree.links.new(bump_1.inputs[2], voronoi_tex.outputs[0])

        # Color Ramp
        material.node_tree.links.new(mix_rgb.inputs[0], color_ramp_1.outputs[0])
        material.node_tree.links.new(bump_3.inputs[2], color_ramp_1.outputs[0])
        material.node_tree.links.new(noise_tex_3.inputs[4], color_ramp_2.outputs[0])  
        material.node_tree.links.new(mix_rgb.inputs[1], color_ramp_3.outputs[0])
        material.node_tree.links.new(material_shader.inputs[9], color_ramp_4.outputs[0])

        # Bump
        material.node_tree.links.new(bump_2.inputs[3], bump_1.outputs[0])
        material.node_tree.links.new(bump_3.inputs[3], bump_2.outputs[0])
        if(bpy.context.scene.bool_detail_bark):
            material.node_tree.links.new(material_shader.inputs[22], bump_3.outputs[0])
        

        # MixRGB+Linear-Light
        material.node_tree.links.new(material_shader.inputs[0], mix_rgb.outputs[0])
        material.node_tree.links.new(mapping.inputs[0], linear_light.outputs[0])

        # Rest (Mapping, Shader, Displacement)
        material.node_tree.links.new(voronoi_tex.inputs[0], mapping.outputs[0])       
        material.node_tree.links.new(material_output.inputs[0], material_shader.outputs[0])
        if(bpy.context.scene.bool_detail_bark):
            material.node_tree.links.new(material_output.inputs[2], displacement.outputs[0])

        return {'FINISHED'}

class GenNewLeaf(bpy.types.Operator):
    bl_idname = "object.gennewleaf"
    bl_label = "Genenate Leaf Material"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        if(bpy.data.materials.find("leaf_material") != -1):
            bpy.data.materials.remove(bpy.data.materials["leaf_material"])
        material = bpy.data.materials.new(name="leaf_material")
        bpy.context.scene.leaf_mat = material
        material.use_nodes = True

    # Node Creation
        material_output: bpy.types.ShaderNodeOutputMaterial = material.node_tree.nodes.get('Material Output')
        material_shader: bpy.types.ShaderNodeBsdfPrincipled = material.node_tree.nodes.get('Principled BSDF')
        texture_coor: bpy.types.ShaderNodeTexCoord = material.node_tree.nodes.new("ShaderNodeTexCoord")
        noise_tex_1: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        noise_tex_2: bpy.types.ShaderNodeTexNoise = material.node_tree.nodes.new("ShaderNodeTexNoise")
        color_ramp_1: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        color_ramp_2: bpy.types.ShaderNodeValToRGB = material.node_tree.nodes.new("ShaderNodeValToRGB")
        bump_1: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        bump_2: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        bump_3: bpy.types.ShaderNodeBump = material.node_tree.nodes.new("ShaderNodeBump")
        linear_light: bpy.types.ShaderNodeMixRGB = material.node_tree.nodes.new("ShaderNodeMixRGB")
        mapping: bpy.types.ShaderNodeMapping = material.node_tree.nodes.new("ShaderNodeMapping")
        voronoi_tex: bpy.types.ShaderNodeTexVoronoi = material.node_tree.nodes.new("ShaderNodeTexVoronoi")
        displacement: bpy.types.ShaderNodeDisplacement = material.node_tree.nodes.new("ShaderNodeDisplacement")
        
    # Node Position
        material_output.location = (2600,1000)
        material_shader.location = (2300,800)
        texture_coor.location = (0,1000)
        noise_tex_1.location = (900,500)
        noise_tex_2.location = (400,0)
        color_ramp_1.location = (1700,500)
        color_ramp_2.location = (1700,200)
        bump_1.location = (1700,-100)
        bump_2.location = (1900,-100)
        bump_3.location = (2100,-100)
        linear_light.location = (1100,500)
        mapping.location = (1300,500)
        voronoi_tex.location = (1500,500)
        displacement.location = (1700,1000)

    # Node Settings
        # Noise-Texture
        noise_tex_1.inputs["Scale"].default_value = 5.0
        noise_tex_1.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_1.inputs["Roughness"].default_value = 0.4
        noise_tex_1.inputs["Distortion"].default_value = 0.3
        
        noise_tex_2.inputs["Scale"].default_value = 3.0
        noise_tex_2.inputs["Detail"].default_value = bpy.context.scene.texture_quality/5
        noise_tex_2.inputs["Roughness"].default_value = 0.5
        noise_tex_2.inputs["Distortion"].default_value = 0.0

        # Voronoi-Texture
        voronoi_tex.inputs["Scale"].default_value = 1.5
        voronoi_tex.inputs["Randomness"].default_value = 1.0

        # Color-Ramp
        color_ramp_1.color_ramp.elements[0].position = 0.495
        color_ramp_1.color_ramp.elements[0].color = (0.021,0.037,0.009,1)
        color_ramp_1.color_ramp.elements[1].position = 0.955
        color_ramp_1.color_ramp.elements[1].color = (0.117,0.150,0.040,1)

        color_ramp_2.color_ramp.elements[0].position = 0.0
        color_ramp_2.color_ramp.elements[0].color = (0.451,0.451,0.451,1)
        color_ramp_2.color_ramp.elements[1].position = 0.0
        color_ramp_2.color_ramp.elements[1].color = (0.847,0.847,0.847,1)

        # Bump
        bump_1.inputs["Strength"].default_value = 0.35
        bump_2.inputs["Strength"].default_value = 0.5
        bump_3.inputs["Strength"].default_value = 1.0


        # Mapping
        mapping.inputs["Scale"].default_value[2] = 0.5
        mapping.inputs["Location"].default_value[0] = 5*GetRand(2)
        mapping.inputs["Location"].default_value[1] = 5*GetRand(2)
        mapping.inputs["Location"].default_value[2] = 5*GetRand(2)

        #Rest  (Mapping, Displacement, MixRGB, Linear-Light)
        linear_light.blend_type = "LINEAR_LIGHT"
        linear_light.inputs["Fac"].default_value = 0.4
        displacement.inputs["Scale"].default_value = 0.140
        material_shader.inputs["Specular"].default_value = 0.0

    # Node Linking
        # Texture Coordinate
        material.node_tree.links.new(noise_tex_1.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(noise_tex_2.inputs[0], texture_coor.outputs[3])
        material.node_tree.links.new(linear_light.inputs[1], texture_coor.outputs[3])
            
        # Noise Texture
        material.node_tree.links.new(linear_light.inputs[2], noise_tex_1.outputs[1])
        material.node_tree.links.new(bump_2.inputs[2], noise_tex_2.outputs[0])
            
        # Voronoi texture
        material.node_tree.links.new(color_ramp_1.inputs[0], voronoi_tex.outputs[1])
        material.node_tree.links.new(color_ramp_2.inputs[0], voronoi_tex.outputs[0])
        material.node_tree.links.new(displacement.inputs[0], voronoi_tex.outputs[0])
        material.node_tree.links.new(bump_1.inputs[2], voronoi_tex.outputs[0])
        material.node_tree.links.new(bump_3.inputs[2], voronoi_tex.outputs[1])

        # Color Ramp
        material.node_tree.links.new(material_shader.inputs[0], color_ramp_1.outputs[0])
        material.node_tree.links.new(material_shader.inputs[9], color_ramp_2.outputs[0])

        # Bump
        material.node_tree.links.new(bump_2.inputs[3], bump_1.outputs[0])
        material.node_tree.links.new(bump_3.inputs[3], bump_2.outputs[0])
        if(bpy.context.scene.bool_detail_leaf):
            material.node_tree.links.new(material_shader.inputs[22], bump_3.outputs[0])
        

        # MixRGB+Linear-Light
        material.node_tree.links.new(mapping.inputs[0], linear_light.outputs[0])

        # Rest (Mapping, Shader, Displacement)
        material.node_tree.links.new(voronoi_tex.inputs[0], mapping.outputs[0])       
        material.node_tree.links.new(material_output.inputs[0], material_shader.outputs[0])
        if(bpy.context.scene.bool_detail_leaf):
            material.node_tree.links.new(material_output.inputs[2], displacement.outputs[0])

        return {'FINISHED'}


class PrimarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.primaryseedgen"
    bl_label = "Generate Priamry Seed"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        random.seed(datetime.now().timestamp())
        bpy.context.scene.primary_seed = str(random.randint(0,sys.maxsize))
        return {'FINISHED'}

class SecondarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.secondaryseedgen"
    bl_label = "Generate Secondary Seed"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        random.seed(datetime.now().timestamp())
        bpy.context.scene.secondary_seed = str(random.randint(0,sys.maxsize))
        return {'FINISHED'}

class TertiarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.tertiaryseedgen"
    bl_label = "Generate Tertiary Seed"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        random.seed(datetime.now().timestamp())
        bpy.context.scene.tertiary_seed = str(random.randint(0,sys.maxsize))
        return {'FINISHED'}


def make_empty(name, location, coll_name): #string, vector, string of existing coll
    empty_obj = bpy.data.objects.new( "empty", None, )
    empty_obj.name = name
    empty_obj.empty_display_size = 1 
    bpy.data.collections[coll_name].objects.link(empty_obj)
    empty_obj.location = location
    return empty_obj


random1: np.random.RandomState = np.random.RandomState(1)
random2: np.random.RandomState = np.random.RandomState(1)
random3: np.random.RandomState = np.random.RandomState(1)

def GetRand(seedtype: int): 
    if(seedtype == 1):
        return random1.random()
    if(seedtype == 2):
        return random2.random()
    if(seedtype == 3):
        return random3.random()
    
def StringSeedToNumber(_str: str):
    num: int = 0
    for i in range(len(_str)):
        num += ord(_str[i])       
    return num

def ResetSeed():
    currSeed = StringSeedToNumber(bpy.context.scene.primary_seed)
    global random1
    random1 = np.random.RandomState(currSeed)
    currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
    global random2
    random2 = np.random.RandomState(currSeed)
    currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
    global random3
    random3 = np.random.RandomState(currSeed)


old_primary_seed: str = ""
old_secondary_seed: str = ""
old_tertiary_seed: str = ""

def mainfunc():
    leaf_obj: bpy.types.Object = bpy.context.scene.leaf_object
    leaf_mat: bpy.types.Material = bpy.context.scene.leaf_mat
    global old_primary_seed
    global random1
    global old_secondary_seed
    global random2
    global old_tertiary_seed
    global random3
    materialChanged = False
    barkChanged = False
    if leaf_obj is not None and leaf_mat is not None:
        if leaf_obj.data.materials:
            if(leaf_obj.data.materials[0] != leaf_mat):
                leaf_obj.data.materials[0] = leaf_mat
                materialChanged = True
                print("Leaf changed")
        else:
            leaf_obj.data.materials.append(leaf_mat)
            materialChanged = True
            print("Leaf changed")
    
    bark_obj: bpy.types.Object = bpy.context.scene.bark_object
    bark_mat: bpy.types.Material = bpy.context.scene.bark_mat
    
    if bark_obj is not None and bark_mat is not None:
        if bark_obj.data.materials:
            if(bark_obj.data.materials[0] != bark_mat):
                bark_obj.data.materials[0] = bark_mat
                materialChanged = True
                print("Bark changed")
        else:
            bark_obj.data.materials.append(bark_mat)
            materialChanged = True
            print("Bark changed")
   

    if(old_primary_seed != bpy.context.scene.primary_seed):
        old_primary_seed = bpy.context.scene.primary_seed
        currSeed = StringSeedToNumber(bpy.context.scene.primary_seed)
        random1 = np.random.RandomState(currSeed)
        print("Primary Seed Changed")

    if(old_secondary_seed != bpy.context.scene.secondary_seed):
        old_secondary_seed = bpy.context.scene.secondary_seed
        currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
        random2 = np.random.RandomState(currSeed)
        print("Secondary Seed Changed")

    if(old_tertiary_seed != bpy.context.scene.tertiary_seed):
        old_tertiary_seed = bpy.context.scene.tertiary_seed
        currSeed = StringSeedToNumber(bpy.context.scene.tertiary_seed)
        random3 = np.random.RandomState(currSeed)
        print("Tertiary Seed Changed")


    if(materialChanged):
        currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
        random2 = np.random.RandomState(currSeed)

    if(barkChanged):
        currSeed = StringSeedToNumber(bpy.context.scene.primary_seed)
        random1 = np.random.RandomState(currSeed)

class TreeGenPanel(bpy.types.Panel):
    bl_label = "Tree Generator"
    bl_idname = "VIEW3D_Tree_Gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TreeGen"

    def draw(self, context):
        layout = self.layout

        mainfunc()
        row = layout.row()
        row.label(text="Tree Properties")
        row = layout.row()
        row.prop(context.scene, "max_height", slider=True)
        row = layout.row()
        row.prop(context.scene, "path_length", slider=True)
        row = layout.row()
        row.prop(context.scene, "radius", slider=True)
        row = layout.row()
        row.prop(context.scene, "straightness", slider=True)
        row = layout.row()
        row.prop(context.scene, "branch_chance", slider=True)
        row = layout.row()
        row.prop(context.scene, "branch_change", slider=True)
        row = layout.row()
        row.prop(context.scene, "max_distance_from_middle", slider=True)
        row = layout.row()
        row.prop(context.scene, "texture_quality", slider=True)

        layout.separator()
        row = layout.row()
        row.label(text="Bark Generation:")
        row = layout.row()
        row.prop(context.scene, "bark_object")
        row = layout.row()
        row.prop(context.scene, "bark_mat")
        row = layout.row()
        row.prop(context.scene, "bool_detail_bark")
        row = layout.row()
        row.operator("object.gennewbark")

        layout.separator()
        row = layout.row()
        row.label(text="Leaf Generation:")
        row = layout.row()
        row.prop(context.scene, "leaf_object")
        row = layout.row()
        row.prop(context.scene, "leaf_mat")
        row = layout.row()
        row.prop(context.scene, "bool_detail_leaf")
        row = layout.row()
        row.operator("object.gennewleaf")

        layout.separator()
        row = layout.row()
        row.label(text="Seed Generation:")
        row = layout.row()
        row.prop(context.scene, "primary_seed")
        row = layout.row()
        row.operator("object.primaryseedgen")
        row = layout.row()
        row.prop(context.scene, "secondary_seed")
        row = layout.row()
        row.operator("object.secondaryseedgen")
        row = layout.row()
        row.prop(context.scene, "tertiary_seed")
        row = layout.row()
        row.operator("object.tertiaryseedgen")


        layout.separator()
        row = layout.row()
        row.label(text="Generation Option:")
        row = layout.row()
        row.prop(context.scene, "base_object")
        row = layout.row()
        row.operator("object.testoperator", text="Generate Tree")

        layout.separator()
        row = layout.row()
        row.label(text="Exchange Strings:")
        row = layout.row()
        row.prop(context.scene, "exchange_string")
        row = layout.row()
        row.operator("object.genexchangestring", text="Generate Exchange string")
        row = layout.row()
        row.operator("object.useexchangestring", text="Use Exchange String")

def register():
    bpy.utils.register_class(TestOperator)
    bpy.utils.register_class(GenExchangeString)
    bpy.utils.register_class(UseExchangeString)
    bpy.utils.register_class(GenNewBark)
    bpy.utils.register_class(GenNewLeaf)
    bpy.utils.register_class(PrimarySeedGenOperator)
    bpy.utils.register_class(SecondarySeedGenOperator)
    bpy.utils.register_class(TertiarySeedGenOperator)
    bpy.utils.register_class(TreeGenPanel)
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

def unregister():
    bpy.utils.unregister_class(TestOperator)
    bpy.utils.unregister_class(GenExchangeString)
    bpy.utils.unregister_class(UseExchangeString)
    bpy.utils.unregister_class(GenNewBark)
    bpy.utils.unregister_class(GenNewLeaf)
    bpy.utils.unregister_class(PrimarySeedGenOperator)
    bpy.utils.unregister_class(SecondarySeedGenOperator)
    bpy.utils.unregister_class(TertiarySeedGenOperator)
    bpy.utils.unregister_class(TreeGenPanel)
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

if __name__ == "__main__":
    register()

