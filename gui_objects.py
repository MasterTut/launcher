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


class Button:
      def __init__(self, x, y, buttonText='Default'):
          self.x = x
          self.y = y
          self.width = 256
          self.height = 256
          self.buttonText = buttonText
          self.buttonImage = pygame.image.load("./Assets/testing.png")
          self.surface = canvas 
          self.cmd = "echo " + self.buttonText

          self.fillColors = { 'normal' : '#ffffff', 'hover' : '#666666',  'pressed' : '#333333', }

          #self.buttonSurface = pygame.Surface((self.width, self.height))
          self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
          self.font = pygame.font.Font('./Font/VarinonormalRegular-1GXaM.ttf', 18)
          self.font_rendered = self.font.render(self.buttonText, True, (255,200,200))
          self.font_rendered_highlighted = self.font.render(self.buttonText, True, (255, 255, 200))
          self.highlighted = False
      def onclickFunction(self):
          subprocess.call(self.cmd, shell=True)
          #override this function
      def display(self):
          mousePos = pygame.mouse.get_pos()
          if self.buttonRect.collidepoint(mousePos):
              self.surface.blit(self.font_rendered_highlighted, self.buttonRect)
          else:
              self.surface.blit(self.font_rendered, self.buttonRect)
      def displayImage(self):
           self.surface.blit(self.buttonImage, self.buttonRect)
      def process(self):
          mousePos = pygame.mouse.get_pos()
          if self.buttonRect.collidepoint(mousePos):
              self.onclickFunction()
      def processSelection(self, selection):
        selectionPos = selection.selectionRect.x, selection.selectionRect.y
        if self.buttonRect.collidepoint(selectionPos):
            self.onclickFunction()
      def buttonScale(self):
        pygame.transform.scale(self.buttonImage, (55,55))

        
            
class Selection:
    def __init__(self, appLayout, displaySurface) -> None:
        self.displaySurface = displaySurface
        self.appLayout = appLayout
        self.x = appLayout[0][0].buttonRect.x 
        self.y = appLayout[0][0].buttonRect.y 
        self.width = 255
        self.height = 255
        self.selectionImage = pygame.image.load("./Assets/testing.png")
        # self.selectionSurface = pygame.Surface((self.width, self.height))
        self.selectionRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.selectionGrid = [0, 0]
    
    def displayImage(self):
        #selectionCanvas.blit(self.selectionImage, self.selectionRect)
        pygame.draw.rect(self.displaySurface, (255,255,255), self.selectionRect)
    

    def move(self, option):
        numberOfLines = len(self.appLayout)
        numberOfAppsInRow = len(self.appLayout[self.selectionGrid[1]])
        if option == 'LEFT':
            if numberOfAppsInRow == self.selectionGrid[0] + 1:
                self.selectionGrid[0] = 0 
            else:
                self.selectionGrid[0] += 1
        if option == 'RIGHT':
            if 0 == self.selectionGrid[0]:
                self.selectionGrid[0] = numberOfAppsInRow -1 
            else:
                self.selectionGrid[0] -= 1
        if option == 'UP':
            if self.selectionGrid[1] == 0:
                self.selectionGrid[1] = numberOfLines -2 
            else:
                self.selectionGrid[1] -= 1

        if option == 'DOWN':
            if self.selectionGrid[1] == numberOfLines -2:
                self.selectionGrid[1] = 0
            else:
                self.selectionGrid[1] += 1
        #update numberOfAppsInRow with the adjust before checking agian(betterway?) 
        numberOfAppsInRow = len(self.appLayout[self.selectionGrid[1]])
        if numberOfAppsInRow - 1 <= self.selectionGrid[0]:
            self.selectionGrid[0] = numberOfAppsInRow - 1
        

        
        nextApp = self.appLayout[self.selectionGrid[1]][self.selectionGrid[0]]

        self.selectionRect.x, self.selectionRect.y = nextApp.buttonRect.x, nextApp.buttonRect.y 


class Apps:
    def __init__(self, appsFile, displaySurface) -> None:
        self.displaySurface = displaySurface
        self.appsFile = appsFile
        self.appLayout = [[]]
        self.hightAdjustment = self.displaySurface.get_height() * .010 
        self.widthAdjustment = self.displaySurface.get_width() * .79
        self.lineNumber = 0
    def importApps(self):
        with open(self.appsFile, 'r') as apps:

            data = json.load(apps)
            for app in data['apps']:
                newButton = Button(self.widthAdjustment, self.hightAdjustment, app['name'])
                newButton.buttonImage = pygame.image.load(app['image'])
                newButton.buttonImage = pygame.transform.scale(newButton.buttonImage,(256,256))
                newButton.cmd = app['cmd']
                newButton.surface = self.displaySurface
                self.appLayout[self.lineNumber].append(newButton)
                #after button is appended it adjusts the location 
                if self.widthAdjustment < (self.displaySurface.get_width() * .50):
                     self.lineNumber += 1
                     self.appLayout.append([])
                     self.hightAdjustment += self.hightAdjustment + 256
                     self.widthAdjustment = self.displaySurface.get_width() * .79
                else:
                     self.widthAdjustment += -266
            return self.appLayout
    def displayApps(self):
        for line in self.appLayout:
            for button in line:
                button.displayImage()
    def processApps(self, selection):
        for line in self.appLayout:
            for button in line:
                button.processSelection(selection)
    

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
































































































