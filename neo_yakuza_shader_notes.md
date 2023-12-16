## Neo Yakuza Shader changes and notes

 - Most (character) shaders are accounted for, and can handle both Dragon Engine and Old Engine shaders.
 - Minimum asset shader support for now, all it does is swizzle texture_multi (from RGB to RBG) and disable ambient occlusion. No blending support yet.
 - Shaders with reflection cubemaps are not supported simply because cubemap textures aren't supported in Blender yet.
 - Hair shaders aren't supported yet.

