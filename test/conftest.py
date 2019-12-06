from pytest import fixture
import reiz


@fixture(scope="session")
def canvas():
    c = reiz.Canvas((5, 5), (10, 10))
    c.open()
    yield c
    c.close()
