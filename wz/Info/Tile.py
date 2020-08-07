import pygame


class Tile:
    def __init__(self):
        self.name = 'Tile'
        self.x = None
        self.y = None
        self.u = None
        self.no = None
        self.zM = None
        self.canvas = None

    def draw_footholds(self, screen, offset=None):

        # TODO: Set line thickness
        width = 1

        # If canvas does not exist, return
        if not self.canvas:
            return

        # Keep track of points
        points = []

        # Iterate over footholds
        for foothold in self.canvas.footholds:

            # Adjust using tile position
            fx = foothold.x + self.x
            fy = foothold.y + self.y

            # Adjust usin offset
            if offset:
                fx -= offset.x
                fy -= offset.y

            # Create a point and draw
            points.append((fx, fy))

        # Draw lines
        if points:
            pygame.draw.lines(screen, (255, 255, 0), False, points, width)
