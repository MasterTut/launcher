#!/usr/bin/python3
import pygame 
from ui_components import * 
import json
#setup
#canvas = guiobjects.canvas
pygame.display.set_caption("TVLauncher")
clock = pygame.time.Clock()



# Add text fields and submit button
name_field = TextField(50, 50, 500, 50, "Name")
image_field = TextField(50, 120, 500, 50, "Image")
cmd_field = TextField(50, 190, 500, 50, "Cmd")
submit_button = Button(200, 260, 200, 50, "Submit")
name_field.layer = addAppMenu.surface
image_field.layer = addAppMenu.surface
cmd_field.layer = addAppMenu.surface
submit_button.layer = addAppMenu.surface
submit_button.isImage = False  # Text button

# Add to menu
addAppMenu.buttons = [name_field, image_field, cmd_field, submit_button]
addAppMenu.button_matrix = [[name_field], [image_field], [cmd_field], [submit_button]]  # 1 per row for form navigation

def showMenu():
    guiobjects.Menus[1] = addAppMenu

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
        
        newButton = Button(x, y, button_width, button_height, app['name'])
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
    # Draw appsMenu and sideMenu first
    for menu in Menus:
        if menu.name != "addAppMenu":
            menu.surface.fill((0, 0, 0, 0))
            menu.surface.set_alpha(255)
            for button in menu.buttons:
                button.display()
            menu.show_hide_toggle()
    
    # Draw addAppMenu on top if active
    if selection.menuSelected.name == "addAppMenu":
        addAppMenu = selection.menuSelected
        addAppMenu.surface.fill((50, 50, 50, 200) if addAppMenu.is_form else (0, 0, 0, 0))  # Semi-transparent for forms
        addAppMenu.surface.set_alpha(255)
        for button in addAppMenu.buttons:
            button.display()
        canvas.blit(addAppMenu.surface, (addAppMenu.x, addAppMenu.y))


def updateCanvas():
    while True:
        canvas.blit(background_img, dest = background_position) 
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
