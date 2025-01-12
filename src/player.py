import sys
import math

import pygame

from settings import BASE, ENV, PLAYER
from utils import create_rect_hitbox_image, read_images_as_list, display_message
from keys import Keys


class Player(pygame.sprite.Sprite):
    RIGHT = 1
    LEFT = -1
    IDLE = 0
    UP = 1
    DOWN = -1

    IMAGE_SCALE = 0.8

    def __init__(
        self,
        scale: float,
        pos: tuple[int | float, int | float],
        groups,
        rect_obstacles,
        create_attack,
        npc_sprites,
        sprite_type: str = "player",
    ) -> None:
        super().__init__(groups)
        # base
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.image = create_rect_hitbox_image(
            scale,
            (
                ENV.TILE_SIZE * PLAYER.WIDTH * Player.IMAGE_SCALE,
                ENV.TILE_SIZE * PLAYER.HEIGHT * Player.IMAGE_SCALE,
            ),
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect
        self.rect_obstacles = rect_obstacles
        self.horizontal_facing = Player.RIGHT
        self.vertical_facing = Player.IDLE
        self.prestatus = "idle"
        self.status = "idle"
        self.npc_sprites = npc_sprites
        now = pygame.time.get_ticks()
        self.sprite_type = sprite_type

        # keys
        self.keys = Keys()
        self.have_released_K_LSHIFT = True
        self.have_released_K_SPACE = True
        self.have_released_K_c = True
        self.have_released_K_j = True

        # movement
        self.velocity: pygame.Vector2 = pygame.math.Vector2()
        ## sprint
        self.can_sprint = True
        self.is_sprinting = False
        self.sprint_time = now
        ## stepback
        self.can_stepback = True
        self.is_steping_back = False
        self.stepback_time = now
        ## jump
        self.can_jump = False
        self.jump_count = 0
        self.jump_power_exists = False
        self.jump_time = now
        self.touch_ground = False
        self.touch_ground_time = now

        # combat
        self.health = PLAYER.HEALTH
        self.vulnerable = True
        self.last_hit_time = now
        self.create_attack = create_attack
        self.can_attack = True
        ## sword
        self.sword_time = now
        self.is_performing_sword = False
        self.is_performing_downattack = False
        ## throwing sword
        self.throwing_sword_time = now
        self.is_performing_throwing_sword = False
        ## magic
        self.magic = 3
        self.magic_time = now
        self.is_performing_magic = False

        # animation
        self.animations: dict[str, list[pygame.Surface]] = {
            "idle": read_images_as_list(scale * Player.IMAGE_SCALE, "assets/graphics/player/idle"),
            "walk": read_images_as_list(scale * Player.IMAGE_SCALE, "assets/graphics/player/walk"),
            "run": read_images_as_list(scale * Player.IMAGE_SCALE, "assets/graphics/player/walk"),
            "jump": read_images_as_list(scale * Player.IMAGE_SCALE, "assets/graphics/player/jump"),
            "sword": read_images_as_list(
                scale * Player.IMAGE_SCALE, "assets/graphics/player/sword"
            ),
            "throwing_sword": read_images_as_list(
                scale * Player.IMAGE_SCALE, "assets/graphics/player/throwing_sword"
            ),
            "magic": read_images_as_list(
                scale * Player.IMAGE_SCALE, "assets/graphics/player/magic"
            ),
        }
        self.frame_index = 0
        self.frame_rate: dict[str, float] = {
            "idle": 0.02,
            "walk": 0.13,
            "run": 0.2,
            "jump": 0.15,
            "sword": 0.15,
            "downattack": 0.15,
            "throwing_sword": 0.3,
            "magic": 0.15,
        }
        if "--DEBUG" not in sys.argv:
            self.image = self.animations["idle"][0]
        self.last_flash_time = now

        # npc
        self.talking_to = None
        self.is_recording_input = False

        # money
        self.money = 0

    def preinput(self) -> bool:
        if not self.have_released_K_LSHIFT and not self.keys.query(pygame.K_LSHIFT):
            self.have_released_K_LSHIFT = True
        if not self.have_released_K_SPACE and not self.keys.query(pygame.K_SPACE):
            self.have_released_K_SPACE = True
        if not self.have_released_K_c and not self.keys.query(pygame.K_c):
            self.have_released_K_c = True
        if not self.have_released_K_j and not self.keys.query(pygame.K_j):
            self.have_released_K_j = True
        # movement
        ## sprinting
        if self.is_sprinting:
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = PLAYER.SPRINT_SPEED * self.scale
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = -PLAYER.SPRINT_SPEED * self.scale
            self.velocity.y = 0
            return True
        ## steping back
        if self.is_steping_back:
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = -PLAYER.STEPBACK_SPEED * self.scale
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = PLAYER.STEPBACK_SPEED * self.scale
            self.velocity.y = 0
            return True
        # attack
        ## down attack
        if self.is_performing_downattack:
            angle = PLAYER.SWORD_DOWNATTACK_ANGLE
            speed = PLAYER.SWORD_DOWNATTACK_SPEED * self.scale
            self.velocity.x = speed * math.cos(math.radians(angle))
            if self.horizontal_facing == Player.LEFT:
                self.velocity.x = -self.velocity.x
            self.velocity.y = speed * math.sin(math.radians(angle))
            return True
        ## magic
        if self.is_performing_magic or self.is_performing_throwing_sword:
            self.velocity.x = 0
            self.velocity.y = 0
            return True
        # npc
        if self.is_recording_input:
            return True

        return False

    def input(self) -> None:
        now = pygame.time.get_ticks()
        # movement
        ## horizontal
        ### begin sprint
        if self.keys.query(pygame.K_LSHIFT) and self.can_sprint and self.have_released_K_LSHIFT:
            self.can_sprint = False
            self.is_sprinting = True
            self.have_released_K_LSHIFT = False
            self.sprint_time = now
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = max(self.velocity.x, PLAYER.SPRINT_SPEED * self.scale)
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = min(self.velocity.x, -PLAYER.SPRINT_SPEED * self.scale)
        ### begin step back
        if (
            self.keys.query(pygame.K_c)
            and self.can_stepback
            and self.have_released_K_c
            and self.velocity.x == 0
        ):
            self.can_stepback = False
            self.is_steping_back = True
            self.have_released_K_c = False
            self.stepback_time = now
            if self.horizontal_facing == Player.RIGHT:
                self.velocity.x = min(self.velocity.x, -PLAYER.STEPBACK_SPEED * self.scale)
            elif self.horizontal_facing == Player.LEFT:
                self.velocity.x = max(self.velocity.x, PLAYER.STEPBACK_SPEED * self.scale)
        ### walk and running
        if self.keys.query(pygame.K_a) and self.keys.query(pygame.K_d):
            self.velocity.x = 0
        elif self.keys.query(pygame.K_a):
            self.velocity.x = min(self.velocity.x, -PLAYER.SPEED * self.scale)
            if self.keys.query(pygame.K_LSHIFT) == 2:
                self.velocity.x = min(self.velocity.x, -PLAYER.RUN_SPEED * self.scale)
                self.status = "run"
            else:
                self.status = "walk"
            self.horizontal_facing = Player.LEFT
        elif self.keys.query(pygame.K_d):
            self.velocity.x = max(self.velocity.x, PLAYER.SPEED * self.scale)
            if self.keys.query(pygame.K_LSHIFT) == 2:
                self.velocity.x = max(self.velocity.x, PLAYER.RUN_SPEED * self.scale)
                self.status = "run"
            else:
                self.status = "walk"
            self.horizontal_facing = Player.RIGHT
        ## vertical
        if self.touch_ground:
            if self.keys.query(pygame.K_SPACE) and self.can_jump:  # a jump starts
                self.velocity.y = min(self.velocity.y, -PLAYER.JUMP_POWER * self.scale)
                self.jump_time = now
                self.can_jump = False
                self.jump_power_exists = True
                self.touch_ground = False
                self.jump_count = 1
                self.have_released_K_SPACE = False
            else:
                self.velocity.y += ENV.GRAVITY_ACCELERATION * self.scale
        else:
            if self.keys.query(pygame.K_SPACE) and self.jump_power_exists:  # a jump continuing
                self.velocity.y = min(
                    -PLAYER.JUMP_POWER * self.scale,
                    self.velocity.y + ENV.GRAVITY_ACCELERATION * self.scale,
                )
            elif (
                self.keys.query(pygame.K_SPACE)
                and self.jump_count == 1
                and self.have_released_K_SPACE
            ):  # a double jump
                self.velocity.y = min(self.velocity.y, -PLAYER.DOUBLE_JUMP_POWER * self.scale)
                self.jump_time = now
                self.can_jump = False
                self.jump_power_exists = True
                self.jump_count = 2
                self.have_released_K_SPACE = False
            else:
                self.velocity.y += ENV.GRAVITY_ACCELERATION * self.scale
        if self.keys.query(pygame.K_w) and not self.keys.query(pygame.K_s):
            self.vertical_facing = Player.UP
        elif self.keys.query(pygame.K_s) and not self.keys.query(pygame.K_w):
            self.vertical_facing = Player.DOWN
        else:
            self.vertical_facing = Player.IDLE
        # combat
        ## sword
        if self.have_released_K_j and self.keys.query(pygame.K_j) and self.can_attack:
            flag = True  # whether the player can attack or not
            attack_direction = "right" if self.horizontal_facing == Player.RIGHT else "left"
            # TODO: up attack and down attack are not implemented
            # if self.vertical_facing == Player.UP:
            #     attack_direction = "up_" + attack_direction
            # elif self.vertical_facing == Player.DOWN:
            #     if self.touch_ground:
            #         flag = False  # the player cannot attack downward when standing on the ground
            #     self.is_performing_downattack = True
            #     attack_direction = "down_" + attack_direction
            if flag:
                if not self.is_performing_downattack:
                    self.is_performing_sword = True
                self.can_attack = False
                self.have_released_K_j = False
                self.sword_time = now
                self.create_attack("sword", attack_direction)

        ## throwing sword
        if self.keys.query(pygame.K_h) and self.can_attack:
            attack_direction = "right" if self.horizontal_facing == Player.RIGHT else "left"
            self.can_attack = False
            self.throwing_sword_time = now
            self.is_performing_throwing_sword = True
            self.create_attack("throwing_sword", attack_direction)

        ## magic
        if (
            self.magic > 0
            and not self.touch_ground
            and self.keys.query(pygame.K_u)
            and self.can_attack
        ):
            self.magic -= 1
            self.is_performing_magic = True
            self.can_attack = False
            self.magic_time = now
            self.create_attack("magic")

        # npc
        if not self.is_recording_input and self.keys.query(pygame.K_SLASH):
            self.is_recording_input = True
        if self.talking_to is not None and self.keys.query(pygame.K_t):
            self.talking_to.clear_messages()
            self.talking_to = None

    def collision(self, direction: int) -> None:
        if direction == 0:  # horizontal
            for obstacle in self.rect_obstacles:
                if self.hitbox.colliderect(obstacle.hitbox):
                    if self.velocity.x > 0:
                        self.hitbox.right = obstacle.hitbox.left
                    elif self.velocity.x < 0:
                        self.hitbox.left = obstacle.hitbox.right
                    self.velocity.x = 0
                    if self.is_performing_downattack:
                        self.is_performing_downattack = False
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
                    if self.is_performing_downattack:
                        self.is_performing_downattack = False
            self.touch_ground = touch_ground

            if touch_ground or self.velocity.y == 0:
                if self.status == "jump":
                    self.status = "idle"
            else:
                self.status = "jump"

    def cooldown(self) -> None:
        current_time = pygame.time.get_ticks()
        # movement
        ## sprint
        if self.is_sprinting and current_time - self.sprint_time >= PLAYER.SPRINT_DURATION:
            self.is_sprinting = False
        if not self.can_sprint and current_time - self.sprint_time >= PLAYER.SPRINT_COOLDOWN:
            self.can_sprint = True
        ## stepback
        if self.is_steping_back and current_time - self.stepback_time >= PLAYER.STEPBACK_DURATION:
            self.is_steping_back = False
        if not self.can_stepback and current_time - self.stepback_time >= PLAYER.STEPBACK_COOLDOWN:
            self.can_stepback = True
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
        if not self.vulnerable and current_time - self.last_hit_time >= PLAYER.VULNERABLE_TIME:
            self.vulnerable = True
        if (
            not self.can_attack
            and current_time - self.sword_time >= PLAYER.SWORD_COOLDOWN
            and current_time - self.throwing_sword_time >= PLAYER.THROWING_SWORD_COOLDOWN
            and current_time - self.magic_time >= PLAYER.MAGIC_COOLDOWN
        ):
            self.can_attack = True
        if self.is_performing_sword and current_time - self.sword_time >= PLAYER.SWORD_LIFETIME:
            self.is_performing_sword = False
        if self.is_performing_magic and current_time - self.magic_time >= PLAYER.MAGIC_LIFETIME:
            self.is_performing_magic = False
        if (
            self.is_performing_throwing_sword
            and current_time - self.throwing_sword_time >= PLAYER.THORWING_SWORD_DURATION
        ):
            self.is_performing_throwing_sword = False
        # npc
        if self.is_recording_input and self.keys.query(pygame.K_RETURN):
            self.is_recording_input = False
            message = self.keys.query_recorded_text()
            if message != "" and self.talking_to is not None:
                self.talking_to.fetch_message(message)

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
        if self.velocity.x == 0 and self.touch_ground:
            self.status = "idle"
        self.rect.center = self.hitbox.center
        self.friction()

    def animate(self) -> None:
        if self.is_performing_sword:
            self.status = "sword"
        if self.is_performing_magic:
            self.status = "magic"
        if self.is_performing_downattack:
            self.status = "downattack"
        if self.is_performing_throwing_sword:
            self.status = "throwing_sword"
        if self.status != self.prestatus:
            if (self.status == "run" and self.prestatus == "walk") or (
                self.status == "walk" and self.prestatus == "run"
            ):
                pass
            else:
                self.frame_index = 0
            self.prestatus = self.status
        self.frame_index += self.frame_rate[self.status]
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == "jump":
                self.frame_index = 5
            elif self.status == "throwing_sword":
                self.frame_index = 1
            else:
                self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        # TODO: turning animation is not implemented
        if self.horizontal_facing == Player.RIGHT:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def npc_interaction(self) -> None:
        if self.talking_to is None:
            if self.keys.query(pygame.K_e):
                for npc in self.npc_sprites:
                    if self.hitbox.colliderect(npc.hitbox):
                        self.talking_to = npc
                        npc.fetch_message("Hello")
        else:
            if self.keys.query(pygame.K_r):
                self.talking_to = None
            else:
                display_message(
                    self.scale,
                    PLAYER.TALKING_POS,
                    BASE.WRAPLEN,
                    self.talking_to.displaying_message,
                )

    def flash(self) -> None:
        """
        Flash the player when it is hit by an enemy.
        """
        if self.vulnerable:
            self.image.set_alpha(255)
            return
        now = pygame.time.get_ticks()
        if now - self.last_flash_time >= PLAYER.FLASH_INTERVAL:
            self.last_flash_time = now
            if self.image.get_alpha() == 192:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(192)

    def update(self) -> None:
        self.cooldown()
        if not self.preinput():
            self.input()
        self.move()
        if "--DEBUG" not in sys.argv:
            self.animate()
        self.npc_interaction()
        if self.is_recording_input:
            display_message(
                self.scale, PLAYER.RECORDING_POS, BASE.WRAPLEN, self.keys.query_recorded_text()
            )
        self.flash()
