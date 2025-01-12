import sys

import pygame

from npc import NPC


class NPCBlacksmith(NPC):
    def __init__(
        self,
        scale: float,
        pos: tuple[int, int],
        groups,
        npc_type: str = "blacksmith",
        sprite_type: str = "npc",
    ) -> None:
        super().__init__(scale, pos, groups, npc_type, sprite_type)
        if "--DEBUG" not in sys.argv:
            self.image = pygame.image.load("assets/graphics/npc/blacksmith.png").convert_alpha()
            self.image = pygame.transform.scale(
                self.image,
                (
                    int(scale * self.image.get_width()),
                    int(scale * self.image.get_height()),
                ),
            )
            self.image = pygame.transform.flip(
                self.image,
                True,
                False,
            )
