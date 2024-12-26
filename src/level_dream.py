import pygame

from settings import ENV
from level import Level
from tile import Tile
from player import Player


class LevelDream(Level):
    def __init__(self, scale: float) -> None:
        super().__init__(scale)

    def create_map(self) -> None:
        self.player = Player(
            self.scale,
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
        )
        # floor = pygame.image.load("assets/graphics/environment/dream/floor.png")
        plat_main = pygame.image.load("assets/graphics/environment/dream/dream_BG_plats_0000_4.png")
        plat_large = pygame.image.load(
            "assets/graphics/environment/dream/platform/dream_plat_large.png"
        )
        plat_mid = pygame.image.load(
            "assets/graphics/environment/dream/platform/dream_plat_mid.png"
        )
        plat_small = pygame.image.load(
            "assets/graphics/environment/dream/platform/dream_plat_small.png"
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-10 * self.scale, 0),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (160 * self.scale, 30 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (300 * self.scale, 30 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (440 * self.scale, 30 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-120 * self.scale, 30 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-160 * self.scale, -80 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_mid,
            ENV.LEVEL_DREAM.PLAT_MID_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (0 * self.scale, -150 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_small,
            ENV.LEVEL_DREAM.PLAT_SMALL_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (170 * self.scale, -180 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (560 * self.scale, 0 * self.scale),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (-120 * self.scale, 150 * self.scale),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     floor,
        #     ENV.LEVEL_DREAM.FLOOR_HITBOX_OFFSET,
        # )
