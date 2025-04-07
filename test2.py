from text_input import *
import json
# Variables to store input
# Main game loop


input_boxes = []

submitButton = Button(500, 300,150,40, "Submit")

submitButton.layer = Canvas
def importInputBox():
    input_box_fields = ['Menu', 'name', 'image','cmd']
    x = 100
    for field in input_box_fields:
        input_box = TextInput(500, x, 600, 40, field)
        x += 50
        input_boxes.append(input_box)

def submitButtonFunc():
    dataFromTextInput = {'name': '', 'image': '', 'cmd': ''}
    menuFromInput = input_boxes[0].text
    for input in input_boxes[1:]:
        print(input.name)
        dataFromTextInput[input.name] = input.text
    with open (APPS_PATH, 'r') as file:
        dataFromFile = json.load(file)
    if menuFromInput in dataFromFile:
        dataFromFile[input_boxes[0].text].append(dataFromTextInput) 
    else:
        dataFromFile[input_boxes[0].text] = [dataFromTextInput]
    with open (APPS_PATH, 'w') as file:
        json.dump(dataFromFile, file, indent =4)

    print(dataFromTextInput)


importInputBox()
submitButton.onclickFunction = submitButtonFunc


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.TEXTINPUT:
            for input in input_boxes:
                if input.isActive:
                    input.text += event.text
                    input.update_text()
                    
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_TAB:
                 # Switch active input box
                for i, box in enumerate(input_boxes):
                    if box.isActive:
                        box.isActive = False
                        next_box = input_boxes[(i + 1) % len(input_boxes)]
                        next_box.isActive = True
                        print(f"Switched to {next_box.name}, isActive: {next_box.isActive}")
                        break
                # Activate the first box if none were active
                if not any(box.isActive for box in input_boxes):
                    input_boxes[0].isActive = True 

            elif event.key == pygame.K_BACKSPACE:
                for input in input_boxes:
                    if input.isActive:
                        input.text =  input.text[:-1]
                        input.update_text()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if submitButton.buttonRect.collidepoint(mouse_pos):
                submitButton.onclickFunction()
            for input in input_boxes:
                input.isActive = False
                if input.rect.collidepoint(mouse_pos):
                    input.isActive = True
                else:
                    input.isActive = False

            
    # Clear the screen
    
    
    Canvas.fill((255, 255, 255))
    submitButton.display() 
    # Draw the input boxes
    for input in input_boxes:
        input.display(Canvas)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
