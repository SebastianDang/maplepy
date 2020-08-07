import pygame


class Instance:
    """
    Class contains canvases use to draw and instance variables for:
        backgrounds
        objects
        tiles
    """

    def __init__(self):

        # Common
        self.x = None
        self.y = None
        self.zM = None
        self.f = None

        # Back
        self.cx = None
        self.cy = None
        self.rx = None
        self.ry = None
        self.type = None
        self.a = None
        self.front = None
        self.ani = None

        # Object
        self.r = None
        self.move = None
        self.dynamic = None
        self.piece = None

        # Sprite
        self.bS = None
        self.oS = None
        self.l0 = None
        self.l1 = None
        self.l2 = None
        self.u = None
        self.no = None

        # Canvas
        self.canvas = []
        self.canvas_index = 0
        self.frame_count = 0

    def add_canvas(self, canvas):
        self.canvas.append(canvas)

    def get_canvas(self):
        return self.canvas[self.canvas_index]

    def step_frame(self):

        # Check if this instance can animate
        n = len(self.canvas)
        if n < 1:
            return

        # Update frame count
        self.frame_count += 1

        # Convert to correct rate
        factor = 15  # TODO: Verify conversion rate
        count = self.frame_count * factor
        delay = self.canvas[self.canvas_index].delay

        # Check individual canvas delay, update if reached
        if count > delay:
            self.canvas_index = (self.canvas_index + 1) % n
            self.frame_count = 0

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
