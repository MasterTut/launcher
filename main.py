#!/usr/bin/python3
from ui import *
from components import *
import json
#setup
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()


def showAddAppsMenu():
    menu = activeMenus[2]
    menu.hide = False
    selection.menuSelected = menu

#Not using this function may implment as feature
def play_music():
    Mixer.music.load(MUSIC)
    Mixer.music.set_volume(100)
    #if Music_Switch:
    Mixer.music.play()
    #elif not Music_Switch:
    #    mixer.music.stop()

#Displays Menus and the buttons on those menus
def updateMenus():
    #for button in sideMenu.menu.buttons:
        #if button.isSelected:
        #    activeMenus[1] = next(( menu for menu in sideMenu.menu.nestedMenus if menu.name == button.buttonText), None)
            #if len(activeMenus[1].menuList) > 0:
            #    activeMenus[2] = activeMenus[1].nestedMenus[0] 
    #for menu in activeMenus:
    sideMenu.menu.surface.set_alpha(255)
    sideMenu.menu.display()

#Creates the game loop to update the screen
def updateCanvas():
    while True:
        Canvas.blit(background_img, dest = background_position) 
        selection.moveSelection()
        updateMenus()
        clock.tick(FPS)
        pygame.display.update()

#Initalize and run
if __name__ == "__main__":
    defaultMenu = Menu(Canvas.get_width() * .19, 0, Canvas.get_width(), Canvas.get_height() -40,'defaultMenu')
    sideMenu = SideMenu(0, 20, 300, Canvas.get_height() -40)
    
    sideMenu.importMenusFromFile()
    activeMenus = [sideMenu.menu ] 
    selection = Selection(sideMenu.menu)
    updateCanvas()
    pygame.quit()
