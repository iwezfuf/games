import math
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

    def update(self):
        if self == player1:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[self.keys[0]]:
                self.rect.move_ip(0, -self.speed)
            if pressed_keys[self.keys[1]]:
                self.rect.move_ip(0, self.speed)
                
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                
        elif bp == 1 and self == player2:
            if ball.rect.center[1] > self.rect.center[1]:
                self.rect.move_ip(0, self.speed)
            elif ball.rect.center[1] < self.rect.center[1]:
                self.rect.move_ip(0, -self.speed)
        

balls = pygame.sprite.Group()
ball = Ball([5,5])
players = pygame.sprite.Group()
player1 = Player([SCREEN_WIDTH-10, SCREEN_HEIGHT//2-25], [K_UP, K_DOWN])
player2 = Player([10,SCREEN_HEIGHT//2-25], [K_w, K_s])
clock = pygame.time.Clock()

running = True
bp = False
myfont = pygame.font.SysFont('Arial', 30)
textsurface = myfont.render("2 Players", False, [255,255,255])
textsurface2 = myfont.render("1 Player", False, [255,255,255])
screen.fill((0,0,0))
pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2-40,150,80],2)
pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2+50,SCREEN_HEIGHT//2-40,150,80],2)
screen.blit(textsurface, [SCREEN_WIDTH//2-180,SCREEN_HEIGHT//2-20])
screen.blit(textsurface2, [SCREEN_WIDTH//2+70,SCREEN_HEIGHT//2-20])
        
while running:
    if not bp:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] in range(SCREEN_WIDTH//2-180, SCREEN_WIDTH//2-30) and pos[1] in range(SCREEN_HEIGHT//2-40, SCREEN_HEIGHT//2+40):
                    bp = 2
                elif pos[0] in range(SCREEN_WIDTH//2+70, SCREEN_WIDTH//2+220)  and pos[1] in range(SCREEN_HEIGHT//2-40, SCREEN_HEIGHT//2+40):
                    bp = 1
            if event.type == QUIT:
                running = False
                pygame.display.quit()
    else:    
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
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
            player.update()
            screen.blit(player.surf, player.rect)
            if player.score == 10:
                running = False
                
    pygame.draw.rect(screen, [255,255,255], [SCREEN_WIDTH//2-1,0,2,SCREEN_HEIGHT])
    pygame.display.flip()
    clock.tick(60)
