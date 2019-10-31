# -*- coding: utf-8 -*-
"""
Pyglet based primitive geometric shapes

    
"""
import pyglet            
from pyglet import gl
from pyglet.text import Label

# %% Primitives
'''
The visual primitives have been adapted from cocos2d_. 

   .. _cocos2d https://github.com/los-cocos/cocos

# cocos2d
# Copyright (c) 2008-2012 Daniel Moisset, Ricardo Quesada, Rayentray Tappa,
# Lucio Torre
# Copyright (c) 2009-2017  Richard Jones, Claudio Canepa
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of cocos2d nor the names of its
#     contributors may be used to endorse or promote products
#     derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
'''
class Base(object):
    """
    Basic attributes of all drawing primitives
    """
    def __init__(self, x, y, z=0, color=(0.,0.,0.,1.), stroke=0, rotation=0):
        try :
            self.rect
        except AttributeError:
            self.rect = Rect(x,y,1,1) # this inits x,y and loc as well
        self.visible = 1 #
        self.z = z 
        self.rotation = rotation
        self.stroke = stroke
        self.color = color
        self.q = gl.gluNewQuadric()
    def setLoc(self, p) : self.rect.loc = p 
    def getLoc(self) : return self.rect.loc
    def setX(self, x) : self.rect.x = x 
    def getX(self) : return self.rect.x 
    def setY(self, y) : self.rect.y = y 
    def getY(self) : return self.rect.y
    loc = property(getLoc, setLoc)
    x = property(getX, setX)
    y = property(getY, setY)
    def setWidth(self,w) : self.rect.width = w
    def getWidth(self) : return self.rect.width
    def setHeight(self, h) : self.rect.height = h
    def getHeight(self) : return self.rect.height
    width = property(getWidth, setWidth)
    height = property(getHeight, setHeight)
        
    def draw(self):
        self.render()
    
class Pixel(Base):
    """ A pixel at a given x,y,z position and color.
        Pixel(x=12, y=100, z=900, color=(1,0,0,0.5))
    """
    def render(self):
        """
            Draws a pixel at a given x and y with given color .
            Color = 3 or 4 arg tuple. RGB values from 0 to 1 being 1 max value (1, 1, 1) would be white
        """
        gl.glColor4f(*self.color)
##        glDisable(GL_TEXTURE_2D) # disable in case it was on
            
        gl.glPushMatrix() # remember previous matrix state before translating, rotating
        gl.glTranslatef(self.x, self.y, -self.z) # translate to point to draw

        gl.glBegin(gl.GL_POINTS) # draw point
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glEnd()

        gl.glPopMatrix() # back to previous matrix state

    def intersects(self, x,y):
        if x==self.x and y==self.y : return True


