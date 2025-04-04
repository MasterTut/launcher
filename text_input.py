from ui import *


class TextInput:
    def __init__(self, x, y, width, height, name="Default") -> None:
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
    def display(self, surface):
        if self.isActive:
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 0)
        
        # Adjust rect position to align with name text
        self.rect = pygame.Rect(self.x, self.nameY, self.width, self.height)
        pygame.draw.rect(surface, self.color, self.rect, 2)
        
        # Draw the input text inside the box (separate from name)
        surface.blit(self.nameSurface, (self.nameX, self.nameY))
        surface.blit(self.textSurface, (self.textX, self.textY))


