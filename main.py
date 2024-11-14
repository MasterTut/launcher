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

    
def importSideMenu():
    sideMenuList = ['Media', 'Settings', 'other', 'other2']
    sideMenuButtons = []
    height = 20
    for button in sideMenuList:
        sideMenuButton = gui_objects.Button(sideMenu.surface.get_width() * .1, height, button)
        sideMenuButton.buttonRect.width= 20
        sideMenuButton.buttonRect.height = 50 
        sideMenuButton.surface = sideMenu.surface 
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
            newButton.surface = appsMenu.surface
            appsArray.append(newButton)
            #after button is appended it adjusts the location
            #location of apps are adjusted based on the surface area of appsMenu vs the window size
            #the idea is more consistancy dispite window size
            if x > (appsMenu.surface.get_width() -newButton.width*2 + panding ):
                 y += newButton.height + panding 
                 x = panding 
            else:
                 x += newButton.width + panding 
        return appsArray 

#Start Selction on the top right App
allButtons =[ *importApps(), *importSideMenu() ]
selection = gui_objects.Selection(allButtons)

#select the first button when program is run >
# selection.select()
    
def displayButtons(allButtons):
    for button in allButtons:
        button.display()

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


#defines key mappings, the event listener needs to be in gameLoop
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
                selection.move('RIGHT')
            if event.key == pygame.K_LEFT:
                selection.move('LEFT')
            if event.key == pygame.K_DOWN:
                selection.move('DOWN') 
            if event.key == pygame.K_UP:
                selection.move('UP') 
            if event.key == pygame.K_RETURN:
                selection.move('ENTER')


def updateMenus():
    appsMenu.surface.fill((40,40,40))
    sideMenu.surface.fill((40,40,40))

def updateCanvas(): 
    #canvas.blit(background, dest = background_position)
    canvas.blit(appsMenu.surface, (appsMenu.x, appsMenu.y))
    canvas.blit(sideMenu.surface, (sideMenu.x, sideMenu.y))
    #appsMenu.blit(selection.selectionImage, selection.x, selection.y) 
    updateMenus()
    displayButtons(allButtons)
    pygame.display.update()

def gameLoop():
    global text, elapsed_time 
    while True:
        clock.tick(gui_objects.FPS)
        # controls()
        selection.moveSlection()
        updateCanvas()


#RUN
if __name__ == "__main__":
    gameLoop()
    pygame.quit()
