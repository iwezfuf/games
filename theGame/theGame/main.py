from turtle import up
from pygame.locals import *
import random
import time
import os
import sys
import pygame
import pygame.freetype
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_g,
    QUIT,
    K_SPACE)

os.chdir(os.path.dirname(sys.argv[0]))

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
TILE_SIZE = 32
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
class Screen(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.surf = pygame.Surface([width, height])
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(topleft=(0,0))
screeen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)

gravity = pygame.Vector2((0, 0.5))
gravity_direction = gravity[1]/abs(gravity[1])
buoyancy = pygame.Vector2((0, -0.55))

level = (
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP                                                                                                                            PP",
        "PP                                                                                                                            PP",
        "PP                                                                                                                            PP",
        "PP                    PPPPPPPPPPP                                                                                             PP",
        "PP                                WWWWWWWW                                                                                            PP",
        "PP               WWWWWWWWW                                                                                                    PP",
        "PP                WWWWWW                                                                                                      PP",
        "PP      PPP       WWWWW                                                            PPPPPPPPPPPP                               PP",
        "PP PP P                                       WWWWW                                                                                PP",
        "PP                    B     SSSSSSS                                                                                           PP",
        "PP                 PPPPPP                   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP        PPPPPPPPPPPPPPPPP",
        "PP          1                            WWW                                                                                     PP",
        "PP         PPPPPPP                                                                                                            PP",
        "PP                      3                                                                                                     PP",
        "PP                     PPPPPP                                                                                                 PP",
        "PP         <B                                                                                                                 PP",
        "PP   PPPPPPPPPPP                       WWWWWWW       WWWWWWWW                                                                                PP",
        "PP                    >  B         WWWWWWW                                  PPPPPPPPP                                               PP",
        "PP                 PPPPPPPPPPP  P  WWWWWWW                                                                                    PP",
        "PP                              P  WWWWWWWWWWWWWWWW                                                                                    PP",
        "PP                              P  WWWWWWW                        WWWWW                                                            PP",
        "PP                              P  WWWWWWW                                                                                    PP",
        "PP                              P  WWWWWWW                                                                                    PP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")


def is_on_screen(object):
    if pygame.sprite.collide_rect(screeen, object):
        return True
    return False

class Sign(pygame.sprite.Sprite):
    def __init__(self, position, text, size, color):
        super(Sign, self).__init__()
        self.position = position
        self.text = text
        self.size = size
        self.color = color
        self.myfont = pygame.font.SysFont('Arial', self.size)
        self.textsurface = self.myfont.render("".join([str(i) for i in self.text]), False, self.color)
        signs.add(self)


class Wall(pygame.sprite.Sprite):
    def __init__(self, center, color):
        super(Wall, self).__init__()
        self.surf = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.surf.fill(color)
        self.rect = self.surf.get_rect(bottomleft=center)
        all_sprites.add(self)
        walls.add(self)

spike_image = pygame.image.load(r'spike.png')

class Spike(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Spike, self).__init__()
        self.surf = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(bottomleft=position)
        spikes.add(self)
        all_sprites.add(self)
    
    def update(self):
        if is_on_screen(self):
            screen.blit(spike_image, (self.rect.center[0]-15, self.rect.center[1]-15))

