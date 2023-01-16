import bpy
import random
from datetime import datetime
import numpy as np
import sys

bl_info = {
    "name": "Fantasy Tree Generator",
    "author": "Wir <wir@hs-furtwangen.de>",
    "version": (1, 1),
    "blender": (3, 3, 1),
    "location": "View3D > Sidepanel > TreeGen",
    "description": "Create Awesome Trees",
    "category": "Mesh-Generation",
    "support": "TESTING",
}



PROPS = [
    ('max_height', bpy.props.FloatProperty(name='Max Height',default=4.0,min=1.0, max=100.0, soft_max=20.0, soft_min=4.0, step=0.1 ,precision=3, unit='LENGTH')),
    ('path_lenght', bpy.props.FloatProperty(name='Path Lenght', default=1.0,min=0.1, max=100.0, soft_max=2.0, soft_min=0.01, step=0.01 ,precision=3 , unit='LENGTH')),
    ('branch_chance', bpy.props.IntProperty(name='Branch Chance', subtype="PERCENTAGE",default = 10, min=0, max=100, step=1)),
    ('max_distance_from_middle', bpy.props.IntProperty(name='Max Distance From Middle', default = 10, min = 1, max = 100, step=1)),
    ('straightness', bpy.props.IntProperty(name='Straigness', subtype="PERCENTAGE",default = 10, min=0, max=100, step=1)),
    ('leaf_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Leaf Object')),
    ('base_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Base Object')),
    ('leaf_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Leaf Material')),
    ('bark_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Bark Material')),
    ('primary_seed', bpy.props.StringProperty(name='Primary Seed', default = "0")),
    ('secondary_seed', bpy.props.StringProperty(name='Secondary Seed', default = "0")),
    ('material_list', bpy.props.PointerProperty(type=bpy.types.Material,name='Material')),
]

class TestOperator(bpy.types.Operator):
    bl_idname = "object.testoperator"
    bl_label = "Simple Test Operator "

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        print(np.random.RandomState(1).random())
        print(GetRand(1))
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
        bpy.data.materials.new(name="bark_material")
        bpy.context.scene.bark_mat = bpy.data.materials["bark_material"]
        return {'FINISHED'}

class GenNewLeaf(bpy.types.Operator):
    bl_idname = "object.gennewleaf"
    bl_label = "Genenate Leaf Material"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
# TODO: Generate the Bark and select it
        if(bpy.data.materials.find("leaf_material") != -1):
            bpy.data.materials.remove(bpy.data.materials["leaf_material"])
        bpy.data.materials.new(name="leaf_material")
        bpy.context.scene.leaf_mat = bpy.data.materials["leaf_material"]

        return {'FINISHED'}

class PrimarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.primaryseedgen"
    bl_label = "Generate Priamry Seed"

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

# TODO: Add Generating Logic
    def execute(self, context):
        random.seed(datetime.now().timestamp())
        bpy.context.scene.primary_seed = str(random.randint(0,sys.maxsize))
        return {'FINISHED'}

class SecondarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.secondaryseedgen"
    bl_label = "Generate Secondary Seed"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

# TODO: Add Generating Logic
    def execute(self, context):
        random.seed(datetime.now().timestamp())
        bpy.context.scene.secondary_seed = str(random.randint(0,sys.maxsize))
        return {'FINISHED'}


def leafNodeLogic():
    current_mat:bpy.types.Material =  bpy.data.materials["leaf_material"]
    

def barkNodeLogic():
    current_mat:bpy.types.Material =  bpy.data.materials["bark_material"]
    


# 
# class LeafMaterialOperator(bpy.types.Operator):
#     bl_idname = "object.leafmaterialoperator"
#     bl_label = "Generate Leaf Material"

#     @classmethod
#     def poll(cls, context): # was notwending sit für di aktivierung
#         return True# context.active_object is not None


#     def execute(self, context):
#         return {'FINISHED'}

#     def draw(self, context):
#         layout = self.layout
#         layout.prop(context.scene, "max_height", slider=True)
#         layout.prop_search(self, "material_name", bpy.data, "materials")
# 

random1: np.random.RandomState = np.random.RandomState(1)
random2: np.random.RandomState = np.random.RandomState(1)

