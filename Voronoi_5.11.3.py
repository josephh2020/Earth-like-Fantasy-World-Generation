from PIL import Image
import random
import math
import numpy as np
import noise
def addTectBordToFaultList(x,y,nx,ny):
    currTectType = tectType[x][y]
    nextToTectType = tectType[nx][ny]
    if(currTectType == continental):
        if (nextToTectType == continental):
            conCon.append([x,y])
            heightMap[x][y] = -99
        elif(nextToTectType != continental):
            conOcean.append([x,y])
            coMarked[x][y] = True
            coOrigin[x][y] = True
    elif(currTectType != continental):
        if (nextToTectType == continental):
            oceanCon.append([x,y])
        elif(nextToTectType != continental):
            oceanOcean.append([x,y])
def SearchThroughBordList():
    i = 0
    for j in queueBord:
        x = queueBord[i][0]
        y = queueBord[i][1]
        i += 1
        if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):
            addTectBordToFaultList(x,y,x,y-1)
        if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):
            addTectBordToFaultList(x,y,x,y+1)
        if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):
            addTectBordToFaultList(x,y,x-1,y)
        if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):
            addTectBordToFaultList(x,y,x+1,y)
def initialBordSetUp(x,y,nx,ny,listTest,other):
    queueBord.append([x,y])
    currTectType = tectType[x][y]
    nextToTectType = tectType[nx][ny]
    ori[x][y] = True
    inQ[x][y] = True
    if(currTectType == continental):
        if (nextToTectType == continental):
            conCon.append([x,y])
        elif(nextToTectType != continental):
            conOcean.append([x,y])
    elif(currTectType != continental):
        if (nextToTectType == continental):
            oceanCon.append([x,y])
        elif(nextToTectType != continental):
            oceanOcean.append([x,y])
    if((moveType[x][y] == listTest[0] and moveType[nx][ny] == other[0])):
      putpixel((x, y),(255,0,0))
      if((currTectType == continental and nextToTectType == continental) or
         (currTectType == continental and nextToTectType != continental)):
        heightMap[x][y] = highElevContinental
        converge.append((x,y))
        increase[x][y] = .8
        marked[x][y] = 1
      elif(currTectType != continental):
        converge.append((x,y))
        increase[x][y] = .8
        heightMap[x][y] = highElev
        marked[x][y] = 2
    elif((moveType[x][y] == listTest[1] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[2] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[3] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[1] and moveType[nx][ny] == other[3]) or
         (moveType[x][y] == listTest[1] and moveType[nx][ny] == other[4]) or
         (moveType[x][y] == listTest[0] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[1] and moveType[nx][ny] == other[0])):
      putpixel((x, y),(0,0,255))
      diverge.append((x,y))
      decrease[x][y] = -.8
      heightMap[x][y] = lowElev
      marked[x][y] = 3
    elif((moveType[x][y] == listTest[4] and moveType[nx][ny] == other[2]) or
         (moveType[x][y] == listTest[5] and moveType[nx][ny] == other[2]) or
         (moveType[x][y] == listTest[0] and moveType[nx][ny] == other[3]) or
         (moveType[x][y] == listTest[0] and moveType[nx][ny] == other[4])):
      putpixel((x,y),(128,0,128))
      converge.append((x,y))
      increase[x][y] = .8
      marked[x][y] = 5
      heightMap[x][y] = highElev
    elif((moveType[x][y] == listTest[6] and moveType[nx][ny] == other[3]) or
        (moveType[x][y] == listTest[6] and moveType[nx][ny] == other[4]) or
        (moveType[x][y] == listTest[7] and moveType[nx][ny] == other[4]) or
        (moveType[x][y] == listTest[7] and moveType[nx][ny] == other[3])):
      putpixel((x,y),(0,255,0))
      transform.append((x,y))
      marked[x][y] = 4
      heightMap[x][y] = midElev
    else:
        marked[x][y] = 6
        putpixel((x,y),(255,255,255))
        heightMap[x][y] = midElev
def giveTectBordInfoDependingOnNeighbor(x,y,prevX,prevY):
    if(marked[prevX][prevY] == 1):
        converge.append((x,y))
        increase[x][y] = .8
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElevContinental
        marked[x][y] = 1
    elif(marked[prevX][prevY] == 2):
        increase[x][y] = .8
        converge.append((x,y))
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElev
        marked[x][y] = 2
    elif(marked[prevX][prevY] == 3):
        diverge.append((x,y))
        decrease[x][y] = -.8
        putpixel((x, y),(0,0,255))
        heightMap[x][y] = lowElev
        marked[x][y] = 3
    elif(marked[prevX][prevY] == 4):
        transform.append((x,y))
        putpixel((x, y),(0,255,0))
        heightMap[x][y] = midElev
        marked[x][y] = 4
    elif(marked[prevX][prevY] == 5):
        converge.append((x,y))
        increase[x][y] = .8
        putpixel((x, y),(128,0,128))
        heightMap[x][y] = highElev
        marked[x][y] = 5
    elif(marked[prevX][prevY] == 6):
        putpixel((x, y),(255,255,255))
        heightMap[x][y] = midElev
        marked[x][y] = 6
