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
    ('bark_object', bpy.props.PointerProperty(type=bpy.types.Object ,name='Bark Object')),
    ('leaf_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Leaf Material')),
    ('bark_mat', bpy.props.PointerProperty(type=bpy.types.Material ,name='Bark Material')),
    ('primary_seed', bpy.props.StringProperty(name='Primary Seed', default = "0")),
    ('secondary_seed', bpy.props.StringProperty(name='Secondary Seed', default = "0")),
    ('material_list', bpy.props.PointerProperty(type=bpy.types.Material,name='Material')),
    ('texture_quality', bpy.props.FloatProperty(name='Texture Quality', default=1.0,min=0.1, max=15.0, soft_max=15.0, soft_min=0.01, step=0.01 ,precision=3)),
]

class TestOperator(bpy.types.Operator):
    bl_idname = "object.testoperator"
    bl_label = "Simple Test Operator "

    @classmethod
    def poll(cls, context): # was notwending ist für die aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        print("Start Testing")

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
        noise_tex_1.inputs["Scale"].default_value = 7.0
        noise_tex_1.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_1.inputs["Roughness"].default_value = 0.65
        noise_tex_1.inputs["Distortion"].default_value = 0.3
        
        noise_tex_2.inputs["Scale"].default_value = 3.0
        noise_tex_2.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_2.inputs["Roughness"].default_value = 0.5
        noise_tex_2.inputs["Distortion"].default_value = 0.0

        noise_tex_3.inputs["Scale"].default_value = 8.0
        noise_tex_3.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_3.inputs["Distortion"].default_value = 0.0

        noise_tex_4.inputs["Scale"].default_value = 4.0
        noise_tex_4.inputs["Detail"].default_value = bpy.context.scene.texture_quality
        noise_tex_4.inputs["Roughness"].default_value = 0.60
        noise_tex_4.inputs["Distortion"].default_value = 0.0
        
            # Voronoi-Texture
        voronoi_tex.inputs["Scale"].default_value = 8.0
        voronoi_tex.inputs["Randomness"].default_value = 1.0

            # Color-Ramp
        color_ramp_1.color_ramp.elements[0].position = 0.6
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
        material.node_tree.links.new(material_shader.inputs[22], bump_3.outputs[0])

            # MixRGB+Linear-Light
        material.node_tree.links.new(material_shader.inputs[0], mix_rgb.outputs[0])
        material.node_tree.links.new(mapping.inputs[0], linear_light.outputs[0])

            # Rest (Mapping, Shader, Displacement)
        material.node_tree.links.new(voronoi_tex.inputs[0], mapping.outputs[0])
        material.node_tree.links.new(material_output.inputs[2], displacement.outputs[0])
        material.node_tree.links.new(material_output.inputs[0], material_shader.outputs[0])



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
        material = bpy.data.materials.new(name="leaf_material")
        bpy.context.scene.leaf_mat = material
        

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
    global old_primary_seed
    global random1
    global old_secondary_seed
    global random2
    materialChanged = False
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
    
    # bark_obj: bpy.types.Object = bpy.context.scene.bark_object
    bark_obj: bpy.types.Object = bpy.context.scene.objects["Cube"]
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

    if(materialChanged):
        currSeed = StringSeedToNumber(bpy.context.scene.secondary_seed)
        random2 = np.random.RandomState(currSeed)




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
        row = layout.row()
        row.prop(context.scene, "texture_quality", slider=True)
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
        row.prop(context.scene, "bark_object")
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

