import pygame

class TextField:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.text_color = (0, 0, 0)
        self.background_color = (255, 255, 255)

    def change_text(self, new_text):
        self.text = new_text

    def draw(self, screen):
        # Draw the text field
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

        # Render the text
        # text_surface = self.font.render(self.text, True, self.text_color)
        # screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))
        lines = self.text.split('\n')

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5 + i * self.font.get_linesize()))