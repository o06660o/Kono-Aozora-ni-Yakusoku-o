import pygame

from settings import ENV, PLAYER
from utils import create_rect_hitbox_image
from keys import Keys
from debug import display


class Player(pygame.sprite.Sprite):
    RIGHT = 1
    LEFT = -1
    IDLE = 0
    UP = 1
    DOWN = -1

    def __init__(
        self,
        scale: float,
        pos: tuple[int | float, int | float],
        groups,
        rect_obstacles,
        create_attack,
    ) -> None:
        super().__init__(groups)
        # base
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.image = create_rect_hitbox_image(scale, (ENV.TILE_SIZE, ENV.TILE_SIZE * 2))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect
        self.rect_obstacles = rect_obstacles
        self.horizontal_facing = Player.RIGHT
        self.vertical_facing = Player.IDLE
        self.keys = Keys()
        now = pygame.time.get_ticks()

        # movement
        self.velocity: pygame.Vector2 = pygame.math.Vector2()
        self.can_sprint = True
        self.is_sprinting = False
        self.sprint_time = now
        self.can_jump = False
        self.jump_count = 0
        self.have_released_K_SPACE = True
        self.jump_power_exists = False
        self.jump_time = now
        self.touch_ground = False
        self.touch_ground_time = now

        # combat
        self.can_attack = True
        self.attack_time = now
        self.create_attack = create_attack

    def input(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.have_released_K_SPACE and not keys[pygame.K_SPACE]:
            self.have_released_K_SPACE = True

        # movement
        ## horizontal
        if self.is_sprinting:
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = PLAYER.SPRINT_SPEED * self.scale
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = -PLAYER.SPRINT_SPEED * self.scale
            self.velocity.y = 0
            return

        if keys[pygame.K_LSHIFT] and self.can_sprint:
            self.can_sprint = False
            self.is_sprinting = True
            self.sprint_time = pygame.time.get_ticks()
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = PLAYER.SPRINT_SPEED * self.scale
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = -PLAYER.SPRINT_SPEED * self.scale

        if keys[pygame.K_a] and keys[pygame.K_d]:
            self.velocity.x = 0
        elif keys[pygame.K_a]:
            self.velocity.x = -PLAYER.SPEED * self.scale
        elif keys[pygame.K_d]:
            self.velocity.x = PLAYER.SPEED * self.scale

        if self.velocity.x == 0:
            pass
        elif self.velocity.x > 0:
            self.horizontal_facing = Player.RIGHT
        elif self.velocity.x < 0:
            self.horizontal_facing = Player.LEFT

        ## vertical
        if self.touch_ground:
            if keys[pygame.K_SPACE] and self.can_jump:  # a jump starts
                self.velocity.y = -PLAYER.JUMP_POWER * self.scale
                self.jump_time = pygame.time.get_ticks()
                self.can_jump = False
                self.jump_power_exists = True
                self.touch_ground = False
                self.jump_count = 1
                self.have_released_K_SPACE = False
            else:
                self.velocity.y += ENV.GRAVITY_ACCELERATION * self.scale
        else:
            if keys[pygame.K_SPACE] and self.jump_power_exists:  # a jump continuing
                self.velocity.y = min(
                    -PLAYER.JUMP_POWER * self.scale,
                    self.velocity.y + ENV.GRAVITY_ACCELERATION * self.scale,
                )
            elif (
                keys[pygame.K_SPACE] and self.jump_count == 1 and self.have_released_K_SPACE
            ):  # a double jump
                self.velocity.y = min(self.velocity.y, -PLAYER.DOUBLE_JUMP_POWER * self.scale)
                self.jump_time = pygame.time.get_ticks()
                self.can_jump = False
                self.jump_power_exists = True
                self.jump_count = 2
                self.have_released_K_SPACE = False
            else:
                self.velocity.y += ENV.GRAVITY_ACCELERATION * self.scale

        # combat
        if keys[pygame.K_j] and self.can_attack:
            attack_direction = "right" if self.horizontal_facing == Player.RIGHT else "left"
            if keys[pygame.K_w]:
                attack_direction = "up_" + attack_direction
            elif keys[pygame.K_s]:
                attack_direction = "down_" + attack_direction
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.create_attack(PLAYER.SWORD_LIFETIME, "sword", attack_direction)

    def collision(self, direction: int) -> None:
        if direction == 0:  # horizontal
            for obstacle in self.rect_obstacles:
                if self.hitbox.colliderect(obstacle.hitbox):
                    if self.velocity.x > 0:
                        self.hitbox.right = obstacle.hitbox.left
                    elif self.velocity.x < 0:
                        self.hitbox.left = obstacle.hitbox.right
                    self.velocity.x = 0
        elif direction == 1:  # vertical
            touch_ground = False
            for obstacle in self.rect_obstacles:
                if self.hitbox.colliderect(obstacle.hitbox):
                    if self.velocity.y > 0:  # touch floor
                        touch_ground = True
                        self.jump_count = 0
                        if not self.touch_ground:
                            self.touch_ground_time = pygame.time.get_ticks()
                        self.hitbox.bottom = obstacle.hitbox.top
                    elif self.velocity.y < 0:  # touch ceiling
                        self.hitbox.top = obstacle.hitbox.bottom
                    self.velocity.y = 0
            self.touch_ground = touch_ground

    def cooldown(self) -> None:
        current_time = pygame.time.get_ticks()
        # movement
        ## sprint
        if self.is_sprinting and current_time - self.sprint_time >= PLAYER.SPRINT_DURATION:
            self.is_sprinting = False
        if not self.can_sprint and current_time - self.sprint_time >= PLAYER.SPRINT_COOLDOWN:
            self.can_sprint = True
        ## jump
        if (
            not self.can_jump
            and self.touch_ground
            and current_time - self.touch_ground_time >= PLAYER.JUMP_COOLDOWN
        ):
            self.can_jump = True
        if self.jump_power_exists and current_time - self.jump_time >= PLAYER.JUMP_DURATION:
            self.jump_power_exists = False

        # combat
        ## attack
        if not self.can_attack and current_time - self.attack_time >= PLAYER.ATTACK_COOLDOWN:
            self.can_attack = True

    def friction(self) -> None:
        if self.velocity.x > 0 and self.touch_ground:
            self.velocity.x = max(0, self.velocity.x - ENV.FRICTION_ACCERATION * self.scale)
        elif self.velocity.x < 0 and self.touch_ground:
            self.velocity.x = min(0, self.velocity.x + ENV.FRICTION_ACCERATION * self.scale)

        self.velocity.x = self.velocity.x * (1 - ENV.AIR_FRICTION)

    def move(self) -> None:
        self.hitbox.x += int(self.velocity.x)
        self.collision(0)  # horizontal collision
        self.hitbox.y += int(self.velocity.y)
        self.collision(1)  # vertical collision
        self.rect.center = self.hitbox.center
        self.friction()

    def update(self) -> None:
        self.cooldown()
        self.input()
        self.move()
        display(self.velocity)
