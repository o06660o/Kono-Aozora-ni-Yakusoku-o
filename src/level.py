import pygame

from settings import ENV, BASE
from player import Player
from weapon import PlayerSword, PlayerThrowingSword, PlayerMagic
from debug import FreeCamera
from enemy import Enemy


class Level:
    def __init__(self, scale: float) -> None:
        self.scale = scale

        self.visible_sprites = Level.VisibleGroups(scale)
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.current_attack = None

        self.display_surface = pygame.display.get_surface()
        self.create_map()
        self.create_player()

    def create_map(self) -> None:
        """
        override this method to create a map
        """
        pass

    def create_player(self) -> None:
        """
        override this method to create a player
        """
        self.player = Player(
            self.scale,
            (0, ENV.TILE_SIZE * -2),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.npc_sprites,
        )
        pass

    def respawn_player(self) -> None:
        self.player.kill()
        self.create_player()

    def trigger_death(self, entity: Enemy) -> None:
        entity.kill()
        self.player.money += 5

    def custom_update(self) -> None:
        """
        override this method to update the level
        """
        pass

    def create_attack(self, attack_type: str, attack_direction: str = "") -> None:
        assert type(self.player) is Player
        if attack_type == "sword":
            self.current_attack = PlayerSword(
                self.scale, self.player, [self.visible_sprites], attack_direction, self.erase_attack
            )
        elif attack_type == "throwing_sword":
            self.current_attack = PlayerThrowingSword(
                self.scale,
                self.player,
                [self.visible_sprites],
                attack_direction,
                self.obstacle_sprites,
                self.erase_attack,
            )
        elif attack_type == "magic":
            self.current_attack = PlayerMagic(
                self.scale, self.player, [self.visible_sprites], self.erase_attack
            )

    def erase_attack(self) -> None:
        if self.current_attack is not None:
            self.current_attack.kill()
            self.current_attack = None

    def attack_enemies(self) -> None:
        if self.current_attack is None:
            return
        now = pygame.time.get_ticks()
        for target in self.attackable_sprites:
            if target.vulnerable and self.current_attack.hitbox.colliderect(target.hitbox):
                target.vulnerable = False
                target.last_hit_time = now
                target.health -= self.current_attack.damage
                if target.health <= 0:
                    target.status = "death"
                    target.death_time = now

    def attack_player(self) -> None:
        if not self.player.vulnerable:
            return
        now = pygame.time.get_ticks()
        for enemy in self.attackable_sprites:
            if enemy.hitbox.colliderect(self.player.hitbox):
                if self.player.vulnerable:
                    self.player.vulnerable = False
                    self.player.last_hit_time = now
                    self.player.health -= enemy.damage
                    if self.player.health <= 0:
                        self.respawn_player()
                    return

    def draw(self) -> None:
        self.attack_enemies()
        self.attack_player()
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
            self.background_image = pygame.image.load(
                "assets/graphics/background.png"
            ).convert_alpha()
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
                if sprite.sprite_type != "blocks":
                    continue
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite.sprite_type == "blocks" or sprite == player:
                    continue
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

            self.display_surface.blit(player.image, player.rect.topleft - self.offset)
