def test():
    import time
    from os.path import join
    from reiz.visual import PATH
    from reiz.visual.primitives import Polygon
    from reiz.visual import Mural, Image, Canvas
    
    p1 = Polygon(v=[(50, 50), (50, 100), (100, 100), (100, 50)], z=0, color=(1,0.3,0.1,1), stroke=0, rotation=0)
    p2 = Polygon(v=[(250, 250), (250, 100), (100, 100), (100, 250)], z=0, color=(1,0.3,0.1,1), stroke=0, rotation=0)
    
    s = Canvas()    
    l = Mural('Hello, world')
    
    s.open()
    s.set_fullscreen()
    
    img = Image(imgpath=join(PATH, 'lablogo.png'))
    
    s.show(img)
    time.sleep(5)
    s.show([p1, p2, l])
    time.sleep(5)
    s.close()
    
if __name__=="__main__":
    '''Example'''
    test()
