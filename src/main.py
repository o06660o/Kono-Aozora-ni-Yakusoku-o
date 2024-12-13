import sys
import pygame
from settings import WIDTH, HEIGHT, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, FPS

# from world import World
from level_test import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        scale_x = pygame.display.Info().current_w / DEFAULT_SCREEN_WIDTH
        scale_y = pygame.display.Info().current_h / DEFAULT_SCREEN_HEIGHT
        self.scale = min(scale_x, scale_y)  # TODO: test for non integer `sacle` values
        self.screen = pygame.display.set_mode((int(WIDTH * self.scale), int(HEIGHT * self.scale)))
        self.clock = pygame.time.Clock()
        # TODO: a title and icon for the window needed

        # self.world = World(self.scale)
        self.world = Level(self.scale)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("lightblue")
            self.world.draw()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
