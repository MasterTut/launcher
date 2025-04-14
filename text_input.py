from ui import *
import json

class TextInput:
    def __init__(self, x, y, width, height, menu, name="Default") -> None:
        self.menu = menu
        self.name = name
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.isActive = False
        self.color = (0, 0, 0)
        self.nameSurface = Font.render(f"{self.name}: ", True, (0, 0, 0))
        self.nameX = self.x - self.nameSurface.get_width() - 5  # Position to the left of the box
        self.nameY = self.y + (self.height - self.nameSurface.get_height()) // 2  # Center vertically
        self.text = ""
        self.textSurface = Font.render(self.text, True, (0, 0, 0))
        self.textX = self.x + 5  # Small padding inside the box
        self.textY = self.y + (self.height - self.textSurface.get_height()) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def update_text(self):
         #Update the text surface when text changes
        self.textSurface = Font.render(self.text, True, (0, 0, 0))
        self.textY = self.y + (self.height - self.textSurface.get_height()) // 2  # Recenter vertically
    def display(self):
        if self.isActive:
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 0)
        
        # Adjust rect position to align with name text
        self.rect = pygame.Rect(self.x, self.nameY, self.width, self.height)
        pygame.draw.rect(self.menu, self.color, self.rect, 2)
        
        # Draw the input text inside the box (separate from name)
        self.menu.blit(self.nameSurface, (self.nameX, self.nameY))
        self.menu.blit(self.textSurface, (self.textX, self.textY))

class AddAppMenu:
    def __init__(self,x, y,width,height, name='addAppMenu'):
        self.menu = Menu(x, y, width, height, name)
        self.name = self.menu.name
        self.surface = self.menu.surface
        self.input_box_fields = ['Menu', 'name', 'image','cmd']
        self.menu.input_boxes = [TextInput(500, 100 + i * 50, 600, 40,self.menu.surface, field) 
            for i, field in enumerate(self.input_box_fields)]
        self.input_boxes = self.menu.input_boxes
        self.menu.buttons.append(Button(1000,300,150,40,self.menu.surface, "Submit"))
        self.menu.isList = True
        self.menu.hide = True
        self.menu.isSelected = False
    
    def submitButtonFunc(self):
        dataFromTextInput = {'name': '', 'image': '', 'cmd': ''}
        self.menuFromInput = self.input_boxes[0].text
        for input in self.input_boxes[1:]:
            dataFromTextInput[input.name] = input.text
        with open (APPS_PATH, 'r') as file:
            dataFromFile = json.load(file)
        if self.menuFromInput in dataFromFile:
            dataFromFile[self.input_boxes[0].text].append(dataFromTextInput) 
        else:
            dataFromFile[self.input_boxes[0].text] = [dataFromTextInput]
        if os.path.exists(dataFromTextInput['image']):
            with open (APPS_PATH, 'w') as file:
                json.dump(dataFromFile, file, indent =4)
            self.toggleDisplay()
            print('Write Complete')
        else:
            self.showError(message="Path Does not exit")
    def display(self):
            self.menu.display()
    def toggleDisplay(self):
            self.menu.toggleDisplay()
    def showError(self, message, duration=2000):
            return self.menu.showError(message, duration)
           
#Testing 
class SideMenu:
    def __init__(self,x, y,width,height, name='sideMenu'):
        self.menu = Menu(x, y, width, height, name)
        self.sideMenuList = []
        self.isList = self.menu.isList 
        self.buttons = self.menu.buttons
        self.button_matrix = self.menu.button_matrix
        self.sideMenus = [] 

    
    def importSideMenu(self):
        sideMenu = Menu(0, 20, 300, Canvas.get_height() -40,"sideMenu")
        height = 20
        for button in self.sideMenuList:
            sideMenuButton = Button(sideMenu.surface.get_width() * .2, height,150,40,sideMenu.surface, button)
            self.buttons.append(sideMenuButton)
            height += 50
        self.button_matrix[0] = sideMenu.buttons
        #return sideMenu

    def importApps(self, menuFromFile):
        menuFromFile = Menu(Canvas.get_width() * .19, 20, Canvas.get_width(), Canvas.get_height() -40, menuFromFile)
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
            newButton.cmd = app['cmd']
            newButton.isImage = True
            #newButton.layer = menuFromFile.surface
            menuFromFile.button_matrix[row].append(newButton)
            menuFromFile.buttons.append(newButton)
        self.sideMenus.append(menuFromFile) 
        return menuFromFile.buttons

    def importMenusFromFile(self):
        #menusFromFile =[]
        with open('./apps.json', 'r') as apps:
            data = json.load(apps)
        for menu in data:
            self.importApps(menu)
            self.sideMenuList.append(menu)
        #takes list of strings from file 
        self.importSideMenu()

    def processSideMenuSelect(self, activeMenus):
        for button in activeMenus[0].buttons:
            if button.isSelected:
                activeMenus[1] = next(( menu for menu in self.sideMenus if menu.name == button.buttonText), None)
