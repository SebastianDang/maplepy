import pygame


class Instance(pygame.sprite.Sprite):
    """
    Class contains canvases use to draw and instance variables for:
        backgrounds
        objects
        tiles
    """

    def __init__(self):

        # pygame.sprite.Sprite
        super().__init__()
        self.image = None
        self.mask = None
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
        self.dx = 0
        self.dy = 0

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

        # Collision
        self.forbidFallDown = None

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
            self.mask = pygame.mask.from_surface(self.image)
        if not self.rect:
            self.rect = canvas.rect.copy()
            self.rect = canvas.rect.copy().move(self.x, self.y)

    def step_frame(self):

        # Check if this instance can animate
        n = len(self.canvas_list)
        if n > 1:

            # Update frame count
            self.frame_count += 1

            # Convert to correct rate
            factor = 15  # TODO: Verify conversion rate
            count = self.frame_count * factor
            canvas = self.canvas_list[self.canvas_list_index]

            # Update alpha
            if canvas.delay > 0:
                alpha = canvas.a0 + (count / canvas.delay) * \
                    (canvas.a1 - canvas.a0)
                self.image.set_alpha(alpha)

            # Check individual canvas delay, update if reached
            if count > canvas.delay:

                # Update canvas index
                self.canvas_list_index = (self.canvas_list_index + 1) % n
                self.frame_count = 0

                # Update current image and rect
                canvas = self.canvas_list[self.canvas_list_index]
                self.image = canvas.image
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = canvas.rect.copy().move(self.x, self.y)

    def step_scroll(self):
        horizontal = [4, 6]
        vertical = [5, 7]
        if self.type in horizontal and self.cx > 0:
            self.dx += self.rx
            self.dx %= (2 * self.cx)
        if self.type in vertical and self.cy > 0:
            self.dy += self.ry
            self.dy %= (2 * self.cy)

    def update(self):
        n = len(self.canvas_list)
        if n > 1:
            self.step_frame()
        elif n > 0:
            self.step_scroll()

    def get_footholds(self):
        canvas = self.canvas_list[self.canvas_list_index]
        return canvas.footholds

    def get_foothold_points(self, offset=None):

        # Get current canvas
        canvas = self.canvas_list[self.canvas_list_index]

        # Create a list of points
        points = []

        # Iterate over footholds
        for foothold in canvas.footholds:

            # Adjust using tile position
            fx = foothold.x + self.x
            fy = foothold.y + self.y

            # Adjust using offset
            if offset:
                fx -= offset.x
                fy -= offset.y

            # Add to points
            points.append((fx, fy))

        return points

    def draw_footholds(self, screen, offset=None):

        # TODO: Set line thickness
        width = 5

        # If canvas does not exist, return
        if not self.canvas_list:
            return

        # Get all foothold points
        points = self.get_foothold_points(offset)

        # Draw lines
        if points:
            pygame.draw.lines(screen, (255, 255, 0), False, points, width)
