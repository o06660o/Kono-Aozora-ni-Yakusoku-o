import sys
import pygame

from settings import TILE_SIZE
from utils import read_csv, read_images, create_rect_hitbox_image
from tile import Tile
from player import Player
from debug import FreeCamera


class World:
    def __init__(self, scale: float) -> None:
        self.scale = scale

        self.visible_sprites = YSortGroups(scale)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.display_surface = pygame.display.get_surface()
        self.create_map()

    def create_map(self) -> None:
        layouts = {"block": read_csv("assets/map/block.csv")}
        graphics = {"block": read_images("assets/graphics/block")}
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, col in enumerate(row):
                    col = col.lstrip()
                    col = col.rstrip()
                    if col == "-1":
                        continue
                    x = j * TILE_SIZE
                    y = i * TILE_SIZE
                    if style == "block":
                        Tile(
                            self.scale,
                            (x, y),
                            [self.visible_sprites, self.obstacle_sprites],
                            "blocks",
                            graphics[style][col],
                        )
        if "--DEBUG" in sys.argv:
            self.player = FreeCamera(self.scale, [self.visible_sprites])
        else:
            self.player = Player(
                self.scale,
                (0, 0),
                [self.visible_sprites],
                self.obstacle_sprites,
                self.create_attack,
            )

    def create_attack(self, attack_lifetime: int, attack_type: str) -> None:
        assert type(self.player) == Player
        if attack_type == "sword":
            from weapon import Sword

            self.current_attack = Sword(
                self.scale,
                attack_lifetime,
                self.player,
                [self.visible_sprites, self.attack_sprites],
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
            if "--DEBUG" in sys.argv:
                self.display_surface.blit(sprite.hitbox, offset_pos)
            else:
                self.display_surface.blit(sprite.image, offset_pos)
