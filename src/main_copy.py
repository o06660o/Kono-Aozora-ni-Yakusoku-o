import sys

import pygame

from settings import BASE
from keys import Keys
from level_dream import LevelDream as Level

import app_data

from menu import MenuForm

import speech_recognition as sr  #用于语音识别

import pyttsx3

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

        # 使用默认Microphone
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.audio = None

    def voice_recognition(self):
        pygame.mixer.music.unpause()
        try:
            # 使用Google Speech API进行识别，尝试中英文两种方式
            textZh = self.recognizer.recognize_google(self.audio, language='zh-CN')
            print(f"你说了：{textZh}")
            #textEn = r.recognize_google(audio, language='en-US')
            if textZh.find('退出')!=-1 or textZh.upper().find('EXIT')!=-1:
                #engine.say("即将退出游戏")
                #engine.runAndWait()
                sys.exit(0)
            elif textZh.find('开始')!=-1 or textZh.upper().find('START')!=-1:
                #engine.say("Game start")
                #engine.runAndWait()
                app_data.CurrentWin = app_data.AppForm.MAIN_FORM                
            elif textZh.find('声音')!=-1 and textZh.find('大')!=-1 or textZh.upper().find('UP')!=-1:
                vol = pygame.mixer.music.get_volume()+0.3
                if vol>1:
                    pygame.mixer.music.set_volume(1)
                else:
                    pygame.mixer.music.set_volume(vol)
            elif textZh.find('声音')!=-1 and textZh.find('小')!=-1 or textZh.upper().find('DOWN')!=-1:
                vol = pygame.mixer.music.get_volume()-0.3
                if vol<0:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(vol)
            elif textZh.find('静音')!=-1  or textZh.upper().find('mute')!=-1:
                pygame.mixer.music.set_volume(0)
            #print(f"你说了：{textZh}, You said: {textEn}")
        except sr.UnknownValueError:
            print("无法理解语音")
            self.engine.say("无法理解语音")
            self.engine.runAndWait()
        except sr.RequestError as e:
            print(f"识别服务连接错误；{e}")

    def run(self) -> None:
        while app_data.IsRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if app_data.CurrentWin == app_data.AppForm.MENU_FORM:  #CurrentWinName=="WIN_MENU"
                        self.frmMenu.onMouseDownHandler(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if app_data.CurrentWin == app_data.AppForm.MENU_FORM:
                        self.frmMenu.onMouseUpHandler(event)
                        self.frmMenu.onMouseClickHandler(event)
                elif event.type == pygame.MOUSEMOTION:
                    if app_data.CurrentWin == app_data.AppForm.MENU_FORM:  #CurrentWinName=="WIN_MENU"
                        self.frmMenu.onMouseMotionHandler(event)
                else:
                    if  event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: # 按了Esc键
                            if app_data.CurrentWin == app_data.AppForm.MAIN_FORM:
                                app_data.CurrentWin = app_data.AppForm.MENU_FORM
                                self.frmMenu.load()
                        elif event.key == pygame.K_SPACE and app_data.CurrentWin == app_data.AppForm.MENU_FORM: # 按了空格键
                            pygame.mixer.music.pause()
                            with sr.Microphone() as source:
                                print("请开始说话...")
                                self.audio = self.recognizer.listen(source)
                    elif event.type == pygame.KEYUP:  # 键盘按下
                        if event.key == pygame.K_SPACE and app_data.CurrentWin == app_data.AppForm.MENU_FORM: # 按了空格键
                            self.voice_recognition()
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
