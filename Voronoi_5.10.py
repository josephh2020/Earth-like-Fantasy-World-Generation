from PIL import Image
import random
import math
import numpy as np
import noise
def determineType(x,y,nx,ny):
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
def typesOfBord():
    i = 0
    for j in queueAll:
        x = queueAll[i][0]
        y = queueAll[i][1]
        i += 1
        if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):
            determineType(x,y,x,y-1)
        if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):
            determineType(x,y,x,y+1)
        if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):
            determineType(x,y,x-1,y)
        if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):
            determineType(x,y,x+1,y)
def randomizeNum():
    k = 1
##    lowElev = random.uniform(-.1,-.05)
##    midElev = random.uniform(-.05,-.01)
##    highElev = random.uniform(-.01,0)
##    highElevContinental = random.uniform(0.0,1.0)
def setUp(x,y,nx,ny,listTest,other):
    queueXBorder.append(x)
    queueYBorder.append(y)
    queueAll.append([x,y])
    currTectType = tectType[x][y]
    nextToTectType = tectType[nx][ny]
    ori[x][y] = True
    inQ[x][y] = True
    highList.append([x,y])
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
        marked[x][y] = 1
      elif(currTectType != continental):
        heightMap[x][y] = highElev
        marked[x][y] = 2
    elif((moveType[x][y] == listTest[1] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[2] and moveType[nx][ny] == other[1]) or
         (moveType[x][y] == listTest[3] and moveType[nx][ny] == other[1])):
      putpixel((x, y),(0,0,255))
      heightMap[x][y] = lowElev
      marked[x][y] = 3
    elif((moveType[x][y] == listTest[4] and moveType[nx][ny] == other[2]) or
         (moveType[x][y] == listTest[5] and moveType[nx][ny] == other[2])):
      putpixel((x,y),(0,255,0))
      marked[x][y] = 4
      heightMap[x][y] = midElev
    elif((moveType[x][y] == listTest[6] and moveType[x][ny] == other[3]) or
        (moveType[x][y] == listTest[7] and moveType[x][ny] == other[4])):
      putpixel((x,y),(128,0,128))
      marked[x][y] = 5
      heightMap[x][y] = midElev
    else:
      marked[x][y] = 6
      putpixel((x,y),(255,255,255))
      heightMap[x][y] = midElev
def checkMark(x,y,prevX,prevY):
    highList.append([x,y])
    if(marked[prevX][prevY] == 1):
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElevContinental
        marked[x][y] = 1
    elif(marked[prevX][prevY] == 2):
        putpixel((x, y),(255,0,0))
        heightMap[x][y] = highElev
        marked[x][y] = 2
    elif(marked[prevX][prevY] == 3):
        putpixel((x, y),(0,0,255))
        heightMap[x][y] = lowElev
        marked[x][y] = 3
    elif(marked[prevX][prevY] == 4):
        putpixel((x, y),(0,255,0))
        heightMap[x][y] = midElev
        marked[x][y] = 4
    elif(marked[prevX][prevY] == 5):
        putpixel((x, y),(128,0,128))
        heightMap[x][y] = midElev
        marked[x][y] = 5
    elif(marked[prevX][prevY] == 6):
        putpixel((x, y),(255,255,255))
        heightMap[x][y] = midElev
        marked[x][y] = 6
