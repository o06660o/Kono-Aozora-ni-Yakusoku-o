import random

import pygame

from enemy import Enemy
from settings import ENEMY


class EnemyBoss(Enemy):
    def __init__(
        self,
        scale: float,
        pos: tuple[int, int],
        groups,
        trigger_death,
        sprite_type: str = "enemy",
    ) -> None:
        super().__init__(scale, pos, groups, "boss", trigger_death, sprite_type)
        self.horizontal_direction = Enemy.LEFT

        self.dx: float = 0

    def move(self) -> None:
        # turn around
        if random.random() < ENEMY.BOSS.TURN_PROBABILTY:
            self.horizontal_direction = -self.horizontal_direction  # left -> right, right -> left
        self.dx += self.horizontal_direction * ENEMY.SPEED[self.enemy_type]
        self.rect.x += self.horizontal_direction * ENEMY.SPEED[self.enemy_type]
        if abs(self.dx) > ENEMY.BOSS.MOVE_LEN:
            self.dx -= self.horizontal_direction * ENEMY.SPEED[self.enemy_type]
            self.rect.x -= self.horizontal_direction * ENEMY.SPEED[self.enemy_type]
            self.horizontal_direction = -self.horizontal_direction