def goThroughRemainingNoInfoBord(bord):
    i = 0
    newBord = []
    for j in bord:
        x = bord[i][0]
        y = bord[i][1]
        if( y != 0 and (heightMap[x][y-1] != -99 )
        and (tectNum[x][y-1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x,y-1)
        elif( y != imgy-1 and (heightMap[x][y+1] != -99 )
            and (tectNum[x][y+1] == tectNum[x][y] )):
            giveTectBordInfoDependingOnNeighbor(x,y,x,y+1)
        elif( x != 0 and (heightMap[x-1][y] != -99)
            and (tectNum[x-1][y] == tectNum[x][y] )):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y)
        elif( x != imgx-1 and(heightMap[x+1][y] != -99)
            and (tectNum[x+1][y] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y)
        elif(x != imgx-1 and y != imgy-1 and
             heightMap[x+1][y+1] != -99 and
             (tectNum[x+1][y+1] == tectNum[x][y]) ):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y+1)
        elif(x != 0 and y != 0 and
             heightMap[x-1][y-1] != -99 and
             (tectNum[x-1][y-1] == tectNum[x][y]) ):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y-1)
        elif(x != imgx-1 and
             y != 0 and
             heightMap[x+1][y-1] != -99 and
             (tectNum[x+1][y-1] == tectNum[x][y])):
            giveTectBordInfoDependingOnNeighbor(x,y,x+1,y-1)
        elif(x != 0 and
             y != imgy-1 and
             heightMap[x-1][y+1] != -99 and
             (tectNum[x-1][y+1] == tectNum[x][y]) ):
            giveTectBordInfoDependingOnNeighbor(x,y,x-1,y+1)
        if(heightMap[x][y] == -99):
            putpixel((x, y),(255,165,0))
            newBord.append([x,y])
        else:
            queueBord.append([x,y])
            ori[x][y] = True
        i += 1
    return newBord
def generateNoise(width,height,octave):
    scale       = 100 # Number that determines at what distance to view the noisemap
    octaves     = octave # the number of levels of detail you want you perlin noise to have
    persistence = 0.2 # number that determines how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2.0 # number that determines how much each octave contributes to the overall shape (adjusts amplitude)
    for x in range(width):
        for y in range(height):
            world_test[x][y] = noise.pnoise2(x/100, 
                                        y/100, 
                                        octaves     = octaves, 
                                        persistence = persistence, 
                                        lacunarity  = lacunarity, 
                                        repeatx     = width, 
                                        repeaty     = height, 
                                        base        = 0)
    return world_test
def generate_voronoi_diagram(width, height, num_cells):
    for i in range(num_cells):
            nx.append(random.randrange(imgx))
            ny.append(random.randrange(imgy))
            nx2.append(nx[i]+width)
            ny2.append(ny[i])
            nx3.append(nx[i]-width)
            ny3.append(ny[i])
            t = random.randrange(2)
            if t == 0:
                isOceanic.append(True)
                red = random.randrange(150)
                nr.append(red)
                ng.append(red+50)
                nb.append(red+100)
            else:
                isOceanic.append(False)
                green = random.randrange(150,256)
                nr.append(green)
                ng.append(green-50)
                nb.append(green-100)
            tectMovement.append(random.choice(tectMovementList))
    for y in range(int(imgy)):
        for x in range(int(imgx)):
            dmin = math.hypot(imgx-1, imgy-1)
            j = -1
            for i in range(num_cells):
                    d = math.hypot((nx[i]-x), (ny[i]-y))
                    if d < dmin:
                        dmin = d
                        j = i
                    d = math.hypot((nx3[i]-x), (ny3[i]-y))
                    if d < dmin:
                        dmin = d
                        j = i
                    d = math.hypot((nx2[i]-x), (ny2[i]-y))
                    if d < dmin:
                        dmin = d
                        j = i
            tectNum[x][y] = j+1
            tectType[x][y] = isOceanic[j]
            if(tectType[x][y] == False):
                high[x][y] = 255
            else:
                high[x][y] = 0
            moveType[x][y] = tectMovement[j]
            putpixel((x, y), (nr[j], ng[j], nb[j]))
    image.save("Tect_Without_Fault_Bord.png", "PNG")
##    image.show()   
def rest():
    remainingBord = []
    for x in range(imgx):
        for y in range(imgy):
          num = 0
          if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):
             num += 1
          if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):
             num += 2
          if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):
             num += 4
          if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):
             num += 8
          if(num == 1):
              listTest = [Up,Down,Left,Right,Right,Left,Right,Left]
              other = [Down,Up,Down,Left,Right]
              initialBordSetUp(x,y,x,y-1,listTest,other)
          elif( num == 2):
              listTest = [Down,Up,Left,Right,Right,Left,Left,Right]
              other = [Up,Down,Up,Right,Left]
              initialBordSetUp(x,y,x,y+1,listTest,other)              
          elif( num == 4):
              listTest = [Left,Right,Up,Down,Up,Down,Up,Down]
              other = [Right,Left,Right,Down,Up]
              initialBordSetUp(x,y,x-1,y,listTest,other)
          elif( num == 8):
              listTest = [Right,Left,Up,Down,Up,Down,Up,Down]
              other = [Left,Right,Left,Down,Up]
              initialBordSetUp(x,y,x+1,y,listTest,other)
          else:
              if(num > 0):
                remainingBord.append([x,y])
              heightMap[x][y] = -99    
    while True:
        remainingBord = goThroughRemainingNoInfoBord(remainingBord)
        if len(remainingBord) == 0:
            break
    image.save("Tect_With_Fault_Bord.png", "PNG")
