import pygame


class Instance(pygame.sprite.Sprite):
    """
    Class contains canvases use to draw and instance variables for:
        backgrounds
        objects
        tiles
    """

    def __init__(self):

        # Sprite
        super().__init__()
        self.image = None
        self.rect = None
        self._layer = 0

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

        # Asset
        self.bS = None
        self.oS = None
        self.l0 = None
        self.l1 = None
        self.l2 = None
        self.u = None
        self.no = None

        # Canvas
        self.canvas_list = []
        self.canvas_list_index = 0
        self.frame_count = 0

    def update_layer(self, layer):
        self._layer = layer

    def add_canvas(self, canvas):

        # Add to canvas list
        self.canvas_list.append(canvas)

        # Update current image and rect
        if not self.image:
            self.image = canvas.image
        if not self.rect:
            self.rect = canvas.rect.copy()
            self.rect = canvas.rect.copy().move(self.x, self.y)

    def step_frame(self):

        # Check if this instance can animate
        n = len(self.canvas_list)
        if n > 0:

            # Update frame count
            self.frame_count += 1

            # Convert to correct rate
            factor = 15  # TODO: Verify conversion rate
            count = self.frame_count * factor
            delay = self.canvas_list[self.canvas_list_index].delay

            # Check individual canvas delay, update if reached
            if count > delay:

                # Update canvas index
                self.canvas_list_index = (self.canvas_list_index + 1) % n
                self.frame_count = 0

                # Update current image and rect
                canvas = self.canvas_list[self.canvas_list_index]
                self.image = canvas.image
                self.rect = canvas.rect.copy().move(self.x, self.y)

    def update(self):
        if len(self.canvas_list) > 0:
            self.step_frame()

    def draw_footholds(self, screen, offset=None):

        # TODO: Set line thickness
        width = 1

        # If canvas does not exist, return
        if not self.canvas_list:
            return

        # Get current canvas
        canvas = self.canvas_list[self.canvas_list_index]

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
