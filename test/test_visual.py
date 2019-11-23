import reiz


def test_visual_library():
    "contains Image, Cross, Mural and Trapezoid"
    c = reiz.Canvas()
    for item in reiz.visual.library.__dict__.values():
        item.draw(c)


def test_colors():
    "also draws a background"
    from reiz._visual.colors import COLORS
    from reiz._visual.colors import resolve_rgb
    canvas = reiz.Canvas()
    for c in COLORS:
        resolve_rgb("white", c)
        reiz.visual.Background(color=c).draw(canvas)


def test_complex():
    canvas = reiz.Canvas()
    reiz._visual.complex.Line().draw(canvas)
    reiz._visual.complex.Polygon().draw(canvas)
    reiz._visual.complex.Bar().draw(canvas)
    reiz._visual.complex.Cylinder().draw(canvas)
