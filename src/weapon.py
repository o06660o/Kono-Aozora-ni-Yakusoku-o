import sys

import pygame

from settings import ENV, PLAYER
from utils import create_rect_hitbox_image, read_images_as_list
from player import Player

# TODO
# refactor needed


class PlayerSword(pygame.sprite.Sprite):
    HEIGHT_RATIO = 0.05
    CLOSER_RATIO = 0.4
    DAMAGE = 100

    def __init__(
        self,
        scale: float,
        owner: Player,
        groups,
        attack_direction: str,
        erase_attack,
        sprite_type: str = "weapon",
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.sprite_type = sprite_type
        self.owner = owner
        if "--DEBUG" in sys.argv:
            self.image = create_rect_hitbox_image(
                scale,
                (ENV.TILE_SIZE * PLAYER.SWORD_LENGTH, ENV.TILE_SIZE * PLAYER.SWORD_WIDTH),
                color="brown",
            )
        else:
            self.image = create_rect_hitbox_image(
                scale,
                (ENV.TILE_SIZE * PLAYER.SWORD_LENGTH, ENV.TILE_SIZE * PLAYER.SWORD_WIDTH),
                color=pygame.SRCALPHA,
            )

        self.original_image = self.image
        self.create_time = pygame.time.get_ticks()
        self.attack_direction = attack_direction
        self.move_and_rotate()
        self.hitbox = self.rect
        self.damage = PlayerSword.DAMAGE
        self.erase_attack = erase_attack

    def move_and_rotate(self) -> None:
        if self.attack_direction == "right":
            rotated_image = self.image
            self.rect = self.image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(
                    -self.owner.rect.width * PlayerSword.CLOSER_RATIO,
                    -self.owner.rect.height * PlayerSword.HEIGHT_RATIO,
                )
            )
        elif self.attack_direction == "left":
            rotated_image = self.image
            self.rect = self.image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(
                    self.owner.rect.width * PlayerSword.CLOSER_RATIO,
                    -self.owner.rect.height * PlayerSword.HEIGHT_RATIO,
                )
            )
        # elif self.attack_direction[:3] == "up_":
        #     rotated_image = pygame.transform.rotate(self.original_image, 90)
        #     self.rect = rotated_image.get_rect(
        #         midbottom=self.owner.rect.midtop
        #         - pygame.math.Vector2(0, -self.owner.rect.height * PlayerSword.CLOSER_RATIO)
        #     )
        # elif self.attack_direction[:5] == "down_":
        #     angle = PLAYER.SWORD_DOWNATTACK_ANGLE
        #     l = self.original_image.get_width() / 2
        #     dx = l * (1 - math.cos(math.radians(angle)))
        #     dy = l * math.sin(math.radians(angle))
        #     rotated_image = pygame.transform.rotate(self.original_image, -angle)
        #     if self.attack_direction[5:] == "left":
        #         rotated_image = pygame.transform.flip(rotated_image, True, False)
        #         dy = -dy
        #     self.rect = rotated_image.get_rect(
        #         midtop=self.owner.rect.midbottom + pygame.math.Vector2(dy, -dx)
        #     )
        self.image = rotated_image
        self.hitbox = self.rect

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > PLAYER.SWORD_LIFETIME:
            self.erase_attack()
        else:
            self.move_and_rotate()


class PlayerThrowingSword(pygame.sprite.Sprite):
    LOWER_RATIO = 0.07
    CLOSER_RATIO = 0.5
    DAMAGE = 80

    def __init__(
        self,
        scale: float,
        owner: Player,
        groups,
        attack_direction: str,
        rect_obstacles,
        erase_attack,
        sprite_type: str = "weapon",
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.sprite_type = sprite_type
        self.owner = owner
        self.image_ = create_rect_hitbox_image(
            scale,
            (
                ENV.TILE_SIZE * PLAYER.THROWING_SWORD_LENGTH,
                ENV.TILE_SIZE * PLAYER.THROWING_SWORD_WIDTH,
            ),
            color="brown",
        )
        self.animation = read_images_as_list(scale, "assets/graphics/player/weapon/throwing_sword")[
            0
        ]
        self.original_image = self.image_
        self.create_time = pygame.time.get_ticks()
        self.stoptime = pygame.time.get_ticks()
        self.attack_direction = attack_direction
        self.status = 0
        self.flytime = PLAYER.THROWING_SWORD_FLYINGTIME
        self.speed = PLAYER.THROWING_SWORD_SPEED * self.scale
        self.rect_obstacles = rect_obstacles
        self.distance = 0
        self.move()
        self.hitbox = self.rect
        if "--DEBUG" in sys.argv:
            self.image = self.image_
        else:
            self.animate()
        self.damage = PlayerThrowingSword.DAMAGE
        self.erase_attack = erase_attack

    def move(self) -> None:
        if self.status == 0:
            self.distance += self.speed
        elif self.status == 2:
            self.distance -= self.speed
        if self.attack_direction == "right":
            self.rect = self.original_image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(
                    -self.owner.rect.width * PlayerThrowingSword.CLOSER_RATIO,
                    PlayerThrowingSword.LOWER_RATIO * self.owner.rect.height * self.scale,
                )
                + pygame.math.Vector2(self.distance, 0)
            )
        elif self.attack_direction == "left":
            self.rect = self.original_image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(
                    self.owner.rect.width * PlayerThrowingSword.CLOSER_RATIO,
                    PlayerThrowingSword.LOWER_RATIO * self.owner.rect.height * self.scale,
                )
                + pygame.math.Vector2(-self.distance, 0)
            )
        self.hitbox = self.rect

    def collision(self) -> None:
        for obstacle in self.rect_obstacles:
            if self.hitbox.colliderect(obstacle.hitbox):
                if self.attack_direction == "right":
                    self.hitbox.right = obstacle.hitbox.left
                    self.distance = self.rect.midleft[0] - self.owner.rect.midright[0]
                elif self.attack_direction == "left":
                    self.hitbox.left = obstacle.hitbox.right
                    self.distance = self.owner.rect.midleft[0] - self.rect.midright[0]
                else:
                    assert False, "The attack direction is not right or left."
                if self.status == 0:
                    self.status = 1
                    self.stoptime = pygame.time.get_ticks()
                    self.flytime = self.stoptime - self.create_time

    def animate(self) -> None:
        if self.owner.horizontal_facing == Player.RIGHT:
            self.image = pygame.transform.flip(self.animation, True, False)
        else:
            self.image = self.animation

    def update(self) -> None:
        now = pygame.time.get_ticks()
        if self.status == 2 and now - self.stoptime > self.flytime + PLAYER.THROWING_SWORD_STOPTIME:
            self.erase_attack()
        else:
            self.collision()
            if self.status == 0 and now - self.create_time > self.flytime:
                self.status = 1
                self.stoptime = now
            if self.status == 1 and now - self.stoptime > PLAYER.THROWING_SWORD_STOPTIME:
                self.status = 2
            self.move()


