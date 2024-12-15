import math
import pygame

from settings import ENV, PLAYER
from utils import create_rect_hitbox_image
from player import Player


class Sword(pygame.sprite.Sprite):
    HEIGHT_RATIO = 0.125  # make the sword a little bit higher than the middle of the player

    def __init__(
        self, scale: float, lifetime: int, owner: Player, groups, attack_direction: str
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.lifetime = lifetime
        self.owner = owner
        self.image = create_rect_hitbox_image(
            scale,
            (ENV.TILE_SIZE * PLAYER.SWORD_LENGTH, ENV.TILE_SIZE * PLAYER.SWORD_WIDTH),
            color="brown",
        )
        self.original_image = self.image
        self.create_time = pygame.time.get_ticks()
        self.attack_direction = attack_direction
        self.move_and_rotate()
        self.hitbox = self.rect

    def move_and_rotate(self) -> None:
        current_time = pygame.time.get_ticks()
        angle = PLAYER.SWORD_ROTATE_ANGLE * (current_time - self.create_time) / self.lifetime
        angle -= PLAYER.SWORD_ROTATE_ANGLE // 2
        l = self.original_image.get_width() / 2
        dx = l * (1 - math.cos(math.radians(angle)))
        dy = l * math.sin(math.radians(angle))

        if self.attack_direction == "right":
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            self.rect = rotated_image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(-dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
            )
        elif self.attack_direction == "left":
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            self.rect = rotated_image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
            )
        elif self.attack_direction[:3] == "up_":
            angle += 90
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            if self.attack_direction[3:] == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                dy = -dy
            self.rect = rotated_image.get_rect(
                midbottom=self.owner.rect.midtop + pygame.math.Vector2(dy, dx)
            )
        elif self.attack_direction[:5] == "down_":
            angle -= 90
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            if self.attack_direction[5:] == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                dy = -dy
            self.rect = rotated_image.get_rect(
                midtop=self.owner.rect.midbottom + pygame.math.Vector2(dy, -dx)
            )
        self.image = rotated_image
        self.hitbox = self.rect

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > self.lifetime:
            self.kill()
        else:
            self.move_and_rotate()
