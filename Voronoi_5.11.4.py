import pygame
from PIL import Image
import random
import math
import numpy as np
import noise
class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.h = 0
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
def astar(paramWorld, start):
    """Returns a list of tuples as a path from the given start to the given end in the given world_test"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = 0
    start_node.f = 0
    start_node.h = paramWorld[start[0]][start[1]]
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if (terrainFall[current_node.position[0]][current_node.position[1]] == False):
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                putpixel((current.position[0],current.position[1]),(0,0,255))
                current = current.parent
            return path[::-1] # Return reversed path
        # Generate children
        num = 0
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(paramWorld) - 1) or node_position[0] < 0 or node_position[1] > (len(paramWorld[len(paramWorld)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if paramWorld[current_node.position[0]][current_node.position[1]] < paramWorld[node_position[0]][node_position[1]]:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)
            num += 1
        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = paramWorld[child.position[0]][child.position[1]]
            child.f = current_node.h + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.f > open_node.f:
                    continue
            # Add the child to the open list
            open_list.append(child)
def addTectBordToFaultList(x,y,nx,ny):#depending on other bord (from other plate), current bord
    currTectType = landOrOceanTectPlate[x][y]#will be labeled as concon,conocean,oceancon,
    nextToTectType = landOrOceanTectPlate[nx][ny]#or oceanocean, and added to appropriate list
    if(currTectType == continental):#hasBeenVisited
        if (nextToTectType == continental):
            conCon.append([x,y])
            heightMap[x][y] = invalidNum
        elif(nextToTectType != continental):
            conOcean.append([x,y])
            coHasBeenVisited[x][y] = True
            coOrigin[x][y] = True
    elif(currTectType != continental):
        if (nextToTectType == continental):
            oceanCon.append([x,y])
        elif(nextToTectType != continental):
            oceanOcean.append([x,y])
def SearchThroughBordList():#goes through every bord and runs addTectBordToFaultList
    i = 0
    for j in queueBord:
        x = queueBord[i][0]
        y = queueBord[i][1]
        i += 1
        if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):#curr bord and lower bord arent from same plate
            addTectBordToFaultList(x,y,x,y-1)
        if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):#curr bord and upper bord arent from same plate
            addTectBordToFaultList(x,y,x,y+1)
        if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):#curr bord and left bord arent from same plate
            addTectBordToFaultList(x,y,x-1,y)
        if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):#curr bord and right bord arent from same plate
            addTectBordToFaultList(x,y,x+1,y)
            
def initialBordSetUp(x,y,nx,ny,listTest,other):#bord is given many of its elements here
    queueBord.append([x,y])#bord added to master list
    currTectType = landOrOceanTectPlate[x][y] #find out if bord is continental or ocean
    nextToTectType = landOrOceanTectPlate[nx][ny] #same for bord from other tect plate
    inQueue[x][y] = True #bord is added to master list in form of index
    if(currTectType == continental): #If/elif statments determine what neighbor bord list to add curr bord to
        if (nextToTectType == continental):
            conCon.append([x,y])
        elif(nextToTectType != continental):
            conOcean.append([x,y])
    elif(currTectType != continental):
        if (nextToTectType == continental):
            oceanCon.append([x,y])
        elif(nextToTectType != continental):
            oceanOcean.append([x,y])
    if((tectMovementDirection[x][y] == listTest[0] and tectMovementDirection[nx][ny] == other[0])):#if bords converge
        putpixel((x, y),(255,0,0))
        if((currTectType == continental and nextToTectType == continental) or #if bords are conCon or conOcean
         (currTectType == continental and nextToTectType != continental)):#gives curr bord to converge list, gives special starting height at bord, and marks it as converge
            heightMap[x][y] = highElevContinental 
            converge.append((x,y))
            increase[x][y] = .8
            hasBeenVisited[x][y] = convergeLandNum
        elif(currTectType != continental): #if curr bord is oceanic
            converge.append((x,y))#gives curr bord to converge list, gives special starting height at bord, and marks it as converge
            increase[x][y] = .8
            heightMap[x][y] = highElev
            hasBeenVisited[x][y] = convergeOceanNum
    elif((tectMovementDirection[x][y] == listTest[1] and tectMovementDirection[nx][ny] == other[1]) or #if bords diverge
         (tectMovementDirection[x][y] == listTest[2] and tectMovementDirection[nx][ny] == other[1]) or
         (tectMovementDirection[x][y] == listTest[3] and tectMovementDirection[nx][ny] == other[1]) or
         (tectMovementDirection[x][y] == listTest[1] and tectMovementDirection[nx][ny] == other[3]) or
         (tectMovementDirection[x][y] == listTest[1] and tectMovementDirection[nx][ny] == other[4]) or
         (tectMovementDirection[x][y] == listTest[0] and tectMovementDirection[nx][ny] == other[1]) or
         (tectMovementDirection[x][y] == listTest[1] and tectMovementDirection[nx][ny] == other[0])):
        putpixel((x, y),(0,0,255))#gives curr bord to diverge list, gives special starting height at bord, and marks it as diverge
        diverge.append((x,y))
        decrease[x][y] = -.8
        heightMap[x][y] = lowElev
        hasBeenVisited[x][y] = divergeNum
    elif((tectMovementDirection[x][y] == listTest[6] and tectMovementDirection[nx][ny] == other[3]) or #if bords are transform
        (tectMovementDirection[x][y] == listTest[6] and tectMovementDirection[nx][ny] == other[4]) or
        (tectMovementDirection[x][y] == listTest[7] and tectMovementDirection[nx][ny] == other[4]) or
        (tectMovementDirection[x][y] == listTest[7] and tectMovementDirection[nx][ny] == other[3])):
        putpixel((x,y),(0,255,0))#gives curr bord to transform list, gives special starting height at bord, and marks it as transform
        transform.append((x,y))
        hasBeenVisited[x][y] = transformNum
        heightMap[x][y] = midElev
    elif((tectMovementDirection[x][y] == listTest[4] and tectMovementDirection[nx][ny] == other[2]) or #if bords converge (not both bords heading into one another)
         (tectMovementDirection[x][y] == listTest[5] and tectMovementDirection[nx][ny] == other[2]) or
         (tectMovementDirection[x][y] == listTest[0] and tectMovementDirection[nx][ny] == other[3]) or
         (tectMovementDirection[x][y] == listTest[0] and tectMovementDirection[nx][ny] == other[4])):
        putpixel((x,y),(128,0,128))#gives curr bord to converge list, gives special starting height at bord, and marks it as converge
        converge.append((x,y))
        increase[x][y] = .8
        hasBeenVisited[x][y] = convergeOtherNum
        heightMap[x][y] = highElev
def giveTectBordInfoDependingOnNeighbor(x,y,prevX,prevY):#depending on prevous bord mark, its neighbor will be given the same mark and attributes
    if(hasBeenVisited[prevX][prevY] == convergeLandNum):
        converge.append((x,y))
        increase[x][y] = .8
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElevContinental
        hasBeenVisited[x][y] = convergeLandNum
    elif(hasBeenVisited[prevX][prevY] == convergeOceanNum):
        increase[x][y] = .8
        converge.append((x,y))
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElev
        hasBeenVisited[x][y] = convergeOceanNum
    elif(hasBeenVisited[prevX][prevY] == divergeNum):
        diverge.append((x,y))
        decrease[x][y] = -.8
        putpixel((x, y),(0,0,255))
        heightMap[x][y] = lowElev
        hasBeenVisited[x][y] = divergeNum
    elif(hasBeenVisited[prevX][prevY] == transformNum):
        transform.append((x,y))
        putpixel((x, y),(0,255,0))
        heightMap[x][y] = midElev
        hasBeenVisited[x][y] = transformNum
    elif(hasBeenVisited[prevX][prevY] == convergeOtherNum):
        converge.append((x,y))
        increase[x][y] = .8
        putpixel((x, y),(128,0,128))
        heightMap[x][y] = highElev
        hasBeenVisited[x][y] = convergeOtherNum
def goThroughRemainingNoInfoBord(bord):#if bord element doesnt have a mark/other attributes, look to see if neighbors (from same tect plate) do. 
    i = 0 # if they do, use giveTectBordInfoDependingOnNeighbor on curr bord element
    newBord = []
    for j in bord:
        x = bord[i][0]
        y = bord[i][1]
        if( y != 0 and (heightMap[x][y-1] != invalidNum) and (tectNum[x][y-1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x,y-1)
        elif( y != imgy-1 and (heightMap[x][y+1] != invalidNum ) and (tectNum[x][y+1] == tectNum[x][y] )):
            giveTectBordInfoDependingOnNeighbor(x,y,x,y+1)
        elif( x != 0 and (heightMap[x-1][y] != invalidNum) and (tectNum[x-1][y] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y)
        elif( x != imgx-1 and(heightMap[x+1][y] != invalidNum) and (tectNum[x+1][y] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y)
        elif(x != imgx-1 and y != imgy-1 and heightMap[x+1][y+1] != invalidNum and(tectNum[x+1][y+1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y+1)
        elif(x != 0 and y != 0 and heightMap[x-1][y-1] != invalidNum and (tectNum[x-1][y-1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y-1)
        elif(x != imgx-1 and y != 0 and heightMap[x+1][y-1] != invalidNum and (tectNum[x+1][y-1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y-1)
        elif(x != 0 and y != imgy-1 and heightMap[x-1][y+1] != invalidNum and (tectNum[x-1][y+1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y+1)
        #if bord has no neighbors that are hasBeenVisited, add it to newBord list where it will go through goThroughRemainingNoInfoBord again until hasBeenVisited neighbor is found         
        if(heightMap[x][y] == invalidNum): 
            newBord.append([x,y])
        else:
            queueBord.append([x,y]) #if curr bord element is now hasBeenVisited, add it to master bord list
        i += 1
    return newBord # return list of unhasBeenVisited bords
def generateNoise(width,height,scal,octave,persist):
    scale       = scal # Number that determines at what distance to view the noisemap
    octaves     = octave # the number of levels of detail you want you perlin noise to have
    persistence = persist # number that determines how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2.0 # number that determines how much each octave contributes to the overall shape (adjusts amplitude)
    world_test = np.zeros(image.size)
    for x in range(width):
        for y in range(height):
            world_test[x][y] = noise.pnoise2(x/scale, 
                                        y/scale, 
                                        octaves     = octaves, 
                                        persistence = persistence, 
                                        lacunarity  = lacunarity, 
                                        repeatx     = width, 
                                        repeaty     = height, 
                                        base        = 0)
    return world_test
def generate_voronoi_diagram(width, height, num_cells):
    nx = []
    ny = []
    nx2 = []
    ny2 = []
    nx3 = []
    ny3 = []
    nr = []
    ng = []
    nb = []
    numLandPlates = 0
    for i in range(num_cells):
            nx.append(random.randrange(imgx))
            ny.append(random.randrange(imgy))
            nx2.append(nx[i]+width)
            ny2.append(ny[i])
            nx3.append(nx[i]-width)
            ny3.append(ny[i])
            if numLandPlates < int(inputLandTect):
                isOceanic.append(False)
                green = random.randrange(150,256)
                nr.append(green)#gives water color
                ng.append(green-50)
                nb.append(green-100)
                numLandPlates += 1
            else:
                isOceanic.append(True)
                red = random.randrange(150)#gives land color
                nr.append(red)
                ng.append(red+50)
                nb.append(red+100)
            tectMovement.append(random.choice(tectMovementList))
    for y in range(int(imgy)):
        for x in range(int(imgx)):
            dmin = math.hypot(imgx-1, imgy-1)
            j = -1
            for i in range(num_cells):
                    d = math.hypot((nx[i]-x), (ny[i]-y))#makes voronoi cells on screen
                    if d < dmin:
                        dmin = d
                        j = i
                    d = math.hypot((nx3[i]-x), (ny3[i]-y)) #makes voronoi cells to the left of screen
                    if d < dmin:
                        dmin = d
                        j = i
                    d = math.hypot((nx2[i]-x), (ny2[i]-y)) #makes voronoi cells to the right of screen
                    if d < dmin:
                        dmin = d
                        j = i
            tectNum[x][y] = j+1
            landOrOceanTectPlate[x][y] = isOceanic[j]
            tectMovementDirection[x][y] = tectMovement[j]
            putpixel((x, y), (nr[j], ng[j], nb[j]))
    image.save("Tect_Without_Fault_Bord.png", "PNG")
    print("Generated Plates")
def setFaultBordToInvalidHeight(bordList):
    i = 0
    for j in range(len(bordList)):
        x = bordList[i][0]
        y = bordList[i][1]
        if(landOrOceanTectPlate[x][y] == oceanicPlate):
            heightMap[x][y] = invalidNum
        i += 1
def colorMap():
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] <= -0.30:
                col = (122,170,219)
            elif heightMap[x][y] <= -0.01:
                col = (168,211,241)
            elif heightMap[x][y] < 0.0:
                col = (217,236,255)
            elif heightMap[x][y] < 0.0667:
                col = (0,192,96) 
            elif heightMap[x][y] < 0.1667:
                col = (0,255,128)
            elif heightMap[x][y] < 0.33:
                col = (255,255,128)
            elif heightMap[x][y] < 0.667:
                col = (128,128,64)
            elif heightMap[x][y] < 1.0:
                col = (128,128,192)
            else:
                col = (255,255,255)
            putpixel((x,y), col)
def makeMountains():
    i= 0
    for j in converge:#sets up where mountains can form
        x = converge[i][0]
        y = converge[i][1]
        convergeComplete[x][y] = True
        i += 1
        oldHeight = 0
        if((terrainFall[x][y] == False)):#if not on land, then keep looking
            currElev = increase[x][y]
        else:#if on land, decrease currElev counter
            ran = random.uniform(.9,1.0)
            currElev = increase[x][y] * ran
        if(currElev > .01):#once counter reaches .01, then mountains cant form out of area
            if(y != 0 and (convergeComplete[x][y-1] != True)and(tectNum[x][y-1] == tectNum[x][y])):
                  converge.append([x,y-1])
                  convergeComplete[x][y-1] = True
                  increase[x][y-1] = currElev
            if(y != imgy-1 and (convergeComplete[x][y+1] != True)and(tectNum[x][y+1] == tectNum[x][y])):
                  converge.append([x,y+1])
                  convergeComplete[x][y+1] = True
                  increase[x][y+1] = currElev 
            if(x != 0  and (convergeComplete[x-1][y] != True)and(tectNum[x-1][y] == tectNum[x][y])):
                  converge.append([x-1,y])
                  convergeComplete[x-1][y] = True
                  increase[x-1][y] = currElev
            elif(x == 0 and (convergeComplete[imgx-1][y] != True)and(tectNum[imgx-1][y] == tectNum[x][y])):
                  converge.append([imgx-1,y])
                  convergeComplete[imgx-1][y] = True
                  increase[imgx-1][y] = currElev 
            if(x != imgx-1 and (convergeComplete[x+1][y] != True)and(tectNum[x+1][y] == tectNum[x][y])):
                  converge.append([x+1,y])
                  convergeComplete[x+1][y] = True
                  increase[x+1][y] = currElev
            elif(x == imgx-1 and (convergeComplete[0][y] != True)and(tectNum[0][y] == tectNum[x][y])):
                  converge.append([0,y])
                  convergeComplete[0][y] = True
                  increase[0][y] = currElev
    mountain = []
    prevHeight = np.zeros(image.size)
    if(len(converge) != 0):
        while True:
            m = random.choice(converge)
            if terrainFall[m[0]][m[1]] == True:
                mountain.append(m)
                prevHeight[m[0]][m[1]] = True
                break
        randNum = random.randint(1,30)#size of mountain's "spine"
        new_position = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        increase2 = np.zeros(image.size)
        convergeComplete2 = np.zeros(image.size)
        startingPeak = random.uniform(.7,.90)
        for i in range(randNum):#for mountain length
            addPos = random.choice(new_position)
            newPos = (mountain[i][0]+addPos[0],mountain[i][1]+addPos[1])#nex mountain location
            if(prevHeight[newPos[0]][newPos[1]] != True and terrainOrigin[newPos[0]][newPos[1]] != True and convergeComplete[newPos[0]][newPos[1]] == True and terrainFall[newPos[0]][newPos[1]] == True
               and newPos[0] <= (imgx - 1) and newPos[0] >= 0 and
               newPos[1] <= (imgy-1) or newPos[1] >= 0):#if it goes through for loop, go through for loop, is added as new mountain spin location
                mountain.append(newPos)
                prevHeight[newPos[0]][newPos[1]] = True
                increase2[newPos[0]][newPos[1]] = startingPeak + random.uniform(0.0,.1)#mountain pos starting height
                convergeComplete2[newPos[0]][newPos[1]] = True       
        image.save("mountain.png", "PNG")
        i = 0
        converge2 = []
        goingDown = random.uniform(.3,.90)#base mountain decreas amount
        for j in mountain:
            x = mountain[i][0]
            y = mountain[i][1]
            i += 1
            if(terrainFall[x][y] == True):#if on land
                convergeComplete2[x][y] = True
                rand = goingDown + random.uniform(0.0,0.1)
                currElev = increase2[x][y] * rand #decrease mountain height by random amount
                oldHeight = heightMap[x][y]
                heightMap[x][y]  = currElev
                if(currElev> oldHeight):#if current Height > old height, expand
                    if(y != 0 and (convergeComplete2[x][y-1] != True)):
                          mountain.append([x,y-1])
                          convergeComplete2[x][y-1] = True
                          increase2[x][y-1] = currElev
                    if(y != imgy-1 and (convergeComplete2[x][y+1] != True)):
                          mountain.append([x,y+1])
                          convergeComplete2[x][y+1] = True
                          increase2[x][y+1] = currElev 
                    if(x != 0  and (convergeComplete2[x-1][y] != True)):
                          mountain.append([x-1,y])
                          convergeComplete2[x-1][y] = True
                          increase2[x-1][y] = currElev
                    elif(x == 0 and (convergeComplete2[imgx-1][y] != True)):
                          mountain.append([imgx-1,y])
                          convergeComplete2[imgx-1][y] = True
                          increase2[imgx-1][y] = currElev 
                    if(x != imgx-1 and (convergeComplete2[x+1][y] != True)):
                          mountain.append([x+1,y])
                          convergeComplete2[x+1][y] = True
                          increase2[x+1][y] = currElev
                    elif(x == imgx-1 and (convergeComplete2[0][y] != True)):
                          mountain.append([0,y])
                          convergeComplete2[0][y] = True
                          increase2[0][y] = currElev
def leftArrow(x,y):
    putpixel((x,y), (0,0,0))
    if(x < imgx-1):
        putpixel((x+1,y), (0,0,0))
    if(x <imgx-1 and y < imgy-1):
        putpixel((x+1,y+1), (0,0,0))
    if(x < imgx-1 and y > 0):
        putpixel((x+1,y-1), (0,0,0))
    if(x < imgx-2):
        putpixel((x+2,y), (0,0,0))
    if(x < imgx-2 and y < imgy-1):
        putpixel((x+2,y+1), (0,0,0))
    if(x < imgx-2 and y > 0):
        putpixel((x+2,y-1), (0,0,0))
    if(x < imgx-2 and y < imgy-2):
        putpixel((x+2,y+2), (0,0,0))
    if(x < imgx-2 and y > 1):    
        putpixel((x+2,y-2), (0,0,0))
def rightArrow(x,y):
    putpixel((x,y), (0,0,0))
    if(x > 0):
        putpixel((x-1,y), (0,0,0))
    if(x > 0 and y < imgy-1):
        putpixel((x-1,y+1), (0,0,0))
    if(x > 0 and y > 0):
        putpixel((x-1,y-1), (0,0,0))
    if(x > 1):
        putpixel((x-2,y), (0,0,0))
    if(x > 1 and y < imgy-1):
        putpixel((x-2,y+1), (0,0,0))
    if(x > 1 and y > 0): 
        putpixel((x-2,y-1), (0,0,0))
    if(x > 1 and y < imgy-2):
        putpixel((x-2,y+2), (0,0,0))
    if(x > 1 and y > 1):
        putpixel((x-2,y-2), (0,0,0))
def rest():
    remainingBord = [] #Borders without fault type(ex: convirgent,divergent,etc)
    for x in range(imgx):
        for y in range(imgy):
            num = 0 #if the current pixel is a border, find how many sides it is bordered on
            if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):#bordered above
                num += 1
            if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):#bordered below
                num += 2
            if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):#bordered to the left
                num += 4
            if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):#border to the right
                num += 8
            if(num == 1):#if bordered above only, find what kind of fault type
                listTest = [Up,Down,Left,Right,Right,Left,Right,Left]
                other = [Down,Up,Down,Left,Right]
                initialBordSetUp(x,y,x,y-1,listTest,other)
            elif( num == 2):#if bordered below only, find what kind of fault type
                listTest = [Down,Up,Left,Right,Right,Left,Left,Right]
                other = [Up,Down,Up,Right,Left]
                initialBordSetUp(x,y,x,y+1,listTest,other)              
            elif( num == 4):#if bordered left only, find what kind of fault type
                listTest = [Left,Right,Up,Down,Up,Down,Up,Down]
                other = [Right,Left,Right,Down,Up]
                initialBordSetUp(x,y,x-1,y,listTest,other)
            elif( num == 8):#if bordered right only, find what kind of fault type
                listTest = [Right,Left,Up,Down,Up,Down,Up,Down]
                other = [Left,Right,Left,Down,Up]
                initialBordSetUp(x,y,x+1,y,listTest,other)
            else:#if border has multiple borders next to it, add it to list tbd
                if(num > 0):
                    remainingBord.append([x,y])
                heightMap[x][y] = invalidNum    
    while True:#go through undefined borders to determine their type
        remainingBord = goThroughRemainingNoInfoBord(remainingBord)
        if len(remainingBord) == 0:
            break
    image.save("Tect_With_Fault_Bord.png", "PNG")
    SearchThroughBordList()
    setFaultBordToInvalidHeight(converge)#makes it so oceanic bords have invalid height so not to effect con bords in conOcean
    setFaultBordToInvalidHeight(diverge)
    setFaultBordToInvalidHeight(transform)
    i = 0
    for j in conOcean:#Go through contiental plate bord of conOcean border and BFS to determine start of deep ocean and continental shelf
        x = conOcean[i][0]
        y = conOcean[i][1]
        i += 1
        elev = 0
        num = 0
        if(coOrigin[x][y] != True):#if it is a part of the orginial border: look at neighbors that are valid
            if(y != 0 and heightMap[x][y-1] != invalidNum):# and get their heights added to a sum height and their total number
                elev += heightMap[x][y-1]
                num += 1
            if(y != imgy-1 and heightMap[x][y+1] != invalidNum):
                elev += heightMap[x][y+1]
                num += 1
            if(x != 0 and heightMap[x-1][y] != invalidNum ):
                elev += heightMap[x-1][y]
                num += 1
            elif(x == 0 and heightMap[imgx-1][y] != invalidNum ):
                elev += heightMap[imgx-1][y]
                num += 1
            if(x != imgx-1 and heightMap[x+1][y] != invalidNum ):
                elev += heightMap[x+1][y]
                num += 1
            elif(x == imgx-1 and heightMap[0][y] != invalidNum ):
                elev += heightMap[0][y]
                num += 1
            if(x != imgx-1 and y != imgy-1 and heightMap[x+1][y+1] != invalidNum ):
                elev += heightMap[x+1][y+1]
                num += 1
            if(x != 0 and y != 0 and heightMap[x-1][y-1] != invalidNum ):
                elev += heightMap[x-1][y-1]
                num += 1
            if(x != imgx-1 and y != 0 and heightMap[x+1][y-1] != invalidNum ):
                elev += heightMap[x+1][y-1]
                num += 1
            if(x != 0 and y != imgy-1 and heightMap[x-1][y+1] != invalidNum ):
                elev += heightMap[x-1][y+1]
                num += 1    
            if(num != 0):# if the num of valid neighbors is greater than zero
                if(landOrOceanTectPlate[x][y] == False):#if curr bord is land plate
                    if((elev/num) < 0.0):# if height would make it land 
                        heightMap[x][y] = (elev/num)+ 0.0025
                    else:
                        heightMap[x][y] = (elev/num)+ 0.005
                elif(landOrOceanTectPlate[x][y] == True):#if curr bord is ocean plate
                    if((elev/num) > -.30):# if height greater than deep ocean
                        heightMap[x][y] = (elev/num) - 0.025
                    else:
                        heightMap[x][y] = (elev/num) - 0.01
            
        if(y != 0 and (coHasBeenVisited[x][y-1] != True)):#add neighbors to conOcean list and mark them as visited
          conOcean.append([x,y-1])
          coHasBeenVisited[x][y-1] = True            
        if(y != imgy-1 and (coHasBeenVisited[x][y+1] != True)):
          conOcean.append([x,y+1])
          coHasBeenVisited[x][y+1] = True            
        if(x != 0 and (coHasBeenVisited[x-1][y] != True)):
          conOcean.append([x-1,y])
          coHasBeenVisited[x-1][y] = True
        elif(x == 0 and(coHasBeenVisited[imgx-1][y] != True)):
          conOcean.append([imgx-1,y])
          coHasBeenVisited[imgx-1][y] = True
        if(x != imgx-1 and (coHasBeenVisited[x+1][y] != True)):
          conOcean.append([x+1,y])
          coHasBeenVisited[x+1][y] = True
        elif(x == imgx-1 and (coHasBeenVisited[0][y] != True)):
          conOcean.append([0,y])
          coHasBeenVisited[0][y] = True 
        if(x != imgx-1 and y != imgy-1 and coHasBeenVisited[x+1][y+1] != True):
          conOcean.append([x+1,y+1])
          coHasBeenVisited[x+1][y+1] = True
        if(x != 0 and y != 0 and coHasBeenVisited[x-1][y-1] != True):
          conOcean.append([x-1,y-1])
          coHasBeenVisited[x-1][y-1] = True
        if(x != imgx-1 and y != 0 and coHasBeenVisited[x+1][y-1] != True):
          conOcean.append([x+1,y-1])
          coHasBeenVisited[x+1][y-1] = True
        if(x != 0 and y != imgy-1 and coHasBeenVisited[x-1][y+1] != True):
          conOcean.append([x-1,y+1])
          coHasBeenVisited[x-1][y+1] = True

    for x in range(imgx):#Marks pixels that are continental crust
        for y in range(imgy):
            if(heightMap[x][y] >= 0.0):
                landTotal[x][y] = True
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] <= -0.75:
                col = (122,170,219)
            elif heightMap[x][y] <= -0.01:
                col = (168,211,241)
            elif heightMap[x][y] < 0.0:
                col = (217,236,255)
                if(y != 0 and heightMap[x][y-1] < 0.0):#if current height is continental crust and next to
                  borderShelf[x][y-1] = True#ocean height, add them to landList
                  landFall[x][y] = True
                  landList.append([x,y])
                if(y != imgy-1 and heightMap[x][y+1] < 0.0):
                  borderShelf[x][y+1] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != 0 and heightMap[x-1][y] < 0.0 ):
                  borderShelf[x-1][y] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                elif(x == 0 and heightMap[imgx-1][y] < 0.0 ):
                  borderShelf[imgx-1][y] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != imgx-1 and heightMap[x+1][y] < 0.0 ):
                  borderShelf[x+1][y] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                elif(x == imgx-1 and heightMap[0][y] < 0.0 ):
                  borderShelf[0][y] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != imgx-1 and y != imgy-1 and heightMap[x+1][y+1] < 0.0 ):
                  borderShelf[x+1][y+1] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != 0 and y != 0 and heightMap[x-1][y-1] < 0.0 ):
                  borderShelf[x-1][y-1] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != imgx-1 and y != 0 and heightMap[x+1][y-1] < 0.0 ):
                  borderShelf[x+1][y-1] = True
                  landFall[x][y] = True
                  landList.append([x,y])
                if(x != 0 and y != imgy-1 and heightMap[x-1][y+1] < 0.0 ):
                  borderShelf[x-1][y+1] = True
                  landFall[x][y] = True
                  landList.append([x,y])
            elif heightMap[x][y] < 0.0667:
                col = (0,192,96) 
            elif heightMap[x][y] < 0.1667:
                col = (0,255,128)
            elif heightMap[x][y] < 0.33:
                col = (255,255,128)
            elif heightMap[x][y] < 0.667:
                col = (128,128,64)
            elif heightMap[x][y] < 1.0:
                col = (128,128,192)
            else:
                col = (255,255,255)
            putpixel((x,y), col)
    i = 0
    for j in range(len(landList)):
        x = landList[i][0]
        y = landList[i][1]
        landOrigin[x][y] = True
        heightMap[x][y] = 0.0
        i += 1
    i = 0
    for j in landList:
        x = landList[i][0]
        y = landList[i][1]
        elev = 0
        num = 0
        if(landOrigin[x][y] != True): #if not landOrigin, add up neighbors and divde by their num to get new height
            if(y != 0):
              elev += heightMap[x][y-1]
              num += 1
            if(y != imgy-1):
              elev += heightMap[x][y+1]
              num += 1
            if(x != 0):
              elev += heightMap[x-1][y]
              num += 1
            elif(x == 0):
              elev += heightMap[imgx-1][y]
              num += 1
            if(x != imgx-1):
              elev += heightMap[x+1][y]
              num += 1
            elif(x == imgx-1):
              elev += heightMap[0][y]
              num += 1
            if(x != imgx-1 and y != imgy-1):
              elev += heightMap[x+1][y+1]
              num += 1
            if(x != 0 and y != 0):
              elev += heightMap[x-1][y-1]
              num += 1
            if(x != imgx-1 and y != 0):
              elev += heightMap[x+1][y-1]
              num += 1
            if(x != 0 and y != imgy-1):
              elev += heightMap[x-1][y+1]
              num += 1
            if(num != 0):
                heightMap[x][y] = (elev/num)+ .02 #Add .02 to height
        if(y != 0 and landTotal[x,y-1] == True and (landFall[x][y-1] != True)):#add neighbors to conOcean list and mark them as visited
              landList.append([x,y-1])
              landFall[x][y-1] = True            
        if(y != imgy-1 and landTotal[x][y+1] == True and (landFall[x][y+1] != True)):
              landList.append([x,y+1])
              landFall[x][y+1] = True            
        if(x != 0 and landTotal[x-1][y] == True and (landFall[x-1][y] != True)):
              landList.append([x-1,y])
              landFall[x-1][y] = True
        elif(x == 0 and landTotal[imgx-1][y] == True and (landFall[imgx-1][y] != True)):
              landList.append([imgx-1,y])
              landFall[imgx-1][y] = True
        if(x != imgx-1 and landTotal[x+1][y] == True and (landFall[x+1][y] != True)):
              landList.append([x+1,y])
              landFall[x+1][y] = True
        elif(x == imgx-1 and landTotal[0][y] == True and (landFall[0][y] != True)):
              landList.append([0,y])
              landFall[0][y] = True 
        if(x != imgx-1 and y != imgy-1 and landTotal[x+1][y+1] == True and landFall[x+1][y+1] != True):
              landList.append([x+1,y+1])
              landFall[x+1][y+1] = True
        if(x != 0 and y != 0 and landTotal[x-1][y-1] == True and landFall[x-1][y-1] != True):
              landList.append([x-1,y-1])
              landFall[x-1][y-1] = True
        if(x != imgx-1 and y != 0 and landTotal[x+1][y-1] == True and landFall[x+1][y-1] != True):
              landList.append([x+1,y-1])
              landFall[x+1][y-1] = True
        if(x != 0 and y != imgy-1 and landTotal[x-1][y+1] == True and landFall[x-1][y+1] != True):
              landList.append([x-1,y+1])
              landFall[x-1][y+1] = True
        i += 1
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if landTotal[x][y] == True:
                if heightMap[x][y] < 0.0:
                    col = (217,236,255)
                elif heightMap[x][y] < 0.0667:
                    col = (0,192,96) 
                elif heightMap[x][y] < 0.1667:
                    col = (0,255,128)
                elif heightMap[x][y] < 0.33:
                    col = (255,255,128)
                elif heightMap[x][y] < 0.667:
                    col = (128,128,64)
                elif heightMap[x][y] < 1.0:
                    col = (128,128,192)
                else:
                    col = (255,255,255)
                putpixel((x,y), col)
    world2 = generateNoise(wid,hei,100,12,.5)
    for x in range(imgx):
        for y in range(imgy):#add noise to world height
            if(landTotal[x][y] == True):
                heightMap[x][y] += (heightMap[x][y]+.3)* (world2[x][y])
            elif (heightMap[x][y] <= -0.1):
                heightMap[x][y] += (heightMap[x][y]-.5)* (world2[x][y])
                if heightMap[x][y] > -0.01:
                    heightMap[x][y] = -0.01
            if(heightMap[x][y] >= .01):
                heightMap[x][y] = 0.01
                terrainTotal[x][y] = True
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):#Finds terrain that borders continental crust
            if landTotal[x][y] == True:
                if heightMap[x][y] < 0.0:
                    col = (217,236,255)
                elif heightMap[x][y] < 0.0667:
                    col = (0,192,96)
                    if(y != 0 and heightMap[x][y-1] < 0.01):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(y != imgy-1 and heightMap[x][y+1] < 0.01):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != 0 and heightMap[x-1][y] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    elif(x == 0 and heightMap[imgx-1][y] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != imgx-1 and heightMap[x+1][y] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    elif(x == imgx-1 and heightMap[0][y] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != imgx-1 and y != imgy-1 and heightMap[x+1][y+1] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != 0 and y != 0 and heightMap[x-1][y-1] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != imgx-1 and y != 0 and heightMap[x+1][y-1] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                    if(x != 0 and y != imgy-1 and heightMap[x-1][y+1] < 0.01 ):
                      terrainFall[x][y] = True
                      terrainList.append([x,y])
                putpixel((x,y), col)               
    i = 0
    for j in range(len(terrainList)):
        x = terrainList[i][0]
        y = terrainList[i][1]
        terrainOrigin[x][y] = True
        heightMap[x][y] = 0
        i += 1
    i = 0
    world2 = generateNoise(wid,hei,100,12,.7)
    for j in terrainList:
        x = terrainList[i][0]
        y = terrainList[i][1]
        i+=1
        elev = 0
        num = 0
        tIncrease = .0015
        if(terrainOrigin[x][y] == True):#adds to current terrain height
            heightMap[x][y] = tIncrease
        if(y != 0 and terrainTotal[x,y-1] == True and (terrainFall[x][y-1] != True)):#finds neighboring terrain
              terrainList.append([x,y-1])
              terrainFall[x][y-1] = True
              heightMap[x][y-1] = heightMap[x][y] + tIncrease
        if(y != imgy-1 and terrainTotal[x][y+1] == True and (terrainFall[x][y+1] != True)):
              terrainList.append([x,y+1])
              terrainFall[x][y+1] = True
              heightMap[x][y+1] = heightMap[x][y] + tIncrease
        if(x != 0 and terrainTotal[x-1][y] == True and (terrainFall[x-1][y] != True)):
              terrainList.append([x-1,y])
              terrainFall[x-1][y] = True
              heightMap[x-1][y] = heightMap[x][y] + tIncrease
        elif(x == 0 and terrainTotal[imgx-1][y] == True and (terrainFall[imgx-1][y] != True)):
              terrainList.append([imgx-1,y])
              terrainFall[imgx-1][y] = True
              heightMap[imgx-1][y] = heightMap[x][y] + tIncrease
        if(x != imgx-1 and terrainTotal[x+1][y] == True and (terrainFall[x+1][y] != True)):
              terrainList.append([x+1,y])
              terrainFall[x+1][y] = True
              heightMap[x+1][y] = heightMap[x][y] + tIncrease
        elif(x == imgx-1 and terrainTotal[0][y] == True and (terrainFall[0][y] != True)):
              terrainList.append([0,y])
              terrainFall[0][y] = True
              heightMap[0][y] = heightMap[x][y] + tIncrease
              
    heightMap_2 = np.zeros(image.size)#create a seperate height map with dif noise to use for rivers
    for x in range(imgx):
        for y in range(imgy):
            heightMap_2[x][y] = heightMap[x][y]
            if(terrainFall[x][y] != True):
                heightMap_2[x][y] = -10   
    max_grad = np.max(heightMap_2)
    for x in range(imgx):
        for y in range(imgy):
            if(terrainTotal[x][y] == True):#if terrain, add noise
                heightMap_2[x][y] = (heightMap_2[x][y] / max_grad)
                heightMap_2[x][y] += world2[x][y]/15
                heightMap[x][y] += world2[x][y]/2       
    max_grad = np.max(heightMap)
    image.save("Basic.png", "PNG")
    
    riverList =[]
    i = 0
    riverList = []
    riverTrue = np.zeros(image.size)
    for i in range(int(inputRiversNum)):#create num of rivers depending on user input
        riverStart = random.choice(terrainList)
        riverList.append(riverStart)
    i = 0
    for j in riverList:
        x = riverList[i][0]
        y = riverList[i][1]
        path = astar(heightMap_2,riverList[i])
        print("Generated River " + str(i+1))
        i += 1
    image.save("Rivers.png", "PNG")
    convergeComplete = np.zeros(image.size)
    for i in range(int(inputMountainNum)):
        makeMountains()
        print("Generated Mountain " + str(i+1))
    col =(0,0,0)
    for y in range(imgy):
        for x in range(imgx):#color in new terrain heights
            if(terrainTotal[x][y] == True):
                if heightMap[x][y] < 0.0667:
                    col = (0,192,96) 
                elif heightMap[x][y] < 0.1667:
                    col = (0,255,128)
                elif heightMap[x][y] < 0.33:
                    col = (255,255,128)
                elif heightMap[x][y] < 0.667:
                    col = (128,128,64)
                elif heightMap[x][y] < 1.0:
                    col = (128,128,192)
                else:
                    col = (255,255,255)
                putpixel((x,y), col)    
    i = 0
    image.save("mountain2.png", "PNG")
    #defines the standard ocean currents found at certain degrees
    yHalf = int(imgy/2)
    westWinds = int(yHalf * .33) # Goes eastwards
    eastWinds = int(yHalf * .66) # Goes westwards
    polarWinds = int(yHalf * .90) # Goes westwards
    testCurrentMovement = []
    #at starting currents, if not continental shelf, keep moving left.
    for x in range(imgx):
        if(landFall[x][yHalf+5] != True):
            putpixel((x,yHalf+5), (0,255,0))
            currentColor[x][yHalf+5] = yHalf+5
            currentMovement.append([x,yHalf+5])
            testCurrentMovement.append([x,yHalf+5])
            alreadyInCurrent[x][yHalf+5] = True
        if(landFall[x][yHalf-5] != True):
            putpixel((x,yHalf-5), (0,255,0))
            currentColor[x][yHalf-5] = yHalf-5
            currentMovement.append([x,yHalf-5])
            testCurrentMovement.append([x,yHalf-5])
            alreadyInCurrent[x][yHalf-5] = True
        
    i = 0
    for j in currentMovement:
        x = currentMovement[i][0]
        y = currentMovement[i][1]
        black = (0,0,0)
        red = (255,0,0)
        blue = (0,0,255)
        newTest = False #if current is next to continental shelf, give it a color and it passes test
        if(y != 0 and landFall[x][y-1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(y != imgy-1 and landFall[x][y+1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != 0 and landFall[x-1][y] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x == 0 and landFall[imgx-1][y] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != imgx-1 and landFall[x+1][y] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x == imgx-1 and landFall[0][y] == True ):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != imgx-1 and y != imgy-1 and landFall[x+1][y+1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != 0 and y != 0 and landFall[x-1][y-1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != imgx-1 and y != 0 and landFall[x+1][y-1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        elif(x != 0 and y != imgy-1 and landFall[x-1][y+1] == True):
            putpixel((x,y), (0,255,0))
            newTest = True
        if (newTest == True):#if it passes test
            newCurr[x][y] = True #give pixel color depending on current location and origins
            if (currentColor[x][y] == yHalf and y > yHalf):
                putpixel((x,y), black)
            elif (currentColor[x][y] == yHalf and y < yHalf):
                putpixel((x,y), black)
            elif (currentColor[x][y] == yHalf - 5 and y > yHalf - 5):
                putpixel((x,y), black)
            elif (currentColor[x][y] == yHalf - 5 and y < yHalf - 5):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + 5 and y > yHalf + 5):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + 5 and y < yHalf + 5):
                putpixel((x,y), black)
            elif (currentColor[x][y] == yHalf - westWinds and y > yHalf - westWinds):
                putpixel((x,y), blue)
            elif (currentColor[x][y] == yHalf - westWinds and y < yHalf - westWinds):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + westWinds and y > yHalf + westWinds):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + westWinds and y < yHalf + westWinds):
                putpixel((x,y), blue)
            elif (currentColor[x][y] == yHalf - eastWinds and y > yHalf - eastWinds):
                putpixel((x,y), blue)
            elif (currentColor[x][y] == yHalf - eastWinds and y < yHalf - eastWinds):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + eastWinds and y > yHalf + eastWinds):
                putpixel((x,y), red)
            elif (currentColor[x][y] == yHalf + eastWinds and y < yHalf + eastWinds):
                putpixel((x,y), blue)
        if(y == yHalf):
            putpixel((x,y), (255,0,0))
            currentColor[x][y] = yHalf #yHalf is new origin
            if(x != imgx-1 and x >= 3 and landFall[x+1][y] == True and newCurr[x-2][y] == True):#draws arrow if next to continenal shelf
                rightArrow(x,y)
            if(x != imgx-1 and landFall[x+1][y] != True): #if not continental shelf, add only one neighbor in current direction and it fails test
                putpixel((x,y), black)
                currentMovement.append([x+1,y])
                alreadyInCurrent[x+1][y] = True
                newCurr[x+1][y] = True
                newTest = False
            elif(x == imgx-1 and landFall[0][y] != True):
                putpixel((0,y), black)
                currentMovement.append([0,y])
                alreadyInCurrent[0][y] = True
                newCurr[0][y] = True
                newTest = False
        if(y == yHalf - 5 or y == yHalf + 5 ):
            putpixel((x,y), (0,0,255))
            if (y == yHalf - 5):
                currentColor[x][y] = yHalf - 5#yHalf-5 is new origin
            elif(y == yHalf + 5):
                currentColor[x][y] = yHalf + 5#yHalf+5 is new origin
            if(x != 0 and x <= imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):#draws arrow if next to continenal shelf
                leftArrow(x,y)
            if(x != 0 and landFall[x-1][y] != True):#if not continental shelf, add only one neighbor in current direction and it fails test
                putpixel((x,y), black)
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
                newCurr[x-1][y] = True
                newTest = False
            elif(x == 0 and landFall[imgx-1][y] != True):
                putpixel((imgx-1,y), black)
                currentMovement.append([imgx-1,y])
                alreadyInCurrent[imgx-1][y] = True
                newCurr[imgx-1][y] = True
                newTest = False
        if(y == yHalf - westWinds or y == yHalf + westWinds):
            putpixel((x,y), (255,0,0))
            if (y == yHalf - westWinds):#westerlies are new origin
                currentColor[x][y] = yHalf - westWinds
            elif(y == yHalf + westWinds):
                currentColor[x][y] = yHalf + westWinds
            if(x != imgx-1 and x <= imgx - 3 and landFall[x+1][y] == True and newCurr[x-2][y] == True):#draws arrow if next to continenal shelf
                rightArrow(x,y)
            if(x != imgx-1 and landFall[x+1][y] != True):#if not continental shelf, add only one neighbor in current direction and it fails test
                putpixel((x,y), black)
                currentMovement.append([x+1,y])
                alreadyInCurrent[x+1][y] = True
                newCurr[x+1][y] = True
                newTest = False
            elif(x == imgx-1 and landFall[0][y] != True):
                putpixel((0,y), black)
                currentMovement.append([0,y])
                alreadyInCurrent[0][y] = True
                newCurr[0][y] = True
                newTest = False
        if(y == yHalf - eastWinds or y == yHalf + eastWinds):
            putpixel((x,y), (0,0,255))
            if (y == yHalf - eastWinds):#easterlies are new origin
                currentColor[x][y] = yHalf - eastWinds
            elif(y == yHalf + eastWinds):
                currentColor[x][y] = yHalf + eastWinds
            if(x != 0 and x <= imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):#draws arrow if next to continenal shelf
                leftArrow(x,y)
            if(x != 0 and landFall[x-1][y] != True):#if not continental shelf, add only one neighbor in current direction and it fails test
                putpixel((x,y), black)
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
                newCurr[x-1][y] = True
                newTest = False
            elif(x == 0 and landFall[imgx-1][y] != True):
                putpixel((imgx-1,y), black)
                currentMovement.append([imgx-1,y])
                alreadyInCurrent[imgx-1][y] = True
                newCurr[imgx-1][y] = True
                newTest = False
        if(y == yHalf - polarWinds or y == yHalf + polarWinds ):
            putpixel((x,y), (0,0,255))
            if (y == yHalf - polarWinds):#polar current is new origin
                currentColor[x][y] = yHalf - polarWinds
            elif(y == yHalf + polarWinds):
                currentColor[x][y] = yHalf + polarWinds
            if(x != 0 and x < imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):#draws arrow if next to continenal shelf
                leftArrow(x,y)
            if(x != 0 and landFall[x-1][y] != True):#if not continental shelf, add only one neighbor in current direction and it fails test
                putpixel((x,y), black)
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
                newCurr[x-1][y] = True
                newTest = False
            elif(x == 0 and landFall[imgx-1][y] != True):
                putpixel((imgx-1,y), black)
                currentMovement.append([imgx-1,y])
                alreadyInCurrent[imgx-1][y] = True
                newCurr[imgx-1][y] = True
                newTest = False
            elif(x != 0 and landFall[x-1][y] == True):
                newTest = False
            elif(x == 0 and landFall[imgx-1][y] == True):
                newTest = False   
                
        if (newTest == True):#if it passes test, look at all neighbors to add it to list to see if it's a current
            if(y != 0 and landFall[x][y-1] != True and alreadyInCurrent[x][y-1] != True):
              currentMovement.append([x,y-1])
              currentColor[x][y-1] = currentColor[x][y]
              alreadyInCurrent[x][y-1] = True
            if(y != imgy-1 and landFall[x][y+1] != True and alreadyInCurrent[x][y+1] != True):
              currentMovement.append([x,y+1])
              currentColor[x][y+1] = currentColor[x][y]
              alreadyInCurrent[x][y+1] = True
            if(x != 0 and landFall[x-1][y] != True and alreadyInCurrent[x-1][y] != True):
              currentMovement.append([x-1,y])
              currentColor[x-1][y] = currentColor[x][y]
              alreadyInCurrent[x-1][y] = True
            elif(x == 0 and landFall[imgx-1][y] != True and alreadyInCurrent[imgx-1][y] != True):
              currentMovement.append([imgx-1,y])
              currentColor[imgx-1][y] = currentColor[x][y]
              alreadyInCurrent[imgx-1][y] = True
            if(x != imgx-1 and landFall[x+1][y] != True and alreadyInCurrent[x+1][y] != True):
              currentMovement.append([x+1,y])
              currentColor[x+1][y] = currentColor[x][y]
              alreadyInCurrent[x+1][y] = True
            elif(x == imgx-1 and landFall[0][y] != True and alreadyInCurrent[0][y] != True):
              currentMovement.append([0,y])
              currentColor[0][y] = currentColor[x][y]
              alreadyInCurrent[0][y] = True
            if(x != imgx-1 and y != imgy-1 and landFall[x+1][y+1] != True and alreadyInCurrent[x+1][y+1] != True and (y+1 != yHalf - westWinds or y+1 != yHalf + westWinds)):
              currentMovement.append([x+1,y+1])
              currentColor[x+1][y+1] = currentColor[x][y]
              alreadyInCurrent[x+1][y+1] = True
            if(x != 0 and y != 0 and landFall[x-1][y-1] != True and alreadyInCurrent[x-1][y-1] != True and (y-1 != yHalf - westWinds or y-1 != yHalf + westWinds)):
              currentMovement.append([x-1,y-1])
              currentColor[x-1][y-1] = currentColor[x][y]
              alreadyInCurrent[x-1][y-1] = True
            if(x != imgx-1 and y != 0 and landFall[x+1][y-1] != True and alreadyInCurrent[x+1][y-1] != True and (y-1 != yHalf - westWinds or y-1 != yHalf + westWinds)):
              currentMovement.append([x+1,y-1])
              currentColor[x+1][y-1] = currentColor[x][y]
              alreadyInCurrent[x+1][y-1] = True
            if(x != 0 and y != imgy-1 and landFall[x-1][y+1] != True and alreadyInCurrent[x-1][y+1] != True and (y+1 != yHalf - westWinds or y+1 != yHalf + westWinds)):
              currentMovement.append([x-1,y+1])
              currentColor[x-1][y+1] = currentColor[x][y]
              alreadyInCurrent[x-1][y+1] = True
        i += 1
    image.save("Ocean_Currents.png", "PNG")
    print("Currents Generated")
wid = 500
hei = 250
shape = (wid,hei)
image = Image.new("RGB",(wid,hei))
world = generateNoise(wid,hei,100,2,.2)
world2 = np.zeros(image.size)
putpixel = image.putpixel
imgx, imgy = image.size
coHasBeenVisited = np.zeros(image.size)
tectMovementDirection = np.zeros(image.size)
landOrOceanTectPlate = np.zeros(image.size)
heightMap = np.zeros(image.size)
hasBeenVisited = np.zeros(image.size)
tectNum = np.zeros(image.size)
inQueue = np.zeros(image.size)
coOrigin = np.zeros(image.size)
increase = np.zeros(image.size)
decrease = np.zeros(image.size)
convergeComplete = np.zeros(image.size)
newCurr = np.zeros(image.size)
terrainOrigin = np.zeros(image.size)
terrainTotal = np.zeros(image.size)
prevHeight = np.zeros(image.size)
landOrigin = np.zeros(image.size)
landTotal = np.zeros(image.size)
terrainFall = np.zeros(image.size)
alreadyInCurrent = np.zeros(image.size)
currentColor = np.zeros(image.size)
landFall = np.zeros(image.size)
borderShelf = np.zeros(image.size)
continental = False
oceanicPlate = True
tectMovementList = [1.0,2.0,3.0,4.0]
Left = 1.0
Right = 2.0
Up = 3.0
Down = 4.0
lowElev = -0.1
midElev = -0.05
highElev = -0.01
highElevContinental = 0.01
convergeLandNum = 1
convergeOceanNum = 2
divergeNum = 3
transformNum = 4
convergeOtherNum = 5
queueBord = []
conCon = []
conOcean = []
oceanCon = []
oceanOcean = []
converge = []
diverge = []
transform = []
currentMovement = []
landList = []
terrainList = []
tectMovement = []
isOceanic = []
inputTotalTect = 0
inputLandTect = 0
inputRiversNum = 0
inputMountainNum = 0
invalidNum = -99
while True:
    print("Enter number of Tect Plates (MAX: 20, MIN: 2): ")
    inputTotalTect = input()
    try:
        int(inputTotalTect)
    except ValueError:
        print("Please enter a valid number")
    if int(inputTotalTect) < 2 or int(inputTotalTect) > 20:
        print("The number enter was invalid. Please try again: ")
    else:
        break
while True:
    print("Enter the number of those " +str(inputTotalTect)+ " total plates that will be land plates: ")
    inputLandTect = input()
    try:
        int(inputLandTect)
    except ValueError:
        print("Please enter a valid number")
    if int(inputLandTect) >= int(inputTotalTect) or int(inputLandTect) < 1:
        print("The number of land plates entered was invalid. Please try again: ")
    else:
        break
while True:
    print("Enter number of rivers you want on land (MAX: 20, MIN: 0): ")
    inputRiversNum = input()
    try:
        int(inputRiversNum)
    except ValueError:
        print("Please enter a valid number")
    if  0 > int(inputRiversNum) or int(inputRiversNum) > 20:
        print("The number of land plates entered was invalid. Please try again: ")
    else:
        break
while True:
    print("Enter number of mountains you want on land (MAX: 20, MIN: 0): ")
    inputMountainNum = input()
    try:
        int(inputMountainNum)
    except ValueError:
        print("Please enter a valid number")
    if int(inputMountainNum) > 20 or int(inputMountainNum) < 0:
        print("The number of land plates entered was invalid. Please try again: ")
    else:
        break
generate_voronoi_diagram(wid,hei,int(inputTotalTect))
rest()
print("Window Generated")
pygame.init()
gameDisplay = pygame.display.set_mode((800, 270))
howieImg_front = pygame.image.load('Basic.PNG').convert_alpha()
howieImg_back = pygame.image.load('Rivers.PNG').convert_alpha()
howieImg_left = pygame.image.load('Tect_With_Fault_Bord.PNG').convert_alpha()
howieImg_right = pygame.image.load('Ocean_Currents.PNG').convert_alpha()

# Assign the current howie image to this variable.
howieImg = howieImg_front

x = 10
y = 10
clock = pygame.time.Clock()
click = 0
gameExit = False
text = ""
text2 = ""
num = 0
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            rectangle = pygame.Rect(10,10,500,250)
            pos = pygame.mouse.get_pos()
            click = rectangle.collidepoint(pos)    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                howieImg = howieImg_back
                pygame.init()
                pygame.display.set_caption("River Map")
                text = "River Map"
                num = 1
            if event.key == pygame.K_s:
                howieImg = howieImg_front
                pygame.init()
                pygame.display.set_caption("Height Map")
                text = "Height Map"
                num = 2
            if event.key == pygame.K_a:
                howieImg = howieImg_left
                pygame.init()
                pygame.display.set_caption("Tectonic Plate Map")
                text = "Tectonic Plate Map"
                num = 3
            if event.key == pygame.K_d:
                howieImg = howieImg_right
                pygame.init()
                pygame.display.set_caption("Ocean Current Map")
                text = "Ocean Current Map"
                num = 4

    gameDisplay.fill((255, 255, 255))
    # Just blit the current `howieImg`.
    gameDisplay.blit(howieImg, (x, y))
    col = [0,0,255]
    if click == 1:
        if(num == 1):
            text = "River Map"
            text2 = "Position: " +str(pos)
        elif(num == 2):
            text = "Height Map"
            text2 = "Position: " +str(pos)
        elif(num == 3):
            text = "Tectonic Plate Map"
            text2 = "Position: " +str(pos)
        elif(num == 4):
            text = "Ocean Current Map"
            text2 = "Position: " +str(pos)
        gameDisplay.fill(col,((pos[0],pos[1]-1),(1,1)))
        gameDisplay.fill(col,((pos[0]-1,pos[1]),(1,1)))
        gameDisplay.fill(col,((pos[0],pos[1]+1),(1,1)))
        gameDisplay.fill(col,((pos[0]+1,pos[1]),(1,1)))
        gameDisplay.fill(col,((pos[0]-1,pos[1]-1),(1,1)))
        gameDisplay.fill(col,((pos[0]+1,pos[1]+1),(1,1)))
        gameDisplay.fill(col,((pos[0]+1,pos[1]-1),(1,1)))
        gameDisplay.fill(col,((pos[0]-1,pos[1]+1),(1,1)))
    pygame.font.init() 
    myfont = pygame.font.SysFont(None, 20)
    textsurface1 = myfont.render(text, True, (0, 0, 0))
    gameDisplay.blit(textsurface1,(520,0))
    textsurface2 = myfont.render(text2, True, (0, 0, 0))
    gameDisplay.blit(textsurface2,(520,40))
    pygame.display.update()
    clock.tick(60)

pygame.quit()

