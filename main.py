#!/usr/bin/python3
import pygame 
from ui import *
import json
#setup
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

#Define Menus
appsMenu = Menu(Canvas.get_width() * .19, 0, 1500, Canvas.get_height(),'appsMenu')
addAppsMenu = Menu(Canvas.get_width() * .19, 0, 1500, Canvas.get_height(),'addAppsMenu')
settingsMenu = Menu(Canvas.get_width() * .19, 0, 1500, Canvas.get_height(),'settingsMenu')
sideMenu = Menu(0, 0, 200, Canvas.get_height(),"sideMenu")
activeMenus = [ sideMenu, appsMenu ]

def showAddAppsMenu():
    activeMenus[1] = addAppsMenu


#Import Buttons to be displayed on Menus

def importSettingsMenu():
    settingsMenuList = [ 'AddApp', 'SomethingFun']
    height =20
    for button in settingsMenuList:
        settingsMenuButton = Button(sideMenu.surface.get_width() * .1, height,150,40, button)
        settingsMenuButton.layer = settingsMenu.surface 
        settingsMenu.buttons.append(settingsMenuButton)
        height += 50
    settingsMenu.button_matrix[0] = sideMenu.buttons
    settingsMenu.isList = True
    return sideMenu.buttons 

def importSideMenu():
    sideMenuList = ['Apps', 'Settings']
    height = 20
    for button in sideMenuList:
        sideMenuButton = Button(sideMenu.surface.get_width() * .1, height,150,40, button)
        sideMenuButton.layer = sideMenu.surface 
        sideMenu.buttons.append(sideMenuButton)
        height += 50
    sideMenu.button_matrix[0] = sideMenu.buttons
    sideMenu.isList = True
    return sideMenu.buttons 

#maybe re-Write this to include other menus
def importApps():
    padding = 25
    button_width = 256
    button_height = 256
    max_width = appsMenu.surface.get_width() - padding
    buttons_per_row = max_width // (button_width + padding)
    
    # Load JSON
    if not os.path.exists('./apps.json'):
        print("apps.json not found, creating a default file.")
        default_data = {"apps": [{"name": "defaultApp", "image": "./Assets/defaultApp.png", "cmd": "echo 'hello'"}]}
        with open('./apps.json', 'w') as f:
            json.dump(default_data, f, indent=2)
    with open('./apps.json', 'r') as apps:
        data = json.load(apps)
        apps_list = data['apps']
    
    # Calculate grid dimensions
    total_buttons = len(apps_list)
    rows = (total_buttons + buttons_per_row - 1) // buttons_per_row  # Ceiling division
    
    # Create a 2D matrix
    appsMenu.button_matrix = [[] for _ in range(rows)]
    
    for i, app in enumerate(apps_list):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = padding + col * (button_width + padding)
        y = padding + row * (button_height + padding)
        
        newButton = Button(x, y, button_width, button_height, app['name'])
        newButton.buttonImage = pygame.image.load(app['image'])
        newButton.buttonImage = pygame.transform.scale(newButton.buttonImage, (button_width, button_height))
        if newButton.buttonText == "defaultApp":
            newButton.onclickFunction = showAddAppsMenu
        newButton.cmd = app['cmd']
        newButton.isImage = True
        newButton.layer = appsMenu.surface
        
        appsMenu.button_matrix[row].append(newButton)
        appsMenu.buttons.append(newButton)
   
    return appsMenu.buttons

def processSideMenuSelect():
    for button in sideMenu.buttons:
        if button.isSelected:
            if button.buttonText == "Apps":
                activeMenus[1] = appsMenu
            if button.buttonText == "Settings":
                activeMenus[1] = settingsMenu

def play_music():
    Music_Switch = not guiobjects.Music_Switch
    mixer = pygame.mixer
    mixer.init()
    mixer.music.load("./Sound/Music/space-trip.mp3")
    mixer.music.set_volume(0.7)
    if Music_Switch:
        mixer.music.play(-1)
    elif not Music_Switch:
        mixer.music.stop()

def updateMenus():
    for menu in activeMenus:
        if menu.name is not "sideMenu":
            menu.surface.fill((0, 0, 0, 25))
        menu.surface.set_alpha(255)
        for button in menu.buttons:
            button.display()
        menu.display()
    

def updateCanvas():
    while True:
        processSideMenuSelect()
        Canvas.blit(background_img, dest = background_position) 
        selection.moveSelection()
        updateMenus()
        clock.tick(FPS)
        pygame.display.update()

#RUN
if __name__ == "__main__":
    importSettingsMenu()
    importApps()
    importSideMenu()
    selection = Selection(sideMenu, activeMenus)
    updateCanvas()
    pygame.quit()
