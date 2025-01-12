import pygame

import app_data

class Bar(pygame.sprite.Sprite):
    def __init__(self, target, x, y):
        pygame.sprite.Sprite.__init__(self) # 基类的init方法
        self.image = None
        self.rect = None
        self.target_surface = target
              
        self.width = 1
        self.height = 1

        self.x = x
        self.y = y
        
    def load(self, filename, width, height):
        self.image = pygame.image.load(filename).convert_alpha()  #加载滚动条图
        self.width = width      # 菜单项的宽度
        self.height = height    # 菜单项的高度
        self.rect = pygame.Rect(self.x,self.y,width,height)  #滚动条显示位置

        
    def update(self, currentTime, rate=90):
        #更新动画帧
        #print("currentTime {}\n".format(currentTime))
        #if(self.image.is)
        pos = pygame.mouse.get_pos()
        # 创建鼠标光标的矩形
        '''
        if pos[0]>=self.rect[0] and pos[0]<=self.rect[0]+self.rect[2] and pos[1]>=self.rect[1] and pos[1]<=self.rect[1]+self.rect[3]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        '''
            
class Cursor(pygame.sprite.Sprite):
    def __init__(self, target, x, y):
        pygame.sprite.Sprite.__init__(self) # 基类的init方法
        self.image = None
        self.rect = None
        self.target_surface = target
              
        self.width = 1
        self.height = 1

        self.x = x
        self.y = y
        
    def load(self, filename, width, height):
        self.image = pygame.image.load(filename).convert_alpha()  #加载滚动条图
        self.width = width      # 菜单项的宽度
        self.height = height    # 菜单项的高度
        self.rect = pygame.Rect(self.x,self.y,width,height)  #滚动条显示位置

        
    def update(self, currentTime, rate=90):
        #更新动画帧
        #print("currentTime {}\n".format(currentTime))
        #if(self.image.is)
        pos = pygame.mouse.get_pos()
        # 创建鼠标光标的矩形
        if pos[0]>=self.rect[0] and pos[0]<=self.rect[0]+self.rect[2] and pos[1]>=self.rect[1] and pos[1]<=self.rect[1]+self.rect[3]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            print("CURSOR_HAND")
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
class ScrollBar:
    def __init__(self,target,x,y):
        self.screen = target
        self.x = x
        self.y = y
        self.group = pygame.sprite.Group() 
        self.bar = Bar(self.screen,x,y)
        self.bar.load('assets/graphics/menu/bar.png', 10, 500)
        self.cursor = Cursor(self.screen,x-15,y)
        self.cursor.load('assets/graphics/menu/cursor.png', 40, 40)
        
        self.cursorSelected = False
    
    def load(self):
        vol= pygame.mixer.music.get_volume()
        y = self.cursor.y + (1 - vol ) * (self.bar.rect.height - self.cursor.rect.height)
        self.cursor.rect = pygame.Rect(self.cursor.x,y,40,40) 
        self.group.empty()
        self.group.add(self.bar)
        self.group.add(self.cursor)
    
    def refresh(self,ticks):
        #self.screen.blit(self.backgroundImage, (0, 0))
        self.group.update(ticks)
        self.group.draw(self.screen)
    
    def onMouseClickHandler(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if self.mitAdventure.rect.collidepoint(mouse_pos):
            app_data.CurrentWin = app_data.AppForm.MAIN_FORM
        if self.mitSurvival.rect.collidepoint(mouse_pos):
            self.group.add(self.settingSound)
            self.group.add(self.soundCursor)
        if self.mitChallenge.rect.collidepoint(mouse_pos):
            app_data.IsRunning = False
            print("退出程序")
    
    def onMouseDownHandler(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if self.cursor.rect.collidepoint(mouse_pos):
            self.cursorSelected = True
        else:
            self.cursorSelected = False
            
    def onMouseUpHandler(self, event: pygame.event.Event):
        self.cursorSelected = False
        self.group.empty()
        
    def onMouseMotionHandler(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if self.cursorSelected == True:
            y=mouse_pos[1]
            if mouse_pos[1]<self.bar.rect.top:
                y = self.bar.rect.top
            elif mouse_pos[1]>self.bar.rect.bottom-40:
                y = self.bar.rect.bottom-40
            self.cursor.rect = pygame.Rect(self.cursor.x,y,40,40) 
            vol = 1-(y-self.bar.rect.top)/(self.bar.rect.height-40)
            print(vol)
            pygame.mixer.music.set_volume(vol)