##    image.show()
    i = 0
    SearchThroughBordList()
    for j in range(len(converge)):
        currX = converge[i][0]
        currY = converge[i][1]
        if(tectType[currX][currY] == True):
            heightMap[currX][currY] = -99
        i += 1
    i = 0
    for j in range(len(diverge)):
        currX = diverge[i][0]
        currY = diverge[i][1]
        if(tectType[currX][currY] == True):
            heightMap[currX][currY] = -99
        i += 1
    i = 0
    for j in range(len(transform)):
        currX = transform[i][0]
        currY = transform[i][1]
        if(tectType[currX][currY] == True):
            heightMap[currX][currY] = -99
        i += 1
    i = 0
    for j in conOcean:
        currX = conOcean[i][0]
        currY = conOcean[i][1]
        elev = 0
        num = 0
        if(coOrigin[currX][currY] != True):
          if(currY != 0 and heightMap[currX][currY-1] != -99):
              elev += heightMap[currX][currY-1]
              num += 1
          if(currY != imgy-1 and heightMap[currX][currY+1] != -99):
              elev += heightMap[currX][currY+1]
              num += 1
          if(currX != 0 and heightMap[currX-1][currY] != -99 ):
              elev += heightMap[currX-1][currY]
              num += 1
          elif(currX == 0 and heightMap[imgx-1][currY] != -99 ):
              elev += heightMap[imgx-1][currY]
              num += 1
          if(currX != imgx-1 and heightMap[currX+1][currY] != -99 ):
              elev += heightMap[currX+1][currY]
              num += 1
          elif(currX == imgx-1 and heightMap[0][currY] != -99 ):
              elev += heightMap[0][currY]
              num += 1
          if(currX != imgx-1 and currY != imgy-1 and heightMap[currX+1][currY+1] != -99 ):
              elev += heightMap[currX+1][currY+1]
              num += 1
          if(currX != 0 and currY != 0 and heightMap[currX-1][currY-1] != -99 ):
              elev += heightMap[currX-1][currY-1]
              num += 1
          if(currX != imgx-1 and currY != 0 and heightMap[currX+1][currY-1] != -99 ):
              elev += heightMap[currX+1][currY-1]
              num += 1
          if(currX != 0 and currY != imgy-1 and heightMap[currX-1][currY+1] != -99 ):
              elev += heightMap[currX-1][currY+1]
              num += 1    
          ran = .005
          if(num != 0):
              if(tectType[currX][currY] == False):
                  if((elev/num) < 0.0):
                    heightMap[currX][currY] = (elev/num)+ 0.0025
                  else:
                    heightMap[currX][currY] = (elev/num)+ ran
              elif(tectType[currX][currY] == True):
                  if((elev/num) > -.30):
                      heightMap[currX][currY] = (elev/num) - 0.025
                  else:
                      heightMap[currX][currY] = (elev/num) - 0.01
            
        if(heightMap[currX][currY] < 0.99):
          if(currY != 0 and (coMarked[currX][currY-1] != True)):
              conOcean.append([currX,currY-1])
              coMarked[currX][currY-1] = True            
          if(currY != imgy-1 and (coMarked[currX][currY+1] != True)):
              conOcean.append([currX,currY+1])
              coMarked[currX][currY+1] = True            
          if(currX != 0 and (coMarked[currX-1][currY] != True)):
              conOcean.append([currX-1,currY])
              coMarked[currX-1][currY] = True
          elif(currX == 0 and(coMarked[imgx-1][currY] != True)):
              conOcean.append([imgx-1,currY])
              coMarked[imgx-1][currY] = True
          if(currX != imgx-1 and (coMarked[currX+1][currY] != True)):
              conOcean.append([currX+1,currY])
              coMarked[currX+1][currY] = True
          elif(currX == imgx-1 and (coMarked[0][currY] != True)):
              conOcean.append([0,currY])
              coMarked[0][currY] = True 
          if(currX != imgx-1 and currY != imgy-1 and coMarked[currX+1][currY+1] != True):
              conOcean.append([currX+1,currY+1])
              coMarked[currX+1][currY+1] = True
          if(currX != 0 and currY != 0 and coMarked[currX-1][currY-1] != True):
              conOcean.append([currX-1,currY-1])
              coMarked[currX-1][currY-1] = True
          if(currX != imgx-1 and currY != 0 and coMarked[currX+1][currY-1] != True):
              conOcean.append([currX+1,currY-1])
              coMarked[currX+1][currY-1] = True
          if(currX != 0 and currY != imgy-1 and coMarked[currX-1][currY+1] != True):
              conOcean.append([currX-1,currY+1])
              coMarked[currX-1][currY+1] = True
        i += 1
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] <= -0.73:
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

    for x in range(imgx):
        for y in range(imgy):
            if(heightMap[x][y] >= 0.0):
                heightMap[x][y] = 0.0
                landTotal[x][y] = True
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] <= -0.75:
                col = (122,170,219)
            elif heightMap[x][y] <= -0.01:
                col = (168,211,241)
            elif heightMap[x][y] < 0.01:
                col = (217,236,255)
                if(y != 0 and heightMap[x][y-1] < 0.0):
                  borderShelf[x][y-1] = True
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
    for x in range(imgx):
        for y in range(imgy):
            if(landTotal[x][y] == True):
                heightMap[x][y] = -99
    i = 0
    for j in range(len(landList)):
        currX = landList[i][0]
        currY = landList[i][1]
        landOrigin[currX][currY] = True
        heightMap[currX][currY] = 0.0
        i += 1
    i = 0
    scale       = 100 # Number that s at what distance to view the noisemap
    octaves     = 12 # the number of levels of detail you want you perlin noise to have
    persistence = .5 # number that s how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2 # number that s how much each octave contributes to the overall shape (adjusts amplitude)
    for x in range(500):
        for y in range(250):
            world2[x][y] += noise.snoise2(x/scale, 
                                        y/scale, 
                                        octaves     = octaves, 
                                        persistence = persistence, 
                                        lacunarity  = lacunarity, 
                                        repeatx     = wid, 
                                        repeaty     = hei, 
                                        base        = 0)
    for j in landList:
        currX = landList[i][0]
        currY = landList[i][1]
        elev = 0
        num = 0
        if(landOrigin[currX][currY] != True):
            if(currY != 0 and heightMap[currX][currY-1] != -99):
              elev += heightMap[currX][currY-1]
              num += 1
            if(currY != imgy-1 and heightMap[currX][currY+1] != -99):
              elev += heightMap[currX][currY+1]
              num += 1
            if(currX != 0 and heightMap[currX-1][currY] != -99 ):
              elev += heightMap[currX-1][currY]
              num += 1
            elif(currX == 0 and heightMap[imgx-1][currY] != -99 ):
              elev += heightMap[imgx-1][currY]
              num += 1
            if(currX != imgx-1 and heightMap[currX+1][currY] != -99 ):
              elev += heightMap[currX+1][currY]
              num += 1
            elif(currX == imgx-1 and heightMap[0][currY] != -99 ):
              elev += heightMap[0][currY]
              num += 1
            if(currX != imgx-1 and currY != imgy-1 and heightMap[currX+1][currY+1] != -99 ):
              elev += heightMap[currX+1][currY+1]
              num += 1
            if(currX != 0 and currY != 0 and heightMap[currX-1][currY-1] != -99 ):
              elev += heightMap[currX-1][currY-1]
              num += 1
            if(currX != imgx-1 and currY != 0 and heightMap[currX+1][currY-1] != -99 ):
              elev += heightMap[currX+1][currY-1]
              num += 1
            if(currX != 0 and currY != imgy-1 and heightMap[currX-1][currY+1] != -99 ):
              elev += heightMap[currX-1][currY+1]
              num += 1
            ran = .02
            if(num != 0):
                heightMap[currX][currY] = (elev/num)+ ran
        if(currY != 0 and landTotal[currX,currY-1] == True and (landFall[currX][currY-1] != True)):
              landList.append([currX,currY-1])
              landFall[currX][currY-1] = True            
        if(currY != imgy-1 and landTotal[currX][currY+1] == True and (landFall[currX][currY+1] != True)):
              landList.append([currX,currY+1])
              landFall[currX][currY+1] = True            
        if(currX != 0 and landTotal[currX-1][currY] == True and (landFall[currX-1][currY] != True)):
              landList.append([currX-1,currY])
              landFall[currX-1][currY] = True
        elif(currX == 0 and landTotal[imgx-1][currY] == True and (landFall[imgx-1][currY] != True)):
              landList.append([imgx-1,currY])
              landFall[imgx-1][currY] = True
        if(currX != imgx-1 and landTotal[currX+1][currY] == True and (landFall[currX+1][currY] != True)):
              landList.append([currX+1,currY])
              landFall[currX+1][currY] = True
        elif(currX == imgx-1 and landTotal[0][currY] == True and (landFall[0][currY] != True)):
              landList.append([0,currY])
              landFall[0][currY] = True 
        if(currX != imgx-1 and currY != imgy-1 and landTotal[currX+1][currY+1] == True and landFall[currX+1][currY+1] != True):
              landList.append([currX+1,currY+1])
              landFall[currX+1][currY+1] = True
        if(currX != 0 and currY != 0 and landTotal[currX-1][currY-1] == True and landFall[currX-1][currY-1] != True):
              landList.append([currX-1,currY-1])
              landFall[currX-1][currY-1] = True
        if(currX != imgx-1 and currY != 0 and landTotal[currX+1][currY-1] == True and landFall[currX+1][currY-1] != True):
              landList.append([currX+1,currY-1])
              landFall[currX+1][currY-1] = True
        if(currX != 0 and currY != imgy-1 and landTotal[currX-1][currY+1] == True and landFall[currX-1][currY+1] != True):
              landList.append([currX-1,currY+1])
              landFall[currX-1][currY+1] = True
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

    for x in range(imgx):
        for y in range(imgy):
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
        for x in range(imgx):
            if heightMap[x][y] <= -0.75:
                col = (122,170,219)
                putpixel((x,y), col)
            if landTotal[x][y] == True:
                if heightMap[x][y] < 0.01:
                    col = (217,236,255)
                elif heightMap[x][y] <= 0.0667:
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
    for x in range(imgx):
        for y in range(imgy):
            if(terrainTotal[x][y] == True):
                heightMap[x][y] = -99
    i = 0
    for j in range(len(terrainList)):
        currX = terrainList[i][0]
        currY = terrainList[i][1]
        terrainOrigin[currX][currY] = True
        heightMap[currX][currY] = -0.01
        i += 1
    i = 0
    scale       = 100 # Number that s at what distance to view the noisemap
    octaves     = 10 # the number of levels of detail you want you perlin noise to have
    persistence = 0.7 # number that s how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2.0 # number that s how much each octave contributes to the overall shape (adjusts amplitude)
    for x in range(500):
        for y in range(250):
            world2[x][y] = noise.pnoise2(x/100, 
                                        y/100, 
                                        octaves     = octaves, 
                                        persistence = persistence, 
                                        lacunarity  = lacunarity, 
                                        repeatx     = wid, 
                                        repeaty     = hei, 
                                        base        = 0)
    for j in terrainList:
        currX = terrainList[i][0]
        currY = terrainList[i][1]
        elev = 0
        num = 0
        if(terrainOrigin[currX][currY] != True):
            if(currY != 0 and heightMap[currX][currY-1] != -99):
              elev += heightMap[currX][currY-1]
              num += 1
            if(currY != imgy-1 and heightMap[currX][currY+1] != -99):
              elev += heightMap[currX][currY+1]
              num += 1
            if(currX != 0 and heightMap[currX-1][currY] != -99 ):
              elev += heightMap[currX-1][currY]
              num += 1
            elif(currX == 0 and heightMap[imgx-1][currY] != -99 ):
              elev += heightMap[imgx-1][currY]
              num += 1
            if(currX != imgx-1 and heightMap[currX+1][currY] != -99 ):
              elev += heightMap[currX+1][currY]
              num += 1
            elif(currX == imgx-1 and heightMap[0][currY] != -99 ):
              elev += heightMap[0][currY]
              num += 1
            if(currX != imgx-1 and currY != imgy-1 and heightMap[currX+1][currY+1] != -99 ):
              elev += heightMap[currX+1][currY+1]
              num += 1
            if(currX != 0 and currY != 0 and heightMap[currX-1][currY-1] != -99 ):
              elev += heightMap[currX-1][currY-1]
              num += 1
            if(currX != imgx-1 and currY != 0 and heightMap[currX+1][currY-1] != -99 ):
              elev += heightMap[currX+1][currY-1]
              num += 1
            if(currX != 0 and currY != imgy-1 and heightMap[currX-1][currY+1] != -99 ):
              elev += heightMap[currX-1][currY+1]
              num += 1
            ran = .0025
            if(num != 0):
                heightMap[currX][currY] = (elev/num)+ ran
        if(currY != 0 and terrainTotal[currX,currY-1] == True and (terrainFall[currX][currY-1] != True)):
              terrainList.append([currX,currY-1])
              terrainFall[currX][currY-1] = True            
        if(currY != imgy-1 and terrainTotal[currX][currY+1] == True and (terrainFall[currX][currY+1] != True)):
              terrainList.append([currX,currY+1])
              terrainFall[currX][currY+1] = True            
        if(currX != 0 and terrainTotal[currX-1][currY] == True and (terrainFall[currX-1][currY] != True)):
              terrainList.append([currX-1,currY])
              terrainFall[currX-1][currY] = True
        elif(currX == 0 and terrainTotal[imgx-1][currY] == True and (terrainFall[imgx-1][currY] != True)):
              terrainList.append([imgx-1,currY])
              terrainFall[imgx-1][currY] = True
        if(currX != imgx-1 and terrainTotal[currX+1][currY] == True and (terrainFall[currX+1][currY] != True)):
              terrainList.append([currX+1,currY])
              terrainFall[currX+1][currY] = True
        elif(currX == imgx-1 and terrainTotal[0][currY] == True and (terrainFall[0][currY] != True)):
              terrainList.append([0,currY])
              terrainFall[0][currY] = True 
        if(currX != imgx-1 and currY != imgy-1 and terrainTotal[currX+1][currY+1] == True and terrainFall[currX+1][currY+1] != True):
              terrainList.append([currX+1,currY+1])
              terrainFall[currX+1][currY+1] = True
        if(currX != 0 and currY != 0 and terrainTotal[currX-1][currY-1] == True and terrainFall[currX-1][currY-1] != True):
              terrainList.append([currX-1,currY-1])
              terrainFall[currX-1][currY-1] = True
        if(currX != imgx-1 and currY != 0 and terrainTotal[currX+1][currY-1] == True and terrainFall[currX+1][currY-1] != True):
              terrainList.append([currX+1,currY-1])
              terrainFall[currX+1][currY-1] = True
        if(currX != 0 and currY != imgy-1 and terrainTotal[currX-1][currY+1] == True and terrainFall[currX-1][currY+1] != True):
              terrainList.append([currX-1,currY+1])
              terrainFall[currX-1][currY+1] = True
        i += 1
    i = 0
    riverList = []
    riverTrue = np.zeros(image.size)
    for i in range(40):
        riverStart = random.choice(terrainList)
        riverList.append(riverStart)
    i = 0
    for j in riverList:
        lowestTerrain = 99
        currX = riverList[i][0]
        currY = riverList[i][1]
        if i < 40:
            putpixel((currX,currY),(255,0,0))
        else:
            putpixel((currX,currY),(0,0,255))
        lowestX = 9
        lowestY = 9
        riverTrue[currX][currY] = True
        if(currY != 0
           and heightMap[currX][currY-1] <= lowestTerrain):
              lowestX = currX
              lowestY = currY-1
              lowestTerrain = heightMap[currX][currY-1]            
        if(currY != imgy-1
           and heightMap[currX][currY+1] <= lowestTerrain ):
              lowestX = currX
              lowestY = currY+1
              lowestTerrain = heightMap[currX][currY+1]            
        if(currX != 0
           and heightMap[currX-1][currY] <= lowestTerrain ):
              lowestX = currX-1
              lowestY = currY
              lowestTerrain = heightMap[currX-1][currY]
        elif(currX == 0
           and heightMap[imgx-1][currY] <= lowestTerrain):
              lowestX = imgx-1
              lowestY = currY
              lowestTerrain = heightMap[imgx-1][currY]
        if(currX != imgx-1
           and heightMap[currX+1][currY] <= lowestTerrain ):
              lowestX = currX+1
              lowestY = currY
              lowestTerrain = heightMap[currX+1][currY]
        elif(currX == imgx-1
           and heightMap[0][currY] <= lowestTerrain ):
              lowestX = 0
              lowestY = currY
              lowestTerrain = heightMap[0][currY]
        if(currX != imgx-1 and currY != imgy-1
           and heightMap[currX+1][currY+1] <= lowestTerrain ):
              lowestX = currX+1
              lowestY = currY+1
              lowestTerrain = heightMap[currX+1][currY+1]
        if(currX != 0 and currY != 0
           and heightMap[currX-1][currY-1] <= lowestTerrain):
              lowestX = currX-1
              lowestY = currY-1
              lowestTerrain = heightMap[currX-1][currY-1]
        if(currX != imgx-1 and currY != 0
           and heightMap[currX+1][currY-1] <= lowestTerrain):
              lowestX = currX+1
              lowestY = currY-1
              lowestTerrain = heightMap[currX+1][currY-1] 
        if(currX != 0 and currY != imgy-1
           and heightMap[currX-1][currY+1] <= lowestTerrain):
              lowestX = currX-1
              lowestY = currY+1
              lowestTerrain = heightMap[currX-1][currY+1]
        if(lowestTerrain != 99 and heightMap[currX][currY] >= -0.01 and riverTrue[lowestX][lowestY] != True):
            riverList.append([lowestX,lowestY])
        i += 1
    image.save("Rivers.png", "PNG")
