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
        self.flag = False

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
        ground_image = pygame.image.load("assets/graphics/environment/ground/long_ground.png")
        battle_image = pygame.image.load("assets/graphics/environment/ground/en2_ground.png")

        # print(self.scale)
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (-40, 0),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     plat_main,
        #     ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        # )
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (320, 60),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     plat_large,
        #     ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        # )
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (600, 60),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     plat_large,
        #     ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        # )
        # Tile(
        #     self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
        #     (880, 60),
        #     [self.visible_sprites, self.obstacle_sprites],
        #     "blocks",
        #     plat_large,
        #     ENV.LEVEL_DREAM.PLAT_LARGE_HITBOX_OFFSET,
        # )
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
        Tile(  # 虫子1的plat
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (340, 66),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            ground_image,
            ENV.LEVEL_DREAM.GROUND_HITBOX_OFFSET,
        )
        Tile(  # 虫子2的plat
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (320, -350),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            battle_image,
            ENV.LEVEL_DREAM.GROUND_HITBOX_OFFSET,
        )
        Tile(  # 虫子3的plat
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (600, -550),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_small,
            ENV.LEVEL_DREAM.PLAT_SMALL_HITBOX_OFFSET,
        )
        Tile(
            self.scale * ENV.LEVEL_DREAM.IMAGE_SCALE,
            (-40, -10),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            plat_main,
            ENV.LEVEL_DREAM.PLAT_HITBOX_OFFSET,
        )

        NPCTutorial(
            self.scale,
            (-450, -65),
            [self.visible_sprites, self.npc_sprites],
        )

    # def try_create_enemy(self) -> None:
    #     if len(self.attackable_sprites) == 0:
    #         now = pygame.time.get_ticks()
    #         if self.last_enemy_summon_time == -1:
    #             self.last_enemy_summon_time = now
    #         elif now - self.last_enemy_summon_time > self.SUMMON_ENEMY_INTERVAL:
    #             self.last_enemy_summon_time = -1
    #             EnemyCentipede(
    #                 self.scale,
    #                 (2000, 80),
    #                 [self.visible_sprites, self.attackable_sprites],
    #                 self.trigger_death,
    #             )

    def try_create_enemy(self) -> None:
        if len(self.attackable_sprites) == 0 and not self.flag:
            self.flag = True
            EnemyCentipede(  # enemy 1
                self.scale,
                (2000, 80),
                [self.visible_sprites, self.attackable_sprites],
                self.trigger_death,
            )
            EnemyCentipede(  # enemy 2
                self.scale,
                (700, -763),
                [self.visible_sprites, self.attackable_sprites],
                self.trigger_death,
            )
            EnemyCentipede(  # enemy 3
                self.scale,
                (1180, -1130),
                [self.visible_sprites, self.attackable_sprites],
                self.trigger_death,
            )
        # EnemyCentipede(
        #     self.scale,
        #     (2000, 80),
        #     [self.visible_sprites, self.attackable_sprites],
        #     self.trigger_death,
        # )
        # EnemyCentipede(
        #     self.scale,
        #     (2000, 80),
        #     [self.visible_sprites, self.attackable_sprites],
        #     self.trigger_death,
        # )

    def win_check(self) -> bool:
        if len(self.attackable_sprites) == 0 and self.flag:
            return True
        else:
            return False

    def print_win(self) -> None:
        display_surface = pygame.display.get_surface()
        win_image = pygame.image.load(r"assets/graphics/menu/win.png")

        # 获取屏幕的宽度和高度
        screen_width, screen_height = display_surface.get_size()

        # 计算放缩比例
        scale_x = screen_width / win_image.get_width()
        scale_y = screen_height / win_image.get_height()

        # 选择较小的放缩比例，以确保图片完全显示在屏幕上
        scale = min(scale_x, scale_y)

        # 计算放缩后的图像大小
        new_width = int(win_image.get_width() * scale)
        new_height = int(win_image.get_height() * scale)

        # 放缩图像
        win_image = pygame.transform.scale(win_image, (new_width, new_height))

        # 计算图像在屏幕上的居中位置
        x = (screen_width - new_width) // 2
        y = (screen_height - new_height) // 2

        # 在屏幕上绘制放缩后的图像
        display_surface.blit(win_image, (x, y))
        display_surface.blit(win_image, (0, 0))

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

    def magic_image(self):
        if self.player.magic == 0:
            return pygame.image.load(r"assets/graphics/ui/0_energy.png")
        elif self.player.magic == 1:
            return pygame.image.load(r"assets/graphics/ui/1_energy.png")
        elif self.player.magic == 2:
            return pygame.image.load(r"assets/graphics/ui/2_energy.png")
        elif self.player.magic == 3:
            return pygame.image.load(r"assets/graphics/ui/3_energy.png")

    def print_health(self) -> None:
        # display(self.player.health) Visualize player health

        health_image = pygame.image.load(r"assets/graphics/ui/select_game_HUD_0001_health.png")
        health_image = pygame.transform.scale(
            health_image,
            (
                int(health_image.get_width() * self.scale),
                int(health_image.get_height() * self.scale),
            ),
        )

        head_image = self.magic_image()
        head_image = pygame.transform.scale(
            head_image,
            (int(head_image.get_width() * self.scale), int(head_image.get_height() * self.scale)),
        )

        empty_image = pygame.image.load(r"assets/graphics/ui/empty_blood.png")
        empty_image = pygame.transform.scale(
            empty_image,
            (int(empty_image.get_width() * self.scale), int(empty_image.get_height() * self.scale)),
        )

        display_surface = pygame.display.get_surface()

        display_surface.blit(head_image, (10 * self.scale, 10 * self.scale))
        x = 10 * self.scale + health_image.get_width() + 60 * self.scale
        y = 60
        y *= self.scale
        for i in range(self.player.health):
            display_surface.blit(health_image, (x, y))
            x += health_image.get_width() + 5 * self.scale
        for i in range(8 - self.player.health):
            display_surface.blit(empty_image, (x, y))
            x += empty_image.get_width() + 5 * self.scale

    def custom_update(self) -> None:
        if type(self.player) is Player:
            if self.player.rect.y > 2000:
                self.respawn_player()
        self.try_create_enemy()
        self.print_health()