class Water(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Water, self).__init__()
        self.surf = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.surf.fill([0,0,255])
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(bottomleft=position)
        all_sprites.add(self)
        water.add(self)
        self.water_blocks_above_me = []
        self.water_blocks_below_me = []

    def update(self, forced=False):
        if is_on_screen(self) or forced:
            potential_spots = ((0, 1*gravity_direction), (1, 1*gravity_direction), (-1, 1*gravity_direction))
            for spot in potential_spots:
                new_spot = (int(self.rect.center[0]+spot[0]*TILE_SIZE), int(self.rect.center[1]+spot[1]*TILE_SIZE))
                if not any(wall.rect.collidepoint(new_spot) for wall in walls) and not any(water_block.rect.collidepoint(new_spot) for water_block in water):
                    self.update_water_blocks_above_and_below_me(True, True)
                    self.rect.move_ip(spot[0]*TILE_SIZE, spot[1]*TILE_SIZE)

                    global update_water_blocks
                    for i in self.water_blocks_above_me:
                        update_water_blocks[1].append(i)
                    
                    return
                        
        

    def update_water_blocks_above_and_below_me(self, above=True, below=True):
        # below
        if below:
            self.water_blocks_below_me = []
            potential_spots = ((0, 1*gravity_direction), (1, 1*gravity_direction), (-1, 1*gravity_direction))
            for spot in potential_spots:
                new_spot = (int(self.rect.center[0]+spot[0]*TILE_SIZE), int(self.rect.center[1]+spot[1]*TILE_SIZE))
                for water_block in water:
                    if water_block.rect.collidepoint(new_spot):
                        self.water_blocks_below_me.append(water_block)

        # above
        if above:
            self.water_blocks_above_me = []
            potential_spots = ((0, -1*gravity_direction), (1, -1*gravity_direction), (-1, -1*gravity_direction))
            for spot in potential_spots:
                new_spot = (int(self.rect.center[0]+spot[0]*TILE_SIZE), int(self.rect.center[1]+spot[1]*TILE_SIZE))
                for water_block in water:
                    if water_block.rect.collidepoint(new_spot):
                        self.water_blocks_above_me.append(water_block)
        

class Gravity_thing(pygame.sprite.Sprite):
    def __init__(self, position, speed, max_hp, weight, noImage=True):
        super(Gravity_thing, self).__init__()
        self.surf = pygame.Surface([30,30])
        if noImage:
            self.surf.fill([50,50,50])
        else: 
            self.surf.set_alpha(0)
        self.rect = self.surf.get_rect(bottomleft=position)
        self.position = position
        self.onGround = False
        self.vector = pygame.Vector2((0, 0))
        self.speed = speed
        self.max_hp = max_hp
        self.hp = max_hp
        self.weight = weight
        self.inWater = False
        self.onRope = False
        self.freefall = False
        self.velocity = 0
        all_sprites.add(self)
        gravity_things.add(self)


    def move(self, x, y):
        self.vector.x += x
        self.vector.y += y
        if x > 0:
            self.direction = "right"
        if x < 0:
            self.direction = "left"

    def gravity(self):
        if not self.onRope:
            if self != player or not self.hooked[0]:
                self.vector += gravity*self.weight
            if self.vector.y > 40:
                self.vector.y = 40

    def buoyancy(self):
        self.vector += buoyancy*gravity_direction
        if self.vector.y > 30:
            self.vector.y = 30


    def friction(self):
        friction_y = pygame.Vector2((0, 0.02))
        friction_x = pygame.Vector2((0.02, 0))
        if self.inWater:
            self.freefall = False
            friction_x = pygame.Vector2((3, 0))
        if self.onGround:
            self.freefall = False
            friction_x = pygame.Vector2((2, 0))
        if isinstance(self, Node):
            friction_y = pygame.Vector2((0, 1))
            friction_x = pygame.Vector2((0, 0))

        if self.vector.y > 0:
            self.vector -= friction_y
        if self.vector.y < 0:
            self.vector += friction_y
        if self.vector.x > 0:
            self.vector -= friction_x
        if self.vector.x < 0:
            self.vector += friction_x


    def hp_change(self, hp):
        self.hp += hp
        if self.hp < 0:
            if self in boxes:
                for i in range(5):
                    coin = Coin(list(self.rect.midbottom))
                    coin.vector.y -= 7
                    coin.vector.x += random.choice((-2,2,2.5,-2.5,1,-1,1.5,-1.5, 1.2,-1.2,2.2,-2.2))
            self.kill()
            del(self)
        
            
    def moving(self):
        if self.vector.x > 0:
            self.direction = "right"
        if self.vector.x < 0:
            self.direction = "left"

        self.velocity = self.vector.magnitude()
        if isinstance(self, Node):
            if self.sticked:
                return
            dist_x, dist_y, pnode = self.dist()
            self.move(0, -dist_y/55)
            self.move(-dist_x/3, 0)
            pnode.move(dist_x/5, 0)
            dist_x, dist_y, pnode = self.dist()


        if pygame.sprite.spritecollideany(self, water):
            self.inWater = True
            self.buoyancy()
        else: 
            self.inWater = False
            if self != player or not self.hooked[0]:
                self.gravity()

        if self != player or not self.hooked[0]:
            self.friction()
        self.onGround = False
        
        self.rect.move_ip(self.vector.x, 0)
        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block != self:
                if self.vector.x > 0:
                    self.rect.right = block.rect.left
                    if self != player or not self.hooked[0]:
                        if self.vector.y > 5:
                            self.vector.y *= 0.5
                elif self.vector.x < 0:
                    self.rect.left = block.rect.right
                    if self != player or not self.hooked[0]:
                        if self.vector.y > 5:
                            self.vector.y *= 0.5
                self.vector.x = 0
        
        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for box in box_hit_list:
            if box != self:
                if self.vector.x > 0:
                    self.rect.right = box.rect.left
                    box.move(box.speed, 0)
                elif self.vector.x < 0:
                    self.rect.left = box.rect.right
                    box.move(-box.speed, 0)

 
        self.rect.move_ip(0, self.vector.y)
        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            if block != self:
                if self.vector.y > 0:
                    self.rect.bottom = block.rect.top
                    if gravity_direction == 1:
                        self.onGround = True
                elif self.vector.y < 0:
                    self.rect.top = block.rect.bottom
                    if gravity_direction == -1:
                        self.onGround = True
                self.vector.y = 0

        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for box in box_hit_list:
            if box != self:
                if self.vector.y > 0:
                    self.rect.bottom = box.rect.top
                    if gravity_direction == 1:
                        self.onGround = True
                    #box.move(0, box.speed)
                elif self.vector.y < 0:
                    self.rect.top = box.rect.bottom
                    if gravity_direction == -1:
                        self.onGround = True
                    #box.move(0, -box.speed)
                self.vector.y = 0


        spikess = pygame.sprite.spritecollide(self, spikes, False)
        for spike in spikess:
            if self.rect.bottom < spike.rect.bottom:
                self.rect.bottom = spike.rect.top
                self.hp -= 5
                self.vector.y -= 5
            else:
                self.rect.top = spike.rect.bottom
                self.vector.y = 0

            self.freefall = False
        
        if self == player and self.hooked[0]:
            if spikess or box_hit_list or block_hit_list:
                self.end_hook()

        
        if pygame.sprite.spritecollideany(self, bullets):
            self.hp_change(-20)


            
