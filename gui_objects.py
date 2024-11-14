import pygame
import subprocess
import os
import sys
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
    def __init__(self, x, y, buttonWidth, buttonHeight,panding,numberOfButtonsPerLine,numberOfRows, name='Default') -> None:
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.name = name
        self.panding = panding 
        self.numberOfButtonsPerLine = numberOfButtonsPerLine 
        self.numberOfRows = numberOfRows 
        self.x = x 
        self.y = y 
        self.width = (self.buttonWidth + self.panding) * self.numberOfButtonsPerLine+ self.panding
        self.height =(self.buttonHeight + self.panding)* self.numberOfRows + self.panding
        self.surface = pygame.Surface((self.width,self.width)) 
        self.menuRect = pygame.Rect(self.x, self.y, self.width, self.height)

appsMenu = Menu(canvas.get_width() * .19, 20, 256, 256, 25, 5, 1,'appsMenu')
sideMenu = Menu(10, 20, 200, 200, 5, 1, 5,"sideMenu")       
# settingMenu = Menu(256, 256, 25, 5, 1,'appsMenu') 
Menus = [appsMenu, sideMenu]

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
        self.menus = Menus 
        self.menu = appsMenu
        self.buttons = buttons
        self.menuSelected = False 
        self.x = buttons[0].buttonRect.x  
        self.y = buttons[0].buttonRect.y 
        self.width = 20 
        self.height = 30 
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # adding a selection surface is to get a visual of what it is selcting this should 
        # able to comment out in production
        self.selectionSurface = pygame.Surface((self.width, self.height))
        self.selectionSurface.fill((100, 100, 100))

    def select(self):
        selectedButton = None
        for Menu in self.menus:
            if Menu.menuRect.contains(self.selectionRect):
                self.menu = Menu 
        for Button in self.buttons:
            if Button.buttonRect.contains(self.selectionRect):
                Button.isSelected = True
                selectedButton = Button 
            else:
                Button.isSelected = False
        return selectedButton

        
    def moveSlection(self ):
        currentlySelected = self.select()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    self.moving(1, 0, 0, 0, currentlySelected)
                if event.key == pygame.K_LEFT:
                    self.moving(0, 1, 0, 0, currentlySelected)
                if event.key == pygame.K_UP:
                    self.moving(0, 0, 1, 0, currentlySelected)
                if event.key == pygame.K_DOWN:
                    self.moving(0, 0, 0, 1, currentlySelected)
                if event.key == pygame.K_RETURN:
                    if currentlySelected != None:
                        currentlySelected.onclickFunction()
    
    def moving(self, RIGHT, LEFT, UP, DOWN, currentlySelected):
        button = currentlySelected 
        while button == currentlySelected or button == None:
            self.menu.surface.blit(self.selectionSurface, self.selectionRect)
            self.selectionRect.x += RIGHT
            self.selectionRect.x -= LEFT
            self.selectionRect.y -= UP 
            self.selectionRect.y += DOWN
            if self.selectionRect.x <= 0:
                self.selectionRect.x = resolutionWidth
            if self.selectionRect.x > resolutionWidth:
                self.selectionRect.x = 1
            if self.selectionRect.y > resolutionHeight:
                self.selectionRect.y = 1
            if self.selectionRect.y <=0:
                self.selectionRect.y = resolutionHeight
            button = self.select()
            if button == None:
               currentlySelected = None
            
            
            
                        



