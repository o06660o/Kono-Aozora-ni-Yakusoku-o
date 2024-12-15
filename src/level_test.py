import sys
import pygame

from settings import BASE, ENV
from utils import create_rect_hitbox_image
from tile import Tile
from player import Player
from debug import FreeCamera


class Level:
    def __init__(self, scale: float) -> None:
        self.scale = scale

        self.visible_sprites = YSortGroups(scale)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.display_surface = pygame.display.get_surface()
        self.create_map()

    def create_map(self) -> None:
        self.floor = Tile(
            self.scale,
            (-BASE.DEFAULT_SCREEN_WIDTH * 0.6, 0),
            [self.visible_sprites, self.obstacle_sprites],
            "floor",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 1.2, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )
        self.left_wall = Tile(
            self.scale,
            (-BASE.DEFAULT_SCREEN_WIDTH * (0.6 + 0.1), -BASE.DEFAULT_SCREEN_HEIGHT),
            [self.visible_sprites, self.obstacle_sprites],
            "wall",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 0.1, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )
        self.right_wall = Tile(
            self.scale,
            (BASE.DEFAULT_SCREEN_WIDTH * 0.6, -BASE.DEFAULT_SCREEN_HEIGHT),
            [self.visible_sprites, self.obstacle_sprites],
            "wall",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 0.1, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )

        Tile(
            self.scale,
            (ENV.TILE_SIZE * -15, -ENV.TILE_SIZE * 5),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            create_rect_hitbox_image(
                1,
                (ENV.TILE_SIZE * 10, ENV.TILE_SIZE),
                color="black",
            ),
        )
        Tile(
            self.scale,
            (ENV.TILE_SIZE * 5, -ENV.TILE_SIZE * 7),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            create_rect_hitbox_image(
                1,
                (ENV.TILE_SIZE * 10, ENV.TILE_SIZE),
                color="black",
            ),
        )

        # if "--DEBUG" in sys.argv:
        # self.player = FreeCamera(self.scale, [self.visible_sprites])
        # else:
        #     self.player = Player(
        #         self.scale,
        #         (0, 0),
        #         [self.visible_sprites],
        #         self.obstacle_sprites,
        #         self.create_attack,
        #     )
        self.player = Player(
            self.scale,
            (0, ENV.TILE_SIZE * -2),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
        )

    def create_attack(self, attack_lifetime: int, attack_type: str, attack_direction: str) -> None:
        assert type(self.player) == Player
        if attack_type == "sword":
            from weapon import Sword

            self.current_attack = Sword(
                self.scale,
                attack_lifetime,
                self.player,
                [self.visible_sprites, self.attack_sprites],
                attack_direction,
            )

    def draw(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortGroups(pygame.sprite.Group):
    def __init__(self, scale: float) -> None:
        super().__init__()
        self.scale = scale
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.Surface(
            (self.display_surface.get_width(), self.display_surface.get_height()), pygame.SRCALPHA
        )
        self.floor_surface = pygame.transform.scale(
            self.floor_surface,
            (
                self.floor_surface.get_width() * scale,
                self.floor_surface.get_height() * scale,
            ),
        )
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player: Player | FreeCamera) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
