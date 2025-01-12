import sys

import pygame

from settings import BASE, ENV, ENEMY
from utils import create_rect_hitbox_image, read_images_as_list


class Enemy(pygame.sprite.Sprite):
    LEFT = -1
    RIGHT = 1

    def __init__(
        self,
        scale: float,
        pos: tuple[int, int],
        groups,
        enemy_type: str,
        trigger_death,
        sprite_type: str = "enemy",
    ) -> None:
        super().__init__(groups)
        self.scale = scale * ENEMY.INFO[enemy_type]["scale"]
        self.enemy_type = enemy_type
        self.sprite_type = sprite_type
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.image = create_rect_hitbox_image(
            scale,
            (
                ENEMY.INFO[enemy_type]["width"] * ENV.TILE_SIZE * self.scale,
                ENEMY.INFO[enemy_type]["height"] * ENV.TILE_SIZE * self.scale,
            ),
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect
        self.health = ENEMY.INFO[enemy_type]["health"]
        self.damage = ENEMY.INFO[enemy_type]["damage"]
        self.prestatus = ""
        self.status = ENEMY.INFO[enemy_type]["status"]
        self.death_time = -1
        self.vulnerable = True
        now = pygame.time.get_ticks()
        self.last_hit_time = now
        self.speed: pygame.Vector2 = pygame.Vector2(0, 0)
        self.frame_index = 0
        self.animations = {}
        self.frame_rate = {}
        self.horizontal_direction = -Enemy.RIGHT
        for key, value in ENEMY.ANIMATIONS[enemy_type].items():
            self.animations[key] = read_images_as_list(
                self.scale,
                f"assets/graphics/enemy/{enemy_type}/{key}",
            )
            self.frame_rate[key] = value
        self.death_time = -1
        self.trigger_death = trigger_death
        if "--DEBUG" not in sys.argv:
            self.image = self.animations[self.status][0]

    def cooldown(self) -> None:
        now = pygame.time.get_ticks()
        if not self.vulnerable and now - self.last_hit_time > ENEMY.VULNERABLE_TIME:
            self.vulnerable = True

    def animate(self) -> None:
        if self.status != self.prestatus:
            self.frame_index = 0
            self.prestatus = self.status
        self.image = self.animations[self.status][int(self.frame_index)]
        self.frame_index += self.frame_rate[self.status]
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        if self.horizontal_direction == Enemy.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

    def action(self) -> None:
        """
        Override this method to implement the action of the enemy.
        """
        pass

    def move(self) -> None:
        """
        Override this method to implement the movement of the enemy.
        """
        pass

    def check_death(self) -> None:
        if self.status != "death":
            return
        now = pygame.time.get_ticks()
        if now - self.death_time > BASE.DEATH_DURATION:
            self.trigger_death(self)

    def update(self) -> None:
        self.check_death()
        self.cooldown()
        self.action()
        self.move()
        if "--DEBUG" not in sys.argv:
            self.animate()