def cleanUp(bord):
    i = 0
    newBord = []
    for j in bord:
        x = bord[i][0]
        y = bord[i][1]
        if( y != 0 and (heightMap[x][y-1] != -99 )
        and (tectNum[x][y-1] == tectNum[x][y])):
            checkMark(x,y,x,y-1)
        elif( y != imgy-1 and (heightMap[x][y+1] != -99 )
            and (tectNum[x][y+1] == tectNum[x][y] )):
            checkMark(x,y,x,y+1)
        elif( x != 0 and (heightMap[x-1][y] != -99)
            and (tectNum[x-1][y] == tectNum[x][y] )):
            checkMark(x,y,x-1,y)
        elif( x != imgx-1 and(heightMap[x+1][y] != -99)
            and (tectNum[x+1][y] == tectNum[x][y])):
            checkMark(x,y,x+1,y)
        elif(x != imgx-1 and y != imgy-1 and
             heightMap[x+1][y+1] != -99 and
             (tectNum[x+1][y+1] == tectNum[x][y]) ):
            checkMark(x,y,x+1,y+1)
        elif(x != 0 and y != 0 and
             heightMap[x-1][y-1] != -99 and
             (tectNum[x-1][y-1] == tectNum[x][y]) ):
            checkMark(x,y,x-1,y-1)
        elif(x != imgx-1 and
             y != 0 and
             heightMap[x+1][y-1] != -99 and
             (tectNum[x+1][y-1] == tectNum[x][y])):
            checkMark(x,y,x+1,y-1)
        elif(x != 0 and
             y != imgy-1 and
             heightMap[x-1][y+1] != -99 and
             (tectNum[x-1][y+1] == tectNum[x][y]) ):
            checkMark(x,y,x-1,y+1)
        if(heightMap[x][y] == -99):
            putpixel((x, y),(255,165,0))
            newBord.append([x,y])
        else:
            queueAll.append([x,y])
            ori[x][y] = True
        i += 1
    return newBord
def generateNoise(width,height,octave):
    scale       = 100 # Number that determines at what distance to view the noisemap
    octaves     = octave # the number of levels of detail you want you perlin noise to have
    persistence = 0.7 # number that determines how much detail is added or removed at each octave (adjusts frequency)
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
            queueXBorder.append(nx[i])
            queueYBorder.append(ny[i])
            nx2.append(nx[i]+width)
            ny2.append(ny[i])
            nx3.append(nx[i]-width)
            ny3.append(ny[i])
            t = random.randrange(2)
            if t == 0:
                isOceanic.append(True)
                nr.append(0)
                ng.append(0)
                nb.append(0)
            else:
                isOceanic.append(False)
                nr.append(random.randrange(256))
                ng.append(random.randrange(256))
                nb.append(random.randrange(256))
            tectMovement.append(random.choice(tectMovementList))
    for y in range(int(imgy)):
        for x in range(int(imgx)):
            dmin = math.hypot(imgx-1, imgy-1)
            j = -1
            for i in range(num_cells):
                    d = math.hypot(nx[i]-x, ny[i]-y)
                    if d < dmin:
                            dmin = d
                            j = i
                    d = math.hypot(nx3[i]-x, ny3[i]-y)
                    if d < dmin:
                            dmin = d
                            j = i
                    d = math.hypot(nx2[i]-x, ny2[i]-y)
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
    image.save("VoronoiDiagram.png", "PNG")
    image.show()
