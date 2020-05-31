import pygame
import sys
from pygame.locals import *
from random import *

pygame.init()
screen = pygame.display.set_mode((1024, 580), RESIZABLE)
pygame.display.set_caption("Greed is Not Good")
clock = pygame.time.Clock()

background_image = pygame.image.load("img/background.png").convert()
background_image = pygame.transform.scale(background_image, (1024, 580))

backdrop_image = pygame.image.load("img/backdrop.png").convert()
backdrop_image = pygame.transform.scale(backdrop_image, (1024, 580))

full_card = []
play_card = []
players = []
isPlaying = False
left = 0
right = 9
turn = 0
dp = [[[None for i in range(110)]for j in range(110)]for k in range(2)]
opt = [[[None for i in range(110)]for j in range(110)]for k in range(2)]
takeLeft = 0
takeRight = 0

class Card:
    def __init__(self, img, val):
        self.img = img
        self.val = val
        self.x = 0
        self.y = 100
        self.width = 80
        self.height = 120
        self.active = False
        self.view = True

    def __copy__(self):
        return Card(self.img, self.val)

class Player:
    def __init__(self):
        self.score = 0
        self.isBot = False

    def reset(self):
        self.score = 0

def createPlayer():
    for i in range(2):
        aPlayer = Player()
        players.append(aPlayer)

def createDeck():    
    for i in range(1, 14):
        print("img/"+str(i)+".png")
        img = pygame.image.load("img/"+str(i)+".png").convert_alpha()
        img = pygame.transform.scale(img, (80, 120))
        theCard = Card(img, i)
        full_card.append(theCard)


def playGenerator():
    count = 10
    for i in range(count):
        theRand = randint(0, 12)
        play_card.append(full_card[theRand].__copy__())
        play_card[i].x = 103*i+10
        if i == 0 or i == 9:
            play_card[i].active = True
        print(play_card[i].val)


def draw():
    screen.fill((255, 255, 255))
    screen.blit(backdrop_image, [0, 0])
    for i in range(0, 10):
        if play_card[i].view:
            screen.blit(play_card[i].img, [play_card[i].x, play_card[i].y])
    pygame.display.flip()
    clock.tick(60)


def minimax(turn, left, right):
    if left > right:
        return 0
    if turn==0:
        takeLeft = play_card[left].val + minimax(1, left+1, right)
        takeRight = play_card[right].val + minimax(1, left, right - 1)
        if takeLeft > takeRight:
            dp[turn][left][right] = takeLeft
            opt[turn][left][right] = 0
        else:
            dp[turn][left][right] = takeRight
            opt[turn][left][right] = 1
    else:
        takeLeft = -play_card[left].val + minimax(0, left + 1, right)
        takeRight = -play_card[right].val + minimax(0, left, right - 1)
        if (takeLeft < takeRight):
            dp[turn][left][right] = takeLeft
            opt[turn][left][right] = 0
        else:
            dp[turn][left][right] = takeRight;
            opt[turn][left][right] = 1;
    return dp[turn][left][right]


def main_menu():
    global left
    global right
    global turn
    playing = False
    while True:
        if not playing:
            players[0].reset()
            players[1].reset()
            playing = True
        draw()
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])):
                pygame.quit()
                sys.exit()
            if turn == 0:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    for card in play_card:
                        if card.active == True:
                            if pos[0] > card.x and pos[0] < card.x+card.width:
                                if pos[1] > card.y and pos[1] < card.y+card.height:
                                    if card == play_card[left]:
                                        left += 1
                                        play_card[left].active = True
                                    else:
                                        right -= 1
                                        play_card[right].active = True
                                    players[0].score += card.val
                                    print(players[0].score, end=' ')
                                    card.active = False
                                    card.view = False
                                    print(players[1].score)
                                    turn += 1

            elif turn == 1:
                if opt[1][left][right] == None:
                    minimax(1, left, right)
                take = opt[1][left][right]
                if take == 0:
                    players[1].score += play_card[left].val
                    play_card[left].active = False
                    play_card[left].view = False
                    left += 1
                    play_card[left].active = True
                else:
                    players[1].score += play_card[right].val
                    play_card[right].active = False
                    play_card[right].view = False
                    right -= 1
                    play_card[right].active = True
                print(players[0].score, end=' ')
                print(players[1].score)
                turn -= 1

def main():
        createDeck()
        createPlayer()
        playGenerator()
        main_menu()

main()