class Creature(Gravity_thing):
    def __init__(self, position, speed, max_hp, noImage=True):
        super(Creature, self).__init__(position, speed, max_hp, 1, noImage)
        self.gun_ready = True
        self.max_hp = max_hp
        self.hp = max_hp
        self.direction = "right"
        self.freefall = False
        

    def hp_bar(self):
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.max_hp, 5), 2)
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.hp, 5))


    def shoot(self):
        if self.gun_ready:
            if self.direction == "right":
                bullet = Bullet([self.rect.midright, self.direction])
            else: bullet = Bullet([self.rect.midleft, self.direction])
            self.gun_ready = False
            pygame.time.set_timer(RELOAD, 700)



class Player(Creature):
    def __init__(self):
        super().__init__([SCREEN_WIDTH//2, SCREEN_HEIGHT//2], 8, 100, False)
        self.coins = 0
        self.onRope = False
        self.hooked = [False, 0, 0, 0]
        self.player_image = pygame.image.load(r'character.png')

    def end_hook(self):
        self.hooked = [False, 0, 0, 0]
        self.freefall = True
        self.vector.y *= 1.5

    
    def update(self):
        coin_collisions = pygame.sprite.spritecollide(self, coins, False)
        for coin in coin_collisions:
            self.coins += 1
            coin.kill()
            del(coin)
            return

        if not self.freefall: self.vector.x = 0               

        if not self.hooked[0] and not self.freefall:
            rope_collisions = pygame.sprite.spritecollide(self, nodes, False)
            if not rope_collisions:
                self.onRope = False
            else:
                for rope in rope_collisions:
                    self.onRope = rope
                    self.vector.y = 0
                    
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP]:
                if self.onRope:
                    self.move(0, -4)
                elif self.onGround:
                    self.move(0, -14*gravity_direction)
                    self.onGround = False
            if pressed_keys[K_DOWN]:
                if self.onRope:
                    self.move(0,4)
            if pressed_keys[K_LEFT]:
                self.move(-self.speed, 0)
                if self.onRope:
                    self.onRope.move(-self.speed, 0)
            if pressed_keys[K_RIGHT]:
                self.move(self.speed, 0)
                if self.onRope:
                    self.onRope.move(self.speed, 0)
            if pressed_keys[K_SPACE]:
                self.shoot()

        if self.hp != self.max_hp:
            self.hp_bar()
            if self.hp < 0:
                self.kill()
                del(self)
                return


        if self.hooked[0]:

                x,y = self.hooked[0].rect.center
                pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]],[x,y])

                vector_to_me = (x - self.rect.center[0], y - self.rect.center[1])

                if abs(vector_to_me[1]) < 40:
                    self.end_hook()
                else:
                    self.vector.x = 0; self.vector.y = 0

                    perp_vector = (1, -vector_to_me[0]/vector_to_me[1])

                    k = self.hooked[2]/(abs(perp_vector[0]) + abs(perp_vector[1]))
                    
                    if self.hooked[3] == "right":
                        multiply = 1
                    else: multiply = -1

                    self.vector.x = perp_vector[0]*k*multiply
                    self.vector.y = perp_vector[1]*k*multiply

                    if (self.hooked[3] == "right" and x < self.rect.center[0]) or (self.hooked[3] == "left" and x > self.rect.center[0]):

                            self.hooked[2] *= 0.99 - 0.07*self.hooked[4]

                            mag = self.vector.magnitude()

                            if abs(mag*((y - self.rect.center[1])/self.hooked[1])) < 0.8:
                                self.hooked[2] *= 2.5
                                self.hooked[4] += 1
                                if abs(x-self.rect.center[0]) < 8:
                                    self.hooked[2] = 0
                                elif self.hooked[3] == "right":
                                    self.hooked[3] = "left"
                                else: self.hooked[3] = "right"
                    
                    else: self.hooked[2] *= 1.06


        self.moving()


        if self.direction == "left":
            screen.blit(self.player_image, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        else: screen.blit(pygame.transform.flip(self.player_image, True, False), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))


