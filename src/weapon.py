import math
import pygame

from settings import ENV, PLAYER
from utils import create_rect_hitbox_image
from player import Player


class PlayerSword(pygame.sprite.Sprite):
    HEIGHT_RATIO = 0.125  # make the sword a little bit higher than the middle of the player

    def __init__(
        self,
        scale: float,
        owner: Player,
        groups,
        attack_direction: str,
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.owner = owner
        self.image = create_rect_hitbox_image(
            scale,
            (ENV.TILE_SIZE * PLAYER.SWORD_LENGTH, ENV.TILE_SIZE * PLAYER.SWORD_WIDTH),
            color="brown",
        )
        self.original_image = self.image
        self.create_time = pygame.time.get_ticks()
        self.attack_direction = attack_direction
        self.move_and_rotate()
        self.hitbox = self.rect

    def move_and_rotate(self) -> None:
        if self.attack_direction == "right":
            rotated_image = self.image
            self.rect = self.image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(0, -self.owner.rect.height * Sword.HEIGHT_RATIO)
            )
        elif self.attack_direction == "left":
            rotated_image = self.image
            self.rect = self.image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(0, -self.owner.rect.height * Sword.HEIGHT_RATIO)
            )
        elif self.attack_direction[:3] == "up_":
            rotated_image = pygame.transform.rotate(self.original_image, 90)
            self.rect = rotated_image.get_rect(midbottom=self.owner.rect.midtop)
        elif self.attack_direction[:5] == "down_":
            angle = PLAYER.SWORD_DOWNATTACK_ANGLE
            l = self.original_image.get_width() / 2
            dx = l * (1 - math.cos(math.radians(angle)))
            dy = l * math.sin(math.radians(angle))
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            if self.attack_direction[5:] == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                dy = -dy
            self.rect = rotated_image.get_rect(
                midtop=self.owner.rect.midbottom + pygame.math.Vector2(dy, -dx)
            )
        self.image = rotated_image
        self.hitbox = self.rect

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > PLAYER.SWORD_LIFETIME:
            self.kill()
        else:
            self.move_and_rotate()


class PlayerThrowingSword(pygame.sprite.Sprite):
    HEIGHT_RATIO = 0.125  # make the sword a little bit higher than the middle of the player

    def __init__(
        self,
        scale: float,
        owner: Player,
        groups,
        attack_direction: str,
        rect_obstacles,
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.owner = owner
        self.image = create_rect_hitbox_image(
            scale,
            (
                ENV.TILE_SIZE * PLAYER.THROWING_SWORD_LENGTH,
                ENV.TILE_SIZE * PLAYER.THROWING_SWORD_WIDTH,
            ),
            color="brown",
        )
        self.original_image = self.image
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

    def move(self) -> None:
        if self.status == 0:
            self.distance += self.speed
        elif self.status == 2:
            self.distance -= self.speed
        if self.attack_direction == "right":
            self.rect = self.image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(0, -self.owner.rect.height * Sword.HEIGHT_RATIO)
                + pygame.math.Vector2(self.distance, 0)
            )
        elif self.attack_direction == "left":
            self.rect = self.image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(0, -self.owner.rect.height * Sword.HEIGHT_RATIO)
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

    def update(self) -> None:
        now = pygame.time.get_ticks()
        if self.status == 2 and now - self.stoptime > self.flytime + PLAYER.THROWING_SWORD_STOPTIME:
            self.kill()
        else:
            self.collision()
            if self.status == 0 and now - self.create_time > self.flytime:
                self.status = 1
                self.stoptime = now
            if self.status == 1 and now - self.stoptime > PLAYER.THROWING_SWORD_STOPTIME:
                self.status = 2
            self.move()


class PlayerMagic(pygame.sprite.Sprite):
    def __init__(self, scale: float, owner: Player, groups) -> None:
        super().__init__(groups)
        self.scale = scale
        self.owner = owner
        self.image = create_rect_hitbox_image(
            scale,
            (ENV.TILE_SIZE * PLAYER.MAGIC_LENGTH, ENV.TILE_SIZE * PLAYER.MAGIC_WIDTH),
            color="brown",
        )
        self.rect = self.image.get_rect(center=self.owner.rect.center)
        self.create_time = pygame.time.get_ticks()
        self.move()
        self.hitbox = self.rect

    def move(self) -> None:
        self.rect = self.image.get_rect(center=self.owner.rect.center)

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > PLAYER.MAGIC_LIFETIME:
            self.kill()
        else:
            self.move()


class Sword(pygame.sprite.Sprite):
    HEIGHT_RATIO = 0.125  # make the sword a little bit higher than the middle of the player

    def __init__(
        self,
        scale: float,
        lifetime: int,
        size: tuple[int, int],
        owner,
        groups,
        attack_direction: str,
    ) -> None:
        super().__init__(groups)
        self.scale = scale
        self.lifetime = lifetime
        self.owner = owner
        self.image = create_rect_hitbox_image(
            scale,
            (ENV.TILE_SIZE * size[0], ENV.TILE_SIZE * size[1]),
            color="red",
        )
        self.original_image = self.image
        self.create_time = pygame.time.get_ticks()
        self.attack_direction = attack_direction
        self.move_and_rotate()
        self.hitbox = self.rect

    def move_and_rotate(self) -> None:
        current_time = pygame.time.get_ticks()
        angle = PLAYER.SWORD_ROTATE_ANGLE * (current_time - self.create_time) / self.lifetime
        angle -= PLAYER.SWORD_ROTATE_ANGLE // 2
        l = self.original_image.get_width() / 2
        dx = l * (1 - math.cos(math.radians(angle)))
        dy = l * math.sin(math.radians(angle))

        if self.attack_direction == "right":
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            self.rect = rotated_image.get_rect(
                midleft=self.owner.rect.midright
                + pygame.math.Vector2(-dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
            )
        elif self.attack_direction == "left":
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            self.rect = rotated_image.get_rect(
                midright=self.owner.rect.midleft
                + pygame.math.Vector2(dx, -self.owner.rect.height * Sword.HEIGHT_RATIO + dy)
            )
        elif self.attack_direction[:3] == "up_":
            angle += 90
            rotated_image = pygame.transform.rotate(self.original_image, -angle)
            if self.attack_direction[3:] == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                dy = -dy
            self.rect = rotated_image.get_rect(
                midbottom=self.owner.rect.midtop + pygame.math.Vector2(dy, dx)
            )
        elif self.attack_direction[:5] == "down_":
            angle -= 90
            rotated_image = pygame.transform.rotate(self.original_image, angle)
            if self.attack_direction[5:] == "left":
                rotated_image = pygame.transform.flip(rotated_image, True, False)
                dy = -dy
            self.rect = rotated_image.get_rect(
                midtop=self.owner.rect.midbottom + pygame.math.Vector2(dy, -dx)
            )
        self.image = rotated_image
        self.hitbox = self.rect

    def update(self) -> None:
        if pygame.time.get_ticks() - self.create_time > self.lifetime:
            self.kill()
        else:
            self.move_and_rotate()