def GetRand(seedtype: int): 
    if(seedtype == 1):
        return random1.random()
    if(seedtype == 2):
        return random2.random()
    
def StringSeedToNumber(_str: str):
    num: int = 0

    for i in range(len(_str)):
        num += ord(_str[i])       

    return num

old_primary_seed: str = ""
old_secondary_seed: str = ""

def mainfunc():
    leaf_obj: bpy.types.Object = bpy.context.scene.leaf_object
    leaf_mat: bpy.types.Material = bpy.context.scene.leaf_mat

    if leaf_obj is not None and leaf_mat is not None:
        if leaf_obj.data.materials:
            if(leaf_obj.data.materials[0] != leaf_mat):
                leaf_obj.data.materials[0] = leaf_mat
                print("Leaf changed")
        else:
            leaf_obj.data.materials.append(leaf_mat)
            print("Leaf changed")
    
    bark_obj: bpy.types.Object = bpy.context.scene.bark_object
    bark_mat: bpy.types.Material = bpy.context.scene.bark_mat
    
    if bark_obj is not None and bark_mat is not None:
        if leaf_obj.data.materials:
            if(bark_obj.data.materials[0] != bark_mat):
                bark_obj.data.materials[0] = bark_mat
                print("Leaf changed")
        else:
            bark_obj.data.materials.append(bark_mat)
            print("Leaf changed")
   
   
   
   
   
    global old_primary_seed
    global random1
    if(old_primary_seed != bpy.context.scene.primary_seed):
        old_primary_seed = bpy.context.scene.primary_seed
        currSeed = StringSeedToNumber(bpy.context.scene.primary_seed)
        random1 = np.random.RandomState(currSeed)
        print("Primary Seed Changed")
    global old_secondary_seed
    global random2
    if(old_secondary_seed != bpy.context.scene.secondary_seed):
        old_secondary_seed = bpy.context.scene.secondary_seed
        currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
        random2 = np.random.RandomState(currSeed)
        print("Secondary Seed Changed")





class TreeGenPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tree Generator"
    bl_idname = "VIEW3D_Tree_Gen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TreeGen"
    #bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        mainfunc()

        row = layout.row()
        row.label(text="Tree Properties")
        row = layout.row()
        row.prop(context.scene, "max_height", slider=True)
        row = layout.row()
        row.prop(context.scene, "path_lenght", slider=True)
        row = layout.row()
        row.prop(context.scene, "branch_chance", slider=True)
        row = layout.row()
        row.prop(context.scene, "max_distance_from_middle", slider=True)
        row = layout.row()
        row.prop(context.scene, "straightness", slider=True)
        #print(bpy.context.scene.max_height)

        layout.separator()
        row = layout.row()
        row.label(text="Bark Generation:")
        row = layout.row()
        row.prop(context.scene, "bark_mat")
        row = layout.row()
        row.operator("object.gennewbark")

        layout.separator()
        row = layout.row()
        row.label(text="Leaf Generation 1:")
        row = layout.row()
        row.prop(context.scene, "leaf_object")
        row = layout.row()
        row.prop(context.scene, "leaf_mat")
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


        layout.separator()
        row = layout.row()
        row.label(text="Generation Option:")
        row = layout.row()
        row.prop(context.scene, "base_object")
        row = layout.row()
        row.operator("object.testoperator", text="Generate Tree")

def register():
    bpy.utils.register_class(TestOperator)
    bpy.utils.register_class(GenNewBark)
    bpy.utils.register_class(GenNewLeaf)
    bpy.utils.register_class(PrimarySeedGenOperator)
    bpy.utils.register_class(SecondarySeedGenOperator)
    bpy.utils.register_class(TreeGenPanel)
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    
    


def unregister():
    bpy.utils.unregister_class(TestOperator)
    bpy.utils.unregister_class(GenNewBark)
    bpy.utils.unregister_class(GenNewLeaf)
    bpy.utils.unregister_class(PrimarySeedGenOperator)
    bpy.utils.unregister_class(SecondarySeedGenOperator)
    bpy.utils.unregister_class(TreeGenPanel)
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)


if __name__ == "__main__":
    register()

