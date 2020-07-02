import pygame
from pygame import display
from pygame.rect import Rect
import math

pygame.init()

# Init code
(width, height) = (16 * 50, 9 * 50)
color = (0, 0, 0)
lives = [3, 3]
display.set_mode((width, height))
running = True
isBallStopped = False
timer = pygame.time.Clock()
delta = 0
time = 0
playerOne = Rect(100.0, height / 2.0, 20, 100)
playerTwo = Rect(width - 120.0, height / 2.0, 20.0, 100.0)
speed = 1
ballVector = [-0.35, 0]
[ballX, ballY] = [width / 2, height / 2]


# Code for collision detection and ball Movement
def collision():
    global ballX
    global ballY
    global ballVector
    global isBallStopped
    if playerOne.collidepoint(ballX, ballY):
        newBallAngle = (ballY - (playerOne.y + playerOne.height / 2.0)) / (playerOne.height / 2.0) * (math.pi / 4)
        ballVector[0] = math.cos(newBallAngle) * 0.35
        ballVector[1] = math.sin(newBallAngle) * 0.35
    elif playerTwo.collidepoint(ballX, ballY):
        newBallAngle = (ballY - (playerTwo.y + playerTwo.height / 2.0)) / (playerTwo.height / 2.0) * (math.pi / 4)
        ballVector[0] = -math.cos(newBallAngle) * 0.35
        ballVector[1] = math.sin(newBallAngle) * 0.35

    if ballY <= 0 or ballY >= height:
        ballVector[1] *= -1
    if ballX < 0:
        lives[0] -= 1
        isBallStopped = True
    elif ballX > width:
        lives[1] -= 1
        isBallStopped = True

    if not isBallStopped:
        ballX += ballVector[0] * time
        ballY += ballVector[1] * time
    else:
        [ballX, ballY] = [width / 2, height / 2]
        isBallStopped = False
        ballVector = [-0.35, 0]


# Code for drawing on screen
def draw():
    window = display.get_surface()
    display.get_surface().fill(color)
    pygame.draw.rect(window, (255, 255, 255), playerOne)
    pygame.draw.rect(window, (255, 255, 255), playerTwo)
    pygame.draw.circle(window, (255, 255, 255), (int(ballX), int(ballY)), 2)


# Code for moving players based on user input
def user_input():
    keys = pygame.key.get_pressed()
    global playerOne
    global playerTwo
    if keys[pygame.K_w] and playerOne.y > 10:
        playerOne = playerOne.move(0, -speed * time)

    elif keys[pygame.K_s] and playerOne.y < height - playerOne.height - 10:
        playerOne = playerOne.move(0, speed * time)
    if keys[pygame.K_UP] and playerTwo.y > 10:
        playerTwo = playerTwo.move(0, -speed * time)
    elif keys[pygame.K_DOWN] and playerTwo.y < height - playerTwo.height - 10:
        playerTwo = playerTwo.move(0, speed * time)


# Main game loop
while running:

    time = timer.get_time()
    user_input()
    draw()
    collision()

    print("Ball: [ %d , %d ]" % (ballX, ballY))
    print("Player One: [ %d , %d ]" % (playerOne.x, playerOne.y))
    print("Player Two: [ %d , %d ]" % (playerTwo.y, playerTwo.y))

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    timer.tick()