class Coin(Gravity_thing):
    def __init__(self, position):
        super(Coin, self).__init__(position, 10, 5000, 0.7)
        self.surf = pygame.Surface([10, 10])
        self.surf.fill([255,255,0])
        position[1] -= TILE_SIZE//2
        self.rect = self.surf.get_rect(bottomleft=position)
        self.vector = pygame.Vector2((0, 0))
        all_sprites.add(self)
        coins.add(self)

    def update(self):
        self.moving()


class Box(Gravity_thing):
    def __init__(self, position, color, max_hp, speed):
        super(Box, self).__init__(position, speed, max_hp, 1.2)
        boxes.add(self)
        
    def update(self):
        self.moving()
        self.vector.x = 0


class Turret(Gravity_thing):
    def __init__(self, position, direction):
        super(Turret, self).__init__(position, 4, 50000, 1.2)
        self.direction = direction
        turrets.add(self)
        boxes.add(self)

    def update(self):
        self.moving()
        self.vector.x = 0

    def shoot(self):
        if self.direction == -1:
            bullet = Bullet([self.rect.midleft, "left"])
        else: bullet = Bullet([self.rect.midright, "right"])        
        

class Soldier(Creature):
    def __init__(self, position, path):
        super().__init__(position, 3, 50)
        self.left = position
        self.right = path

    def update(self):
        self.right[0] += offset_x
        self.left[0] += offset_x
        self.right[1] += offset_y
        self.left[1] += offset_y
        if self.rect.right > self.right[0]:
            self.speed *= -1
        if self.rect.right < self.left[0]:
            self.speed *= -1
        self.move(self.speed, 0)

        if self.hp != self.max_hp:
            self.hp_bar()
            if self.hp < 0:
                self.kill()
                del(self)
                return
            
        self.moving()

