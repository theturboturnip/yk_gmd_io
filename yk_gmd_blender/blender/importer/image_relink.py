from collections import defaultdict

import bpy
import os
import glob

class YakuzaImageRelink(bpy.types.Operator):

    """Find images with """
    bl_idname = "yk.image_relink"
    bl_label = "Relink Images"
    bl_options = {'REGISTER', 'UNDO'}

    # Define this to tell 'fileselect_add' that we want a directoy
    directory: bpy.props.StringProperty(
        name="Texture Folder",
        description="Folder to pull textures from"
        # subtype='DIR_PATH' is not needed to specify the selection mode.
        # But this will be anyway a directory path.
    )

    # TODO - option to allow/prevent pulling from different image formats other than dds

    overwrite_linked: bpy.props.BoolProperty(
        name="Overwrite Valid Images",
        description="If True, will try to relink images that are already linked to a file (if a valid file exists).",
        default=False
    )

    def execute(self, context):

        self.report({"INFO"}, f"Selected dir: '{self.directory}'")

        if not os.path.isdir(self.directory):
            self.report({"ERROR"}, "Didn't select a valid directory")

        # Escape the directory name with glob to make sure any special characters inside it
        # (such as *) are not treated as globs.
        dir_escaped = glob.escape(self.directory)


        # Gather the set of images we want to remap - multiple Blender images may map to the same yakuza name?
        yk_image_name_to_blender_images = defaultdict(list)
        for img in bpy.data.images:
            if img.yakuza_data.inited:
                yk_image_name_to_blender_images[img.yakuza_data.yk_name].append(img)

        # Gather a list of images in the given directory that could be used for a Yakuza image
        yakuza_image_to_filepath = dict()

        # Match DDS then PNG, so PNGs override DDS
        for valid_ext in ["*.dds", "*.png"]:
            dir_glob = os.path.join(dir_escaped, valid_ext)

            self.report({"INFO"}, f"dir-glob for {valid_ext}: '{dir_glob}'")

            for image_filepath in glob.iglob(dir_glob):
                # Only accept files
                if not os.path.isfile(image_filepath):
                    continue

                # Just the basename i.e. "fileX.png"
                image_basename = os.path.basename(image_filepath)
                image_name, image_ext = os.path.splitext(image_basename)

                # If this image maps to a yakuza image name, remember it.
                # TODO - prioritize images by extension?
                if image_name in yk_image_name_to_blender_images:
                    yakuza_image_to_filepath[image_name] = image_filepath

        relinked_images = 0

        # Link up the newly found files to the respective yakuza images
        for found_yk_image_name, found_yk_filepath in yakuza_image_to_filepath.items():
            for blender_img in yk_image_name_to_blender_images[found_yk_image_name]:
                if blender_img.source == 'GENERATED' or self.overwrite_linked:
                    # Relink the image
                    blender_img.source = 'FILE'
                    blender_img.filepath = found_yk_filepath
                    blender_img.reload()
                    relinked_images += 1

        self.report({"INFO"}, f"Found {len(yakuza_image_to_filepath)} texture files, linked them to {relinked_images} Blender images.")

        return {'FINISHED'}

    def invoke(self, context, event):
        # Open browser, take reference to 'self' read the path to selected
        # file, put path in predetermined self fields.
        # See: https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {'RUNNING_MODAL'}


def menu_func_yk_image_relink(self, context):
    self.layout.operator(YakuzaImageRelink.bl_idname, text="Relink Imported Yakuza Images...")