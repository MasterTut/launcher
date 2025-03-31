import pygame
import subprocess
import os
import sys
#create gui canvas
BLACK = (255,255,255)

resolutionWidth = 1920 
resolutionHeight = 1080 
mixer = pygame.mixer
mixer.init()
pygame.init()
FPS = 120
Music_Switch= False
# os.environ['SDL_VIDEO_CENTERED'] = '12'
info = pygame.display.Info()
#resolutionWidth, resolutionHight = info.current_w, info.current_h
canvas = pygame.display.set_mode((resolutionWidth, resolutionHeight), pygame.RESIZABLE)
background= pygame.image.load("./Assets/background.png")
appMenuImage = pygame.image.load("./Assets/appMenu.png")
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
        self.sound = mixer.Sound('./Assets/Sound/GUI/click.wav')
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
                    self.moveRightLeft('RIGHT')
                if event.key == pygame.K_LEFT:
                    self.moveRightLeft('LEFT')
                if event.key == pygame.K_UP:
                    self.moveUpDown( 'UP')
                if event.key == pygame.K_DOWN:
                    self.moveUpDown( 'DOWN')
                if event.key == pygame.K_RETURN:
                        self.buttonSelected.onclickFunction()
    
        
    def moveUpDown(self, direction):
        if not self.menuSelected.buttons or not hasattr(self.menuSelected, 'button_matrix'):
            print("No buttons or matrix in menu!")
            return
        self.sound.play()
        
        # Find current row/col
        buttonIndex = self.menuSelected.buttons.index(self.buttonSelected)
        buttons_per_row = len(self.menuSelected.button_matrix[0])  # Assume row 0 is full
        row = buttonIndex // buttons_per_row
        col = buttonIndex % buttons_per_row
        
        print(f"Menu: {self.menuSelected.name}")
        print(f"Current row: {row}, col: {col}, Total rows: {len(self.menuSelected.button_matrix)}")
        print(f"Current button position: ({self.buttonSelected.buttonRect.x}, {self.buttonSelected.buttonRect.y})")
        print(f"Direction received: {direction}")
        
        self.buttonSelected.isSelected = False
        if direction == 'UP' and row > 0:
            row -= 1
            if col < len(self.menuSelected.button_matrix[row]):  # Check column exists
                self.buttonSelected = self.menuSelected.button_matrix[row][col]
                print(f"Moving UP to row {row}, col {col}")
        elif direction == 'DOWN' and row + 1 < len(self.menuSelected.button_matrix):
            row += 1
            if col < len(self.menuSelected.button_matrix[row]):
                self.buttonSelected = self.menuSelected.button_matrix[row][col]
                print(f"Moving DOWN to row {row}, col {col}")
        else:
            print(f"Cannot move {direction}: at boundary (row {row}, col {col})")
        
        self.selectionRect.x = self.buttonSelected.buttonRect.x
        self.selectionRect.y = self.buttonSelected.buttonRect.y
        self.buttonSelected.isSelected = True
        print(f"New selection position: ({self.selectionRect.x}, {self.selectionRect.y})") 
            
            
    def moveRightLeft(self, direction):
        if not self.menuSelected.buttons or not hasattr(self.menuSelected, 'button_matrix'):
            print("No buttons or matrix in menu!")
            return
        self.sound.play()
        
        buttonIndex = self.menuSelected.buttons.index(self.buttonSelected)
        buttons_per_row = len(self.menuSelected.button_matrix[0])
        row = buttonIndex // buttons_per_row
        col = buttonIndex % buttons_per_row
        
        self.buttonSelected.isSelected = False
        if direction == 'RIGHT' and col + 1 < len(self.menuSelected.button_matrix[row]):
            col += 1
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        elif direction == 'LEFT' and col > 0:
            col -= 1
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        elif direction == 'LEFT' and col == 0 and self.menuSelected == self.menus[1]:  # Switch to sideMenu
            self.menuSelected = self.menus[0]
            self.buttonSelected = self.menuSelected.buttons[0]
        self.selectionRect.x = self.buttonSelected.buttonRect.x
        self.selectionRect.y = self.buttonSelected.buttonRect.y
        self.buttonSelected.isSelected = True        
            
                        



