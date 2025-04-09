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

class AddAppMenu(Menu):
    def __init__(self,x, y,width,height, name='AddAppMenu'):
        super().__init__(x, y, width, height, name)
        self.input_box_fields = ['Menu', 'name', 'image','cmd']
        self.input_boxes = [TextInput(500, 100 + i * 50, 600, 40,self.surface, field) 
            for i, field in enumerate(self.input_box_fields)]
        self.buttons.append(Button(1000,300,150,40,self.surface, "Submit"))
    def displayFields(self):
        for input in self.input_boxes:
            input.display()
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
        

    def navigateFields(self):
        if self.hide == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.TEXTINPUT:
                    for input in self.input_boxes:
                        if input.isActive:
                            input.text += event.text
                            input.update_text()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_TAB:
                         # Switch active input box
                        for i, box in enumerate(self.input_boxes):
                            if box.isActive:
                                box.isActive = False
                                next_box = self.input_boxes[(i + 1) % len(self.input_boxes)]
                                next_box.isActive = True
                                print(f"Switched to {next_box.name}, isActive: {next_box.isActive}")
                                break
                        # Activate the first box if none were active
                        if not any(box.isActive for box in self.input_boxes):
                            self.input_boxes[0].isActive = True 
                                                                                                     
                    elif event.key == pygame.K_BACKSPACE:
                        for input in self.input_boxes:
                            if input.isActive:
                                input.text =  input.text[:-1]
                                input.update_text()
                                                                                                     
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.buttons[0].buttonRect.collidepoint(mouse_pos):
                        self.submitButtonFunc()
                    for input in self.input_boxes:
                        input.isActive = False
                        if input.rect.collidepoint(mouse_pos):
                            input.isActive = True
                        else:
                            input.isActive = False
        else:
            return
