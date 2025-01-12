import sys
import pygame
import app_data

import speech_recognition as sr  # 用于语音识别
import pyttsx3


class SpeechRecog:
    def __init__(self):
        # 使用默认Microphone
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.audio = None

    def recognition(self):
        pygame.mixer.music.unpause()
        try:
            # 使用Google Speech API进行识别，尝试中英文两种方式
            textZh = self.recognizer.recognize_google(self.audio, language="zh-CN")
            print(f"You said：{textZh}")
            # textEn = r.recognize_google(audio, language='en-US')
            if textZh.find("退出") != -1 or textZh.upper().find("EXIT") != -1:
                self.engine.say("即将退出游戏")
                self.engine.runAndWait()
                sys.exit(0)
            elif textZh.find("开始") != -1 or textZh.upper().find("START") != -1:
                self.engine.say("Game start")
                self.engine.runAndWait()
                app_data.CurrentWin = app_data.AppForm.MAIN_FORM
            elif (
                textZh.find("声音") != -1
                and textZh.find("大") != -1
                or textZh.upper().find("UP") != -1
            ):
                vol = pygame.mixer.music.get_volume() + 0.3
                if vol > 1:
                    pygame.mixer.music.set_volume(1)
                else:
                    pygame.mixer.music.set_volume(vol)
            elif (
                textZh.find("声音") != -1
                and textZh.find("小") != -1
                or textZh.upper().find("DOWN") != -1
            ):
                vol = pygame.mixer.music.get_volume() - 0.3
                if vol < 0:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(vol)
            elif textZh.find("静音") != -1 or textZh.upper().find("mute") != -1:
                pygame.mixer.music.set_volume(0)
            # print(f"你说了：{textZh}, You said: {textEn}")
        except sr.UnknownValueError:
            print("无法理解你说的语音")
            self.engine.say("无法理解你说的语音")
            self.engine.runAndWait()
        except sr.RequestError as e:
            print(f"识别服务连接失败；{e}")

    def listenSpeech(self):
        with sr.Microphone() as source:
            print("请开始说话...")
            self.audio = self.recognizer.listen(source)

