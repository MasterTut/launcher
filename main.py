#!/usr/bin/python3
import pygame 
import gui_objects
import json
#setup
canvas = gui_objects.canvas
canvas.fill((30, 30, 30))
pygame.display.set_caption("GameLauncher")
clock = pygame.time.Clock()
#Import Images 
background= pygame.image.load("./Images/background.png")
background_position = (0, 0)

#setup GUI
addAppMenu = gui_objects.addAppMenu
sideMenu = gui_objects.sideMenu
appsMenu = gui_objects.appsMenu
showAddAppMenu = False 

def addApp():
    global showAddAppMenu
    showAddAppMenu = not showAddAppMenu

def importSideMenu():
    sideMenuList = ['Media', 'Settings']
    height = 20
    for button in sideMenuList:
        sideMenuButton = gui_objects.Button(sideMenu.surface.get_width() * .1, height,150,40, button)
        sideMenuButton.layer = sideMenu.surface 
        sideMenu.buttons.append(sideMenuButton)
        height += 50 
    return sideMenu.buttons 


def importApps():
    panding = 25
    x = panding 
    y = panding 
    with open('./apps.json', 'r') as apps:
        data = json.load(apps)
        for app in data['apps']:
            newButton = gui_objects.Button(x, y,256,256, app['name'])
            newButton.buttonImage = pygame.image.load(app['image'])
            newButton.buttonImage = pygame.transform.scale(newButton.buttonImage,(newButton.width,newButton.height))
            if newButton.buttonText == "AddApp":
                newButton.onclickFunction = addApp
            newButton.cmd = app['cmd']
            newButton.isImage = True
            newButton.layer = appsMenu.surface
            appsMenu.buttons.append(newButton)
            #after button is appended it adjusts the location
            #location of apps are adjusted based on the surface area of appsMenu vs the window size
            #the idea is more consistancy dispite window size
            if x > (appsMenu.surface.get_width() -newButton.width*2 + panding ):
                 y += newButton.height + panding 
                 x = panding 
            else:
                 x += newButton.width + panding
        return appsMenu.buttons 

importApps()
importSideMenu()
selection = gui_objects.Selection()
    

def play_music():
    Music_Switch = not gui_objects.Music_Switch
    mixer = pygame.mixer
    mixer.init()
    mixer.music.load("./Sound/Music/space-trip.mp3")
    mixer.music.set_volume(0.7)
    if Music_Switch:
        mixer.music.play(-1)
    elif not Music_Switch:
        mixer.music.stop()


def updateMenus():
    for menu in gui_objects.Menus:
        if menu.name == 'addApp' and showAddAppMenu == False:
            continue
        canvas.blit(menu.surface, (menu.x, menu.y))
        menu.surface.fill((40,40,40))  
        for button in menu.buttons:
            button.display()


def updateCanvas(): 
    # canvas.blit(background, dest = background_position) #uncomment to add background image
    updateMenus()
    pygame.display.update()

def gameLoop():
    while True:
        clock.tick(gui_objects.FPS)
        selection.moveSelection()
        updateCanvas()


#RUN
if __name__ == "__main__":
    gameLoop()
    pygame.quit()
