# base settings
WIDTH = 1280
HEIGHT = 720
DEFAULT_SCREEN_WIDTH = 1920
DEFAULT_SCREEN_HEIGHT = 1080
FPS = 60

# character settings
## common
### combat
SWORD_LENGTH = 2.5  # the length of the sword relative to `TILE_SIZE`
SWORD_WIDTH = 0.6  # the width of the sword relative to `TILE_SIZE`
SWORD_ROTATE_ANGLE = 150
## player
### movements
PLAYER_SPEED = 8
PLAYER_SPRINT_SPEED = 20
PLAYER_SPRINT_DURATION = 220
PLAYER_SPRINT_COOLDOWN = 800
PLAYER_JUMP_POWER = 35
PLAYER_DOUBLE_JUMP_POWER = 25
PLAYER_JUMP_POWER_MIN = 15
PLAYER_JUMP_DURATION = 250
PLAYER_JUMP_COOLDOWN = (
    100  # the time in milliseconds the player can jump again after touching the ground
)
### combat
PLAYER_ATTACK_COOLDOWN = 500
PLAYER_SWORD_LIFETIME = 200

# environment settings
TILE_SIZE = 64
GRAVITY_ACCELERATION = 2
FRICTION_ACCERATION = 4
AIR_FRICTION = 0.08  # the `k` in formula $f = -kv$
