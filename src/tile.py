import pygame
from settings import ENV


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        scale: float,
        pos: tuple[int | float, int | float],
        groups,
        sprite_type: str,
        surface=pygame.Surface((ENV.TILE_SIZE, ENV.TILE_SIZE)),
        offset: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.sprite_type = sprite_type
        self.image = pygame.transform.scale(
            surface, (surface.get_width() * scale, surface.get_height() * scale)
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(-offset[0] * scale, -offset[1] * scale)
