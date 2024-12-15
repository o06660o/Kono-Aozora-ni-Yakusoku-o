class BASE:
    """
    The base settings for the game.
    """

    WIDTH = 1280
    HEIGHT = 720
    DEFAULT_SCREEN_WIDTH = 1920
    DEFAULT_SCREEN_HEIGHT = 1080
    FPS = 60
    LONG_PRESS_TIME = 200  # the time in milliseconds to recognize a long press


class ENV:
    """
    The settings for the environment.
    """

    TILE_SIZE = 64
    GRAVITY_ACCELERATION = 2
    FRICTION_ACCERATION = 4
    AIR_FRICTION = 0.08  # the `k` in formula $f = -kv$


class PLAYER:
    """
    The settings for the player.
    """

    # movements
    SPEED = 8
    SPRINT_SPEED = 20
    SPRINT_DURATION = 220
    SPRINT_COOLDOWN = 800
    JUMP_POWER = 25
    DOUBLE_JUMP_POWER = 12
    JUMP_POWER_MIN = 8
    JUMP_DURATION = 200
    JUMP_COOLDOWN = (
        100  # the time in milliseconds the player can jump again after touching the ground
    )

    # combat
    ATTACK_COOLDOWN = 500
    ## sword
    SWORD_LIFETIME = 200
    SWORD_LENGTH = 2.5  # the length of the sword relative to `TILE_SIZE`
    SWORD_WIDTH = 0.6  # the width of the sword relative to `TILE_SIZE`
    SWORD_ROTATE_ANGLE = 150
