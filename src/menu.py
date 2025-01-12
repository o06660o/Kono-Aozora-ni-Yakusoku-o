import pygame
import app_data
from settings import BASE
from scrollbar import ScrollBar


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, target, x, y):
        pygame.sprite.Sprite.__init__(self)  # 基类的init方法
        self.image = None
        self.rect = None
        self.target_surface = target
        self.master_image = None

        self.width = 1
        self.height = 1
        self.columns = 1
        self.stateImages = []
        self.currentStateIndex = 0
        self.x = x
        self.y = y

        # 加载声音文件
        self.sound = pygame.mixer.Sound("assets/sound/shoot.mp3")

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(
            filename
        ).convert_alpha()  # 加载整个菜单项图(可能包含多种状态)
        self.width = width  # 菜单项的宽度
        self.height = height  # 菜单项的高度
        self.rect = pygame.Rect(self.x, self.y, width, height)  # 菜单的显示位置
        self.columns = columns  # 整张图像包含的菜单列数
        rect = self.master_image.get_rect()  # 未分割的整张图的rect, 如(0, 0, 331, 292)

        n = (rect.width // width) * (rect.height // height)  # 计算整张图包含多少子项
        for i in range(n):
            row = i // columns
            col = i % columns
            rect = width * col, height * row, width, height
            self.stateImages.append(self.master_image.subsurface(rect))
        self.image = self.stateImages[0]

        # self.image.get_rect()切割后的当前图的rect, 如(0, 0, 331, 146); self.rect切割后的当前图在整个窗口中的rect, 如(470, 80, 331, 146)

    def update(self, currentTime, rate=90):
        # 更新动画帧
        pos = pygame.mouse.get_pos()
        # 如果鼠标光标在菜单项内部，光标形状改为“手型”，并播放提示音
        if (
            pos[0] >= self.rect[0]
            and pos[0] <= self.rect[0] + self.rect[2]
            and pos[1] >= self.rect[1]
            and pos[1] <= self.rect[1] + self.rect[3]
        ):
            if self.currentStateIndex == 0:
                self.sound.play()
            self.currentStateIndex = 1
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.currentStateIndex = 0
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # 修改菜单的显示图
        if self.currentStateIndex < len(self.stateImages):
            self.image = self.stateImages[self.currentStateIndex]


class MenuForm:
    def __init__(self):
        scale_x = pygame.display.Info().current_w  # / BASE.DEFAULT_SCREEN_WIDTH
        scale_y = pygame.display.Info().current_h  # / BASE.DEFAULT_SCREEN_HEIGHT
        self.scale = min(scale_x, scale_y)  # TODO: test for non integer `sacle` values

        self.MENU_WIN_SIZE = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )  # 菜单界面窗口大小
        self.screen = pygame.display.set_mode(self.MENU_WIN_SIZE)
        self.backgroundImage = pygame.image.load(
            "assets/graphics/menu/menu_bg.png"
        ).convert()  # 菜单窗口背景图
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, self.MENU_WIN_SIZE)
        self.group = pygame.sprite.Group()

        # 加载菜单项
        self.mitStart = MenuItem(self.screen, (pygame.display.Info().current_w-400)/2, 450)
        self.mitStart.load("assets/graphics/menu/btnStart.png", 400, 100, 1)
        self.mitSetting = MenuItem(self.screen, (pygame.display.Info().current_w-400)/2, 550)
        self.mitSetting.load("assets/graphics/menu/btnSetting.png", 400, 100, 1)
        self.mitQuit = MenuItem(self.screen, (pygame.display.Info().current_w-400)/2, 650)
        self.mitQuit.load("assets/graphics/menu/btnQuit.png", 400, 100, 1)

        self.scrollBar = ScrollBar(self.screen,200,100)

    def load(self):
        self.group.add(self.mitStart)
        self.group.add(self.mitSetting)
        self.group.add(self.mitQuit)

    def refresh(self, ticks):
        self.screen.blit(self.backgroundImage, (0, 0))
        self.group.update(ticks)
        self.group.draw(self.screen)
        self.scrollBar.refresh(ticks)

    def onMouseClickHandler(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if self.mitStart.rect.collidepoint(mouse_pos):
            app_data.CurrentWin = app_data.AppForm.MAIN_FORM
        if self.mitSetting.rect.collidepoint(mouse_pos):
            self.scrollBar.load()
        if self.mitQuit.rect.collidepoint(mouse_pos):
            app_data.IsRunning = False

    def onMouseDownHandler(self, event: pygame.event.Event):
        self.scrollBar.onMouseDownHandler(event)

            
    def onMouseUpHandler(self, event: pygame.event.Event):
        self.scrollBar.onMouseUpHandler(event)
        
    def onMouseMotionHandler(self, event: pygame.event.Event):
        self.scrollBar.onMouseMotionHandler(event)