class Circle(Base):
    """ Circle class
        Circle(x=20, y=100, z=1, width=300, color=(1,1,0,0.3), stroke=5, rotation=0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, width=2, color=(0,0,0,1), stroke=0, rotation=(0,0,0,1), style=gl.GLU_FILL):
        self.radius = width*0.5
        self.rect = Rect(x, y, width, width)
        self.style = style
        self.circleresolution = 60
        Base.__init__(self, x, y, z, color, stroke, rotation)
        
    def setWidth(self, w):
        self.radius = w*0.5
        self.rect.width = w
    width = property(Base.getWidth, setWidth)
        
    def render(self):
        """ Draw Circle
            x, y, z, width in pixel, rotation, color and line width in px
            style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
            TO DO : textured circles
        """
        
        gl.glColor4f(*self.color)
        gl.glPushMatrix()

        gl.glTranslatef(self.x, self.y, -self.z)
        gl.glRotatef(*self.rotation) #angle, bool per axis (x,y,z)


        if self.radius < 1 : self.radius = 1

        if self.stroke :
            inner = self.radius - self.stroke # outline width
            if inner < 0: inner=0
        else :
             inner = 0 # filled
        
        gl.gluQuadricDrawStyle(self.q, self.style)

        gl.gluDisk(self.q, inner, self.radius, self.circleresolution, 1) # gluDisk(quad, inner, outer, slices, loops)
            
        gl.glPopMatrix()



class Arc(Base):
    """ Arc class
        Arc(x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0, rotation=0.0, style=GLU_FILL)
        style choices are : GLU_LINE, GLU_FILL, GLU_SILHOUETTE, GLU_POINT
    """
    def __init__(self, x=10, y=10, z=0, radius=1, start=0, sweep=1, color=(0,0,0,1), stroke=0,
                 rotation=0.0, style=gl.GLU_FILL):

        Base.__init__(self, x,y,z,color, stroke, rotation)
        self.radius = radius
        self.start = start
        self.sweep = sweep
        self.style = style
        self.circleresolution = 60
        
    def render(self):
        """
        Draws Arc
        """
        gl.glColor4f(*self.color)
        gl.glPushMatrix()
        gl.glTranslatef(self.x, self.y, -self.z)
        gl.glRotatef(self.rotation, 0, 0, 0.1)

        if self.stroke : 
            inner = self.radius - self.stroke
            if inner < 0: inner=0
        else :
            inner = 0 # full, no inner
        self.start -= 180
        
        gl.gluQuadricDrawStyle(self.q, self.style)
        
        gl.gluPartialDisk(self.q, inner, self.radius, self.circleresolution, 1, self.start, self.sweep)
        
        gl.glPopMatrix()

#%%

class Polygon(Base):
    def __init__(self, v, z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ polygon class
            Polygon(vertexarray=[(0, 0), (29, 100), (30, 200)], z=100, color=(0,0.3,0.1,1), stroke=0, rotation=23)
            overwrites few methods from superclass as polygons are more complex, needs to update everyvertex.
        """
        self.v = v
        l, t, r, b = calcPolygonRect(v) # get the bounding rect
        self.rect = Rect(l+(r-l)*0.5, t+(b-t)*0.5, r-l, b-t)
        self.v2 = [(i[0] - self.rect.x, i[1] - self.rect.y) for i in v] #relative polygon

        self.style = style
        
        Base.__init__(self, self.rect.x, self.rect.y, z,color,stroke,rotation)

    def updateV(self):
        self.v = [(self.rect.x + n[0], self.rect.y + n[1]) for n in self.v2]

    def setLoc(self, p):
        self.rect.loc = p ; self.updateV()
    def setX(self, x):
        self.rect.x = x ; self.updateV()
    def setY(self, y):
        self.rect.y = y; self.updateV()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)
    
    def render(self):
        """ Draw Polygon
            v is an array with tuple points like [(x, y), (x2, y2), (x3, y3)]
            min vertex number to draw a polygon is 3
            stroke=0 to fil with color the inside of the shape or stroke=N just to draw N-px thick outline.
            Note. It doesnt work with non convex polygons, need to implement tesselation yet
        """
        l,t,r,b = calcPolygonRect(self.v)
        x,y = calcRectCenter(l,t,r,b)
        self.drawVertex(x, y, self.z, [(i[0] - x, i[1] - y) for i in self.v], self.color, self.stroke, self.rotation, self.style)

    
    def drawVertex(self, x, y,  z=0, v=(), color=(0,0,0,1), stroke=0, rotation=0.0,   style=0):
        
        gl.glColor4f(*self.color)    
        gl.glPushMatrix()

        gl.glTranslatef(x, y, -z)
        gl.glRotatef(self.rotation, 0, 0, 0.1)

        if self.style :
            gl.glEnable(gl.GL_LINE_STIPPLE)
            gl.glLineStipple(1, style)
##        else :
##            glDisable(GL_LINE_STIPPLE)
##            0xF0F0 # dashed line
##            0xF00F # long dashed line
##            0x8888 # dotted lines
##        glRect(x1,y,1,x1,x2)
##        glRectiv(v1,v2) # oposite vertex of rectangle
        # -- start drawing
        if self.stroke : # outlined polygon
            gl.glLineWidth(self.stroke)
            gl.glBegin(gl.GL_LINE_LOOP)
        else: # filled polygon
            if   len(v) == 4 : gl.glBegin(gl.GL_QUADS)
            elif len(v)  > 4 : gl.glBegin(gl.GL_POLYGON)
            else :             gl.glBegin(gl.GL_TRIANGLES) # which type of polygon are we drawing?

        for p in v:
            gl.glVertex3f(p[0], p[1],0)  # draw each vertex

        gl.glEnd()
        # -- end drawing
        
        if self.style : gl.glDisable(gl.GL_LINE_STIPPLE)
        
        gl.glPopMatrix()