class PlayerMagic(pygame.sprite.Sprite):
    DAMAGE = 150

    def __init__(
        self,
        scale: float,
        owner: Player,
        groups,
        erase_attack,
        sprite_type: str = "weapon",
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.sprite_type = sprite_type
        self.owner = owner
        self.image_ = create_rect_hitbox_image(
            scale,
            (ENV.TILE_SIZE * PLAYER.MAGIC_LENGTH, ENV.TILE_SIZE * PLAYER.MAGIC_WIDTH),
            color="brown",
        )
        self.rect = self.image_.get_rect(center=self.owner.rect.center)
        self.hitbox = self.rect
        self.create_time = pygame.time.get_ticks()
        self.animations = read_images_as_list(scale, "assets/graphics/player/weapon/magic")
        self.frame_index = 0
        self.frame_rate = 0.2
        self.move()
        if "--DEBUG" in sys.argv:
            self.image = self.image_
        else:
            self.animate()
        self.damage = PlayerMagic.DAMAGE
        self.erase_attack = erase_attack

    def move(self) -> None:
        self.rect = self.image_.get_rect(center=self.owner.rect.center)
        self.hitbox = self.rect

    def animate(self) -> None:
        self.frame_index += self.frame_rate
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        self.image = self.animations[int(self.frame_index)]

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > PLAYER.MAGIC_LIFETIME:
            self.erase_attack()
        else:
            self.move()
            if "--DEBUG" in sys.argv:
                self.image = self.image_
            else:
                self.animate()


# class Sword(pygame.sprite.Sprite):
#     HEIGHT_RATIO = 0.125  # make the sword a little bit higher than the middle of the player
#
#     def __init__(
#         self,
#         scale: float,
#         lifetime: int,
#         size: tuple[int, int],
#         owner,
#         groups,
#         attack_direction: str,
#     ) -> None:
#         super().__init__(groups)
#         self.scale = scale
#         self.lifetime = lifetime
#         self.owner = owner
#         self.image = create_rect_hitbox_image(
#             scale,
#             (ENV.TILE_SIZE * size[0], ENV.TILE_SIZE * size[1]),
#             color="red",
#         )
#         self.original_image = self.image
#         self.create_time = pygame.time.get_ticks()
#         self.attack_direction = attack_direction
#         self.move_and_rotate()
#         self.hitbox = self.rect
#
#     def move_and_rotate(self) -> None:
#         current_time = pygame.time.get_ticks()
#         angle = PLAYER.SWORD_ROTATE_ANGLE * (current_time - self.create_time) / self.lifetime
#         angle -= PLAYER.SWORD_ROTATE_ANGLE // 2
#         l = self.original_image.get_width() / 2
#         dx = l * (1 - math.cos(math.radians(angle)))
#         dy = l * math.sin(math.radians(angle))
#
#         if self.attack_direction == "right":
#             rotated_image = pygame.transform.rotate(self.original_image, -angle)
#             self.rect = rotated_image.get_rect(
#                 midleft=self.owner.rect.midright
#                 + pygame.math.Vector2(-dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
#             )
#         elif self.attack_direction == "left":
#             rotated_image = pygame.transform.rotate(self.original_image, angle)
#             self.rect = rotated_image.get_rect(
#                 midright=self.owner.rect.midleft
#                 + pygame.math.Vector2(dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
#             )
#         elif self.attack_direction[:3] == "up_":
#             angle += 90
#             rotated_image = pygame.transform.rotate(self.original_image, -angle)
#             if self.attack_direction[3:] == "left":
#                 rotated_image = pygame.transform.flip(rotated_image, True, False)
#                 dy = -dy
#             self.rect = rotated_image.get_rect(
#                 midbottom=self.owner.rect.midtop + pygame.math.Vector2(dy, dx)
#             )
#         elif self.attack_direction[:5] == "down_":
#             angle -= 90
#             rotated_image = pygame.transform.rotate(self.original_image, angle)
#             if self.attack_direction[5:] == "left":
#                 rotated_image = pygame.transform.flip(rotated_image, True, False)
#                 dy = -dy
#             self.rect = rotated_image.get_rect(
#                 midtop=self.owner.rect.midbottom + pygame.math.Vector2(dy, -dx)
#             )
#         self.image = rotated_image
#         self.hitbox = self.rect
#
#     def update(self) -> None:
#         if pygame.time.get_ticks() - self.create_time > self.lifetime:
#             self.kill()
#         else:
#             self.move_and_rotate()
