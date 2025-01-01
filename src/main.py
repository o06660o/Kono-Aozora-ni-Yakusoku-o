import sys

import pygame

from settings import BASE
from keys import Keys
from level_dream import LevelDream as Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        scale_x = pygame.display.Info().current_w / BASE.DEFAULT_SCREEN_WIDTH
        scale_y = pygame.display.Info().current_h / BASE.DEFAULT_SCREEN_HEIGHT
        self.scale = min(scale_x, scale_y)  # TODO: test for non integer `sacle` values
        self.screen = pygame.display.set_mode(
            (int(BASE.WIDTH * self.scale), int(BASE.HEIGHT * self.scale))
        )
        self.clock = pygame.time.Clock()
        # TODO: a title and icon for the window needed
        # 设置窗口图标及标题
        pygame.display.set_icon(pygame.image.load('assets\\graphics\\icon.png').convert())
        pygame.display.set_caption('Shadow Knight')

        self.keys = Keys()
        # self.world = World(self.scale)
        self.world = Level(self.scale)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.keys.update(event)

            self.screen.fill("lightblue")
            self.world.draw()
            pygame.display.update()
            self.clock.tick(BASE.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
