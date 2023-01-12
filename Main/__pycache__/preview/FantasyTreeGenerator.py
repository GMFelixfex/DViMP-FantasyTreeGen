import bpy

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
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        return {'FINISHED'}

class GenNewBark(bpy.types.Operator):
    bl_idname = "object.gennewbark"
    bl_label = "Genenate Bark Material"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

    def execute(self, context):
# TODO: Generate the Bark and select it
        return {'FINISHED'}

class GenNewLeaf(bpy.types.Operator):
    bl_idname = "object.gennewleaf"
    bl_label = "Genenate Leaf Material"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

    def execute(self, context):
# TODO: Generate the Bark and select it
        return {'FINISHED'}

class PrimarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.primaryseedgen"
    bl_label = "Generate Priamry Seed"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

# TODO: Add Generating Logic
    def execute(self, context):
        bpy.context.scene.primary_seed = "2"
        return {'FINISHED'}

class SecondarySeedGenOperator(bpy.types.Operator):
    bl_idname = "object.secondaryseedgen"
    bl_label = "Generate Secondary Seed"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

# TODO: Add Generating Logic
    def execute(self, context): 
        bpy.context.scene.secondary_seed = "1"

        
        return {'FINISHED'}


class LeafMaterialOperator(bpy.types.Operator):
    bl_idname = "object.leafmaterialoperator"
    bl_label = "Generate Leaf Material"

    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None


    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "max_height", slider=True)
        layout.prop_search(self, "material_name", bpy.data, "materials")

        


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

        row = layout.row()
        #row.label(text="Hello world!", icon='WORLD_DATA')

        #row = layout.row()
        #row.label(text="Active object is: " + obj.name)
        #row = layout.row()
        #row.prop(obj, "name")
        #layout.separator()

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


        layout.separator()
        row = layout.row()
        row.prop(context.scene, "bark_mat")
        #row.template_ID(obj, "active_material", new="material.new")
        # row.prop(obj, "leaf_mat")
        row = layout.row()
        row.operator("object.gennewbark")

        layout.separator()
        row = layout.row()
        row.label(text="Leaf Generation:")
        row = layout.row()
        row.prop(context.scene, "leaf_object")
        row = layout.row()
        row.prop(context.scene, "leaf_mat")
        # row.template_ID(obj, "active_material", new="material.new")
        # row.operator("object.leafmaterialoperator", text='Search', icon = 'VIEWZOOM')
        # row.prop(obj, "bark_mat")
        # row.prop_search(obj, "material_name", bpy.data.materials, "materials")
        # row.prop_search(obj, "material_name", context.scene, "materials")
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

