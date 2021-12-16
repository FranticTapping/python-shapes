from PIL import Image
import math

imgSizex = 1920
imgSizey = 1080

class circle():
    def __init__(self,image, pos, radius, baseCol):
        self.image = image
        self.pos = pos
        self.radius = radius
        self.baseCol = baseCol

    def render(self):
        for x in range(self.pos[0]-self.radius, self.pos[0]+self.radius): #iterate through square with pos centred in it
            for y in range(self.pos[1]-self.radius, self.pos[1]+self.radius):
                if math.sqrt(((x-self.pos[0])**2) + ((y-self.pos[1])**2)) <= self.radius: #if the distance from current pixel from centre is less then the radius
                    if x < 0 or x > imgSizex or y < 0 or y > imgSizey or x == imgSizex or y == imgSizey:#if xy is out of image range
                        pass
                    else:
                        self.image.putpixel([x,y], self.baseCol) # colour circle

    def renderSpiral(self,col, degreeChange, distChange, direction):
        degree = 0
        dist = 0

        if direction != 'Anti':
            degreeChange = degreeChange*-1

        while dist < self.radius:# while we are not at the radius calculate and place pixel
            degree +=degreeChange
            dist += distChange
            
            if degree > 360: # keep degree in range
                degree = 0
            elif degree < 0:
                degree = 360

            latitude = int(dist*math.cos(math.radians(degree)))
            departure = int(dist*math.sin(math.radians(degree)))

            x = self.pos[0]+departure
            y = self.pos[1]+latitude

            if x < 0 or x > imgSizex or y < 0 or y > imgSizey or x == imgSizex or y == imgSizey:#if xy is out of image range
                pass
            else:
                self.image.putpixel([x,y], col)

class ellipse():
    def __init__(self,image, pos, semi, baseCol):
        self.image = image
        self.pos = pos
        self.minor = semi[1]
        self.major = semi[0]
        self.baseCol = baseCol
        self.wrap = False

    def render(self):
        for x in range(self.pos[0]-self.major, self.pos[0]+self.major): #iterate through square with pos centred in it
            for y in range(self.pos[1]-self.minor, self.pos[1]+self.minor):
                eq = (((x - self.pos[0])**2)/(self.major**2)) + (((y - self.pos[1])**2)/(self.minor**2))
                if eq <= 1:
                    if x < 0 or x > imgSizex or y < 0 or y > imgSizey or x == imgSizex or y == imgSizey:#if xy is out of image range
                        pass
                    else:
                        self.image.putpixel([x,y], self.baseCol) # colour circle

class rectangle():
    def __init__(self,image,pos,radius,baseCol):
        self.image = image
        self.pos = pos
        self.radius = radius
        self.baseCol = baseCol

    def render(self):
        for x in range(self.pos[0]-int(self.radius[0]/2), self.pos[0]+int(self.radius[0]/2)):
            for y in range(self.pos[1]-int(self.radius[1]/2), self.pos[1]+int(self.radius[1]/2)):
                if x < 0 or x > imgSizex or y < 0 or y > imgSizey or x == imgSizex or y == imgSizey:#if xy is out of image range
                    pass
                else:
                    self.image.putpixel([x,y], self.baseCol) # colour square

class line():
    def __init__(self,image,startpos,endpos,brushSize,baseCol):
        self.image = image
        self.startpos = startpos # type list
        self.endpos = endpos # typle list
        self.brushSize = brushSize
        self.baseCol = baseCol

    def render(self):
        #equation for line: y = mx+c
        # y = m*x + c | m = gradient | c = y intercept
        height = self.endpos[1] - self.startpos[1]
        width = self.endpos[0] - self.startpos[0]
        m=0
        try:# we have to try becasue we could accidently do 0/0 which returns an error
            m = height / width
        except:
            pass
        #c is the y intercept of the line so we calculate that using the slope and one of the x,y points
        c = self.startpos[1] - m*self.startpos[0] 

        for x in range (self.startpos[0]-1,self.endpos[0]+1):
            for y in range (self.startpos[1]-1,self.endpos[1]+1):
                #self.image.putpixel([x,y], (200,0,0,255))
                # y = mx+c | we plug the new xy into the equation to see if it is true, if so then its on the line
                
                if math.isclose(y,(m*x)+c,rel_tol = 0.01, abs_tol  = 1):
                    #image, pos, radius, baseCol
                    circle(self.image,[x,y],self.brushSize,self.baseCol).render()


im = Image.new('RGBA',(imgSizex,imgSizey))

#fill screen with white pixels
# for x in range(0,imgSizex):
#     for y in range(0,imgSizey):
#         im.putpixel((x, y), (100, 100, 100, 255))

# shapes = []

# shapes.append(circle(im,[int(imgSizex/2),int(imgSizey/2)],int(imgSizey/2),(100,0,0,255)))
# shapes.append(ellipse(im,[int(imgSizex/2),int(imgSizey/2)],[int(imgSizey/2),int(imgSizey/4)],(200,200,200,255)))
# shapes.append(ellipse(im,[int(imgSizex/2),int(imgSizey/2)],[int(imgSizey/4),int(imgSizey/2)],(200,200,200,255)))
# shapes.append(rectangle(im,[int(imgSizex/2),int(imgSizey/2)],[int(imgSizey/2),int(imgSizey/2)],(0,0,0,255)))

# for shape in shapes:
#     shape.render()
rect = rectangle(im,[int(imgSizex/2),int(imgSizey/2)],[imgSizex,imgSizey],(255,255,255,255))

lines = []
lines.append(line(im,[0,0],[1920,1080],1,(0,0,0,255)))

rect.render()
for i in lines:
    i.render()

im.show()
#im.save('images\\bg.png')