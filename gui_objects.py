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

#Adding Menus

class Menu:
    def __init__(self, x, y, width, height, name='Default') -> None:
        self.name = name
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height
        self.surface = pygame.Surface((self.width,self.height)) 
        self.menuRect = self.surface.get_rect()
        self.buttons = []

addAppMenu = Menu(canvas.get_width() * .19, 20, 1500, 1000, "addApp")
appsMenu = Menu(canvas.get_width() * .19, 0, 1500, canvas.get_height(),'appsMenu')
sideMenu = Menu(0, 0, 200, canvas.get_height(),"sideMenu")
Menus = [ sideMenu, appsMenu ]

class Button:
      def __init__(self, x, y, width, height, buttonText='Default'):
          self.x = x
          self.y = y
          self.width = width 
          self.height = height 
          self.buttonText = buttonText
          self.isImage = False
          self.buttonImage = pygame.image.load("./Assets/testing.png")
          self.layer = pygame.Surface((self.width,self.height))  
          self.cmd = "echo " + self.buttonText
          self.isSelected = False
          self.fillColors = { 'normal' : '#ffffff', 'hover' : '#666666',  'pressed' : '#333333', }
          self.buttonSurface = pygame.Surface((self.width, self.height))
          self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
          self.font = pygame.font.Font('/usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf', 30)
          self.font_rendered = self.font.render(self.buttonText, True, (255,200,200))
          self.font_rendered_highlighted = self.font.render(self.buttonText, True, (255, 255, 200))
          self.highlighted = False
      def onclickFunction(self):
          subprocess.call(self.cmd, shell=True)
      def displayText(self):
        self.buttonSurface.fill((25,25,25))
        self.layer.blit(self.buttonSurface, self.buttonRect)
        if self.isSelected:
          self.layer.blit(self.font_rendered_highlighted, self.buttonRect)
        else:
          self.layer.blit(self.font_rendered, self.buttonRect)
      def displayImage(self):
        if self.isSelected:
           image = pygame.transform.smoothscale(self.buttonImage, (300,300))
           self.layer.blit(image, (self.buttonRect.x -25, self.buttonRect.y -25))
        else:
           self.layer.blit(self.buttonImage, self.buttonRect)
      def display(self):
        if self.isImage:
           self.displayImage()
        else:
           self.displayText()

            
class Selection:
    def __init__(self) -> None:
        self.menus = Menus 
        self.menuSelected = appsMenu 
        self.buttonSelected = self.menuSelected.buttons[0] 
        self.x = self.buttonSelected.buttonRect.x  
        self.y = self.buttonSelected.buttonRect.y 
        self.width = 25 
        self.height = 25 
         
        # adding a selection surface is to get a visual of what it is selcting this should 
        # able to comment out in production
        self.surface = pygame.Surface((self.width, self.height))
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.surface.fill((100, 100, 100))
        self.isMoving = False

    # look for button or menu that the selection is over. if no button was selected return false
    def select(self):
        isThereAButton = False
        for Button in self.menuSelected.buttons:
            Button.isSelected = False
            if Button.buttonRect.contains(self.selectionRect):
                isThereAButton = True 
                self.buttonSelected = Button
        self.buttonSelected.isSelected = True
        return isThereAButton 

   #listen for keys and run the move function adding 1 pixel to the appropriate direction
    #define key mappings here
    def moveSelection(self):
        self.menuSelected.surface.blit(self.surface, self.selectionRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    self.move('RIGHT')
                if event.key == pygame.K_LEFT:
                    self.move('LEFT')
                if event.key == pygame.K_UP:
                    self.moving(0, 0, 1, 0)
                if event.key == pygame.K_DOWN:
                    self.moving(0, 0, 0, 1)
                if event.key == pygame.K_RETURN:
                        self.buttonSelected.onclickFunction()
    #move 1 pixel until a new button or the same button is reselected
    def moving(self, RIGHT, LEFT, UP, DOWN):
        self.isMoving = True
        deselectedOriginalButton = False 
        while self.isMoving:
            if not self.select():
                deselectedOriginalButton = True
            if deselectedOriginalButton and self.select():
                self.selectionRect.x = self.buttonSelected.x 
                self.selectionRect.y = self.buttonSelected.y
                self.isMoving= False 
            self.selectionRect.x += RIGHT
            self.selectionRect.x -= LEFT
            self.selectionRect.y -= UP 
            self.selectionRect.y += DOWN
            if self.selectionRect.x < 0:
                self.selectionRect.x = resolutionWidth
            if self.selectionRect.x > resolutionWidth:
                self.selectionRect.x =0
            if self.selectionRect.y > resolutionHeight:
                self.selectionRect.y = 1
            if self.selectionRect.y < 0:
                self.selectionRect.y = resolutionHeight
    
    def move(self, direction):
        buttonIndex = self.menuSelected.buttons.index((self.buttonSelected))
        # menuIndex = self.menus.index((self.menuSelected))
        self.buttonSelected.isSelected = False
        if direction == 'RIGHT':
            if buttonIndex + 1 < len(self.menuSelected.buttons):
                if self.menuSelected == self.menus[0]:
                    self.menuSelected = self.menus[1]
                    self.buttonSelected = self.menuSelected.buttons[0]
                else:
                    self.buttonSelected  = self.menuSelected.buttons[buttonIndex + 1]
            else:
                self.buttonSelected = self.menuSelected.buttons[0]
        if direction == 'LEFT':
            if self.selectionRect.x == 25:
                self.menuSelected = self.menus[0]
                self.buttonSelected = self.menuSelected.buttons[0]
            else:
                self.buttonSelected  = self.menuSelected.buttons[buttonIndex -1]

        self.selectionRect.x = self.buttonSelected.x
        self.selectionRect.y = self.buttonSelected.y
        self.buttonSelected.isSelected = True

        
        
        
            
            
            
            
                        



