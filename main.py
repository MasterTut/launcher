#!/usr/bin/python3
import pygame 
import guiobjects 
import json
#setup
canvas = guiobjects.canvas
canvas.blit(guiobjects.background_img, dest = guiobjects.background_position) 
#canvas.fill((30, 30, 50))
pygame.display.set_caption("GameLauncher")
clock = pygame.time.Clock()
#Import Images 


#setup GUI
addAppMenu = guiobjects.addAppMenu
sideMenu = guiobjects.sideMenu
appsMenu = guiobjects.appsMenu
hideAddAppMenu = guiobjects.Button(20, 20, 200, 40, 'hideMenu')
hideAddAppMenu.layer = addAppMenu.surface
addAppMenu.buttons = [hideAddAppMenu]

def showMenu():
    guiobjects.Menus[1] = addAppMenu

def importSideMenu():
    sideMenuList = ['Media', 'Settings']
    height = 20
    for button in sideMenuList:
        sideMenuButton = guiobjects.Button(sideMenu.surface.get_width() * .1, height,150,40, button)
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
    with open('./apps.json', 'r') as apps:
        data = json.load(apps)
        apps_list = data['apps']
    
    # Calculate grid dimensions
    total_buttons = len(apps_list)
    rows = (total_buttons + buttons_per_row - 1) // buttons_per_row  # Ceiling division
    
    # Create a 2D matrix
    button_matrix = [[] for _ in range(rows)]
    button_flat_list = []  # Keep flat list for compatibility
    
    for i, app in enumerate(apps_list):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = padding + col * (button_width + padding)
        y = padding + row * (button_height + padding)
        
        newButton = guiobjects.Button(x, y, button_width, button_height, app['name'])
        newButton.buttonImage = pygame.image.load(app['image'])
        newButton.buttonImage = pygame.transform.scale(newButton.buttonImage, (button_width, button_height))
        if newButton.buttonText == "AddApp":
            newButton.onclickFunction = showMenu 
        newButton.cmd = app['cmd']
        newButton.isImage = True
        newButton.layer = appsMenu.surface
        
        button_matrix[row].append(newButton)
        button_flat_list.append(newButton)
    
    # Assign to appsMenu
    appsMenu.buttons = button_flat_list  # Keep flat list for now
    appsMenu.button_matrix = button_matrix  # Add matrix for grid navigation
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
    for menu in guiobjects.Menus:
        canvas.blit(menu.surface, (menu.x, menu.y))
        menu.surface.fill((0,0,0,0))
        menu.surface.set_alpha(20)
        for button in menu.buttons:
            button.display()

def updateCanvas():
    #canvas.blit(guiobjects.background_img, dest = background_position) 
    updateMenus()
    pygame.display.update()

def gameLoop():
    while True:
        updateCanvas()
        clock.tick(guiobjects.FPS)
        selection.moveSelection()

#RUN
if __name__ == "__main__":
    importApps()
    importSideMenu()
    selection = guiobjects.Selection()
    gameLoop()
    pygame.quit()
