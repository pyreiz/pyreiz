"""
Create complex shapes and murals
................................
"""
from reiz._visual.colors import get_color, ColorType
import pyglet
from pathlib import Path
from reiz._visual._primitives import Polygon as _Polygon
from reiz._visual._primitives import Circle as _Circle
from reiz._visual._primitives import Line as _Line
from typing import Tuple, NewType, List
# : Tuple[float, float], x-y coordinates scaled from -1 to 1 with 0 indicating the center of the screen
XY = NewType("XY", Tuple[float, float])

# %%


class Visual():
    "The base class for all visual cues to inherit from"

    def adapt(self, window):
        pass

    def draw(self, canvas=None):
        if canvas is not None and not canvas.window.has_exit:
            self.adapt(canvas)
        try:
            for v in self.visual:
                v.draw()
        except TypeError:
            self.visual.draw()

    def set_color(self, color: str):
        self.color = get_color(color)

    def __iter__(self):
        yield self

    def __next__(self):
        yield self
        raise StopIteration

# Complex parametric visualisations
# ------------------------------------------------------------------------------


class Background(Visual):
    """Fills the whole screen with a single color

    args
    ----
    color:str
        the color to fill the screen. see also :data:`reiz.visual.colors.COLORS`

    """

    def __init__(self, color='white'):
        self.color = [int(c*255) for c in get_color(color)]

    def adapt(self, window):
        img = pyglet.image.SolidColorImagePattern(color=self.color)
        img = img.create_image(window.width, window.height)
        self.visual = pyglet.sprite.Sprite(img=img, x=0, y=0,
                                           usage='static')

# ------------------------------------------------------------------------------


class Mural(Visual):
    """A text on the screen

    args
    ----

    text:str
        the text to show
    font:str
        the font-type (needs to be installed on the system)
    fontsize: float
        the normalized size of the letters
    position: XY
        where on the screen the text should be located. Coordinates mark the center of the text
    color: ColorType
        the desired color
    """

    def __init__(self, text: str = 'Hello World', font='Times New Roman',
                 fontsize: float = 1, position: Tuple[float, float] = (0, 0), color=(1, 1, 1),
                 anchor_x='center', anchor_y='center'):
        self.scale = 0.05 * fontsize
        self.text = text
        self.font = font
        self.pos = position
        self.set_color(color)
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def adapt(self, canvas):
        color = tuple(int(c*255) for c in self.color)
        x0 = canvas.width//2
        y0 = canvas.height//2
        x = (x0*self.pos[0]) + x0
        y = (y0*self.pos[1]) + y0
        fontsize = int(canvas.width*self.scale)
        self.visual = pyglet.text.Label(self.text, font_name=self.font,
                                        font_size=fontsize, color=color, x=x, y=y,
                                        anchor_x=self.anchor_x, anchor_y=self.anchor_y)

    def __repr__(self):
        return f"Mural('{self.text}')"

# ------------------------------------------------------------------------------


class Line(Visual):
    """A line from a to b

    args
    ----

    a: XY
        x-y coordinates of the start point
    b: XY
        x-y coordinates of the end point
    color: ColorType
        the desired color
    linewidth:float
    """

    def __init__(self, a: XY = (0, 0), b: XY = (0, 0),
                 color: ColorType = 'white', linewidth: float = 1):
        self.a = a
        self.b = b
        self.color = get_color(color)
        self.linewidth = linewidth

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2
        ax = (x0*self.a[0]) + x0
        ay = (y0*self.a[1]) + y0
        bx = (x0*self.b[0]) + x0
        by = (y0*self.b[1]) + y0

        self.visual = _Line(a=(ax, ay), b=(bx, by), z=0,
                            color=self.color, stroke=self.linewidth)


class Polygon(Visual):
    """An arbitrary shape defined by the coordinates of its nodes

    args
    ----
    positions: List[XY, ]
        a list of x-y-coordinates of each node
    color: ColorType
        the desired color
    """

    def __init__(self, positions: List[XY, ] = [(0, 0), (.1, .2), (.3, .1)], color='white'):
        self.positions = positions
        self.color = get_color(color)

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2

        v = []
        for pos in self.positions:
            x = (x0*pos[0]) + x0
            y = (y0*pos[1]) + y0
            v.append((x, y))
        self.visual = _Polygon(
            v=v, z=0, color=self.color, stroke=0, rotation=0)


class Bar(Visual):
    """A rectangle starting from the bottom centre of the screen

    args
    ----
    height:float
        height in normalized units from 0 to 1 (bottom to top of screen)
    width:float
        width in  normalized units from 0 to 1 (nothing to whole screen)
    color: ColorType
        the desired color
    """

    def __init__(self, height: float = .5, width: float = .25, color='white'):
        self.height = height
        self.width = width
        self.color = get_color(color)

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height*3/4
        h = self.height
        w = self.width
        positions = [(-w, 0), (-w, h), (w, h), (w, 0)]
        v = []
        for pos in positions:
            x = (x0*pos[0]) + x0
            y = (y0*pos[1]) + 0
            v.append((x, y))
        self.visual = _Polygon(
            v=v, z=0, color=self.color, stroke=0, rotation=0)


