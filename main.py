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
isBallStopped = True
timer = pygame.time.Clock()
delta = 0
time = 0
playerOne = Rect(100.0, height / 2.0, 20, 100)
playerTwo = Rect(width - 120.0, height / 2.0, 20.0, 100.0)
speed = 1
ballVector = [-0.35, 0]
[ballX, ballY] = [width / 2, height / 2]
textFont = pygame.font.Font(None, 20)
isGameOver = False
winner = None


# Functions for displaying text to screen
def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


def message_display(text, x, y, isCenter=False):
    largeText = pygame.font.Font('Fonts/8-bit Arcade In.ttf', 30)
    TextSurf, TextRect = text_objects(text, largeText)
    if isCenter:
        TextRect.center = (x, y)
    else:
        TextRect.x = x
        TextRect.y = y
    display.get_surface().blit(TextSurf, TextRect)


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
        ballVector = [-0.35, 0]


# Code for drawing on screen
def draw_game():
    window = display.get_surface()
    display.get_surface().fill(color)
    message_display("%d Lives" % lives[0], 20, 20)
    message_display("%d Lives" % lives[1], 680, 20)
    pygame.draw.rect(window, (255, 255, 255), playerOne)
    pygame.draw.rect(window, (255, 255, 255), playerTwo)
    pygame.draw.circle(window, (255, 255, 255), (int(ballX), int(ballY)), 2)
    if isGameOver:
        message_display(winner + " Wins", width / 2, 20, isCenter=True)


# Code for moving players based on user input
def user_input():
    global isBallStopped
    global isGameOver
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

    if isBallStopped and keys[pygame.K_RETURN]:
        if isGameOver:
            isGameOver = False
        isBallStopped = False


# Main game loop
def gameLoop():
    global window
    global time
    global winner
    global isGameOver
    global isBallStopped
    global running

    while running:

        time = timer.get_time()
        user_input()
        draw_game()
        collision()

        if lives[0] < 0:
            winner = "Player 2"
            isGameOver = True
            isBallStopped = True
            lives[0] = 3
            lives[1] = 3
        elif lives[1] < 0:
            winner = "Player 1"
            isGameOver = True
            isBallStopped = True
            lives[0] = 3
            lives[1] = 3

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        timer.tick()


gameLoop()
pygame.quit()
