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
numberOfRows = 1 
#Adding Menus

class Menu:
    def __init__(self, buttonWidth, buttonHeight,panding,numberOfButtonsPerLine,numberOfRows, name='Default') -> None:
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.name = name
        self.panding = panding 
        self.numberOfButtonsPerLine = numberOfButtonsPerLine 
        self.numberOfRows = numberOfRows 
        self.surface = pygame.Surface(((self.buttonWidth + self.panding) * self.numberOfButtonsPerLine+ self.panding, \
                                           (self.buttonHeight + self.panding)* self.numberOfRows + self.panding))

appsMenu = Menu(256, 256, 25, 5, 1,'appsMenu').surface
sideMenu = Menu(200, 40, 5, 1, 5,"sideMenu").surface       
settingMenu = Menu(256, 256, 25, 5, 1,'appsMenu').surface 

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
    def __init__(self,  buttons) -> None:
        self.menu = appsMenu
        self.buttons = buttons
        self.menuSelected = False 
        self.x = (self.menu.get_width() / numberOfAppsPerLine) /2
        self.y = (self.menu.get_height() / numberOfRows) /2 
        self.width = 50 
        self.height = 50
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # adding a selection surface is to get a visual of what it is selcting this should 
        # able to comment out in production
        self.selectionSurface = pygame.Surface((self.width, self.height))
        self.selectionSurface.fill((100, 100, 100))

    def select(self):
        selectedButton = None
        self.menu.blit(self.selectionSurface, self.selectionRect)
        for button in self.buttons:
            if button.buttonRect.collidepoint(self.selectionRect.x, self.selectionRect.y):
                button.isSelected = True
                selectedButton = button
            else:
                button.isSelected = False
        return selectedButton

    
    def move(self, movement):
        if movement == 'RIGHT':
            if self.menu == sideMenu:
                self.menu = appsMenu
                self.selectionRect.x, self.selectionRect.y  = int(self.x), int(self.y) 
            elif self.selectionRect.x >= appsMenu.get_width() -int(self.x):
                self.selectionRect.x = int(self.x) 
            else:
                self.selectionRect.x += 286 
        if movement == 'LEFT':
            if self.selectionRect.x < 286:
                self.menu = sideMenu 
                self.selectionRect.x = 19 
                self.selectionRect.y = 25 
            else:
                self.selectionRect.x -= 286 
        if movement == 'UP':
            if self.menu == sideMenu:
                self.selectionRect.y -= 30 
            elif self.selectionRect.y < 288:
                self.selectionRect.y = int(self.y)  
            else:
                self.selectionRect.y -= 288 
        if movement == 'DOWN':
            if self.menu == sideMenu:
                self.selectionRect.y +=30
            elif self.selectionRect.y >= appsMenu.get_height() -int(self.y):
                self.selectionRect.y = int(self.y) 
            else:
                self.selectionRect.y += 288 
        button = self.select()
        if movement == 'ENTER' and button:
            button.onclickFunction()