class Circle(Visual):
    """A circle, i.e. the outline of a ball

    args
    ----
    zoom: float
        size of the circle
    color: ColorType
        the desired color
    position: XY
        position of the center of the circle
    opacity: float
        how opaque the circle is supposed to be from 0 to 1
    stroke: float
        thickness of the outline
    """

    def __init__(self, zoom: float = 1, color: ColorType = 'red',
                 position: XY = (0, 0), opacity: float = 1, stroke: float = 0):
        self.pos = position
        self.color = get_color(color, opacity)
        self.zoom = zoom
        self.stroke = stroke

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2
        width = int(0.1*min([window.height, window.width]) * self.zoom)

        x = (x0*self.pos[0]) + x0
        y = (y0*self.pos[1]) + y0
        self.visual = _Circle(x=x, y=y, z=0, width=width, color=self.color,
                              stroke=self.stroke)

    def __repr__(self):
        return (f"Circle(zoom={self.zoom}, color={self.color}, " +
                f"position={self.pos})")


class Cylinder(Visual):
    """A rectangular shape which can be rotated around its center

    args
    ----
    position: XY
        position of the center of the circle
    angle:float
        rotation angle around its center
    thickness:float
        width of the cylinder
    length:float
        length of the cylinder
    color: ColorType
        the desired color

    """

    def __init__(self, position=(0, 0), angle: float = 0,
                 thickness: float = .05, length: float = .75,
                 color: ColorType = 'brown'):
        self.color = get_color(color)
        self.length = length
        self.pos = position
        self.angle = angle
        self.thickness = thickness

    def adapt(self, canvas):
        x0 = canvas.width//2
        y0 = canvas.height//2
        x = (x0*self.pos[0]) + x0
        y = (y0*self.pos[1]) + y0
        thickness = int(canvas.height * self.thickness)
        length = int(canvas.width * self.length)

        vertices = ((x-length//2, y-thickness//2),
                    (x-length//2, y+thickness//2),
                    (x+length//2, y+thickness//2),
                    (x+length//2, y-thickness//2))

        self.visual = _Polygon(v=vertices, z=0, color=self.color,
                               stroke=0, rotation=self.angle)


# ------------------------------------------------------------------------------
class Cross(Visual):
    """A fixation cross in the center of the screen

    args
    ----
    zoom: float
        size of the cross
    color: ColorType
        the desired color

    """

    def __init__(self, zoom=1, color='white'):
        self.color = get_color(color)
        self.zoom = zoom

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2
        armlen = int(self.zoom * 100)
        armwid = int(self.zoom * 15)

        y1 = y0-armlen
        y2 = y0-armwid
        y3 = y0+armwid
        y4 = y0+armlen

        x1 = x0-armlen
        x2 = x0-armwid
        x3 = x0+armwid
        x4 = x0+armlen

        v = [(x1, y2), (x1, y3), (x4, y3), (x4, y2)]
        self.ho = _Polygon(v=v, z=0, color=self.color, stroke=0, rotation=0)
        v = [(x2, y1), (x2, y4), (x3, y4), (x3, y1)]
        self.ve = _Polygon(v=v, z=0, color=self.color, stroke=0, rotation=0)

        self.visual = [self.ho, self.ve]

    def __repr__(self):
        return f"Cross(zoom={self.zoom}, color={self.color[:-1]})"


class Trapezoid(Visual):
    """A trapezoid spanned between four nodes

    args
    ----
    xpos: Tuple[float, float, float, float]
        a tuple of x coordinates of the nodes
    ypos: Tuple[float, float]
        a tuple of y coordinates of the nodes
        the first entry is the ypos of the first two xpos
    color: ColorType
        the desired color
    """

    def __init__(self, xpos=(-.33, -.25, .25, .33),
                 ypos=(-.25, .25), color='white'):
        self.xpos = xpos
        self.ypos = ypos
        self.color = get_color(color)

    def adapt(self, window):
        x0 = window.width//2
        y0 = window.height//2

        # generate vertex coordinates
        positions = []
        for x, y in zip(self.xpos[0:2], self.ypos):
            positions.append((x, y))
        for x, y in zip(self.xpos[2:], reversed(self.ypos)):
            positions.append((x, y))

        # create the trapezoid in the first color (default white)
        vertex = []
        for pos in positions:
            x = (x0*pos[0]) + x0
            y = (y0*pos[1]) + y0
            vertex.append((x, y))

        self.visual = _Polygon(
            v=vertex, z=0, color=self.color, stroke=0, rotation=0)

# ------------------------------------------------------------------------------
# %% File-based visualisations


class Image(Visual):
    """Show an image loaded from a file

    args
    ----
    imgpath:str
        path to the imagefile
    position:XY
        x-y-coordinate of the center of the image
    scale:float
        size of the figure relative to the screen size
    """

    def __init__(self, imgpath: str,
                 position: Tuple[float, float] = (0, 0),
                 scale: float = .5):
        self.imgpath = str(Path(imgpath).expanduser().absolute())
        self.img = pyglet.image.load(imgpath)
        self.scale = scale
        self.pos = position

    def adapt(self, window):
        base_scale = min(window.width/self.img.width,
                         window.height/self.img.height)
        scale = self.scale*base_scale
        self.img.scale = scale
        x0 = window.width//2 - (scale * self.img.width//2)
        y0 = window.height//2 - (scale * self.img.height//2)
        x = (x0*self.pos[0]) + x0
        y = (y0*self.pos[1]) + y0

        self.visual = pyglet.sprite.Sprite(img=self.img, x=x, y=y,
                                           usage='static')
        self.visual.scale = scale

    def __repr__(self):
        return f"Image(imgpath='{self.imgpath}')"
# ------------------------------------------------------------------------------
