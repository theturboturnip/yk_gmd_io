from enum import IntEnum
from typing import Tuple, List, Dict


class GMDGame(IntEnum):
    """
    List of games using each engine in release order.
    Can be used to handle engine or game-specific quirks.
    (theoretically) bitmask-capable, so you can test a game against an engine and see if it matches.
    """
    Engine_MagicalV = 0x10
    Kenzan = 0x11
    Yakuza3 = 0x12
    Yakuza4 = 0x13
    DeadSouls = 0x14
    BinaryDomain = 0x15

    Engine_Kiwami = 0x20
    Yakuza5 = 0x21
    Yakuza0 = 0x22
    YakuzaKiwami1 = 0x23
    FOTNS = 0x24

    Engine_Dragon = 0x40
    Yakuza6 = 0x41
    YakuzaKiwami2 = 0x42
    Judgment = 0x43
    Yakuza7 = 0x44

    @staticmethod
    def blender_props() -> List[Tuple[str, str, str]]:
        return [
            ("ENGINE_MAGICALV", "Old Engine", "Magical-V Engine (Kenzan - Binary Domain)"),
            ("KENZAN", "Yakuza Kenzan", "Yakuza Kenzan"),
            ("YAKUZA3", "Yakuza 3", "Yakuza 3"),
            ("YAKUZA4", "Yakuza 4", "Yakuza 4"),
            ("DEADSOULS", "Yakuza Dead Souls", "Yakuza Dead Souls"),
            ("BINARYDOMAIN", "Binary Domain", "Binary Domain"),

            ("ENGINE_KIWAMI", "Kiwami Engine", "Kiwami Engine (Yakuza 5 - Yakuza Kiwami 1)"),
            ("YAKUZA5", "Yakuza 5", "Yakuza 5"),
            ("YAKUZA0", "Yakuza 0", "Yakuza 0"),
            ("YAKUZAK1", "Yakuza K1", "Yakuza Kiwami 1"),
            ("FOTNS", "FOTNS: LP", "Fist of the North Star: Lost Paradise"),

            ("ENGINE_DRAGON", "Dragon Engine", "Dragon Engine (Yakuza 6 onwards)"),
            ("YAKUZA6", "Yakuza 6", "Yakuza 6"),
            ("YAKUZAK2", "Yakuza K2", "Yakuza K2"),
            ("JUDGMENT", "Judgment", "Judgment"),
            ("YAKUZA7", "Yakuza 7", "Yakuza 7"),
        ]

    @staticmethod
    def mapping_from_blender_props() -> Dict[str, 'GMDGame']:
        return {
            "ENGINE_MAGICALV": GMDGame.Engine_MagicalV,
            "KENZAN": GMDGame.Kenzan,
            "YAKUZA3": GMDGame.Yakuza3,
            "YAKUZA4": GMDGame.Yakuza4,
            "DEADSOULS": GMDGame.DeadSouls,
            "BINARYDOMAIN": GMDGame.BinaryDomain,

            "ENGINE_KIWAMI": GMDGame.Engine_Kiwami,
            "YAKUZA5": GMDGame.Yakuza5,
            "YAKUZA0": GMDGame.Yakuza0,
            "YAKUZAK1": GMDGame.YakuzaKiwami1,
            "FOTNS": GMDGame.FOTNS,

            "ENGINE_DRAGON": GMDGame.Engine_Dragon,
            "YAKUZA6": GMDGame.Yakuza6,
            "YAKUZAK2": GMDGame.YakuzaKiwami2,
            "JUDGMENT": GMDGame.Judgment,
            "YAKUZA7": GMDGame.Yakuza7,
        }
