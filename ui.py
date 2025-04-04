import pygame 
import subprocess
import os
import sys
from settings import *
#initalizing 
Mixer = pygame.mixer
Mixer.init()
pygame.init()

#Settings
resolutionWidth = 1920 
resolutionHeight = 1080 

FPS = 120
Music_Switch= False
# os.environ['SDL_VIDEO_CENTERED'] = '12'
info = pygame.display.Info()
#resolutionWidth, resolutionHight = info.current_w, info.current_h
Canvas = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
background_img  = pygame.image.load(BACKGROUND_IMAGE).convert()
background_img = pygame.transform.scale(background_img, (resolutionWidth, resolutionHeight))
background_position = (0, 0)
Font = pygame.font.Font(FONT_PATH, FONT_SIZE)

#Adding Menus

class Menu:
    def __init__(self, x, y, width, height, name='Default') -> None:
        self.name = name
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA) 
        self.menuRect = self.surface.get_rect()
        self.buttons = []
        self.button_matrix = [[]]
        self.is_form = False
        self.hide = False
        self.isList = False
    
    def display(self):
        if self.hide == False:
            Canvas.blit(self.surface, (self.x, self.y))
    def toggleDisplay(self):
        self.hide = not self.hide


class Button:
      def __init__(self, x, y, width, height, buttonText='Default'):
          self.x = x
          self.y = y
          self.width = width 
          self.height = height 
          self.buttonText = buttonText
          self.isImage = False
          self.buttonImage = pygame.image.load(TEST_BUTTON_IMAGE)
          self.layer = None # Will be set to menu.surface in importApps 
          self.cmd = "echo " + self.buttonText
          self.isSelected = False
          self.fillColors = { 'normal' : '#ffffff', 'hover' : '#666666',  'pressed' : '#333333', }
          self.buttonSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
          self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
          self.font = Font 
          self.font_rendered = self.font.render(self.buttonText, True, (255,200,200))
          self.font_rendered_highlighted = self.font.render(self.buttonText, True, (255, 255, 200))
          self.highlighted = False
      def onclickFunction(self):
          subprocess.call(self.cmd, shell=True)
      def displayText(self):
        self.buttonSurface.fill((0,0,0,0))
        self.layer.blit(self.buttonSurface, self.buttonRect)
        if self.isSelected:
          self.layer.blit(self.font_rendered_highlighted, self.buttonRect)
        else:
          self.layer.blit(self.font_rendered, self.buttonRect)
      def displayImage(self):
        self.buttonSurface.fill((0,0,0,0))
        self.layer.blit(self.buttonSurface, (0, 0))
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
    def __init__(self, menuSelected, menus) -> None:
        self.sound = Mixer.Sound(CLICK_SOUND)
        self.menus = menus 
        self.menuSelected = menuSelected 
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


    #define key mappings here
    def moveSelection(self):
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
        self.buttonSelected.isSelected = False
        if not self.menuSelected.buttons:
            print("No Buttons in menu!")
            return
        self.sound.play()
        #Handle up down side Menu 
        if self.menuSelected.isList:
            buttonIndex = self.menuSelected.buttons.index(self.buttonSelected)
            total_buttons = len(self.menuSelected.buttons)
            if direction == 'UP':
                if buttonIndex > 0:
                    buttonIndex -= 1  # Move up in the list
                else:
                    buttonIndex = total_buttons - 1  # Wrap to the bottom
            elif direction == 'DOWN':
                if buttonIndex + 1 < total_buttons:
                    buttonIndex += 1  # Move down in the list
                else:
                    buttonIndex = 0  # Wrap to the top

            self.buttonSelected = self.menuSelected.buttons[buttonIndex]
            self.selectionRect.x = self.buttonSelected.buttonRect.x + self.menuSelected.x
            self.selectionRect.y = self.buttonSelected.buttonRect.y + self.menuSelected.y
            self.buttonSelected.isSelected = True
            return
        
        # Find current row/col
        buttonIndex = self.menuSelected.buttons.index(self.buttonSelected)
        buttons_per_row = len(self.menuSelected.button_matrix[0])  # Assume row 0 is full
        total_rows = len(self.menuSelected.button_matrix)
        row = buttonIndex // buttons_per_row
        col = buttonIndex % buttons_per_row
        
        if direction == 'UP':
            if row > 0:
                row -= 1  # Move up normally
                print(f"Moving UP to row {row}, col {col}")
            else:
                row = total_rows - 1  # Wrap to bottom
                print(f"Wrapping UP to row {row}, col {col}")
            if col < len(self.menuSelected.button_matrix[row]):  # Check column exists
                self.buttonSelected = self.menuSelected.button_matrix[row][col]
            else:
                self.buttonSelected = self.menuSelected.button_matrix[row][-1]  # Last in row if col too big
        elif direction == 'DOWN':
            if row + 1 < total_rows:
                row += 1  # Move down normally
                print(f"Moving DOWN to row {row}, col {col}")
            else:
                row = 0  # Wrap to top
                print(f"Wrapping DOWN to row {row}, col {col}")
            if col < len(self.menuSelected.button_matrix[row]):  # Check column exists
                self.buttonSelected = self.menuSelected.button_matrix[row][col]
            else:
                self.buttonSelected = self.menuSelected.button_matrix[row][-1]  # Last in row if col too big
        else:
            print(f"Invalid direction: {direction}")
            return
        
        self.selectionRect.x = self.buttonSelected.buttonRect.x
        self.selectionRect.y = self.buttonSelected.buttonRect.y
        self.buttonSelected.isSelected = True
        print(f"New selection position: ({self.selectionRect.x}, {self.selectionRect.y})") 
        
            
    def moveRightLeft(self, direction):
        self.buttonSelected .isSelected = False
        if not self.menuSelected.buttons or not hasattr(self.menuSelected, 'button_matrix'):
            print("No buttons or matrix in menu!")
            return
        self.sound.play()
        
        buttonIndex = self.menuSelected.buttons.index(self.buttonSelected)
        buttons_per_row = len(self.menuSelected.button_matrix[0])
        row = buttonIndex // buttons_per_row
        col = buttonIndex % buttons_per_row
        if self.menuSelected.isList:
            if direction == 'RIGHT':
                #Immedialty switch to DisplayedMenu if there are buttons  
                if len(self.menus[1].buttons) == 0:
                    return 
                else:
                    self.menuSelected = self.menus[1]
                    self.buttonSelected = self.menuSelected.buttons[0]
            elif direction == 'LEFT':
                pass
 
        if direction == 'RIGHT' and col + 1 < len(self.menuSelected.button_matrix[row]):
            col += 1
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        elif direction == 'LEFT' and col > 0:
            col -= 1
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        elif direction == 'LEFT' and col == 0 and self.menuSelected == self.menus[1]:  
            # Switch to sideMenu
            self.menuSelected = self.menus[0]
            self.buttonSelected = self.menuSelected.buttons[0]
        elif direction == 'RIGHT' and col + 1 >= len(self.menuSelected.button_matrix[row]):
            # Wrap to first column in AppMenu
            col = 0
            self.menuSelected = self.menus[1]
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        self.selectionRect.x = self.buttonSelected.buttonRect.x
        self.selectionRect.y = self.buttonSelected.buttonRect.y
        self.buttonSelected.isSelected = True        
            
                        