##    image.show()
    convergeComplete = np.zeros(image.size)
    i = 0
    for j in converge:
        currX = converge[i][0]
        currY = converge[i][1]
        convergeComplete[currX][currY] = True
        i += 1
        if(convergeComplete[currX][currY] != True and (landFall[currX][currY] == True and terrainFall[currX][currY] == False)
           or (terrainOrigin[currX][currY] == True)):
            currElev = increase[currX][currY]
            heightMap[currX][currY] += 0
        else:
            ran = random.uniform(.80,.95)
            if(ran <= 0):
                ran = 0
            currElev = increase[currX][currY] * ran
            heightMap[currX][currY]  = currElev
        if(currElev > .01):
            if(currY != 0 and (convergeComplete[currX][currY-1] != True or increase[currX][currY]-.05 >increase[currX][currY-1])):
                  converge.append([currX,currY-1])
                  convergeComplete[currX][currY-1] = True
                  increase[currX][currY-1] = currElev
            if(currY != imgy-1 and (convergeComplete[currX][currY+1] != True or increase[currX][currY]-.05 >increase[currX][currY+1])):
                  converge.append([currX,currY+1])
                  convergeComplete[currX][currY+1] = True
                  increase[currX][currY+1] = currElev 
            if(currX != 0  and (convergeComplete[currX-1][currY] != True or increase[currX][currY]-.05 >increase[currX-1][currY])):
                  converge.append([currX-1,currY])
                  convergeComplete[currX-1][currY] = True
                  increase[currX-1][currY] = currElev
            elif(currX == 0 and (convergeComplete[imgx-1][currY] != True or increase[currX][currY]-.05 >increase[imgx-1][currY])):
                  converge.append([imgx-1,currY])
                  convergeComplete[imgx-1][currY] = True
                  increase[imgx-1][currY] = currElev 
            if(currX != imgx-1 and (convergeComplete[currX+1][currY] != True or increase[currX][currY]-.05 >increase[currX+1][currY])):
                  converge.append([currX+1,currY])
                  convergeComplete[currX+1][currY] = True
                  increase[currX+1][currY] = currElev
            elif(currX == imgx-1 and (convergeComplete[0][currY] != True or increase[currX][currY]-.05 >increase[0][currY])):
                  converge.append([0,currY])
                  convergeComplete[0][currY] = True
                  increase[0][currY] = currElev
            if(currX != imgx-1 and currY != imgy-1 and (convergeComplete[currX+1][currY+1] != True or increase[currX][currY]-.05 >increase[currX+1][currY+1])):
                  converge.append([currX+1,currY+1])
                  convergeComplete[currX+1][currY+1] = True
                  increase[currX+1][currY+1] = currElev
            if(currX != 0 and currY != 0 and (convergeComplete[currX-1][currY-1] != True or increase[currX][currY]-.05 >increase[currX-1][currY-1])):
                  converge.append([currX-1,currY-1])
                  convergeComplete[currX-1][currY-1] = True
                  increase[currX-1][currY-1] = currElev
            if(currX != imgx-1 and currY != 0 and (convergeComplete[currX+1][currY-1] != True or increase[currX][currY]-.05 >increase[currX+1][currY-1])):
                  converge.append([currX+1,currY-1])
                  convergeComplete[currX+1][currY-1] = True
                  increase[currX+1][currY-1] = currElev
            if(currX != 0 and currY != imgy-1 and (convergeComplete[currX-1][currY+1] != True or increase[currX][currY]-.05 >increase[currX-1][currY+1])):
                  converge.append([currX-1,currY+1])
                  convergeComplete[currX-1][currY+1] = True
                  increase[currX-1][currY+1] = currElev
    for y in range(imgy):
        for x in range(imgx):
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
    convergeComplete = np.zeros(image.size)
    for j in diverge:
        convergeComplete[currX][currY] = True
        currX = diverge[i][0]
        currY = diverge[i][1]
        i += 1
        if(tectType[currX][currY] == True):
            currElev = decrease[currX][currY] +.03
            #print(str(currElev))
            heightMap[currX][currY]  = currElev
        if(currElev < -.70):
            if(currY != 0 and convergeComplete[currX][currY-1] != True):
                  diverge.append([currX,currY-1])
                  convergeComplete[currX][currY-1] = True
                  decrease[currX][currY-1] = currElev
            if(currY != imgy-1 and convergeComplete[currX][currY+1] != True):
                  diverge.append([currX,currY+1])
                  convergeComplete[currX][currY+1] = True
                  decrease[currX][currY+1] = currElev 
            if(currX != 0  and convergeComplete[currX-1][currY] != True):
                  diverge.append([currX-1,currY])
                  convergeComplete[currX-1][currY] = True
                  decrease[currX-1][currY] = currElev
            elif(currX == 0 and convergeComplete[imgx-1][currY] != True):
                  diverge.append([imgx-1,currY])
                  convergeComplete[imgx-1][currY] = True
                  decrease[imgx-1][currY] = currElev 
            if(currX != imgx-1 and convergeComplete[currX+1][currY] != True):
                  diverge.append([currX+1,currY])
                  convergeComplete[currX+1][currY] = True
                  decrease[currX+1][currY] = currElev
            elif(currX == imgx-1 and convergeComplete[0][currY] != True):
                  diverge.append([0,currY])
                  convergeComplete[0][currY] = True
                  decrease[0][currY] = currElev
            if(currX != imgx-1 and currY != imgy-1 and convergeComplete[currX+1][currY+1] != True):
                  diverge.append([currX+1,currY+1])
                  convergeComplete[currX+1][currY+1] = True
                  decrease[currX+1][currY+1] = currElev
            if(currX != 0 and currY != 0 and convergeComplete[currX-1][currY-1] != True):
                  diverge.append([currX-1,currY-1])
                  convergeComplete[currX-1][currY-1] = True
                  decrease[currX-1][currY-1] = currElev
            if(currX != imgx-1 and currY != 0 and convergeComplete[currX+1][currY-1] != True):
                  diverge.append([currX+1,currY-1])
                  convergeComplete[currX+1][currY-1] = True
                  decrease[currX+1][currY-1] = currElev
            if(currX != 0 and currY != imgy-1 and convergeComplete[currX-1][currY+1] != True):
                  diverge.append([currX-1,currY+1])
                  convergeComplete[currX-1][currY+1] = True
                  decrease[currX-1][currY+1] = currElev
    i = 0
