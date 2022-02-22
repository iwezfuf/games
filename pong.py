import math
import time
import pygame
import pygame.freetype
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    QUIT)

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Ball(pygame.sprite.Sprite):
    def __init__(self, vector):
        super(Ball, self).__init__()
        self.vector = vector
        self.surf = pygame.Surface([10,10])
        self.rect = self.surf.get_rect(center=[SCREEN_WIDTH//2,SCREEN_HEIGHT//2])
        balls.add(self)

    def update(self):
        pygame.draw.circle(screen, [255,255,255], self.rect.center, 10, width=0)
        self.rect.move_ip(self.vector[0], self.vector[1])
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vector[1] *= -1
        if pygame.sprite.spritecollideany(self, players):
            player = pygame.sprite.spritecollide(self, players, False)[0]
            dist = player.rect.center[1] - self.rect.center[1]
            angle = abs(dist*9.9/player.rect.height)
            z0 = 100-angle**2
            z = float(str(z0**0.5)[:4])
            if angle < 0:
                angle *= -1
            self.vector = [z, angle]
            if player == player1:
                self.vector[0] *= -1


        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            if self.rect.left > SCREEN_WIDTH:
                player1.score += 1
                ball = Ball([-5,5])
            else:
                player2.score += 1
                ball = Ball([5,5])
            self.kill()
            player1.rect.center = [SCREEN_WIDTH-10, SCREEN_HEIGHT//2-25]
            player2.rect.center = [10,SCREEN_HEIGHT//2-25]
            


class Player(pygame.sprite.Sprite):
    def __init__(self, position, keys):
        super(Player, self).__init__()
        self.vector = [0,0]
        self.surf = pygame.Surface([20,100])
        self.surf.fill([255,255,255])
        self.rect = self.surf.get_rect(center=position)
        self.position = position
        self.keys = keys
        self.speed = 6
        self.score = 0 
        players.add(self)

    def update(self, type):
        if type == 1 and self == player2:
            if ball.rect.center[1] > self.rect.center[1]:
                self.rect.move_ip(0, self.speed)
            elif ball.rect.center[1] < self.rect.center[1]:
                self.rect.move_ip(0, -self.speed)
        else: 
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[self.keys[0]]:
                self.rect.move_ip(0, -self.speed)
            if pressed_keys[self.keys[1]]:
                self.rect.move_ip(0, self.speed)
                
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        

balls = pygame.sprite.Group()
ball = Ball([5,5])
players = pygame.sprite.Group()
player1 = Player([SCREEN_WIDTH-10, SCREEN_HEIGHT//2-25], [K_UP, K_DOWN])
player2 = Player([10,SCREEN_HEIGHT//2-25], [K_w, K_s])
clock = pygame.time.Clock()


class Game():
    def __init__(self):
        self.running = True
        self.game(self.introScreen())

    
    def introScreen(self):
        myfont = pygame.font.SysFont('Arial', 30)
        textsurface = myfont.render("2 Players", False, [255,255,255])
        textsurface2 = myfont.render("1 Player", False, [255,255,255])
        screen.fill((0,0,0))
        pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2-40,150,80],2)
        pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2+50,SCREEN_HEIGHT//2-40,150,80],2)
        screen.blit(textsurface, [SCREEN_WIDTH//2-180,SCREEN_HEIGHT//2-20])
        screen.blit(textsurface2, [SCREEN_WIDTH//2+70,SCREEN_HEIGHT//2-20])

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(SCREEN_WIDTH//2-180, SCREEN_WIDTH//2-30) and pos[1] in range(SCREEN_HEIGHT//2-40, SCREEN_HEIGHT//2+40):
                        self.type = 2
                        self.cooldownScreen(5000)
                    elif pos[0] in range(SCREEN_WIDTH//2+70, SCREEN_WIDTH//2+220)  and pos[1] in range(SCREEN_HEIGHT//2-40, SCREEN_HEIGHT//2+40):
                        self.type = 1
                        self.cooldownScreen(1)
                if event.type == QUIT:
                    self.running = False
                    pygame.display.quit()
            
            pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-1,0,2,SCREEN_HEIGHT])
            pygame.display.flip()
            clock.tick(60)
    

    def cooldownScreen(self, cooldown):
        cooldownEvent = pygame.USEREVENT + 1
        pygame.time.set_timer(cooldownEvent, cooldown)
        start_ticks = pygame.time.get_ticks()
        myfont = pygame.font.SysFont('Arial', 70)
        gamestartsin = myfont.render(("Game starts in:"), False, [255,255,255])
        while True:
            screen.fill((0,0,0))
            text = (cooldown - (pygame.time.get_ticks()-start_ticks))/1000
            textsurface = myfont.render((str(text)), False, [255,255,255])
            screen.blit(textsurface, [315,320])
            screen.blit(gamestartsin, [200, 250])
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                if event.type == cooldownEvent:
                    self.game()

            pygame.display.flip()
            clock.tick(60)

    def game(self):
        pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-1,0,2,SCREEN_HEIGHT])
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
   
            screen.fill((0,0,0))
            for ball in balls:
                ball.update()

            for player in players:
                if player == player1:
                    pos = [100,100]
                else: pos = [700,100]
                myfont = pygame.font.SysFont('Arial', 100)
                textsurface = myfont.render(str(player.score), False, [255,255,255])
                screen.blit(textsurface, pos)
                player.update(self.type)
                screen.blit(player.surf, player.rect)
                if player.score == 3:
                    if player == player1:
                        self.endScreen(1)
                    else: self.endScreen(2)
            
            pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-1,0,2,SCREEN_HEIGHT])
            pygame.display.flip()
            clock.tick(60)
                    
    
    def endScreen(self, winner):
        myfont = pygame.font.SysFont('Arial', 70)
        winnertext = myfont.render(("Player " + str(winner) + " won!"), False, [255,255,255])
        anothergame = myfont.render(("New game"), False, [255,255,255])
        while True:
            screen.fill((0,0,0))
            screen.blit(winnertext, [220, 240])
            screen.blit(anothergame, [260, 360])
            pygame.draw.rect(screen, [255,255,255], [240,360,318,90],2)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(240, 240+318) and pos[1] in range(360, 360+90):
                        player1.score = 0
                        player2.score = 0
                        self.introScreen()

            pygame.display.flip()
            clock.tick(60)



game = Game()
