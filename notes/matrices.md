# Matrix Generation

The GMD file format defines each model as a hierarchy of "nodes". There are three types of nodes: a "matrix transform"/"
bone", unskinned objects, and skinned objects. GMDs can be broadly split into two categories.

## Unskinned scenes

Unskinned GMDs contain a hierarchy of matrix transforms and unskinned objects. Unskinned objects can be present at any
depth in the hierarchy, and you can have whole trees of unskinned objects parented to other unskinned objects. Matrix
transform nodes are essentially equivalent to empty unskinned objects.

Because matrix transforms and unskinned objects can affect the transformations of their children, they each hold a **
matrix** based on their position, rotation, and scale. In unskinned scenes, this seems to be calculated as follows:

```python
# pos, rot, scale are local
adjusted_pos, adjusted_rot, adjusted_scale = transform_blender_to_gmd(
    object.location,
    object.rotation_quaternion,
    object.scale
)
inv_t = Matrix.Translation(-adjusted_pos)
inv_r = adjusted_rot.inverted().to_matrix().to_4x4()
inv_s = Matrix.Diagonal(Vector((1 / adjusted_scale.x, 1 / adjusted_scale.y, 1 / adjusted_scale.z))).to_4x4()
parent_mat = parent.matrix if parent is not None else Matrix.Identity(4)
adjusted_matrix = (inv_s @ inv_r @ inv_t @ parent_mat)
```

For a chain of children $O1 -> O2 -> O3$, this matrix is equivalent to

$$ mat = scale_{O3}^{-1} * rot_{O3}^{-1} * trans_{O3}^{-1} * scale_{O2}^{-1} * rot_{O2}^{-1} * trans_{O2}^{-1} * scale_
{O1}^{-1} * rot_{O1}^{-1} * trans_{O1}^{-1} $$

which means if you multiply it by a point in world space, you are essentially undoing the following transformations in
order:

- translation of O1
- rotation of O1
- scale of O1
- translation of O2
- rotation of O2
- ...
- scale of O3

Therefore this matrix is a **world-to-local-space** transformation.

## Skinned scenes

Skinned scenes contain a hierarchy of bones, and multiple skinned objects at the scene root.
The skinned objects hold references to individual bones that can manipulate the vertices inside.
However, *the skinned objects themselves do not have any transformation or matrix associated with them*.
Only the bones have matrices, and only the bones can have non-identity transformations.

From experimentation, the matrix for bones can be derived from the other node fields (pos, rot, scale, parent) just like
for unskinned objects,
but there is a problem: *Blender bones do not have "rotation"*.
It seems like there is no way to reconstruct this data without just passing it through (see the bone_axis field, which
we still don't understand at time of writing).

