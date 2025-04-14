#!/usr/bin/python3
from ui import *
from text_input import *
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
    Music_Switch = not Music_Switch
    mixer = pygame.mixer
    mixer.init()
    mixer.music.load("./Sound/Music/space-trip.mp3")
    mixer.music.set_volume(0.7)
    if Music_Switch:
        mixer.music.play(-1)
    elif not Music_Switch:
        mixer.music.stop()

#Displays Menus and the buttons on those menus
def updateMenus():
    
    for button in sideMenu.menu.buttons:
        if button.isSelected:
            activeMenus[1] = next(( menu for menu in sideMenu.sideMenus if menu.name == button.buttonText), None)
    for menu in activeMenus:
        if menu.name == "addAppMenu" and menu.isSelected:
            menu.hide = False
        elif menu.name == "addAppMenu" and not menu.isSelected:
            menu.hide = True
        menu.surface.set_alpha(255)
        menu.display()

#Creates the game loop to update the screen
def updateCanvas():
    while True:
        #processSideMenuSelect()
        Canvas.blit(background_img, dest = background_position) 
        selection.moveSelection()
        updateMenus()
        clock.tick(FPS)
        pygame.display.update()

#Initalize and run
if __name__ == "__main__":
    defaultMenu = Menu(Canvas.get_width() * .19, 0, Canvas.get_width(), Canvas.get_height(),'defaultMenu')
    addAppMenu = AddAppMenu(Canvas.get_width() *.19, 0, Canvas.get_width(), Canvas.get_height()).menu
    sideMenu = SideMenu(0, 20, 300, Canvas.get_height() -40)
    sideMenu.importMenusFromFile()
    activeMenus = [sideMenu.menu, sideMenu.sideMenus[0], addAppMenu] 
    selection = Selection(activeMenus)
    updateCanvas()
    pygame.quit()
