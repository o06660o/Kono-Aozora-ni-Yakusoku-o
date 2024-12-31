import pygame

from settings import NPC as NPC_SETTINGS
from npc import NPC


class NPCTutorial(NPC):
    def __init__(
        self,
        scale: float,
        pos: tuple[int, int],
        groups,
        npc_type: str = "tutorial",
        sprite_type: str = "npc",
    ) -> None:
        super().__init__(scale, pos, groups, npc_type, sprite_type)
        scale *= NPC_SETTINGS.SCALE
        self.image = pygame.image.load("assets/graphics/npc/tutorial.png")
        self.image = pygame.transform.scale(
            self.image,
            (
                int(scale * self.image.get_width()),
                int(scale * self.image.get_height()),
            ),
        )
