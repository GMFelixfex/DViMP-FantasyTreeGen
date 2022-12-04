import bpy
import bmesh
import mathutils
import math
import random

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

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False,confirm=False)
bpy.ops.outliner.orphans_purge()

grass_mesh = bpy.data.meshes.new("grass_mesh")
grass_object = bpy.data.objects.new("grass_object",grass_mesh)
bpy.context.collection.objects.link(grass_object)


bm = bmesh.new()
bm.from_mesh(grass_mesh)


def map_range(v, from_min, from_max, to_min, to_max):
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

for i in range(BLADES):

    last_vert_l = None
    last_vert_r = None
    
    c_height = random.randrange(HEIGHT_MIN,HEIGHT_MAX)

    c_rot_base = random.uniform(ROT_BASE_MIN,ROT_BASE_MAX)
    c_rot_tip = random.uniform(ROT_TIP_MIN,ROT_TIP_MAX)

    random_angle = random.randrange(0, 360)
    
    rot_matrix_blade = mathutils.Matrix.Rotation(math.radians(random_angle),4,'Z')

    for l in range(c_height):
        progress = l / c_height

        v = math.pow(progress, 0.8)

        pos_x = map_range(v,0,1,WIDTH_MAX,WIDTH_MIN)

        vert_l = bm.verts.new((-pos_x,0,l))
        vert_r = bm.verts.new((pos_x,0,l))

        rot_angle = map_range(math.pow(progress,ROT_FALLOFF),0,1,c_rot_base,c_rot_tip)
        rot_mtx = mathutils.Matrix.Rotation(math.radians(rot_angle),4,'X')
        bmesh.ops.transform(bm,matrix=rot_mtx, verts=[vert_l,vert_r])
        bmesh.ops.transform(bm,matrix=rot_matrix_blade, verts=[vert_l,vert_r])

        if(l!=0):
            bm.faces.new((last_vert_l,vert_l,vert_r,last_vert_r))
        
        last_vert_r = vert_r
        last_vert_l = vert_l


bm.to_mesh(grass_mesh)
bm.free()