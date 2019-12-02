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


def test_smoke_complex():
    canvas = reiz.Canvas()
    reiz._visual.complex.Line().draw(canvas)
    reiz._visual.complex.Polygon().draw(canvas)
    reiz._visual.complex.Bar().draw(canvas)
    reiz._visual.complex.Circle().draw(canvas)
    reiz._visual.complex.Cylinder().draw(canvas)
    reiz._visual.complex.Mural().draw(canvas)
    reiz._visual.complex.Trapezoid().draw(canvas)
    reiz._visual.complex.Cross().draw(canvas)


def test_mural():
    canvas = reiz.Canvas()
    m = reiz._visual.complex.Mural(text="test")
    assert repr(m) == "Mural('test')"


def test_cross():
    canvas = reiz.Canvas()
    m = reiz._visual.complex.Cross(zoom=1, color=(1, 0, 0))
    assert repr(m) == "Cross(zoom=1, color=(1, 0, 0))"


def test_iteration():
    canvas = reiz.Canvas()
    for v in reiz._visual.complex.Line():
        v.draw(canvas)

    for v in [reiz._visual.complex.Line(), reiz._visual.complex.Line()]:
        v.draw(canvas)
