#!/usr/bin/python3
from ui import *
from text_input import *
import json
#setup
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

#Define Default Menu
defaultMenu = Menu(Canvas.get_width() * .19, 0, 1500, Canvas.get_height(),'defaultMenu')
addAppMenu = AddAppMenu(Canvas.get_width() *.21, 0, 1500, Canvas.get_height())
#addAppsMenu = AddAppMenu(0, 0, 1500, Canvas.get_height(),'addAppsMenu')

Menus =[]
activeMenus = [ defaultMenu, defaultMenu, addAppMenu]

def showAddAppsMenu():
    menu = activeMenus[2]
    menu.hide = False
    selection.menuSelected = menu



#The side menu(on right of screen) controls what is displayed on left of screen (apps Menu) 
def importSideMenu(sideMenuList):
    sideMenu = Menu(0, 0, 300, Canvas.get_height(),"sideMenu")
    height = 20
    for button in sideMenuList:
        sideMenuButton = Button(sideMenu.surface.get_width() * .2, height,150,40,sideMenu.surface, button)
        sideMenu.buttons.append(sideMenuButton)
        height += 50
    sideMenu.button_matrix[0] = sideMenu.buttons
    sideMenu.isList = True
    return sideMenu

#Creates app menus and buttons based file from root directory
def importApps(menuFromFile):
    menuFromFile = Menu(Canvas.get_width() * .19, 0, 1450, Canvas.get_height(), menuFromFile)
    padding = 25
    button_width = 256
    button_height = 256
    max_width = menuFromFile.surface.get_width() - padding
    buttons_per_row = max_width // (button_width + padding)
    
    # Load JSON
    if not os.path.exists(APPS_PATH):
        print("apps.json not found, creating a default file.")
        default_data = {"apps": [{"name": "defaultApp", "image": "./Assets/defaultApp.png", "cmd": "echo 'hello'"}]}
        with open(APPS_PATH, 'w') as f:
            json.dump(default_data, f, indent=2)
    with open(APPS_PATH, 'r') as apps:
        data = json.load(apps)
        apps_list = data[menuFromFile.name]
    
    # Calculate grid dimensions
    total_buttons = len(apps_list)
    rows = (total_buttons + buttons_per_row - 1) // buttons_per_row  # Ceiling division
    
    # Create a 2D matrix
    menuFromFile.button_matrix = [[] for _ in range(rows)]
    for i, app in enumerate(apps_list):
        row = i // buttons_per_row
        col = i % buttons_per_row
        x = padding + col * (button_width + padding)
        y = padding + row * (button_height + padding)
        newButton = Button(x, y, button_width, button_height,menuFromFile.surface, app['name'])
        newButton.buttonImage = pygame.image.load(app['image'])
        newButton.buttonImage = pygame.transform.scale(newButton.buttonImage, (button_width, button_height))
        if newButton.buttonText == "defaultApp":
            newButton.onclickFunction = showAddAppsMenu
        newButton.cmd = app['cmd']
        newButton.isImage = True
        #newButton.layer = menuFromFile.surface
        menuFromFile.button_matrix[row].append(newButton)
        menuFromFile.buttons.append(newButton)
    Menus.append(menuFromFile) 
    return menuFromFile.buttons

#Reads a json file from project root and creates menus 
def importMenusFromFile():
    menusFromFile =[]
    with open('./apps.json', 'r') as apps:
        data = json.load(apps)
    for menu in data:
        importApps(menu)
        menusFromFile.append(menu)
    return importSideMenu(menusFromFile)
    
#Displays the App Menu on the right of screen when the sideMenu button is highlighted
def processSideMenuSelect():
    for button in activeMenus[0].buttons:
        if button.isSelected:
            activeMenus[1] = next(( menu for menu in Menus if menu.name == button.buttonText), None)

#Not using this function may implment as feature
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

#Displays Menus and the buttons on those menus
def updateMenus():
    for menu in activeMenus:
        menu.surface.fill((0, 0, 50, 25))
        if menu.name == "addAppMenu" and menu.isSelected:
            menu.hide = False
            menu.surface.fill((100,100,100))
        elif menu.name == "addAppMenu" and not menu.isSelected:
            menu.hide = True

        
        menu.surface.set_alpha(255)
        menu.display()

#Creates the game loop to update the screen
def updateCanvas():
    while True:
        processSideMenuSelect()
        Canvas.blit(background_img, dest = background_position) 
        selection.moveSelection()
        updateMenus()
        clock.tick(FPS)
        pygame.display.update()

#Initalize and run
if __name__ == "__main__":
    activeMenus[0] = importMenusFromFile() 
    selection = Selection(activeMenus)
    updateCanvas()
    pygame.quit()
