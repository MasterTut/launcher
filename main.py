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
    sideMenuList = []
    mediaButton = gui_objects.Button(sideMenu.get_width() * .1,40, "Media")
    mediaButton.isImage = False
    mediaButton.surface = gui_objects.sideMenu
    sideMenuList.append(mediaButton)
    return sideMenuList


def importApps():
    displaySurface = appsMenu 
    appLayout = [[]]
    hightAdjustment = displaySurface.get_height() * .010 
    widthAdjustment = displaySurface.get_width() * .79
    lineNumber = 0
    with open('./apps.json', 'r') as apps:
                                                                                                    
        data = json.load(apps)
        for app in data['apps']:
            newButton = gui_objects.Button(widthAdjustment, hightAdjustment, app['name'])
            newButton.buttonImage = pygame.image.load(app['image'])
            newButton.buttonImage = pygame.transform.scale(newButton.buttonImage,(256,256))
            newButton.cmd = app['cmd']
            newButton.surface = displaySurface
            appLayout[lineNumber].append(newButton)
            #after button is appended it adjusts the location
            #location of apps are adjusted based on the surface area of appsMenu vs the window size
            #the idea is more consistancy dispite window size
            if widthAdjustment < (displaySurface.get_width() * .50):
                 lineNumber += 1
                 appLayout.append([])
                 hightAdjustment += hightAdjustment + 266
                 widthAdjustment = displaySurface.get_width() * .79
            else:
                 widthAdjustment += -280
        return appLayout

#Start Selction on the top right App            
selection = gui_objects.Selection(importApps(), importSideMenu())

    

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
    appsMenu.fill((40,40,40))
    sideMenu.fill((40,40,40))


def updateCanvas(): 
    #canvas.blit(background, dest = background_position)
    canvas.blit(sideMenu, (10, 20))
    canvas.blit(appsMenu, (canvas.get_width() * .19, 20))
    updateMenus()
    selection.select()
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
