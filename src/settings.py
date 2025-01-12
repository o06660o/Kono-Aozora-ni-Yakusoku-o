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
    WRAPLEN = 500
    DEATH_DURATION = 100


class ENV:
    """
    The settings for the environment.
    """

    TILE_SIZE = 64
    GRAVITY_ACCELERATION = 2
    FRICTION_ACCERATION = 3.5
    AIR_FRICTION = 0.08  # the `k` in formula $f = -kv$

    class LEVEL_DREAM:
        IMAGE_SCALE = 2
        FLOOR_HITBOX_OFFSET = (0, 0)
        PLAT_HITBOX_OFFSET = (30, 145)
        GROUND_HITBOX_OFFSET = (0, 500)
        PLAT2_HITBOX_OFFSET = (0, 265)
        PLAT_LARGE_HITBOX_OFFSET = (40, 10)
        PLAT_MID_HITBOX_OFFSET = (20, 10)
        PLAT_SMALL_HITBOX_OFFSET = (15, 10)
        NO_HITBOX_OFFSET = (0, 0)


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
    HEALTH = 8
    VULNERABLE_TIME = 600
    FLASH_INTERVAL = 100
    UPGRADE_DAMAGE = 100
    UPGRADE_COST = 10
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

    # input
    RECORDING_POS = (640, 0)
    TALKING_POS = (0, 180)


class NPC:
    """
    The settings for the NPC.
    """

    WIDTH = 1  # the width of the player relative to `TILE_SIZE`
    HEIGHT = 1.5  # the height of the player relative to `TILE_SIZE`
    SCALE = 1.2
    INIT_MESSAGE = {
        "tutorial": [
            {
                "role": "system",
                "content": "Suppose that you are the guide of the game. Here are some keybindings in the game:\n\n - `<A>` `<D>` to move left and right\n - `<Space>` to jump\n - `<Shift>` to sprint (holding to run) \n - `<C>` to backstep\n - `<J>` to attack\n - `<H>` to throw the sword\n - `<U>` to use magic\n - `<E>` to start a conversation and `<R>` to end it\n - `/` to start typing the response and `<Enter>` to send it.\n\n\n Now the player is going to play the game. You can start the conversation by pressing `<E>`. Now you are going to tell the player how to move around and attack enemies. And the way to win the game is to kill all enemies. You only need to talk those information to the player.",
            }
        ],
        "blacksmith": [
            {
                "role": "system",
                "content": f"Suppose that you are the blacksmith of the game. You can tell the player press `<B>` to upgrade the sword if the player has enough coins. The price for upgrading once is {PLAYER.UPGRADE_COST} coins. The only way to collect coins is to kill the enemies. You only need to talk those information to the player.",
            },
        ],
    }


class ENEMY:
    """
    The settings for the enemy.
    """

    INFO = {
        "centipede": {
            "width": 1.8,
            "height": 0.3,
            "health": 300,
            "damage": 1,
            "status": "move",
            "scale": 0.8,
        }
    }
    # `key`: frame name, `value`: frame rate
    ANIMATIONS = {"centipede": {"move": 0.1, "death": 0}}
    SPEED = {"centipede": 3}
    VULNERABLE_TIME = 600

    class CENTIPEDE:
        MOVE_LEN = 400
        TURN_PROBABILTY = 0.03
