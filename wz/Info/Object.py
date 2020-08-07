import pygame


class Object:
    def __init__(self):
        self.name = 'Object'
        self.x = None
        self.y = None
        self.zM = None
        self.f = None
        self.r = None
        self.move = None
        self.dynamic = None
        self.piece = None
        self.oS = None
        self.l0 = None
        self.l1 = None
        self.l2 = None
        self.canvas = []
        self.canvas_index = 0
        self.frame_count = 0

    def get_canvas(self):
        return self.canvas[self.canvas_index]

    def draw_footholds(self, screen, offset=None):

        # TODO: Set line thickness
        width = 1

        # If canvas does not exist, return
        if not self.canvas:
            return

        # Get current canvas
        canvas = self.canvas[self.canvas_index]

        # Keep track of points
        points = []

        # Iterate over footholds
        for foothold in canvas.footholds:

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
