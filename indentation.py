import random
import numpy as np 
dimensions = 15 
carcoord = []
coordRadius = []
nspheres = 200
counter = 0
minradius = 1.5
maxradius = 2.5
width = 10
height = 10
length = 10
lstcircles = []
spherevols = 0 
maxvol = 0 
spherelist = []
porosity = 0.8
overlap = 0.2
pi = 3.14159265359
tempcoord = []

class spheres: 
	def __init__(self, name): 
		self.name = name

for n in range(0, dimensions): 
    for m in range(0,dimensions):
        for l in range(0,dimensions):
            carcoord.append([n, m, l])

def inthesphere(x,y,z,center,radius):
    if (x-center[0])**2 + (y-center[1])**2 + (z-center[2])**2 <=radius**2: 
        carcoord.remove([x,y,z])
        return True
    else: 
        return False


def checksphere(x,y,z,center,radius):
    if (x-center[0])**2 + (y-center[1])**2 + (z-center[2])**2 <=radius**2: 
        tempcoord.remove([x,y,z])
        return True
    else: 
        return False


failcount = 0
tempcoord = list(carcoord)
while True:

#for spheres in range(0, nspheres):
    if len(carcoord) < 10:#(1-porosity)/2*dimensions**3:
        print("carcoord", len(carcoord))
        print("coordRadius", len(coordRadius))
        break

    if len(tempcoord)<=1:
	    break

    center = random.choice(tempcoord)#carcoord
    print(len(tempcoord))
    print(center)
    radius = random.uniform(minradius, maxradius) 
    #print("center", center)
    #print("radius", radius)
    checkoverlap = 0
    #tempcoord = carcoord
    for n in range(0, len(tempcoord)):
        if n < len(tempcoord):
            if checksphere(tempcoord[n][0], tempcoord[n][1], tempcoord[n][2], center, radius):
                checkoverlap = checkoverlap + 1
        else:
#            print("brcarcoord", len(carcoord))
#            print("brcoordRadius", len(coordRadius))
            break
               
    if checkoverlap >= (1-overlap)*(4/3*pi*radius**3):
        coordRadius.append([center[0], center[1], center[2], radius])
        #spheres = spheres + 1
        failcount = 0
        tempcoord = list(carcoord)
        
        for n in range(0, len(carcoord)):
            if n < len(carcoord):
                inthesphere(carcoord[n][0], carcoord[n][1], carcoord[n][2], center, radius)
            else:
                break
    else:
        failcount = failcount + 1
        
    if len(coordRadius) > nspheres:
        print("coordRadius", len(coordRadius))
        break
    if failcount >500:
        print("failcount",failcount)
        print("coordRadius", len(coordRadius))
        print("carcoord", len(carcoord))
        break


doc = FreeCAD.newDocument() 

box = doc.addObject("Part::Box", "myBox")

doc.addObject("Part::MultiFuse","Fusion")
vol = doc.getObject("Fusion")

box.Width = width 
box.Height = height
box.Length = length
box.Placement = FreeCAD.Placement(FreeCAD.Vector(2.5,2.5,2.5), FreeCAD.Rotation(0,0,0))
#print(coordRadius)


vo = box. ViewObject
vo.DisplayMode  = 'Wireframe'

for n in range(1, len(coordRadius)):#nspheres): 
	name = "sphere" + str(counter)
	sphere = doc.addObject("Part::Sphere", name)
	#randr = random.uniform(minradius, maxradius) 
	sphere.Radius = coordRadius[n][3]
	sphere.Placement = FreeCAD.Placement(FreeCAD.Vector(coordRadius[n][0], coordRadius[n][1], coordRadius[n][2]), FreeCAD.Rotation(0, 0, 0))
	spherelist = spherelist + [sphere]
	doc.Fusion.Shapes = spherelist
	if n%20== 0: 
		doc.recompute()
		print(vol.Shape.Volume)
		if (vol.Shape.Volume > (porosity*width*height*length)): 
			break	
	counter = counter + 1

doc.recompute()
 
print(vol.Shape.Volume)
print(box.Shape.Volume)

Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
doc.recompute()