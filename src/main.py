import sys

import pygame

from settings import BASE
from keys import Keys
from level_dream import LevelDream as Level
import app_data
import menu
from menu import MenuForm
# from level_dream import print_health

class Game:
    def __init__(self) -> None:
        pygame.init()
        scale_x = pygame.display.Info().current_w / BASE.DEFAULT_SCREEN_WIDTH
        scale_y = pygame.display.Info().current_h / BASE.DEFAULT_SCREEN_HEIGHT
        print("scale1:",scale_x,scale_y)
        self.scale = min(scale_x, scale_y)  # TODO: test for non integer `sacle` values
        self.screen = pygame.display.set_mode(
            (int(BASE.WIDTH * self.scale), int(BASE.HEIGHT * self.scale))
        )
        self.clock = pygame.time.Clock()

        # 设置窗口图标及标题
        pygame.display.set_icon(pygame.image.load("assets/graphics/icon.png").convert())
        pygame.display.set_caption("Shadow Knight")

        # background music
        pygame.mixer.music.load('assets/sound/Christopher Larkin - City of Tears.mp3')  
        pygame.mixer.music.set_volume(0.1)  
        pygame.mixer.music.play(-1)  

        self.keys = Keys()
        # self.world = World(self.scale)
        self.world = Level(self.scale)

        self.frmMenu = MenuForm()
        self.frmMenu.load() 
        app_data.IsRunning = True

    def run(self) -> None:
        while app_data.IsRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if app_data.CurrentWin == app_data.AppForm.MENU_FORM:
                        self.frmMenu.onMouseClickHandler(event)
                else:
                    self.keys.update(event)

            if app_data.CurrentWin == app_data.AppForm.MENU_FORM:
                self.frmMenu.refresh(pygame.time.get_ticks())
            else:
                self.screen.fill("lightblue")
                self.world.draw()
                self.world.print_health() # 最后blit血量
            pygame.display.update()
            self.clock.tick(BASE.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
