#!/usr/bin/python3
import pygame 
import sys
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

sideMenu = gui_objects.sideMenu
appsMenu = gui_objects.appsMenu
menuSelected = pygame.Surface

def menuSelect():
    menuSelected = appsMenu
    return menuSelected
    
def importSideMenu():
    sideMenuList = ['Media', 'Settings', 'other', 'other2']
    sideMenuButtons = []
    height = 40
    for button in sideMenuList:
        sideMenuButton = gui_objects.Button(sideMenu.get_width() * .1, height, button)
        sideMenuButton.surface = gui_objects.sideMenu
        sideMenuButtons.append(sideMenuButton)
        height += 40 
    return sideMenuButtons 


def importApps():
    appsArray = [] 
    panding = 25
    y = panding 
    x = panding 
    with open('./apps.json', 'r') as apps:
                                                                                                    
        data = json.load(apps)
        for app in data['apps']:
            newButton = gui_objects.Button(x, y, app['name'])
            newButton.buttonImage = pygame.image.load(app['image'])
            newButton.buttonImage = pygame.transform.scale(newButton.buttonImage,(newButton.width,newButton.height))
            newButton.cmd = app['cmd']
            newButton.isImage = True
            newButton.surface = appsMenu
            appsArray.append(newButton)
            #after button is appended it adjusts the location
            #location of apps are adjusted based on the surface area of appsMenu vs the window size
            #the idea is more consistancy dispite window size
            if x > (appsMenu.get_width() -newButton.width*2 + panding ):
                 y += newButton.height + panding 
                 x = panding 
            else:
                 x += newButton.width + panding 
        return appsArray 

#Start Selction on the top right App
apps, sideMenuButtons = importApps(), importSideMenu()
selection = gui_objects.Selection(apps, sideMenuButtons)

    

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


#defines key mappings
def controls():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("do nothing")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RIGHT:
                selection.anotherMoveFunc('RIGHT')
            if event.key == pygame.K_LEFT:
                selection.anotherMoveFunc('LEFT')
            if event.key == pygame.K_DOWN:
                selection.anotherMoveFunc('DOWN') 
            if event.key == pygame.K_UP:
                selection.anotherMoveFunc('UP') 
            if event.key == pygame.K_RETURN:
                selection.anotherMoveFunc('ENTER')


def displayButtons(buttons):
    for button in buttons:
        button.display()

def updateMenus():
    appsMenu.fill((40,40,40))
    sideMenu.fill((40,40,40))


def updateCanvas(): 
    #canvas.blit(background, dest = background_position)
    canvas.blit(appsMenu, (canvas.get_width() * .19, 20))
    canvas.blit(sideMenu, (10, 20))
    #appsMenu.blit(selection.selectionImage, selection.x, selection.y) 
    updateMenus()
    displayButtons(apps)
    pygame.display.update()

def gameLoop():
    global text, elapsed_time 
    while True:
        clock.tick(gui_objects.FPS)
        controls()
        updateCanvas()


#RUN
if __name__ == "__main__":
    gameLoop()
    pygame.quit()
