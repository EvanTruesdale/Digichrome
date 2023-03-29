#Leviticus Rhoden's Lens library, in which you can:
#define and simulate a lens class
#Generate incoming rays and pass them through a lens class

#https://leviticusrhoden.com/cameras/thinlenssim.php


import numpy as np

def test():
    print("Heyo!")

class opticalSystem:
    '''opticalSystem is a class of object that takes in
    -a numpy array of the focal lengths of the lenses in the system
    -a numpy array of the gaps between lenses'''
    def __init__(self, focalsIn, gapsIn):
        #floats, are what they say, in mms
        #below we set up the above as lists
        self.focal = focalsIn
        self.delX = gapsIn
        self.x = np.cumsum(self.delX)
        ##np.append(self.x, self.x[-1] + 1000)
        #then make a list of the Rates of Convergance of our lenses
        self.c = [1/v for v in focalsIn]
    
    def simRay(self,rayC, y1):
        '''
        simRay takes in itself of a lens object, the float of the incoming ray's slope, and a float of where the ray is incident on the frist lens y1
        '''
        y0 = y1 + (rayC*self.delX[0])
        y = [y0, y1]
        slope = rayC
        for i in range(0,len(self.c)-1):
            slope = slope + self.c[i]*y[-1]
            y.append(y[-1] - slope*self.delX[i])
            
        x = np.array(self.x)
        
        return np.array([x,y])
    

def intersection(x1,y1,x2,y2):
    '''this takes the ray data I'm building up and returns any intersections between the two rays.
    all inputs are lists of points that are connected by lines
    IT IS ASSUMED ALL INPUT LISTS ARE OF SAME LENGTH, x1 = x2'''

    intersects = []
    #find intersections in the between lens regime
    for i in range(1,len(x1),1):
        denom = y1[i-1]-y1[i]-y2[i-1]+y2[i]
        
        if denom != 0:
            intX = (y1[i-1]-y2[i-1]) * (x1[i]-x1[i-1]) / denom
            intX += x1[i-1]
            intY = y2[i-1] + (intX-x2[i-1]) * (y2[i]-y2[i-1])/(x2[i]-x2[i-1])
            if intX <= x1[i] and intX >= x1[i-1]:
                intersects.append([intX, intY])
                
    
    #find any after lens intersections
    return np.array(intersects)


def imageRays(distance,yIn,lensRadius,numRays):
    '''This function generates a list of indident rays defined by an objects location.
    all in are floats except numRays, which is an int
    outputs a numpy array of the rays slopes and x hit on a lens'''
    rays = []
    
    for i in np.linspace(-lensRadius,lensRadius,num=numRays):
        c = (yIn-i)/distance
        y = i
        rays.append(np.array([c,y]))
    
    
    return np.array(rays)