class Node(Gravity_thing):
    def __init__(self, position, rope):
        super(Node, self).__init__(position, 1, 5000, 1)
        self.surf = pygame.Surface([5,5])
        self.surf.fill([176, 134, 18])
        self.rect = self.surf.get_rect(bottomleft=position)
        self.rope = rope
        self.sticked = False
        gravity_things.add(self)
        #boxes.add(self)
        nodes.add(self)

    def update(self):
        self.moving()
        self.vector.x *= 0.8

    def dist(self):
        index = self.rope.nodes.index(self)
        pnode = self.rope.nodes[index-1]
        if index == 0:
            dist_x = dist_y = 0
        else:
            dist_x = self.rect.left - pnode.rect.left
            dist_y = self.rect.top - pnode.rect.top

        return dist_x, dist_y, pnode

    def stick(self, position):
        self.sticked = True
        self.position = position



class Rope(pygame.sprite.Sprite):
    def __init__(self, position, lenght):
        super(Rope, self).__init__()
        self.position = position
        self.lenght = lenght
        self.nodes = []
        for i in range(lenght):
            node = Node([position[0],position[1]+i*40], self)
            self.nodes.append(node)
            if i == 0:
                node.stick([150,50])


class Hook(pygame.sprite.Sprite):
    def __init__(self, position, who):
        super(Hook, self).__init__()
        x = who.rect.center[0]
        y = who.rect.center[1]-25
        self.node = None
        
        vector_x = (x - position[0])/35
        if vector_x > 0:
            vector_x = min(vector_x, 15)
        else: vector_x = max(vector_x, -15)
        vector_y = (y - position[1])/35
        if vector_y > 0:
            vector_y = min(vector_y, 15)
        else: vector_y = max(vector_y, -15)

        i = 1
        while not sum([wall.rect.collidepoint(x,y) for wall in walls]):
            x -= vector_x
            y -= vector_y
            i += 1

            if i > 100:
                pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]], [x, y])
                pygame.display.flip()
                break

        if i < 100 and y < who.rect.y:
            node = Node([x,y], self)
            node.stick([x,y])
            self.node = node

            dist_x = abs(x - player.rect.center[0])
            dist_y = abs(y - player.rect.center[1])
            dist = (dist_x**2+dist_y**2)**0.5

            if x > who.rect.center[0]:
                direction = "right"
            else: direction = "left"

            if dist > 100:
                player.hooked = [self.node, dist, who.velocity*1.35, direction, 1]
        
                

class Bullet(pygame.sprite.Sprite):
    def __init__(self, shooting):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface([9,9])
        self.surf.fill([0,0,0])
        self.shooting = shooting
        self.rect = self.surf.get_rect(bottomleft=shooting[0])
        self.velocity = 30
        bullets.add(self)
        all_sprites.add(self)
        
    def update(self):
        if self.shooting[1] == "left":
            self.rect.move_ip(-self.velocity, 0)
        else: self.rect.move_ip(self.velocity, 0)
    
        if self.velocity == 0.01:
            self.kill()
            del(self)
            return
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
            del(self)
            return
        if pygame.sprite.spritecollideany(self, boxes):
            self.velocity = 0.01
            
cloud_image = pygame.image.load(r'mike_cloud.png')
cloud_image = pygame.transform.scale(cloud_image, (40,25))
cloud_image = pygame.transform.rotate(cloud_image, 45)

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface([80,50])
        self.surf.fill([200,200,200])
        self.rect = self.surf.get_rect(center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),random.randint(0, SCREEN_HEIGHT),))
        self.surf.set_alpha(0)
        
    def update(self):
        self.rect.move_ip(-5, 0)
        screen.blit(cloud_image, (self.rect.center))
        if self.rect.x < 0:
            self.kill()
            del(self)