def rest():
    bord = []
    for y in range(imgy):
        for x in range(imgx):
          num = 0
          if( y != 0 and (tectNum[x][y-1] != tectNum[x][y])):
             num += 1
          if( y != imgy-1 and (tectNum[x][y+1] != tectNum[x][y] )):
             num += 2
          if( x != 0 and (tectNum[x-1][y] != tectNum[x][y] )):
             num += 4
          if( x != imgx-1 and (tectNum[x+1][y] != tectNum[x][y])):
             num += 7
          if(num == 1):
              listTest = [Up,Down,Left,Right,Right,Left,Left,Right]
              other = [Down,Up,Down,Left,Right]
              setUp(x,y,x,y-1,listTest,other)
          elif( num == 2):
              listTest = [Down,Up,Left,Right,Right,Left,Left,Right]
              other = [Up,Down,Up,Right,Left]
              setUp(x,y,x,y+1,listTest,other)              
          elif( num == 4):
              listTest = [Left,Right,Up,Down,Up,Down,Up,Down]
              other = [Right,Left,Right,Down,Up]
              setUp(x,y,x-1,y,listTest,other)
          elif( num == 7):
              listTest = [Right,Left,Up,Down,Up,Down,Up,Down]
              other = [Left,Right,Left,Down,Up]
              setUp(x,y,x+1,y,listTest,other)
          else:
              if(num > 0):
                bord.append([x,y])
              heightMap[x][y] = -99
              
    while True:
        bord = cleanUp(bord)
        if len(bord) == 0:
            break
    image.save("VoronoiDiagram_2.png", "PNG")
    image.show()
    i = 0
    print(str(len(highList)))
    typesOfBord()
    print(str(len(conOcean)))
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
              
          ran = .0025
          if(num != 0):
              if((elev/num) < 0.0):
                heightMap[currX][currY] = (elev/num)+ 0.015
              else:
                heightMap[currX][currY] = (elev/num)+ ran

            
        if(heightMap[currX][currY] < 0.99):
          if(currY != 0 and tectType[currX][currY-1] == False and (coMarked[currX][currY-1] != True)):
              conOcean.append([currX,currY-1])
              isUp[currX][currY-1] = isUp[currX][currY]
              coMarked[currX][currY-1] = True            
          if(currY != imgy-1 and tectType[currX][currY+1] == False and (coMarked[currX][currY+1] != True)):
              conOcean.append([currX,currY+1])
              isUp[currX][currY+1] = isUp[currX][currY]
              coMarked[currX][currY+1] = True            
          if(currX != 0 and tectType[currX-1][currY] == False and (coMarked[currX-1][currY] != True)):
              conOcean.append([currX-1,currY])
              isUp[currX-1][currY] = isUp[currX][currY]
              coMarked[currX-1][currY] = True
          elif(currX == 0 and tectType[imgx-1][currY] == False and (coMarked[imgx-1][currY] != True)):
              conOcean.append([imgx-1,currY])
              isUp[imgx-1][currY] = isUp[currX][currY]
              coMarked[imgx-1][currY] = True
          if(currX != imgx-1 and tectType[currX+1][currY] == False and (coMarked[currX+1][currY] != True)):
              conOcean.append([currX+1,currY])
              isUp[currX+1][currY] = isUp[currX][currY]
              coMarked[currX+1][currY] = True
          elif(currX == imgx-1 and tectType[0][currY] == False and (coMarked[0][currY] != True)):
              conOcean.append([0,currY])
              isUp[0][currY] = isUp[currX][currY]
              coMarked[0][currY] = True 
          if(currX != imgx-1 and currY != imgy-1 and tectType[currX+1][currY+1] == False and coMarked[currX+1][currY+1] != True):
              conOcean.append([currX+1,currY+1])
              coMarked[currX+1][currY+1] = True
          if(currX != 0 and currY != 0 and tectType[currX-1][currY-1] == False and coMarked[currX-1][currY-1] != True):
              conOcean.append([currX-1,currY-1])
              coMarked[currX-1][currY-1] = True
          if(currX != imgx-1 and currY != 0 and tectType[currX+1][currY-1] == False and coMarked[currX+1][currY-1] != True):
              conOcean.append([currX+1,currY-1])
              coMarked[currX+1][currY-1] = True
          if(currX != 0 and currY != imgy-1 and tectType[currX-1][currY+1] == False and coMarked[currX-1][currY+1] != True):
              conOcean.append([currX-1,currY+1])
              coMarked[currX-1][currY+1] = True
        i += 1
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] <= -0.01:
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
    image.save("VoronoiDiagram3.png", "PNG")
    image.show()
    for x in range(imgx):
        for y in range(imgy):
            if(tectType[x][y] == False):
              heightMap[x][y] += (heightMap[x][y]+.3)* (world[x][y])
            if(heightMap[x][y] >= 0.0):
                heightMap[x][y] = 0.0
                landTotal[x][y] = True
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if heightMap[x][y] < 0.0:
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
                
    image.save("VoronoiDiagram4.png", "PNG")
    image.show()
    i = 0
    for j in range(len(landList)):
        currX = landList[i][0]
        currY = landList[i][1]
        landOrigin[currX][currY] = True
        heightMap[currX][currY] = 0.0
        i += 1
    i = 0
    scale       = 100 # Number that determines at what distance to view the noisemap
    octaves     = 6 # the number of levels of detail you want you perlin noise to have
    persistence = 0.7 # number that determines how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2.0 # number that determines how much each octave contributes to the overall shape (adjusts amplitude)
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
            ran = .0035
            if(num != 0):
                heightMap[currX][currY] = (elev/num)+ ran
        if(currY != 0 and landTotal[currX,currY-1] == True and (landFall[currX][currY-1] != True)):
              landList.append([currX,currY-1])
              isUp[currX][currY-1] = isUp[currX][currY]
              landFall[currX][currY-1] = True            
        if(currY != imgy-1 and landTotal[currX][currY+1] == True and (landFall[currX][currY+1] != True)):
              landList.append([currX,currY+1])
              isUp[currX][currY+1] = isUp[currX][currY]
              landFall[currX][currY+1] = True            
        if(currX != 0 and landTotal[currX-1][currY] == True and (landFall[currX-1][currY] != True)):
              landList.append([currX-1,currY])
              isUp[currX-1][currY] = isUp[currX][currY]
              landFall[currX-1][currY] = True
        elif(currX == 0 and landTotal[imgx-1][currY] == True and (landFall[imgx-1][currY] != True)):
              landList.append([imgx-1,currY])
              isUp[imgx-1][currY] = isUp[currX][currY]
              landFall[imgx-1][currY] = True
        if(currX != imgx-1 and landTotal[currX+1][currY] == True and (landFall[currX+1][currY] != True)):
              landList.append([currX+1,currY])
              isUp[currX+1][currY] = isUp[currX][currY]
              landFall[currX+1][currY] = True
        elif(currX == imgx-1 and landTotal[0][currY] == True and (landFall[0][currY] != True)):
              landList.append([0,currY])
              isUp[0][currY] = isUp[currX][currY]
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
    image.save("VoronoiDiagram5.png", "PNG")
    image.show()
    for x in range(imgx):
        for y in range(imgy):
            if(landTotal[x][y] == True):
              heightMap[x][y] += (heightMap[x][y]+.3)* (world2[x][y])
            if(heightMap[x][y] >= .01):
                heightMap[x][y] = 0.01
                terrainTotal[x][y] = True
      
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
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
        heightMap[currX][currY] = 0.00
        i += 1
    i = 0
    scale       = 100 # Number that determines at what distance to view the noisemap
    octaves     = 10 # the number of levels of detail you want you perlin noise to have
    persistence = 0.7 # number that determines how much detail is added or removed at each octave (adjusts frequency)
    lacunarity  = 2.0 # number that determines how much each octave contributes to the overall shape (adjusts amplitude)
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
            ran = .003
            if(num != 0):
                heightMap[currX][currY] = (elev/num)+ ran
        if(currY != 0 and terrainTotal[currX,currY-1] == True and (terrainFall[currX][currY-1] != True)):
              terrainList.append([currX,currY-1])
              isUp[currX][currY-1] = isUp[currX][currY]
              terrainFall[currX][currY-1] = True            
        if(currY != imgy-1 and terrainTotal[currX][currY+1] == True and (terrainFall[currX][currY+1] != True)):
              terrainList.append([currX,currY+1])
              isUp[currX][currY+1] = isUp[currX][currY]
              terrainFall[currX][currY+1] = True            
        if(currX != 0 and terrainTotal[currX-1][currY] == True and (terrainFall[currX-1][currY] != True)):
              terrainList.append([currX-1,currY])
              isUp[currX-1][currY] = isUp[currX][currY]
              terrainFall[currX-1][currY] = True
        elif(currX == 0 and terrainTotal[imgx-1][currY] == True and (terrainFall[imgx-1][currY] != True)):
              terrainList.append([imgx-1,currY])
              isUp[imgx-1][currY] = isUp[currX][currY]
              terrainFall[imgx-1][currY] = True
        if(currX != imgx-1 and terrainTotal[currX+1][currY] == True and (terrainFall[currX+1][currY] != True)):
              terrainList.append([currX+1,currY])
              isUp[currX+1][currY] = isUp[currX][currY]
              terrainFall[currX+1][currY] = True
        elif(currX == imgx-1 and terrainTotal[0][currY] == True and (terrainFall[0][currY] != True)):
              terrainList.append([0,currY])
              isUp[0][currY] = isUp[currX][currY]
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
    col = (0,0,0)
    for y in range(imgy):
        for x in range(imgx):
            if terrainTotal[x][y] == True:
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
    image.save("VoronoiDiagram6.png", "PNG")
    image.show()
    for x in range(imgx):
        for y in range(imgy):
            if(terrainTotal[x][y] == True):
              heightMap[x][y] += (heightMap[x][y]+.3)* (world2[x][y])
            if landOrigin[x][y] == True:
                heightMap[x][y] = 99
                putpixel((x,y),(217,236,255))
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
    image.save("VoronoiDiagram7.png", "PNG")
    image.show()

    yHalf = int(imgy/2)
    westWinds = int(yHalf * .33)
    eastWinds = int(yHalf * .66)
    polarWinds = int(yHalf * .90)
    for x in range(imgx):
        if(heightMap[x][yHalf+5] < 0.0):
            putpixel((x,yHalf+5), (255,0,0))
        if(heightMap[x][yHalf-5] < 0.0):
             if(x != 0 and heightMap[x-1][yHalf-5] < 0.0):
                putpixel((x,yHalf-5), (255,0,0))
             else:
                currentColor[x][yHalf-5] = yHalf-5
                currentMovement.append([x,yHalf-5])
                alreadyInCurrent[x][yHalf-5] = True
             if(x != 0 and heightMap[x-1][yHalf+5] < 0.0):
                putpixel((x,yHalf+5), (255,0,0))
             else:
                currentColor[x][yHalf+5] = yHalf+5
                currentMovement.append([x,yHalf+5])
                alreadyInCurrent[x][yHalf+5] = True
                
        if(heightMap[x][yHalf+westWinds] < 0.0):
            putpixel((x,yHalf+westWinds), (0,0,255))
        if(heightMap[x][yHalf-westWinds] < 0.0):
            putpixel((x,yHalf-westWinds), (0,0,255))
        if(heightMap[x][yHalf+eastWinds] < 0.0):
            putpixel((x,yHalf+eastWinds), (0,0,255))
        if(heightMap[x][yHalf-eastWinds] < 0.0):
            putpixel((x,yHalf-eastWinds), (0,0,255))
        if(heightMap[x][yHalf+polarWinds] < 0.0):
            putpixel((x,yHalf+polarWinds), (0,0,255))
        if(heightMap[x][yHalf-polarWinds] < 0.0):
            putpixel((x,yHalf-polarWinds), (0,0,255))
    i = 0
    for j in currentMovement:
        x = currentMovement[i][0]
        y = currentMovement[i][1]
        if(y == yHalf + 5):
            currentColor[x][y] = yHalf + 5
        elif(y == yHalf - 5):
            currentColor[x][y] = yHalf - 5
        elif(y == yHalf + westWinds):
            currentColor[x][y] = yHalf + westWinds
        elif(y == yHalf - westWinds):
            currentColor[x][y] = yHalf - westWinds
        elif(y == yHalf + eastWinds):
            currentColor[x][y] = yHalf + eastWinds
        elif(y == yHalf - eastWinds):
            currentColor[x][y] = yHalf - eastWinds           
        if(y <= yHalf + 5 and y >= yHalf - 5):
            putpixel((x,y),(0,0,0))
        elif(y == yHalf + westWinds or y == yHalf - westWinds):
            putpixel((x,y),(0,0,0))
        elif(y == yHalf + eastWinds or y == yHalf - eastWinds):
            putpixel((x,y),(0,0,0))
        elif(y == yHalf + polarWinds or y == yHalf - polarWinds):
            putpixel((x,y),(0,0,0))
        elif(currentColor[x][y] == yHalf - 5 and y < yHalf-5):
            putpixel((x,y),(255,0,0))
        elif(currentColor[x][y] == yHalf + 5 and y > yHalf+5):
            putpixel((x,y),(255,0,0))
        elif(currentColor[x][y] == yHalf - westWinds and y < yHalf - westWinds):
            putpixel((x,y),(255,0,0))
        elif(currentColor[x][y] == yHalf - westWinds and y > yHalf - westWinds):
            putpixel((x,y),(0,0,255))
        elif(currentColor[x][y] == yHalf + westWinds and y < yHalf + westWinds):
            putpixel((x,y),(0,0,255))
        elif(currentColor[x][y] == yHalf + westWinds and y > yHalf + westWinds):
            putpixel((x,y),(255,0,0))
        else:
            putpixel((x,y),(0,255,255))
            
        if(y != 0 and borderShelf[x][y-1] == True and alreadyInCurrent[x][y-1] != True):
          currentMovement.append([x,y-1])
          currentColor[x][y-1] = currentColor[x][y]
          alreadyInCurrent[x][y-1] = True
        if(y != imgy-1 and borderShelf[x][y+1] == True and alreadyInCurrent[x][y+1] != True):
          currentMovement.append([x,y+1])
          currentColor[x][y+1] = currentColor[x][y]
          alreadyInCurrent[x][y+1] = True
        if(x != 0 and borderShelf[x-1][y] == True and alreadyInCurrent[x-1][y] != True):
          currentMovement.append([x-1,y])
          currentColor[x-1][y] = currentColor[x][y]
          alreadyInCurrent[x-1][y] = True
        elif(x == 0 and borderShelf[imgx-1][y] == True and alreadyInCurrent[imgx-1][y] != True):
          currentMovement.append([imgx-1,y])
          currentColor[imgx-1][y] = currentColor[x][y]
          alreadyInCurrent[imgx-1][y] = True
        if(x != imgx-1 and borderShelf[x+1][y] == True and alreadyInCurrent[x+1][y] != True):
          currentMovement.append([x+1,y])
          currentColor[x+1][y] = currentColor[x][y]
          alreadyInCurrent[x+1][y] = True
        elif(x == imgx-1 and borderShelf[0][y] == True and alreadyInCurrent[0][y] != True):
          currentMovement.append([0,y])
          currentColor[0][y] = currentColor[x][y]
          alreadyInCurrent[0][y] = True
        if(x != imgx-1 and y != imgy-1 and borderShelf[x+1][y+1] == True and alreadyInCurrent[x+1][y+1] != True and (y+1 != yHalf - westWinds or y+1 != yHalf + westWinds)):
          currentMovement.append([x+1,y+1])
          currentColor[x+1][y+1] = currentColor[x][y]
          alreadyInCurrent[x+1][y+1] = True
        if(x != 0 and y != 0 and borderShelf[x-1][y-1] == True and alreadyInCurrent[x-1][y-1] != True and (y-1 != yHalf - westWinds or y-1 != yHalf + westWinds)):
          currentMovement.append([x-1,y-1])
          currentColor[x-1][y-1] = currentColor[x][y]
          alreadyInCurrent[x-1][y-1] = True
        if(x != imgx-1 and y != 0 and borderShelf[x+1][y-1] == True and alreadyInCurrent[x+1][y-1] != True and (y-1 != yHalf - westWinds or y-1 != yHalf + westWinds)):
          currentMovement.append([x+1,y-1])
          currentColor[x+1][y-1] = currentColor[x][y]
          alreadyInCurrent[x+1][y-1] = True
        if(x != 0 and y != imgy-1 and borderShelf[x-1][y+1] == True and alreadyInCurrent[x-1][y+1] != True and (y+1 != yHalf - westWinds or y+1 != yHalf + westWinds)):
          currentMovement.append([x-1,y+1])
          currentColor[x-1][y+1] = currentColor[x][y]
          alreadyInCurrent[x-1][y+1] = True
          
        if(y == yHalf - westWinds or y == yHalf + westWinds):
            if(x != imgx-1 and heightMap[x+1][y] < 0.0):
                currentMovement.append([x+1,y])
                alreadyInCurrent[x+1][y] = True
            elif(x == imgx-1 and heightMap[0][y] < 0.0):
                currentColor[0][y] = y 
                currentMovement.append([0,y])
                alreadyInCurrent[0][y] = True            
        if(y == yHalf - eastWinds or y == yHalf + eastWinds):
            if(x != 0 and heightMap[x-1][y] < 0.0):
                currentColor[x-1][y] = y
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
            elif(x == 0 and heightMap[imgx-1][y] < 0.0):
                currentColor[imgx-1][y] = y
                currentMovement.append([imgx-1,y])
                alreadyInCurrent[imgx-1][y] = True
        if(y == yHalf - 5 or y == yHalf + 5):
            if(x != 0 and heightMap[x-1][y] < 0.0):
                currentColor[x-1][y] = y
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
            elif(x == 0 and heightMap[imgx-1][y] < 0.0):
                currentColor[imgx-1][y] = y
                currentMovement.append([imgx-1,y])
                alreadyInCurrent[imgx-1][y] = True
        if(y == yHalf - polarWinds or y == yHalf + polarWinds):
            if(x != imgx-1 and heightMap[x-1][y] < 0.0):
                currentColor[x-1][y] = y
                currentMovement.append([x-1,y])
                alreadyInCurrent[x-1][y] = True
            elif(x == imgx-1 and heightMap[0][y] < 0.0):
                currentColor[0][y] = y
                currentMovement.append([0,y])
                alreadyInCurrent[0][y] = True
        if(y == yHalf):
            if(x != imgx-1 and heightMap[x+1][y] < 0.0):
                currentColor[x+1][y] = y
                currentMovement.append([x+1,y])
                alreadyInCurrent[x+1][y] = True
            elif(x == imgx-1 and heightMap[imgx-1][y] < 0.0):
                currentColor[0][y] = y
                currentMovement.append([0,y])
                alreadyInCurrent[0][y] = True 
        i += 1
    image.save("VoronoiDiagram10.png", "PNG")
    image.show()
wid = 500
hei = 250
shape = (wid,hei)
image = Image.new("RGB",(wid,hei))
world_test = np.zeros(image.size)
world = generateNoise(wid,hei,3)
world2 = np.zeros(image.size)
putpixel = image.putpixel
imgx, imgy = image.size
imgx2, imgy2 = image.size
color_world = np.zeros(image.size+(3,))
coMarked = np.zeros(image.size)
moveType = np.zeros(image.size)
tectType = np.zeros(image.size)
isUp = np.zeros(image.size)
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
queueXBorder = []
queueYBorder = []
tectMovement = []
isOceanic = []
tectMovementList = [1,2,3,4]
queueAll = []
maxNum = -0.10
minNum = 0.0
continental = False
Left = 1
Right = 2
Up = 3
Down = 4
lowElev = -0.1
midElev = -0.05
highElev = -0.01
highElevContinental = 0.01
high = np.zeros(image.size)
highList = []
up = np.zeros(image.size)
num_cells = 25
cc = 1
co = 2
oc = 3
oo = 4
coMarked = np.zeros(image.size)
coOrigin = np.zeros(image.size)
conCon = []
conOcean = []
oceanCon = []
oceanOcean = []
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