class LineRel(Base):
    def __init__(self, x,y, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( x,y, a=(1,1), b=(100,100), z=0, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5)
        y = abs(a[1] + h*0.5)
        self.a2 = abs(a[0]) - x, abs(a[1]) - y
        self.b2 = abs(b[0]) - x, abs(b[1]) - y
        self.a = x - w*0.5, y - w*0.5
        self.b = x + w*0.5, y + w*0.5
        self.rect = Rect(x, y, w, h)
        self.style = style
        Base.__init__(self, x, y, z,color,stroke,rotation)

    def render(self):
        """
        Draws Line
        """
        p1 = self.a2
        p2 = self.b2
        gl.glColor4f(*self.color)
        color  = (gl.GLfloat *4)(*self.color)
               
        gl.glPushMatrix()

        gl.glTranslatef(self.x, self.y, -self.z) # translate to GL loc ppint
        gl.glRotatef(self.rotation, 0, 0, 0.1)

        if self.style :
            gl.glEnable(gl.GL_LINE_STIPPLE)
            gl.glLineStipple(1, self.style)
##        else :
##            glDisable(GL_LINE_STIPPLE)
            
        if self.stroke <= 0:
            self.stroke = 1
        gl.glLineWidth(self.stroke)

        gl.glBegin(gl.GL_LINES)
        gl.glVertex2i(int(p1[0]), int(p1[1])) # draw pixel points
        gl.glVertex2i(int(p2[0]), int(p2[1]))
        gl.glEnd()

        if self.style :
            gl.glDisable(gl.GL_LINE_STIPPLE)
        
        gl.glPopMatrix()


    def updateAB(self):
        self.a = self.x + self.a[0], self.y + self.a[0]
        self.b = self.x + self.b[0], self.y + self.b[0]

    def setLoc(self, p):
        self.rect.loc = p ; self.updateAB()
    def setX(self, x):
        self.rect.x = x ; self.updateAB()
    def setY(self, y):
        self.rect.y = y; self.updateAB()
    x = property(Base.getX, setX)
    y = property(Base.getY, setY)
    loc = property(Base.getLoc, setLoc)


class Line(LineRel):
    def __init__(self, a=(0,0), b=(0,0), z=0, color=(0,0,0,1), stroke=0, rotation=0.0, style=0):
        """ Draws a basic line given the begining and end point (tuples), color (tuple) and stroke
            (thickness of line)
            Line( a=(1,1), b=(100,100), z=20, color=(0.2,0,0,1), stroke=10, rotation=45)
        """
        w = (b[0] - a[0]) 
        h = (b[1] - a[1]) 
        x = abs(a[0] + w*0.5) # abs x,y
        y = abs(a[1] + h*0.5)
        a = x-w*0.5, y-h*0.5 # relative a,b
        b = x+w*0.5, y+h*0.5
        LineRel.__init__(self, x, y, a, b, z, color, stroke, rotation, style)



# intersectable shapes (draggable)

class Rect(object):
    def __init__(self, x=0,y=0,w=0,h=0):
        """ rect(self, x=0,y=0,w=0,h=0)
            x,y,loc, width, height
            left,top,right,bottom
            quad ->
            --------------------
            topleft = quad[0]
            topright = quad[1]
            bottomright = quad[2]
            bottomleft = quad[3]
        """
        self.rect = x,y,w,h

    def setRect(self, r):
        self.__x = r[0]
        self.__y = r[1]
        self.__width = r[2]
        self.__height = r[3]
        w = r[2]*0.5 ; h = r[3]*0.5
        self.__rect = r[0]-w, r[1]-h, r[0]+w, r[1]+h # l t r b
    def getRect(self):
        return self.__rect
    rect = property(getRect, setRect)

    def setQuad(self, q): # [ q[0][0], q[0][1], q[1][0], q[2][1] ] # l t r b
        self.rect = q[0][0]+(q[1][0]-q[0][0])*0.5, q[0][1]+(q[2][1]-q[0][1])*0.5, q[1][0]-q[0][0], q[2][1]-q[0][1] 
    def getQuad(self):
        return [(self.rect[0], self.rect[1]),(self.rect[2], self.rect[1]),(self.rect[2], self.rect[3]),(self.rect[0], self.rect[3])] # tl tr br bl
    quad = property(getQuad, setQuad)

    def setX(self, x):
        self.rect = x, self.y, self.width, self.height
    def getX(self) : return self.__x
    x = property(getX, setX)

    def setY(self, y):
        self.rect = self.x, y, self.width, self.height
    def getY(self) : return self.__y
    y = property(getY, setY)

    def setLoc(self, p):
        self.rect = p[0], p[1], self.width, self.height
    def getLoc(self) : return self.__x, self.__y # self.x, self.y
    loc = property(getLoc, setLoc)

    def setWidth(self, w):
        self.rect = self.x, self.y, w, self.height
    def getWidth(self): return self.__width
    width = property(getWidth, setWidth)
    
    def setHeight(self, h):
        self.rect = self.x, self.y, self.width, h
    def getHeight(self): return self.__height
    height = property(getHeight, setHeight)

    def setLeft(self,x):
        self.rect = x+self.width*0.5, self.y, self.width, self.height
    def getLeft(self): return self.rect[0]
    left = property(getLeft, setLeft)
    
    def setTop(self,y):
        self.rect = self.x, y+self.width*0.5, self.width, self.height
    def getTop(self): return self.rect[1]
    top = property(getTop, setTop)
    
    def setRight(self,x):
        self.rect = x-self.width*0.5, self.y, self.width, self.height
    def getRight(self): return self.rect[2]
    right = property(getRight, setRight)
    
    def setBottom(self,x):
        self.rect = self.x, self.y-self.width*0.5, self.width, self.height
    def getBottom(self): return self.rect[3]
    bottom = property(getBottom, setBottom)


        
#%%
def calcPolygonRect(pointArray):
    """ receives a point list and returns the rect that contains them as a tupple -> tuple left, top, right, bottom
    """
    # init to ridiculously big values. not very elegant or eficient
    l, t, r, b = 10000000, 10000000, -10000000, -10000000
##    l = pointArray[0]
##    t = pointArray[1]
##    r = l
##    b = t

    for n in pointArray: # calc bounding rectangle rect
        if n[0] < l : l = n[0]
        if n[0] > r : r = n[0]
        if n[1] < t : t = n[1]
        if n[1] > b : b = n[1]

    return l, t, r, b


def calcRectCenter(l,t,r,b):#,v=()):
    """ returns rect center point -> x,y
        calcRectCenter(l,t,r,b)
    """
##    if len(v) : l,t,r,b = v[0],v[1],v[2],v[3]
    return l+((r-l)*0.5), t+((b-t)*0.5)


