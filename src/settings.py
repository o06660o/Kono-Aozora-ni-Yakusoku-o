class BASE:
    """
    The base settings for the game.
    """

    WIDTH = 1280
    HEIGHT = 720
    DEFAULT_SCREEN_WIDTH = 1920
    DEFAULT_SCREEN_HEIGHT = 1080
    FPS = 60
    LONG_PRESS_TIME = 400  # the time to recognize a long press


class ENV:
    """
    The settings for the environment.
    """

    TILE_SIZE = 64
    GRAVITY_ACCELERATION = 2
    FRICTION_ACCERATION = 3.5
    AIR_FRICTION = 0.08  # the `k` in formula $f = -kv$


class PLAYER:
    """
    The settings for the player.
    """

    # base
    WIDTH = 1.3  # the width of the player relative to `TILE_SIZE`
    HEIGHT = 2.8  # the height of the player relative to `TILE_SIZE`
    # movements
    SPEED = 10
    RUN_SPEED = 14
    SPRINT_SPEED = 18
    SPRINT_DURATION = 250
    SPRINT_COOLDOWN = 800
    STEPBACK_SPEED = 18
    STEPBACK_DURATION = 150
    STEPBACK_COOLDOWN = 800
    JUMP_POWER = 25
    DOUBLE_JUMP_POWER = 12
    JUMP_POWER_MIN = 8
    JUMP_DURATION = 200
    JUMP_COOLDOWN = 100  # the time the player can jump again after touching the ground
    # combat
    # ATTACK_COOLDOWN = 600
    ## sword
    SWORD_LIFETIME = 200
    SWORD_LENGTH = 3.8  # the length of the sword relative to `TILE_SIZE`
    SWORD_WIDTH = 4.2  # the width of the sword relative to `TILE_SIZE`
    SWORD_ROTATE_ANGLE = 150
    SWORD_COOLDOWN = 500
    SWORD_DOWNATTACK_ANGLE = 60
    SWORD_DOWNATTACK_SPEED = 30
    ## throwing the sword
    THROWING_SWORD_LENGTH = 4  # the length of the sword relative to `TILE_SIZE`
    THROWING_SWORD_WIDTH = 0.6  # the width of the sword relative to `TILE_SIZE`
    THROWING_SWORD_FLYINGTIME = 150
    THROWING_SWORD_STOPTIME = 50  # the time the sword stops after reaching the farthest distance
    THROWING_SWORD_SPEED = 40
    THROWING_SWORD_COOLDOWN = 500
    THORWING_SWORD_DURATION = 500
    ## magic
    MAGIC_LIFETIME = 400
    MAGIC_LENGTH = 7
    MAGIC_WIDTH = 5
    MAGIC_COOLDOWN = 1000
    # # misc
    # LOOKING_OFFSET = 600
    # LOOKING_DURATION = 200  # the time for the background to move when looking up/down
