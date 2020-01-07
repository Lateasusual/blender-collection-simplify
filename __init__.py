import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty, BoolProperty

bl_info = {
    "name": "Collection Simplifier",
    "description": "Show/Hide subdivisions in collections",
    "author": "Lateasusual",
    "version": (1, 0, 0),
    "blender": (2, 81, 0),
    "location": "Properties > Render > Simplify",
    "warning": "",  # warning icon text
    "wiki_url": "",  # TODO Github wiki
    "tracker_url": "https://github.com/Lateasusual/blender-pytrails/issues",
    "support": "COMMUNITY",
    "category": "Animation"
}

class SCENE_OT_simplify_collection(Operator):
    """Show/Hide all subdivision surface modifiers in collection"""
    bl_idname = 'scene.simplify_collection'
    bl_label = 'Simplify Collection'
    
    show_v: BoolProperty('Show in Viewport', default=False)
    show_r: BoolProperty('Show in Render', default=True)
    
    @classmethod
    def poll(cls, context):
        return context.scene is not None
    
    def execute(self, context):
        try:
            col = bpy.data.collections[context.scene.simplify_col] 
        except KeyError:
            self.report({'ERROR'}, f'Collection "{context.scene.simplify_col}" not found')
            return {'CANCELLED'}
        for obj in col.objects:
            for mod in obj.modifiers:
                if mod.type == 'SUBSURF':
                    mod.show_viewport = self.show_v
                    mod.show_render = self.show_r
        
        return {'FINISHED'}


class RENDER_PT_simplify_collection(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    bl_label = "Collection"
    bl_parent_id = "RENDER_PT_simplify"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES)
    
    def draw(self, context):
        layout = self.layout
        rd = context.scene.render
        
        layout.use_property_split = True
        
        layout.prop_search(context.scene, "simplify_col", context.scene.collection, "children", text='Collection')
        
        row = layout.row()
        op = row.operator('scene.simplify_collection', text='simplify')
        op.show_v = False
        
        op = row.operator('scene.simplify_collection', text='unsimplify')
        op.show_v = True
        
        
classes = [
    RENDER_PT_simplify_collection,
    SCENE_OT_simplify_collection
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.simplify_col = StringProperty('Collection')
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.simplify_col
        
if __name__ == '__main__':
    register()
