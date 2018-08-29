
bl_info = {
    'name': 'Dupli Frames',
    'author': 'Pavel_Blend',
    'version': (0, 0, 0),
    'blender': (2, 79, 0),
    'category': 'Object'
}


import bpy


class DupliFramesOp(bpy.types.Operator):
    bl_idname = 'object.dupli_frames'
    bl_label = 'Dupli Frames'
    bl_options = {'REGISTER', 'UNDO'}

    start = bpy.props.IntProperty(name='Frame Start', default=0)
    end = bpy.props.IntProperty(name='Frame End', default=100)
    on = bpy.props.IntProperty(name='On', default=1, min=1)
    off = bpy.props.IntProperty(name='Off', default=1, min=1)
    merge_objects = bpy.props.BoolProperty(name='Merge Objects', default=False)
    apply_modifiers = bpy.props.BoolProperty(name='Apply Modifiers', default=False)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, 'start')
        layout.prop(self, 'end')
        layout.prop(self, 'on')
        layout.prop(self, 'off')
        layout.prop(self, 'apply_modifiers')
        row = layout.row()
        row.active = self.apply_modifiers
        row.prop(self, 'merge_objects')

    def execute(self, context):
        scene = context.scene
        frame_current = scene.frame_current
        selected_objects = [object for object in context.selected_objects]
        active_object = context.active_object
        duplicate_objects = []

        for frame_id in range(self.start, self.end + 1, self.off):

            for selected_object in selected_objects:
                selected_object.select = True

            scene.frame_set(frame_id)
            bpy.ops.object.duplicate_move()

            for dupli_object in context.selected_objects:
                if dupli_object.animation_data:
                    action = dupli_object.animation_data.action
                    bpy.data.actions.remove(action)
                dupli_object.animation_data_clear()

            scene.objects.active = context.selected_objects[0]
            if self.apply_modifiers:
                bpy.ops.object.convert(target='MESH')
                if self.merge_objects:
                    duplicate_objects.append(dupli_object)
            bpy.ops.object.select_all(action='DESELECT')

        if self.merge_objects:
            if duplicate_objects:
                context.scene.objects.active = duplicate_objects[0]

                for object in duplicate_objects:
                    object.select = True

                bpy.ops.object.join()
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                bpy.ops.object.select_all(action='DESELECT')

        scene.frame_current = frame_current
        scene.objects.active = active_object

        for object in selected_objects:
            object.select = True

        return{'FINISHED'}


def draw_function(self, context):
    layout = self.layout
    layout.operator('object.dupli_frames')


def register():
    bpy.utils.register_class(DupliFramesOp)
    bpy.types.VIEW3D_PT_tools_object.append(draw_function)


def unregister():
    bpy.types.VIEW3D_PT_tools_object.remove(draw_function)
    bpy.utils.register_class(DupliFramesOp)
