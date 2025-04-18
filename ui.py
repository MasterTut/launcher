import pygame 
import subprocess
import os
import sys
from typing import List, Optional
from settings import *
from enum import Enum
import logging
#initalizing 
Mixer = pygame.mixer
Mixer.init()
pygame.init()

#Settings
resolutionWidth = 1920 
resolutionHeight = 1080 

FPS = 120
Music_Switch= True 
# os.environ['SDL_VIDEO_CENTERED'] = '12'
info = pygame.display.Info()
#resolutionWidth, resolutionHight = info.current_w, info.current_h
Canvas = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
background_img  = pygame.image.load(BACKGROUND_IMAGE).convert()
background_img = pygame.transform.scale(background_img, (resolutionWidth, resolutionHeight))
background_position = (0, 0)
Font = pygame.font.Font(FONT_PATH, FONT_SIZE)
#Adding Menus

class Button:
      def __init__(self, x, y, width, height, surface, buttonText='Default'):
          self.name = buttonText
          self.x = x
          self.y = y
          self.width = width 
          self.height = height 
          self.buttonText = buttonText
          self.isImage = False
          self.buttonImage = pygame.image.load(TEST_BUTTON_IMAGE)
          self.layer = surface # Will be set to menu.surface  
          self.cmd = "echo " + self.buttonText
          self.isSelected = False
          self.fillColors = { 'normal' : '#ffffff', 'hover' : '#666666',  'pressed' : '#333333', }
          self.buttonSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
          self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
          self.font = Font 
          self.font_rendered = self.font.render(self.buttonText, True, (255,200,200))
          self.font_rendered_highlighted = self.font.render(self.buttonText, True, (255, 255, 200))
          self.highlighted = False
          self.bg_color = (DARK_BLUE) 
      
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
        padding = 5
        #draw Dark_BLUE background for button
        pygame.draw.rect(self.layer, (self.bg_color), 
                         (self.buttonRect.x - padding, 
                          self.buttonRect.y - padding, 
                          self.buttonImage.get_width() + 2 * padding, 
                          self.buttonImage.get_height() + 2 * padding))
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
        #self.is_form = False
        self.hide = False
        self.isList = False
        self.bg_color = (0,0,25,100)
        self.radius = 20
        self.input_boxes = []
        self.isSelected = False
        self.menuList: List[str] = [] #if Menu is list this will hold a list of strings that can be selected to display a nested Menu
        self.nestedMenus: List[Menu] =[] # this holds a list of nested Menus
        self.activeNestedMenu: Optional[Menu] = None
        self._nested_menu_map: dict = {} #Map Button Names to nested menus
   

    def importMenuList(self, button_width: int = 150, button_height: int = 40, vertical_spacing: int = 50) -> None:
        """Create buttons from menuList for list-based menus."""
        if not self.isList:
            return
        self.buttons.clear()
        self.button_matrix = [[]]
        y_offset = 20
        x_pos = self.width * 0.2
        for button_text in self.menuList:
            button = Button(x_pos, y_offset, button_width, button_height, self.surface, button_text)
            self.buttons.append(button)
            self.button_matrix[0].append(button)
            y_offset += vertical_spacing
        self._update_nested_menu_map()
  
    def set_button_matrix(self, matrix: List[List['Button']]) -> None:
        """Set the button matrix for grid-based menus."""
        self.button_matrix = matrix
        self.buttons = [button for row in matrix for button in row]
        self.isList = False
        self._update_nested_menu_map()

    def add_nested_menu(self, menu: 'Menu') -> None:
        """Add a nested menu and update the menu map."""
        self.nestedMenus.append(menu)
        self._update_nested_menu_map()

    def _update_nested_menu_map(self) -> None:
        """Update the mapping of button names to nested menus."""
        self._nested_menu_map = {menu.name: menu for menu in self.nestedMenus}

    def displayNestedMenus(self) -> None:
        """Set and display the active nested menu based on the selected button."""
        if not self.buttons:
            return
        for button in self.buttons:
            if button.isSelected:
                self.activeNestedMenu = self._nested_menu_map.get(button.name)
                if self.activeNestedMenu:
                    self.activeNestedMenu.display()
                break

    def displayButtons(self) -> None:
        for button in self.buttons:
            button.display()
    
    def displayFields(self) -> None:
        for input in self.input_boxes:
            input.display()
    
    def display(self) -> None:
        if self.hide:
            return
        pygame.draw.rect(self.surface, self.bg_color, (0, 0, self.width, self.height), border_radius=self.radius)
        self.displayButtons()
        self.displayFields()
        self.displayNestedMenus()
        Canvas.blit(self.surface, (self.x, self.y))
            
    def toggleDisplay(self) -> None:
        self.hide = not self.hide
    
    def showError(self, message, duration=2000):
        message = str(message) if message is not None else "Unknown error"
        text_surface = Font.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            Canvas.blit(text_surface, text_rect)
            pygame.display.flip()
        return True


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

