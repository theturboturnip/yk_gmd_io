from dataclasses import dataclass
from enum import Enum
from typing import Tuple


# TODO: Is there a better way to classify this? GMD files do not evolve with engines pre-dragon
# Could name FeatureSet or something
class GMDVersion(Enum):
    Kenzan = 1 # a.k.a Magical V-Engine?
    # 5?/0/Kiwami era - unknown what this engine was called
    Kiwami1 = 3
    Dragon = 4

@dataclass(frozen=True)
class VersionProperties:
    major_version: GMDVersion
    version_tuple: Tuple[int, int]
    # Are indices relative to the defined "vertex start" in the file?
    relative_indices_used: bool
    # Is vertex offset used to determine the range of values used by a mesh?
    indices_offset_by_min_index: bool

    def combined_version(self):
        return combine_versions(self.version_tuple[0], self.version_tuple[1])

    @property
    def version_str(self):
        return f"{self.version_tuple[0]}.{self.version_tuple[1]}"

def get_major_minor_version(version_combined: int) -> Tuple[int, int]:
    return (version_combined >> 16) & 0xFFFF, (version_combined >> 0) & 0xFFFF

def combine_versions(major_version: int, minor_version: int):
    return ((major_version & 0xFFFF) << 16) | (minor_version & 0xFFFF)

def get_version_properties(version_major: int, version_minor: int) -> VersionProperties:
    if version_major == 1:
        if version_minor <= 4:
            return VersionProperties(
                major_version=GMDVersion.Kenzan,
                version_tuple=(version_major, version_minor),
                relative_indices_used=True,
                indices_offset_by_min_index=True
            )
        else:
            # ex: haruka_on
            return VersionProperties(
                major_version=GMDVersion.Kenzan,
                version_tuple=(version_major, version_minor),
                relative_indices_used=False,
                indices_offset_by_min_index=False
            )
    elif version_major == 2:
        # Yakuza 3
        if version_minor == 8:
            return VersionProperties(
                major_version=GMDVersion.Kiwami1,
                version_tuple=(version_major, version_minor),
                relative_indices_used=False,
                indices_offset_by_min_index=True
            )
    elif version_major == 3:
        # All 0/Kiwami-era files
        return VersionProperties(
            major_version = GMDVersion.Kiwami1,
            version_tuple=(version_major, version_minor),
            relative_indices_used=False,
            indices_offset_by_min_index=True
        )
    elif version_major == 4:
        # Dragon engine
        return VersionProperties(
            major_version = GMDVersion.Dragon,
            version_tuple=(version_major, version_minor),
            relative_indices_used=False,
            indices_offset_by_min_index=True
        )

    print(f"Unknown major/minor combination {version_major}.{version_minor}")

def get_combined_version_properties(version_combined: int):
    return get_version_properties((version_combined >> 16) & 0xFFFF, (version_combined >> 0) & 0xFFFF)
