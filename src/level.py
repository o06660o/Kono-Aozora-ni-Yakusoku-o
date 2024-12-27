import pygame

from settings import ENV, BASE
from player import Player
from weapon import PlayerSword, PlayerThrowingSword, PlayerMagic
from debug import FreeCamera


class Level:
    def __init__(self, scale: float) -> None:
        self.scale = scale

        self.visible_sprites = Level.VisibleGroups(scale)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        self.display_surface = pygame.display.get_surface()
        self.create_map()

    def create_map(self) -> None:
        """
        override this method to create a map
        """
        self.player = Player(
            self.scale,
            (0, ENV.TILE_SIZE * -2),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.npc_sprites,
        )

    def custom_update(self) -> None:
        """
        override this method to update the level
        """
        pass

    def create_attack(self, attack_type: str, attack_direction: str = "") -> None:
        assert type(self.player) is Player
        if attack_type == "sword":
            self.current_attack = PlayerSword(
                self.scale,
                self.player,
                [self.visible_sprites, self.attack_sprites],
                attack_direction,
            )
        elif attack_type == "throwing_sword":
            self.current_attack = PlayerThrowingSword(
                self.scale,
                self.player,
                [self.visible_sprites, self.attack_sprites],
                attack_direction,
                self.obstacle_sprites,
            )
        elif attack_type == "magic":
            self.current_attack = PlayerMagic(
                self.scale,
                self.player,
                [self.visible_sprites, self.attack_sprites],
            )

    def draw(self) -> None:
        self.custom_update()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

    class VisibleGroups(pygame.sprite.Group):
        def __init__(self, scale: float) -> None:
            super().__init__()
            self.scale = scale
            self.display_surface = pygame.display.get_surface()
            self.half_width = self.display_surface.get_width() // 2
            self.half_height = self.display_surface.get_height() // 2
            self.offset = pygame.math.Vector2()

            self.floor_surface = pygame.Surface(
                (self.display_surface.get_width(), self.display_surface.get_height()),
                pygame.SRCALPHA,
            )
            self.floor_surface = pygame.transform.scale(
                self.floor_surface,
                (
                    self.floor_surface.get_width() * scale,
                    self.floor_surface.get_height() * scale,
                ),
            )
            self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
            self.background_image = pygame.image.load("assets/graphics/background.png").convert()
            self.background_image = pygame.transform.scale(
                self.background_image, (int(BASE.WIDTH * self.scale), int(BASE.HEIGHT * self.scale))
            )
            self.background_image.set_alpha(216)

        def custom_draw(self, player: Player | FreeCamera) -> None:
            self.display_surface.blit(self.background_image, (0, 0))
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height
            if type(player) is Player:
                if player.status == "sword":
                    self.offset.y += 18 * self.scale
                elif player.status == "throwing_sword":
                    self.offset.y -= 22.5 * self.scale

            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surface, floor_offset_pos)

            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite is player:
                    continue
                offset_pos = sprite.rect.topleft - self.offset
                # if type(sprite) is Player:
                #     offset_pos.y -= sprite.rect.height * 0.13
                self.display_surface.blit(sprite.image, offset_pos)

            player_offset_pos = player.rect.topleft - self.offset
            self.display_surface.blit(player.image, player_offset_pos)
