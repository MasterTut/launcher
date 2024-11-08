#!/usr/bin/python3
import pygame 
import sys
import gui_objects
#setup
canvas = gui_objects.canvas
canvas.fill((105, 105, 105))
pygame.display.set_caption("GameLauncher")
clock = pygame.time.Clock()
#Import Images 
background= pygame.image.load("./Images/background.png")
background_position = (0, 0)

#setup font 
font = pygame.font.Font('./Font/VarinonormalRegular-1GXaM.ttf', 20)

#setup GUI 
mediaButton = gui_objects.Button(100,40, "Media") 
sideMenu = pygame.Surface((200,gui_objects.resolutionHeight))
sideMenu.fill((50,10,0))
appsMenu = pygame.Surface((gui_objects.resolutionWidth * .8,gui_objects.resolutionHeight *.9))
print(canvas.get_height())
#appsMenu.fill((0,20,0))
mediaButton.surface = sideMenu

apps = gui_objects.Apps('./apps.json', appsMenu)
appLayout = apps.importApps() 

#Start Selction on the top right App            
selection = gui_objects.Selection(appLayout, appsMenu)

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
                apps.processApps(selection)
                print("ENTER")

def updateCanvas():
    #canvas.blit(background, dest = background_position)
    #canvas.blit(sideMenu, (10,0))
    canvas.blit(appsMenu, (canvas.get_width() * .19, 20))
    apps.displayApps()
    # sideMenu.blit(mediaButton.font_rendered, (mediaButton.x, mediaButton.y))
    #mediaButton.display()
    selection.displayImage()
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
