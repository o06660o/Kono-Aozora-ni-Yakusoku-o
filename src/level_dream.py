import pygame

from settings import ENV
from level import Level
from tile import Tile
from player import Player
from npc_tutorial import NPCTutorial
from enemy_centipede import EnemyCentipede
from debug import display


class LevelDream(Level):
    SUMMON_ENEMY_INTERVAL = 2000

    def __init__(self, scale: float) -> None:
        super().__init__(scale)
        self.last_enemy_summon_time = -1

    def create_map(self) -> None:
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
        NPCTutorial(
            self.scale,
            (-450, -65),
            [self.visible_sprites, self.npc_sprites],
        )

    def try_create_enemy(self) -> None:
        if len(self.attackable_sprites) == 0:
            now = pygame.time.get_ticks()
            if self.last_enemy_summon_time == -1:
                self.last_enemy_summon_time = now
            elif now - self.last_enemy_summon_time > self.SUMMON_ENEMY_INTERVAL:
                self.last_enemy_summon_time = -1
                EnemyCentipede(
                    self.scale,
                    (2460, 80),
                    [self.visible_sprites, self.attackable_sprites],
                    self.trigger_death,
                )

    def respawn_player(self) -> None:
        if self.player is not None:
            self.player.kill()
        self.player = Player(
            self.scale,
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.npc_sprites,
        )
   
    def print_health(self) -> None:
        # display(self.player.health) Visualize player health
        
        # 加载血量图片
        health_image = pygame.image.load(r"assets\graphics\ui\select_game_HUD_0001_health.png")
        head_image = pygame.image.load(r"assets\graphics\ui\select_game_HUD_0002_health_frame.png")
        # 获取当前显示表面
        display_surface = pygame.display.get_surface()

        display_surface.blit(head_image, (10, 10))
        # 遍历玩家的血量并在左上角显示相应数量的图片
        for i in range(self.player.health):
            x = 10 + i * (health_image.get_width() + 5)  + health_image.get_width() + 60
            y = 60
            display_surface.blit(health_image, (x, y))
        
    
    def custom_update(self) -> None:
        if type(self.player) is Player:
            if self.player.rect.y > 2000:
                self.respawn_player()
        self.try_create_enemy()
        self.print_health()
