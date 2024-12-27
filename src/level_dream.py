import pygame

from settings import ENV
from level import Level
from tile import Tile
from player import Player
from npc import NPC


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
            self.npc_sprites,
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
        # print(self.scale)
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-40, 0),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (320, 60),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (600, 60),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (880, 60),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-240, 60),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_large,
            ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-320, -160),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_mid,
            ENV.LEVEL_DREAM.PLAT_MID_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (0, -300),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_small,
            ENV.LEVEL_DREAM.PLAT_SMALL_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (340, -360),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (1120, 0),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (-240 ,300),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     floor,
        #     ENV.LEVEL_DREAM.FLOOR_HITBOX_OFFSET,
        # )
        NPC(
            self.scale,
            (-420, -70),
            [self.visible_sprites, self.npc_sprites],
            "tutorial",
        )

    def custom_update(self) -> None:
        if type(self.player) is Player:
            if self.player.rect.y > 2000:
                self.player.kill()
                self.player = Player(
                    self.scale,
                    (0, 0),
                    [self.visible_sprites],
                    self.obstacle_sprites,
                    self.create_attack,
                    self.npc_sprites,
                )
