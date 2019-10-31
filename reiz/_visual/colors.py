# -*- coding: utf-8 -*-
"""
Library of colors
.................
"""
from typing import NewType, Union, Tuple, List

RGB = NewType("RGB", Tuple[float, float, float]
              )  #: Tuple[float, float, float] limited between 0 and 1
ColorType = NewType("ColorType", Union[RGB, str]
                    )  #: Union[RGB, str] either a RGB color or a descriptive string from :data:`~.COLORS`

RGBA = NewType("RGBA", Tuple[float, float, float, float]
               )  #: Tuple[float, float, float, float] limited between 0 and 1
# %%
COLORS = {
    "red": [0.9, 0.1, 0.1],
    'carmine': [.59, .0, .09],
    'pictorial_carmine': (.76, .04, .31),
    'crimson': (.87, .08, .24),
    "pink": [0.9, 0.5, 0.9],
    "green": [.25, .8, .25],
    'moss': (.54, .60, .36),
    'darkgreen': (.0, .39, .0),
    "blue": [0, 0, 1],
    "white": [1, 1, 1],
    "bright": [0.75, 0.75, 0.75],
    "light": [0.5, 0.5, 0.5],
    "gray": [0.25, 0.25, 0.25],
    "dark": [0.125, 0.125, 0.125],
    "darker": [0.1, 0.1, 0.1],
    "black": [0, 0, 0],
    "brown": [.55, .36, .24],
    'darkbrown': [.44, .29, .20],
    'turkis': (.28, .82, .8),
    'darkturkis': (0., .8, .82),
    'celeste': (.69, 1, 1),
}  #: A dictionary of color strings encoding a tuple in RGB


def resolve_rgb(a: RGBA, b: RGBA, n: int = 100) -> List[RGBA, ]:
    '''interpolate an RGBA color in steps

    args
    ----

    a: RGBA
      rgba tuple
    b: RGBA
      rgba tuple
    n: int
      number of steps

    returns
    -------

    color: List[RGBA,]
        list of interpolated rgba tuples

    '''

    def linspace(a, b, n):
        if n < 2:
            return b
        diff = (float(b) - a)/(n - 1)
        return [diff * i + a for i in range(n)]
    if type(a) is str:
        a = get_color(a)
    if type(b) is str:
        b = get_color(b)

    _colors = []
    for _a, _b in zip(a, b):
        _colors.append(linspace(_a, _b, n))
    colors = []
    for i in range(0, n, 1):
        colors.append((_colors[0][i], _colors[1][i], _colors[2][i]))

    return colors


def get_color(color: ColorType = "white", opacity: float = 1) -> RGBA:
    '''get rgba tuple based on color name

    args
    ----
    color: ColorType, i.e. Union[Tuple[float, float, float], str]
        a color name or a tuple of colors, as from :data:`reiz.visual.colors.COLORS`
    opacity: float
        the alpha value


    returns
    -------
    color: RGBA i.e Tuple[float, float, float, float]
        a rgba tuple with values between 0 and 1
    '''

    try:
        color = COLORS[color]
    except KeyError:
        if len(color) != 3:
            raise ValueError('Not a correct color value')
    try:
        color = color.copy()
        color.append(opacity)
    except AttributeError:
        color = (*color, opacity)

    for val in color:
        if val < 0 or val > 1:
            raise ValueError("The desired color is not within range of 0 to 1")

    return color