##    for j in diverge:
##        x = diverge[i][0]
##        y = diverge[i][1]
##        col = (73,119,193)
##        putpixel((x,y), col)
##        i += 1

    image.save("Rivers2.png", "PNG")
#    image.show()

    for x in range(imgx):
        for y in range(imgy):
            if(terrainTotal[x][y] == True):
              heightMap[x][y] += (heightMap[x][y]+.3)* (world2[x][y])
##            if landOrigin[x][y] == True:
##                heightMap[x][y] = 99
##                putpixel((x,y),(217,236,255))

    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if terrainTotal[x][y] == True:
                if heightMap[x][y] < 0.0667:
                    col = (0,192,96)
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
    image.save("Basic.png", "PNG")
##    image.show()

    yHalf = int(imgy/2)
    westWinds = int(yHalf * .33) # Goes eastwards
    eastWinds = int(yHalf * .66) # Goes westwards
    polarWinds = int(yHalf * .90) # Goes westwards
    for x in range(imgx):
        if(landFall[x][yHalf+5] != True):
            #if(x != 0 and landFall[x-1][yHalf+5] == True):
            putpixel((x,yHalf+5), (0,255,0))
            currentColor[x][yHalf+5] = yHalf+5
            currentMovement.append([x,yHalf+5])
            alreadyInCurrent[x][yHalf+5] = True
        if(landFall[x][yHalf-5] != True):
             #if(x != 0 and landFall[x-1][yHalf-5] == True):
            putpixel((x,yHalf-5), (0,255,0))
            currentColor[x][yHalf-5] = yHalf-5
            currentMovement.append([x,yHalf-5])
            alreadyInCurrent[x][yHalf-5] = True
    i = 0
    for j in currentMovement:
        x = currentMovement[i][0]
        y = currentMovement[i][1]
        black = (0,0,0)
        red = (255,0,0)
        blue = (0,0,255)
        newTest = False
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
        if (newTest == True):
            newCurr[x][y] = True
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
            currentColor[x][y] = yHalf
            if(x != imgx-1 and x >= 3 and landFall[x+1][y] == True and newCurr[x-2][y] == True):
                putpixel((x,y), black)
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
            if(x != imgx-1 and landFall[x+1][y] != True):
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
                currentColor[x][y] = yHalf - 5
            elif(y == yHalf + 5):
                currentColor[x][y] = yHalf + 5
            if(x != 0 and x <= imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):
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
            if(x != 0 and landFall[x-1][y] != True):
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
            if (y == yHalf - westWinds):
                currentColor[x][y] = yHalf - westWinds
            elif(y == yHalf + westWinds):
                currentColor[x][y] = yHalf + westWinds
            if(x != imgx-1 and x <= imgx - 3 and landFall[x+1][y] == True and newCurr[x-2][y] == True):
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
            if(x != imgx-1 and landFall[x+1][y] != True):
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
            if (y == yHalf - eastWinds):
                currentColor[x][y] = yHalf - eastWinds
            elif(y == yHalf + eastWinds):
                currentColor[x][y] = yHalf + eastWinds
            if(x != 0 and x <= imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):
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
            
            if(x != 0 and landFall[x-1][y] != True):
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
            if (y == yHalf - polarWinds):
                currentColor[x][y] = yHalf - polarWinds
            elif(y == yHalf + polarWinds):
                currentColor[x][y] = yHalf + polarWinds
            if(x != 0 and x < imgx - 3 and landFall[x-1][y] == True and newCurr[x+2][y] == True ):
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
            if(x != 0 and landFall[x-1][y] != True):
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
                
        if (newTest == True):
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
##    image.show()
    i = 0
