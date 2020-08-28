import pygame


class Console(pygame.sprite.Sprite):
    """ Class that handles display for text that belongs within a 'console'. """

    def __init__(self, w, h):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = pygame.surface.Surface((w, h))
        self.image.fill((20, 20, 20))
        self.image.set_alpha(100)  # transparent
        self.rect = self.image.get_rect()

        # pygame.font.Font
        self.font = pygame.font.Font(None, 24)

    def draw_wrapped(self, surface, text, color, rect, font, aa=True):

        # Starting params
        line_y = rect.top
        line_space = -2
        font_height = font.size('Tg')[1]

        while text:

            # Starting index
            i = 1

            # Check if the current row will be outside rect
            if line_y + font_height > rect.bottom:
                break

            # Determine maximum width of line
            while i < len(text) and font.size(text[:i])[0] < rect.width:
                i += 1

            # Edge case
            if font.size(text[:i])[0] > rect.width:
                i -= 1

            # Adjust the wrap to the last word, if theres a space
            if i < len(text):
                space = text.rfind(' ', 0, i) + 1
                i = space if space > 0 else i

            # Render the line and blit it to the surface
            image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left, line_y))

            # Move to the next line
            line_y += font_height + line_space

            # Remove the text we just blitted
            text = text[i:]

        # Return any remaining text
        return text

    def blit(self, surface, text):

        # Blit the background
        surface.blit(self.image, self.rect)

        # Blit text
        self.draw_wrapped(surface, text, (255, 255, 255), self.rect, self.font)
