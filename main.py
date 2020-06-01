import pygame
import sys
from pygame.locals import *
from random import *

pygame.init()
screen = pygame.display.set_mode((1024, 580), RESIZABLE)
pygame.display.set_caption("Greed is Not Good")
clock = pygame.time.Clock()

background_image = pygame.image.load("assets/img/background.png").convert()
background_image = pygame.transform.scale(background_image, (1024, 580))

backdrop_image = pygame.image.load("assets/img/backdrop.png").convert()
backdrop_image = pygame.transform.scale(backdrop_image, (1024, 580))

howtoplay_image = pygame.image.load("assets/img/how-to-play.jpg").convert()
howtoplay_image = pygame.transform.scale(howtoplay_image, (1024, 580))

game_bgm = pygame.mixer.music

card_sound = pygame.mixer.Sound("assets/sfx/cardSlide8.wav")

title_font = pygame.font.Font("assets/font/ProductSans.ttf",45)
title_font.set_bold(True)
title = title_font.render("G r e e d I s N o t G o o d",True,(255,255,255))

button_font = pygame.font.Font("assets/font/ProductSans.ttf",30)

game_element = []
game_button = []
menu_button = []
full_card = []
play_card = []
players = []

left = 0
right = 9
turn = 0
dp = [[[None for i in range(110)]for j in range(110)]for k in range(2)]
opt = [[[None for i in range(110)]for j in range(110)]for k in range(2)]
takeLeft = 0
takeRight = 0

gameMode = 0
isSong = False
isPlaying = False
isEnd = False


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

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class Player:
    def __init__(self):
        self.score = 0
        self.isBot = False

    def reset(self):
        self.score = 0


class Button:
    def __init__(self, color, x,y,width,height, text,mode):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.mode = mode

    def draw(self,win,outline):
        if outline:
            pygame.draw.rect(win, (255,255,255), (self.x-2,self.y-2,2,self.height+4),0)
            pygame.draw.rect(win, (255,255,255), (self.x+self.width,self.y-2,2,self.height+4),0)
            pygame.draw.rect(win, (255,255,255), (self.x,self.y-2,self.width,2),0)
            pygame.draw.rect(win, (255,255,255), (self.x,self.y+self.height,self.width,2),0)
        
        surf = pygame.Surface((self.width,self.height), pygame.SRCALPHA)  
        surf.fill(self.color)
        win.blit(surf, (self.x,self.y))
        
        text = button_font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Element:
    def __init__(self,x,y,width,height,text,size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size = size
    def draw(self,win):
        element_font = pygame.font.Font("assets/font/ProductSans.ttf",self.size)
        text = element_font.render(self.text,1,(255,255,255))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
                                 
        
    
def createGameElement():
    anElement = Element(20,540,150,30,"Player 1",30)
    game_element.append(anElement)
    anElement = Element(854,540,150,30,"Player 2",30)
    game_element.append(anElement)
    anElement = Element(20,500,150,30,"0",50)
    game_element.append(anElement)
    anElement = Element(854,500,150,30,"0",50)
    game_element.append(anElement)
    anElement = Element(412,330,200,30,"Player 1's turn",50)
    game_element.append(anElement)

def createMenuButton():
    aMenuButton = Button((255,255,255,128),250,330,250,40,"Single Player",1)
    menu_button.append(aMenuButton)
    aMenuButton = Button((255,255,255,128),524,330,250,40,"Multi Player",2)
    menu_button.append(aMenuButton)
    aMenuButton = Button((255,255,255,128),387,390,250,40,"How to Play",3)
    menu_button.append(aMenuButton)
    aMenuButton = Button((255,255,255,128),387,450,250,40,"Exit",4)
    menu_button.append(aMenuButton)

def createGameButton():
    aGameButton = Button((255,255,255,128),387,390,250,40,"Restart",1)
    game_button.append(aGameButton)
    aGameButton = Button((255,255,255,128),387,450,250,40,"Main Menu",0)
    game_button.append(aGameButton)

def createPlayer():
    for i in range(2):
        aPlayer = Player()
        players.append(aPlayer)

def createDeck():    
    for i in range(1, 14):
        print("assets/img/"+str(i)+".png")
        img = pygame.image.load("assets/img/"+str(i)+".png").convert_alpha()
        img = pygame.transform.scale(img, (80, 120))
        theCard = Card(img, i)
        full_card.append(theCard)


def playGenerator():
    count = 11
    for i in range(count):
        theRand = randint(0, 12)
        play_card.append(full_card[theRand].__copy__())
        play_card[i].x = 103*i+10
        if i == 0 or i == 9:
            play_card[i].active = True
        print(play_card[i].val)

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
            dp[turn][left][right] = takeRight
            opt[turn][left][right] = 1
    return dp[turn][left][right]
            

def handle_event():
    global gameMode
    global isSong
    global isPlaying
    global left
    global right
    global turn
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])):
            pygame.quit()
            sys.exit()
        if gameMode == 0:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in menu_button:
                    if button.isOver(pos):
                        gameMode=button.mode
                        isSong = False
        elif gameMode == 1 or gameMode == 2:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in game_button:
                    if button.isOver(pos):
                        gameMode = button.mode
                        isSong = False
                        isPlaying = False
            if players[turn].isBot == False:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    for card in play_card:
                        if card.active == True:
                            if card.isOver(pos):
                                if card == play_card[left]:
                                    left += 1
                                    
                                    play_card[left].active = True
                                else:
                                    right -= 1
                                    play_card[right].active = True
                                card_sound.play()
                                players[turn].score += card.val
                                print(players[0].score, end=' ')
                                card.active = False
                                card.view = False
                                print(players[1].score)
                                turn ^= 1
            else:
                if opt[1][left][right] == None:
                    minimax(1,left,right)
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
                card_sound.play()
                print(players[0].score, end=' ')
                print(players[1].score)
                turn ^= 1
        elif gameMode == 3:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0]>30 and pos[0]<115 and pos[1]>30 and pos[1]<80:
                    gameMode = 0
                    isSong = False