##    for x in range(imgx):
##        for y in range(imgy):
##            if (alreadyInCurrent[x][y] == True):
##                putpixel((x,y),(255,165,0))
##            if (newCurr[x][y] == True):
##                putpixel((x,y),(0,255,255))
##        i += 1
##    i = 0
    for j in diverge:
        x = diverge[i][0]
        y = diverge[i][1]
        putpixel((x,y),(255,165,0))
        i += 1
    image.save("VoronoiDiagram10.png", "PNG")
 #   image.show()
wid = 500
hei = 250
shape = (wid,hei)
image = Image.new("RGB",(wid,hei))
world_test = np.zeros(image.size)
world = generateNoise(wid,hei,2)
world2 = np.zeros(image.size)
putpixel = image.putpixel
imgx, imgy = image.size
color_world = np.zeros(image.size+(3,))
coMarked = np.zeros(image.size)
moveType = np.zeros(image.size)
tectType = np.zeros(image.size)
ori = np.zeros(image.size)
heightMap = np.zeros(image.size)
marked = np.zeros(image.size)
tectNum = np.zeros(image.size)
inQ = np.zeros(image.size)
bord = []
nx = []
ny = []
nx2 = []
ny2 = []
nx3 = []
ny3 = []
nr = []
ng = []
nb = []
tectMovement = []
isOceanic = []
tectMovementList = [1.0,2.0,3.0,4.0]
queueBord = []
continental = False
Left = 1.0
Right = 2.0
Up = 3.0
Down = 4.0
lowElev = -0.1
midElev = -0.05
highElev = -0.01
highElevContinental = 0.01
high = np.zeros(image.size)
highList = []
up = np.zeros(image.size)
num_cells = 15
coOrigin = np.zeros(image.size)
increase = np.zeros(image.size)
decrease = np.zeros(image.size)
convergeComplete = np.zeros(image.size)
newCurr = np.zeros(image.size)
conCon = []
conOcean = []
oceanCon = []
oceanOcean = []
converge = []
diverge = []
transform = []
borderShelf = np.zeros(image.size)
currentMovement = []
alreadyInCurrent = np.zeros(image.size)
currentColor = np.zeros(image.size)
landFall = np.zeros(image.size)
landList = []
landOrigin = np.zeros(image.size)
landTotal = np.zeros(image.size)
terrainFall = np.zeros(image.size)
terrainList = []
terrainOrigin = np.zeros(image.size)
terrainTotal = np.zeros(image.size)
generate_voronoi_diagram(wid,hei,num_cells)
rest()

