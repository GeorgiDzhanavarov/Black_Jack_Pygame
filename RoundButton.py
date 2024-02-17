import pygame

class RoundButton():

    def __init__(self, x, y, radius, color, text=''):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font(None, 28)
        self.clicked = False

    def draw(self, screen):
        # Draw the button
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, 2)  # Outer border

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if self.is_clicked(mouse_pos):
                    self.clicked = True
                    return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.clicked = False

    def is_clicked(self, mouse_pos):
        # Check if the mouse click is within the button
        distance_squared = (mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2
        return distance_squared <= self.radius ** 2