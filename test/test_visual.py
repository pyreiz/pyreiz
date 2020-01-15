import reiz


def test_visual_library(canvas):
    "contains Image, Cross, Mural and Trapezoid"
    for item in reiz.visual.library.__dict__.values():
        item.draw(canvas)


def test_colors(canvas):
    "also draws a background"
    from reiz._visual.colors import COLORS
    from reiz._visual.colors import resolve_rgb

    for c in COLORS:
        resolve_rgb("white", c)
        reiz.visual.Background(color=c).draw(canvas)


def test_smoke_complex(canvas):
    reiz._visual.complex.Line().draw(canvas)
    reiz._visual.complex.Polygon().draw(canvas)
    reiz._visual.complex.Bar().draw(canvas)
    reiz._visual.complex.Circle().draw(canvas)
    reiz._visual.complex.Cylinder().draw(canvas)
    reiz._visual.complex.Mural().draw(canvas)
    reiz._visual.complex.Trapezoid().draw(canvas)
    reiz._visual.complex.Cross().draw(canvas)


def test_circle(canvas):
    v = reiz._visual.complex.Circle(zoom=0.1, color="white", stroke=1, opacity=0.1)
    assert v.color == [1, 1, 1, 0.1]
    assert v.stroke == 1
    v.draw(canvas)


def test_mural(canvas):
    m = reiz._visual.complex.Mural(text="test")
    m.set_color("white")
    assert m.color == [1, 1, 1, 1]
    assert repr(m) == "Mural('test')"
    m.draw(canvas)


def test_cross(canvas):
    m = reiz._visual.complex.Cross(zoom=1, color=(1, 0, 0))
    assert repr(m) == "Cross(zoom=1, color=(1, 0, 0))"


def test_iteration(canvas):
    for v in reiz._visual.complex.Line():
        v.draw(canvas)

    for v in [reiz._visual.complex.Line(), reiz._visual.complex.Line()]:
        v.draw(canvas)


def test_read_folder(canvas):
    lib = reiz.visual.read_folder()
    assert lib.__dict__.get("logo", None) is not None
