import bpy
import bmesh
import mathutils
import math
BLADES = 10
ROT_Blades = 50

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False,confirm=False)
bpy.ops.outliner.orphans_purge()

grass_mesh = bpy.data.meshes.new("grass_mesh")
grass_object = bpy.data.objects.new("grass_object",grass_mesh)
bpy.context.collection.objects.link(grass_object)


bm = bmesh.new()
bm.from_mesh(grass_mesh)
last_vert_l = None
last_vert_r = None
rot_mtx = mathutils.Matrix.Rotation(math.radians(60),4,'X')

for i in range(BLADES):
    vert_l = bm.verts.new((-1+i/BLADES,0,i))
    vert_r = bm.verts.new((1-i/BLADES,0,i))
    rot_angle = 4
    rot_mtx = mathutils.Matrix.Rotation(math.radians(i*rot_angle),4,'X')
    bmesh.ops.transform(bm,matrix=rot_mtx, verts=[vert_l,vert_r])

    if(i!=0):
        bm.faces.new((last_vert_l,vert_l,vert_r,last_vert_r))
    
    last_vert_r = vert_r
    last_vert_l = vert_l


bm.to_mesh(grass_mesh)
bm.free()