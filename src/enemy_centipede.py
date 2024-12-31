import pygame

from enemy import Enemy


class EnemyCentipede(Enemy):
    def __init__(
        self, scale: float, pos: tuple[int, int], groups, trigger_death, sprite_type: str = "enemy"
    ) -> None:
        super().__init__(scale, pos, groups, "centipede", trigger_death, sprite_type)
        self.horizontal_direction = Enemy.LEFT

    def move(self) -> None:
        pass