class Camera():
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target):
        initial_position = target.rect.center
        target.update()
        new_position = target.rect.center
        offset_x = initial_position[0] - new_position[0]
        offset_y = initial_position[1] - new_position[1]
        target.rect.move_ip(offset_x, offset_y)
        return offset_x, offset_y
        

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)
RELOAD = pygame.USEREVENT + 2
TURRETS = pygame.USEREVENT + 3
pygame.time.set_timer(TURRETS, 2000)

boxes = pygame.sprite.Group()
camera = Camera()
all_sprites = pygame.sprite.Group()
gravity_things = pygame.sprite.Group()
walls = pygame.sprite.Group()
spikes = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins = pygame.sprite.Group()
signs = pygame.sprite.Group()
water = pygame.sprite.Group()
turrets = pygame.sprite.Group()
nodes = pygame.sprite.Group()
player = Player()
coins_sign = Sign([10,10], ['Coins: ', player.coins], 30, [0,0,0])
rope = Rope([150,50], 8)
water_update_dict = {}
water_positions = {}

x = y = 0
for row in level:
    for col in row:
        if col == "P":
            platform = Wall([x,y], [200,200,200])
        if col == "S":
            spike = Spike([x,y])
        if col == "B":
            box = Box([x,y], [100, 100, 100], 70, 3)
        try: soldier = Soldier([x,y], [x+int(col)*TILE_SIZE, y])
        except ValueError: pass
        if col == "W":
            water_block = Water([x,y])
        if col == "C":
            coin = Coin([x,y])
        if col == "<":
            turret = Turret([x,y], -1)
        if col == ">":
            turret = Turret([x,y], 1)
            
        x += TILE_SIZE
    y += TILE_SIZE
    x = 0

clock = pygame.time.Clock()

running = 1
target = player
start_time = time.time()
update_water_blocks = [[], []]

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                pygame.display.quit()
            if event.key == K_g:
                gravity = pygame.Vector2((0, 0.5*-gravity_direction))
                gravity_direction = gravity[1]/abs(gravity[1])
        elif event.type == QUIT:
            running = False
            pygame.display.quit()
        elif event.type == ADDCLOUD:
            turrets.update()
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == RELOAD:
            player.gun_ready = True
        elif event.type == TURRETS:
            for turret in turrets:
                turret.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for thing in all_sprites:
                if thing.rect.collidepoint((x,y)):
                    try:
                        thing.update_water_blocks_above_and_below_me(True, True)
                        
                        for block in thing.water_blocks_above_me:
                            block.update(True)
                        
                        thing.update_water_blocks_above_and_below_me(True, False)
                        for block in thing.water_blocks_above_me:
                            block.update(True)

                    except: pass
                    thing.kill()
            hook = Hook([x,y], player)
        elif event.type == pygame.MOUSEBUTTONUP:
            player.end_hook()


    screen.fill((135, 206, 250))
    offset_x, offset_y = camera.update(target)
    screen.blit(screeen.surf, screeen.rect)
    bullets.update()
    


    for entity in all_sprites:
        if entity != player:
            entity.rect.move_ip(offset_x, offset_y) # scrollovanie vsetkeho
            
        if entity not in spikes and entity != player and entity not in clouds:
            screen.blit(entity.surf, entity.rect)

    # Aby sa voda na zaciatku pohla aj ked ju nevidim
    if time.time() - start_time < 1:
        for water_block in water:
            if len(water_block.water_blocks_below_me) == 0:
                water_block.update(True)

    for water_block in water:
        if len(water_block.water_blocks_below_me) == 0:
            water_block.update()
    
    for water_block in update_water_blocks[0]:
        water_block.update(True)
    update_water_blocks = [set(update_water_blocks[1]), []]


    clouds.update()
    spikes.update()
    
    for gravity_thing in gravity_things:
        if gravity_thing != player:
            gravity_thing.update()

            
    coins_sign.kill()
    del(coins_sign)
    coins_sign = Sign([10,10], ['Coins: ', player.coins], 30, [0,0,0])
    for sign in signs:
        screen.blit(sign.textsurface,sign.position)
    
        
    pygame.display.flip()
    clock.tick(100)
