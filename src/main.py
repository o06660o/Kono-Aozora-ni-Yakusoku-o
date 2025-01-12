import sys

import pygame

from settings import BASE
from keys import Keys
from level_dream import LevelDream as Level

import app_data

from menu import MenuForm


class Game:
    def __init__(self) -> None:
        pygame.init()
        scale_x = pygame.display.Info().current_w / BASE.DEFAULT_SCREEN_WIDTH
        scale_y = pygame.display.Info().current_h / BASE.DEFAULT_SCREEN_HEIGHT
        self.scale = min(scale_x, scale_y)  # TODO: test for non integer `sacle` values

        self.game_over = False
        self.screen = pygame.display.set_mode(
            (int(BASE.WIDTH * self.scale), int(BASE.HEIGHT * self.scale))
        )
        self.clock = pygame.time.Clock()

        # 设置窗口图标及标题
        pygame.display.set_icon(pygame.image.load("assets/graphics/icon.png").convert_alpha())
        pygame.display.set_caption("Shadow Knight")

        # background music
        if not self.game_over:
            pygame.mixer.music.load("assets/sound/Christopher Larkin - City of Tears.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load("assets/sound/win.mp3")
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
                    if  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # 按了Esc键
                        if app_data.CurrentWin == app_data.AppForm.MAIN_FORM:
                            app_data.CurrentWin = app_data.AppForm.MENU_FORM
                            self.frmMenu.load()
                    self.keys.update(event)

            if app_data.CurrentWin == app_data.AppForm.MENU_FORM:
                self.frmMenu.refresh(pygame.time.get_ticks())
            else:
                if Level.win_check(self.world):
                    if not self.game_over:
                        Level.print_win(self.world)
                        self.game_over = True  
                        pygame.mixer.music.load("assets/sound/win.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                else:
                    self.screen.fill("lightblue")
                    self.world.draw()
                    self.world.print_health()  # 最后blit血量

            pygame.display.update()
            self.clock.tick(BASE.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
