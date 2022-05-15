import random
import math

dimesion = 0.40
realCoordinates = []
simulationCoordinates = []
nspheres = 50
minRadius = 0.035
maxRadius = 0.045
overlapCordinates = []
sphereVol = 0
totalVol = dimesion**3


for n in range(0,dimesion +0.01): 
    for m in range(0,dimesion + 0.01): 
        for o in range(0,dimesion + 0.01): 
            realCoordinates.append([n,m,o])

tempcoordinates = realCoordinates


def inthesphere(x,y,z,center,radius):
    if (x-center[0])**2 + (y-center[1])**2 + (z-center[2])**2 <= (1+radius)**2: 
        overlapCordinates.append([x,y,z])
        return True
    else: 
        return False

def RemoveCoord(center, radius): 
    for n in range(0, len(tempcoordinates)):
        inthesphere(tempcoordinates[n][0], tempcoordinates[n][1], tempcoordinates[n][2], center, radius)
    
    print(overlapCordinates)
    for n in range(0,len(overlapCordinates)): 
        tempcoordinates.remove(overlapCordinates[n])
    

while True: 
    if len(tempcoordinates) == 0: 
        break

    center = random.choice(tempcoordinates)
    radius = random.uniform(minRadius, maxRadius) 
    simulationCoordinates.append([center[0], center[1], center[2], radius])
    sphereVol = sphereVol + 4/3*(math.pi*(radius**3))

    RemoveCoord(center, radius)
    overlapCordinates = []

print(sphereVol)
print(totalVol)
porosity  = ((totalVol - sphereVol)/totalVol)*100
print(porosity)
# print(tempcoordinates)
print(simulationCoordinates)
