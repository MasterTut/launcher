#!/usr/bin/python3
from ui_components import Menus, Menu, TextField, Button, Canvas 
addAppMenu = Menu(Canvas.get_width() * .19, 20, 1500, 1000, "addApp")



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
addAppMenu.hide = True

# Add to menu
addAppMenu.buttons = [name_field, image_field, cmd_field, submit_button]
addAppMenu.button_matrix = [[name_field], [image_field], [cmd_field], [submit_button]]  # 1 per row for form navigation

def toggleAddAppMenu():
    for menu in Menus:
        menu.hide = not menu.hide 
