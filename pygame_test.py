from tkinter import *
import pygame
input1 = 0
input2 = 0
input3 = 0
while True:
    print("Enter number of Tect Plates: ")
    input1 = input()
    try:
        int(input1)
        break
    except ValueError:
        print("Please enter a number")
while True:
    print("Enter the number of those " +str(input1)+ " total plates that will be land plates: ")
    input2 = input()
    try:
        int(input2)
        if input2 > input1:
            print("The number of land plates enter are greater than total plates given")
        else:
            break
    except ValueError:
        print("Please enter a number")
while True:
    print("Enter number of river you want on land: ")
    input3 = input()
    try:
        int(input3)
        break
    except ValueError:
        print("Please enter a number")
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
