from openai import OpenAI
import pygame

from utils import sanitize_message
from settings import ENV
from settings import NPC as NPC_SETTINGS
from utils import create_rect_hitbox_image
from pygame.locals import *

class DialogBox:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
        self.text_surface = None
        self.text_rect = None
        self.border_color = (0, 0, 0)
        # 设置背景颜色为透明
        self.background_color = (0, 0, 0, 0)  
        self.text_color = (0, 0, 0)
        self.padding = 10
        self.displaying_message = ""
    
        
    def set_text(self, text):
        text = sanitize_message(text)
        self.displaying_message = text
        max_width = self.rect.width - 2 * self.padding
        # split text into lines
        words = text.split(' ')
        lines = []
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + ' ' + word
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        wrapped_text = []
        for line in lines:
            line_surface = self.font.render(line, True, self.text_color, self.background_color)
            wrapped_text.append(line_surface)
       
        total_height = sum([line.get_height() for line in wrapped_text])
        
        self.text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        self.text_surface.fill(self.background_color)
        y = 0
        for line in wrapped_text:
            self.text_surface.blit(line, (0, y))
            y += line.get_height()
        # 设置文本矩形的位置
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        # 创建一个具有 alpha 通道的表面
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # 绘制透明背景
        pygame.draw.rect(surface, self.background_color, self.rect)
        # 绘制边框
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        # 设置文本
        self.set_text(self.displaying_message)
        # 如果有文本表面，绘制文本
        if self.text_surface:
            surface.blit(self.text_surface, self.text_rect)
        # 将表面绘制到屏幕上
        self.screen.blit(surface, self.rect.topleft)
      
class NPC(pygame.sprite.Sprite):
    def __init__(self, scale, pos, groups, npc_type):
        super().__init__(groups)
        self.scale = scale
        self.pos = (pos[0] * scale, pos[1] * scale)
        self.image = create_rect_hitbox_image(
            scale,
            (
                NPC_SETTINGS.WIDTH * ENV.TILE_SIZE * scale,
                NPC_SETTINGS.HEIGHT * ENV.TILE_SIZE * scale,
            ),
        )
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect
        try:
            self.client = OpenAI(
                base_url="http://10.15.88.73:5010/v1",
                api_key="ollama",  # required but ignored
            )
        except Exception as e:
            assert False, f"OpenAI client failed to initialize: {e}"
        self.displaying_message = "test message"
        self.init_message = NPC_SETTINGS.INIT_MESSAGE[npc_type]
        self.messages: list[dict] = self.init_message
        self.dialog_box = DialogBox(pygame.display.get_surface(), 100, 400, 600, 200)
        self.is_dialog_active = False  # 新增：对话状态变量

    def fetch_message(self, new_message: str) -> None:
        try:
            self.messages.append(
                {
                    "role": "user",
                    "content": new_message,
                }
            )
            response = self.client.chat.completions.create(
                model="llama3.2",
                messages=self.messages,  # pyright: ignore
            )
            assistant_reply = response.choices[0].message.content
            self.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply,
                }
            )
            self.displaying_message = assistant_reply
            self.dialog_box.set_text(self.displaying_message)
            self.is_dialog_active = True  # 新增：设置对话状态为激活
            self.dialog_box.draw()  # 新增：绘制对话框
        except Exception as e:
            print(f"Error fetching message: {e}")
            self.is_dialog_active = False

    def clear_messages(self) -> None:
        self.messages = self.init_message
        self.dialog_box.set_text(self.init_message[0]['content'])
        self.is_dialog_active = False  # 新增：设置对话状态为非激活

    def update(self):
        if self.is_dialog_active:  # 新增：根据对话状态决定是否绘制对话框
            self.dialog_box.draw()