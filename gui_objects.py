import pygame
import subprocess
import json
import os
#create gui canvas
BLACK = (255,255,255)

resolutionWidth = 1920 
resolutionHeight = 1080 

pygame.init()
FPS = 60
Music_Switch= False

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
#resolutionWidth, resolutionHight = info.current_w, info.current_h
canvas = pygame.display.set_mode((resolutionWidth, resolutionHeight), pygame.RESIZABLE)
background= pygame.image.load("./Images/background.png")
background_position = (0, 0)

#adding app size so this can be adjusted based on resolutionWidth
buttonWidth = 256
buttonHeight = 256
panding = 25
numberOfAppsPerLine = 5
numberOfRows = 3
#Adding Menus
appsMenu = pygame.Surface(((buttonWidth + panding) * numberOfAppsPerLine + panding, (buttonHeight + panding)* numberOfRows + panding))
print(appsMenu.get_width(), appsMenu.get_height())
sideMenu = pygame.Surface((200,resolutionHeight *.9))



class Button:
      def __init__(self, x, y,  buttonText='Default'):
          self.x = x
          self.y = y
          self.width = buttonWidth 
          self.height = buttonHeight 
          self.buttonText = buttonText
          self.isImage = False
          self.buttonImage = pygame.image.load("./Assets/testing.png")
          self.surface = canvas 
          self.cmd = "echo " + self.buttonText
          self.isSelected = False

          self.fillColors = { 'normal' : '#ffffff', 'hover' : '#666666',  'pressed' : '#333333', }

          #self.buttonSurface = pygame.Surface((self.width, self.height))
          self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
          self.font = pygame.font.Font('/usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf', 30)
          self.font_rendered = self.font.render(self.buttonText, True, (255,200,200))
          self.font_rendered_highlighted = self.font.render(self.buttonText, True, (255, 255, 200))
          self.highlighted = False
      def onclickFunction(self):
          subprocess.call(self.cmd, shell=True)
      def displayText(self):
          if self.isSelected:
              self.surface.blit(self.font_rendered_highlighted, self.buttonRect)
          else:
              self.surface.blit(self.font_rendered, self.buttonRect)
      def displayImage(self):
        if self.isSelected:
            image = pygame.transform.smoothscale(self.buttonImage, (300,300))
            self.surface.blit(image, (self.buttonRect.x -25, self.buttonRect.y -25))
        else:
            self.surface.blit(self.buttonImage, self.buttonRect)
      def display(self):
            if self.isImage:
                self.displayImage()
            else:
                self.displayText()

            
class Selection:
    #find a way to pull in apps from a list
    def __init__(self, appsArray, sideMenuList) -> None:
        self.menu = appsMenu
        self.sideMenuList = sideMenuList
        self.appsArray = appsArray 
        self.menuSelected = False 
        self.x = 143 
        self.y = 144 
        self.width = 25 
        self.height = 25
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # adding a selection surface is to get a visual of what it is selcting this should 
        # able to comment out in production
        self.selectionSurface = pygame.Surface((self.width, self.height))
        self.selectionSurface.fill((100, 100, 100))

    def select(self):
        self.menu.blit(self.selectionSurface, self.selectionRect)
        if self.menu == appsMenu:
            for button in self.appsArray:
                if button.buttonRect.collidepoint(self.selectionRect.x, self.selectionRect.y):
                    button.isSelected = True
                else:
                    button.isSelected = False
        elif self.menu == sideMenu:
            for button in self.sideMenuList:
                if self.selectionRect.collidepoint(button.x, button.y):
                    button.isSelected = True
                else:
                    button.isSelected =False
    
    
    def anotherMoveFunc(self, movement): 
        if movement == 'RIGHT':
            if self.menu == sideMenu:
                self.menu = appsMenu
                self.selectionRect.x, self.selectionRect.y  = int(self.x), int(self.y) 
            if self.selectionRect.x > appsMenu.get_width():
                self.selectionRect.x = 0
            else:
                self.selectionRect.x += 286 
        if movement == 'LEFT':
            if self.selectionRect.x < 286:
                self.menu = sideMenu 
                self.selectionRect.x = 0 
                self.selectionRect.y = 0
            else:
                self.selectionRect.x -= 286 
        if movement == 'UP':
            if self.selectionRect.y < 288:
                self.selectionRect.y = int(self.y)  
            else:
                self.selectionRect.y -= 288 
        if movement == 'DOWN':
            if self.selectionRect.y > appsMenu.get_height():
                self.selectionRect.y = int(self.y) 
            else:
                self.selectionRect.y += 288 
        if movement == 'ENTER':
            print('enter')
        self.select()

class DialogBox:
    def __init__(self, x, y):
        self.x = x
        self.y =y
        self.width = 150
        self.height = 30

        self.dialogSurface = pygame.Surface((self.width, self.height))
        self.dialogRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def print_text(self, text):
        font = pygame.font.Font('./Font/VarinonormalRegular-1GXaM.ttf', 20)
        font_rendered = font.render(text, True, (0,255,0))
        return font_rendered

class menu:
    def __init__(self, x ,y) -> None:
        self.is_open = False 
        self.x = x 
        self.y = y
        self.width =  500
        self.height = 700
        self.image = pygame.image.load("./Images/menu.png")
        self.music_switch = "On"
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.start_stop_music = Button(self.x +150, self.y +60, 'Music: ')
        self.exit_game = Button(self.x +150, self.y + 90, "Exit Game")
    def display(self):
        if self.is_open:
            canvas.blit(self.image, self.rect)
            self.start_stop_music.display()
            self.exit_game.display()
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.is_open = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.start_stop_music.process()
                    self.exit_game.process()
            pygame.display.update()

