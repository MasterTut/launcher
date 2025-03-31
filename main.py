#!/usr/bin/python3
import pygame 
from ui_components import *
from add_app_menu import addAppMenu, toggleAddAppMenu
import json
#setup
#canvas = guiobjects.canvas
pygame.display.set_caption("TVLauncher")
clock = pygame.time.Clock()

Menus.append(addAppMenu)

def showMenu():
    Menus[1] = addAppMenu

def importSideMenu():
    sideMenuList = ['Media', 'Settings']
    height = 20
    for button in sideMenuList:
        sideMenuButton = Button(sideMenu.surface.get_width() * .1, height,150,40, button)
        sideMenuButton.layer = sideMenu.surface 
        sideMenu.buttons.append(sideMenuButton)
        height += 50 
    return sideMenu.buttons 

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
    appsMenu.button_matrix = button_matrix = [[] for _ in range(rows)]
    
    for i, app in enumerate(apps_list):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = padding + col * (button_width + padding)
        y = padding + row * (button_height + padding)
        
        newButton = Button(x, y, button_width, button_height, app['name'])
        newButton.buttonImage = pygame.image.load(app['image'])
        newButton.buttonImage = pygame.transform.scale(newButton.buttonImage, (button_width, button_height))
        if newButton.buttonText == "defaultApp":
            newButton.onclickFunction = toggleAddAppMenu
        newButton.cmd = app['cmd']
        newButton.isImage = True
        newButton.layer = appsMenu.surface
        
        appsMenu.button_matrix[row].append(newButton)
        appsMenu.buttons.append(newButton)
   
    return appsMenu.buttons


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
    for menu in Menus:
        menu.surface.fill((0, 0, 0, 0))
        menu.surface.set_alpha(255)
        for button in menu.buttons:
            button.display()
        menu.display()
    

def updateCanvas():
    while True:
        Canvas.blit(background_img, dest = background_position) 
        selection.moveSelection()
        updateMenus()
        clock.tick(FPS)
        pygame.display.update()

#RUN
if __name__ == "__main__":
    importApps()
    importSideMenu()
    selection = Selection()
    updateCanvas()
    pygame.quit()