def track_winner():
    global turn
    global gameMode
    global left
    global right
    global isEnd
    global isSong
    if left>right and not isEnd:
        isEnd = True
        isSong = False
        if players[0].score > players[1].score:
            game_element[4].text = "Player 1 Wins!"
        elif players[0].score < players[1].score:
            if players[1].isBot == True:
                game_element[4].text = "Computer Wins!"
            else:
                game_element[4].text = "Player 2 Wins!"
        else:
            game_element[4].text = "Draw!"
    elif gameMode == 1 and not isEnd:
        game_element[1].text = "Computer"
        if turn == 1:
            game_element[4].text = "Computer's turn"
    elif gameMode == 2 and not isEnd:
        if turn == 0:
            game_element[4].text = "Player 1's turn"
        else:
            game_element[4].text = "Player 2's turn"
    game_element[2].text = str(players[0].score)
    game_element[3].text = str(players[1].score)
    for element in game_element:
        element.draw(screen)
    

def draw_howtoplay():
    screen.fill((255, 255, 255))
    screen.blit(howtoplay_image, [0, 0])
    pygame.display.flip()
    clock.tick(60)
    handle_event()
        
def draw_game():
    screen.fill((255, 255, 255))
    screen.blit(backdrop_image, [0, 0])
    track_winner()
    for button in game_button:
        button.draw(screen,True)
    for i in range(0, 10):
        if play_card[i].view:
            screen.blit(play_card[i].img, [play_card[i].x, play_card[i].y])
    pygame.display.flip()
    clock.tick(60)
    handle_event()

def draw_menu():
    screen.fill((255, 255, 255))
    screen.blit(background_image, [0, 0])
    screen.blit(title,[210,260])
    for i in range(4):
        menu_button[i].draw(screen,True)
    pygame.display.flip()
    clock.tick(60)
    handle_event()
        

def main_loop():
    global gameMode
    global isSong
    global isPlaying
    global isEnd
    global left
    global right
    global turn

    while True:
        if not isPlaying:
            players.clear()
            play_card.clear()
            game_element.clear()
            createGameElement()
            createPlayer()
            playGenerator()
            left = 0
            right = 9
            turn = 0
            isPlaying = True
            isEnd = False
        if gameMode == 0:
            if not isSong:
                game_bgm.load("assets/bgm/Morning_Stroll.mp3")
                game_bgm.play(-1)
                isSong = True
            draw_menu()
        elif gameMode == 1 or gameMode == 2:
            if gameMode == 1:
                players[1].isBot = True
            if left>right and not isSong and isEnd:
                game_bgm.load("assets/bgm/Final_Reckoning.mp3")
                game_bgm.play(-1)
                isSong = True
            if not isSong:
                game_bgm.load("assets/bgm/National_Express.mp3")
                game_bgm.play(-1)
                isSong = True
            game_button[0].mode = gameMode
            draw_game()
        elif gameMode == 3:
            if not isSong:
                game_bgm.load("assets/bgm/Remember_September.mp3")
                game_bgm.play(-1)
                isSong = True
            draw_howtoplay()
        elif gameMode == 4:
            pygame.quit()
            sys.exit()
        
        
def main():
    createMenuButton()
    createGameButton()
    createDeck()
    main_loop()

main()
