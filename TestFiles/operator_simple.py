import bpy
import bmesh
import mathutils
import math
import random


bl_info = {
    "name": "Grass Gen",
    "author": "Ich <ich@webmail.hs-furtwangen.de>",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "View3D > Add > Mesh",
    "description": "Create some grass",
    "category": "Add Mesh",
    "support": "TESTING",
}


def map_range(v, from_min, from_max, to_min, to_max):
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

def touch_grass(self, context):
        grass_mesh = bpy.data.meshes.new("grass_mesh")
        grass_object = bpy.data.objects.new("grass_object",grass_mesh)
        bpy.context.collection.objects.link(grass_object)
        bm = bmesh.new()
        bm.from_mesh(grass_mesh)
        random.seed(1234)

        for i in range(self.BLADES):

            last_vert_l = None
            last_vert_r = None
            
            
            c_height = random.randrange(self.HEIGHT_MIN,self.HEIGHT_MAX)

            c_rot_base = random.uniform(self.ROT_BASE_MIN,self.ROT_BASE_MAX)
            c_rot_tip = random.uniform(self.ROT_TIP_MIN,self.ROT_TIP_MAX)

            random_angle = random.randrange(0.1, 360.1)
            
            
            rot_matrix_blade = mathutils.Matrix.Rotation(math.radians(random_angle),4,'Z')

            for l in range(c_height):
                progress = l / c_height

                v = math.pow(progress, 0.8)

                pos_x = map_range(v,0,1,self.WIDTH_MAX,self.WIDTH_MIN)

                vert_l = bm.verts.new((-pos_x,0,l))
                vert_r = bm.verts.new((pos_x,0,l))

                rot_angle = map_range(math.pow(progress,self.ROT_FALLOFF),0,1,c_rot_base,c_rot_tip)
                rot_mtx = mathutils.Matrix.Rotation(math.radians(rot_angle),4,'X')
                bmesh.ops.transform(bm,matrix=rot_mtx, verts=[vert_l,vert_r])
                bmesh.ops.transform(bm,matrix=rot_matrix_blade, verts=[vert_l,vert_r])

                if(l!=0):
                    bm.faces.new((last_vert_l,vert_l,vert_r,last_vert_r))
                
                last_vert_r = vert_r
                last_vert_l = vert_l


        bm.to_mesh(grass_mesh)
        bm.free()

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    
    BLADES = 10

    WIDTH_MIN = 0.03
    WIDTH_MAX = 0.6

    HEIGHT_MIN = 4
    HEIGHT_MAX = 12

    ROT_BASE_MIN = 3
    ROT_BASE_MAX = 25
    ROT_TIP_MIN = 30
    ROT_TIP_MAX = 90
    ROT_FALLOFF = 5


    @classmethod
    def poll(cls, context): # was notwending sit für di aktivierung
        return True# context.active_object is not None

    def execute(self, context):
        touch_grass(self, context)
        return {'FINISHED'}

    

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.object.simple_operator()
