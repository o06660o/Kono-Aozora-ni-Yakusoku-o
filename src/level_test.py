from settings import BASE, ENV
from level import Level
from tile import Tile
from player import Player
from utils import create_rect_hitbox_image


class Level_test(Level):
    def __init__(self, scale: float) -> None:
        super().__init__(scale)

    def create_map(self) -> None:
        self.floor = Tile(
            self.scale,
            (-BASE.DEFAULT_SCREEN_WIDTH * 0.6, 0),
            [self.visible_sprites, self.obstacle_sprites],
            "floor",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 1.2, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )
        self.left_wall = Tile(
            self.scale,
            (-BASE.DEFAULT_SCREEN_WIDTH * (0.6 + 0.1), -BASE.DEFAULT_SCREEN_HEIGHT),
            [self.visible_sprites, self.obstacle_sprites],
            "wall",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 0.1, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )
        self.right_wall = Tile(
            self.scale,
            (BASE.DEFAULT_SCREEN_WIDTH * 0.6, -BASE.DEFAULT_SCREEN_HEIGHT),
            [self.visible_sprites, self.obstacle_sprites],
            "wall",
            create_rect_hitbox_image(
                # do not need to scale again
                1,
                (BASE.DEFAULT_SCREEN_WIDTH * 0.1, BASE.DEFAULT_SCREEN_HEIGHT),
                color="green",
            ),
        )

        Tile(
            self.scale,
            (ENV.TILE_SIZE * -15, -ENV.TILE_SIZE * 7),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            create_rect_hitbox_image(
                1,
                (ENV.TILE_SIZE * 10, ENV.TILE_SIZE),
                color="black",
            ),
        )
        Tile(
            self.scale,
            (ENV.TILE_SIZE * 5, -ENV.TILE_SIZE * 10),
            [self.visible_sprites, self.obstacle_sprites],
            "blocks",
            create_rect_hitbox_image(
                1,
                (ENV.TILE_SIZE * 10, ENV.TILE_SIZE),
                color="black",
            ),
        )

        # if "--DEBUG" in sys.argv:
        # self.player = FreeCamera(self.scale, [self.visible_sprites])
        # else:
        #     self.player = Player(
        #         self.scale,
        #         (0, 0),
        #         [self.visible_sprites],
        #         self.obstacle_sprites,
        #         self.create_attack,
        #     )
        self.player = Player(
            self.scale,
            (0, ENV.TILE_SIZE * -2),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
        )
