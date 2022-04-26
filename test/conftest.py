from pytest import fixture


@fixture(scope="session")
def canvas():
    import reiz.api as reiz

    c = reiz.Canvas((5, 5), (10, 10))
    c.open()
    yield c
    c.close()
