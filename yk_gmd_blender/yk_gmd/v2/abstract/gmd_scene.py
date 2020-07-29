from dataclasses import dataclass
from typing import Dict, List

from yk_gmd_blender.yk_gmd.v2.abstract.gmd_node import GMDBone, GMDSkinnedObject, GMDUnskinnedObject


@dataclass(repr=False)
class GMDScene:
    name: str

    # Node Heirarchy stuff
    # Assume only one skeleton exists
    skeleton_root: GMDBone
    skel_bone_from_name: Dict[str, GMDBone]

    skinned_objects: List[GMDSkinnedObject]
    unskinned_objects: List[GMDUnskinnedObject]