#This Class handles moving around on the display and highlighting buttons            
class Selection:
    def __init__(self,  Menu) -> None:
        self.sound = Mixer.Sound(CLICK_SOUND)
        self.Menu = Menu 
        self.menuSelected = Menu 
        self.buttonSelected = self.menuSelected.buttons[0] 
        self.x = self.buttonSelected.buttonRect.x  
        self.y = self.buttonSelected.buttonRect.y 
        self.width = 25 
        self.height = 25 
        # adding a selection surface is to get a visual of what it is selcting this should 
        self.surface = pygame.Surface((self.width, self.height))
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.surface.fill((100, 100, 100))
        self.isEnabled = True


    def selectInputBox(self, direction):
        input_boxes = self.menuSelected.input_boxes
        if not input_boxes:
            return
        for i, box in enumerate(self.menuSelected.input_boxes):
            if box.isActive:
               box.isActive = False
               if direction == "UP":
                    next_box = input_boxes[(i -1) % len(input_boxes)]
               else:
                    next_box = self.menuSelected.input_boxes[(i + 1) % len(self.menuSelected.input_boxes)]
               next_box.isActive = True
               print(f"Switched to {next_box.name}, isActive: {next_box.isActive}")
               break
            # Activate the first box if none were active
            if not any(box.isActive for box in self.menuSelected.input_boxes):
                self.menuSelected.input_boxes[0].isActive = True 
    #define key mappings here
    def moveSelection(self):
        if self.isEnabled:
            self.menuSelected.isSelected = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Mouse Fuction for selecting text fields on AddAppMenu
                    if self.menuSelected.name == "AddAppMenu":
                        mouse_pos = pygame.mouse.get_pos()
                        if self.menuSelected.buttons[0].buttonRect.collidepoint(mouse_pos):
                            self.menuSelected.submitButtonFunc()
                        for input in self.menuSelected.input_boxes:
                            input.isActive = False
                            if input.rect.collidepoint(mouse_pos):
                                input.isActive = True
                            else:
                                input.isActive = False

                elif event.type == pygame.TEXTINPUT:
                    for input in self.menuSelected.input_boxes:
                        if input.isActive:
                            input.text += event.text
                            input.update_text()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_RIGHT:
                        self.move(Direction.RIGHT)
                    if event.key == pygame.K_LEFT:
                        self.move(Direction.LEFT)
                    if event.key == pygame.K_UP:
                        self.move(Direction.UP)
                    if event.key == pygame.K_DOWN:
                        self.move(Direction.DOWN)
                    if event.key == pygame.K_RETURN:
                        self.buttonSelected.onclickFunction()
                    if event.key == pygame.K_TAB and len(self.menuSelected.input_boxes) > 0:
                        self.selectInputBox("DOWN")
                    elif event.key == pygame.K_BACKSPACE and len(self.menuSelected.input_boxes) > 0:
                        for input in self.menuSelected.input_boxes:
                            if input.isActive:
                                input.text = input.text[:-1]
                                input.update_text()
        else:
            return

    def move(self, direction: Direction) -> None:
        """Handle menu navigation based on direction."""

        # Play sound and deselect current button
        self.sound.play()

        
        if direction != Direction.RIGHT and self.buttonSelected:
            self.buttonSelected.isSelected = False

        # Handle input boxes
        if self.menuSelected and self.menuSelected.input_boxes:
            self.selectInputBox(direction.value)
            return

        # Check if menu is selected
        if not self.menuSelected:
            print("No menu selected")
            return

        # Handle list menu
        if self.menuSelected.isList:
            self._move_in_list_menu(direction)
        # Handle grid menu
        else:
            self._move_in_grid_menu(direction)

    def _move_in_list_menu(self, direction: Direction) -> None:
        """Handle navigation in a list menu."""
        if not self.menuSelected.buttons:
            return

        button_index = self.menuSelected.buttons.index(self.buttonSelected)
        total_buttons = len(self.menuSelected.buttons)

        if direction == Direction.UP:
            button_index = (button_index - 1) if button_index > 0 else total_buttons - 1
            self.buttonSelected = self.menuSelected.buttons[button_index]
            self.buttonSelected.isSelected = True
        elif direction == Direction.DOWN:
            button_index = (button_index + 1) if button_index + 1 < total_buttons else 0
            self.buttonSelected = self.menuSelected.buttons[button_index]
            self.buttonSelected.isSelected = True
        elif direction == Direction.RIGHT:
            # Switch to nested menu (e.g., Apps) without deselecting current button
            if self.menuSelected.activeNestedMenu:
                self.menuSelected = self.menuSelected.activeNestedMenu
                self._select_first_item()
            return
        elif direction == Direction.LEFT:
            self.menuSelected.isSelected = False
            self.menuSelected = self.Menu
            self._select_first_item()
            return

        self.buttonSelected = self.menuSelected.buttons[button_index]
        self.buttonSelected.isSelected = True

    def _move_in_grid_menu(self, direction: Direction) -> None:
        """Handle navigation in a grid menu."""
        if not self.menuSelected.button_matrix or not self.menuSelected.button_matrix[0]:
            return

        button_index = self.menuSelected.buttons.index(self.buttonSelected)
        buttons_per_row = len(self.menuSelected.button_matrix[0])
        total_rows = len(self.menuSelected.button_matrix)
        row = button_index // buttons_per_row
        col = button_index % buttons_per_row

        if direction == Direction.UP:
            row = (row - 1) if row > 0 else total_rows - 1
        elif direction == Direction.DOWN:
            row = (row + 1) if row + 1 < total_rows else 0
        elif direction == Direction.RIGHT:
            if self.buttonSelected:
                self.buttonSelected.isSelected = False
            if col + 1 < len(self.menuSelected.button_matrix[row]):
                col += 1
            else:
                return # No nested menus in grid, stay in place
        elif direction == Direction.LEFT:
            if col > 0:
                col -= 1
            elif self.menuSelected in self.Menu.nestedMenus:
                # Switch to sideMenu
                self.menuSelected = self.Menu
                if self.menuSelected.buttons:
                    self.buttonSelected = next(
                    (button for button in self.menuSelected.buttons if button.isSelected), 
                    self.menuSelected.buttons[0]
                )
                self.buttonSelected.isSelected = True
                return
            else:
                return

        # Ensure valid button selection
        if len(self.menuSelected.button_matrix[row]) > col:
            self.buttonSelected = self.menuSelected.button_matrix[row][col]
        else:
            self.buttonSelected = self.menuSelected.button_matrix[row][-1]
        self.buttonSelected.isSelected = True

    def _select_first_item(self) -> None:
        """Select the first button or input box in the current menu."""
        if self.menuSelected.buttons:
            self.buttonSelected = self.menuSelected.buttons[0]
        elif self.menuSelected.input_boxes:
            self.buttonSelected = self.menuSelected.input_boxes[0]
        else:
            self.buttonSelected = None
        if self.buttonSelected:
            self.buttonSelected.isSelected = True
                        



