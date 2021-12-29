import random
import pygame
import pygame.freetype
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_u,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE)

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
TILE_SIZE = 32
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
gravity = pygame.Vector2((0, 0.5))
buoyancy = pygame.Vector2((0, -0.55))

level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP                                                                                                   PP",
        "PP                                     B                                                             PP",
        "PP                                                                                                   PP",
        "PP                    PPPPPPPPPPP                                                                    PP",
        "PP                                                                                                   PP",
        "PP               WWWWWWWWW                                                                           PP",
        "PP                WWWWWW                                                                             PP",
        "PP      PPP       WWWWW                                                            PPPPPPPPPPPP      PP",
        "PP PP P                                                                                              PP",
        "PP                    B     SSSSSSS                                                                  PP",
        "PP                 PPPPPP                             PPPPPPPP                                       PP",
        "PP          1                                                                                        PP",
        "PP         PPPPPPP                                                                                   PP",
        "PP                      3                                                                            PP",
        "PP                     PPPPPP                                                                        PP",
        "PP         <B                                                                                        PP",
        "PP   PPPPPPPPPPP                                                                                     PP",
        "PP                    >  B                                            PPPPPPPPP                      PP",
        "PP                 PPPPPPPPPPP  P  WWWWWWW                                                           PP",
        "PP                              P  WWWWWWW                                                           PP",
        "PP                              P  WWWWWWW                                                           PP",
        "PP                              P  WWWWWWW                                                           PP",
        "PP                              P  WWWWWWW                                                           PP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]


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
    def __init__(self, center, color, *groups):
        super(Wall, self).__init__()
        self.surf = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.surf.fill(color)
        self.rect = self.surf.get_rect(bottomleft=center)
        for group in groups:
            group.add(self)

class Water(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Water, self).__init__()
        self.surf = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.surf.fill([0,0,255])
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(bottomleft=position)
        all_sprites.add(self)
        water.add(self)

    def update(self):
        potential_spots = [[0, 1], [1, 1], [-1, 1]]
        for spot in potential_spots:
            new_spot = [self.rect.center[0]+spot[0]*TILE_SIZE, self.rect.center[1]+spot[1]*TILE_SIZE]
            if not any(wall.rect.collidepoint(new_spot) for wall in walls) and not any(water_block.rect.collidepoint(new_spot) for water_block in water):
                self.rect.move_ip(spot[0]*TILE_SIZE, spot[1]*TILE_SIZE)
                
        

class Gravity_thing(pygame.sprite.Sprite):
    def __init__(self, position, speed, max_hp, weight):
        super(Gravity_thing, self).__init__()
        self.surf = pygame.Surface([30,30])
        self.surf.fill([50,50,50])
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
            self.vector += gravity*self.weight
            if self.vector.y > 40:
                self.vector.y = 40

    def buoyancy(self):
        self.vector += buoyancy
        if self.vector.y > 40:
            self.vector.y = 40


    def friction(self):
        friction_y = pygame.Vector2((0, 0.02))
        friction_x = pygame.Vector2((0.02, 0))
        if self.inWater:
            friction_x = pygame.Vector2((3, 0))
        if self.onGround:
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
                

    def moving(self):
        if isinstance(self, Node):
            if self.sticked:
                return
            dist_x, dist_y, pnode = self.dist()
            self.move(0, -dist_y/55)
            self.move(-dist_x/3, 0)
            pnode.move(dist_x/5, 0)
            dist_x, dist_y, pnode = self.dist()


            
        if self.inWater and not pygame.sprite.spritecollideany(self, water):
            self.inWater = False
        if pygame.sprite.spritecollideany(self, water):
            self.inWater = True
        if self.inWater:
            self.buoyancy()
        else:
            self.gravity()
        self.friction()
        self.onGround = False

        
        self.rect.move_ip(self.vector.x, 0)

        if self == player:
            if self.hooked[0]:
                x,y = self.hooked[0].rect.center
                pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]],[x,y])
                dist_x = abs(x - self.rect.center[0])
                dist_y = abs(y - self.rect.center[1])
                dist = self.hooked[1]
                distt = (dist_x**2+dist_y**2)**0.5
                pygame.draw.rect(screen,[0,0,0],(x-dist, y-dist, dist*2, dist*2), 2)

                if dist_x >= dist:
                    self.rect.move_ip(-self.vector.x, 0)
                elif distt > dist:
                    if  self.rect.center[0] < x:
                        new_y = ((dist**2 - dist_x**2)**0.5 - dist_y).real
                    else: new_y = -((dist**2 - dist_x**2)**0.5 - dist_y).real

                    if (self.rect.center[0] < x and self.rect.center[1] < y) or (self.rect.center[0] > x and self.rect.center[1] > y):
                        new_y *= -1

                    self.move(0, new_y)

        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if block != self:
                if self.vector.x > 0:
                    self.rect.right = block.rect.left
                    if self.vector.y > 5:
                        self.vector.y *= 0.5
                elif self.vector.x < 0:
                    self.rect.left = block.rect.right
                    if self.vector.y > 5:
                        self.vector.y *= 0.5
                self.vector.x = 0
        
        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for box in box_hit_list:
            if box != self:
                if (self.vector.x-box.vector.x) > 0:
                    self.rect.right = box.rect.left
                    box.rect.move_ip(box.speed,0)
                    #box.vector.x += box.speed
                elif (self.vector.x-box.vector.x) < 0:
                    self.rect.left = box.rect.right
                    box.rect.move_ip(-box.speed,0)
                    #box.vector.x -= box.speed

 
        self.rect.move_ip(0, self.vector.y)

        if self == player:
            if self.hooked[0]:
                x,y = self.hooked[0].rect.center
                pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]],[x,y])
                dist_x = abs(x - self.rect.center[0])
                dist_y = abs(y - self.rect.center[1])
                dist = self.hooked[1]
                distt = (dist_x**2+dist_y**2)**0.5
                pygame.draw.rect(screen,[0,0,0],(x-dist, y-dist, dist*2, dist*2), 2)

                if dist_y >= dist:
                    self.move(5, -2*self.vector.y)
                
                elif distt > dist:

                    if self.rect.center[1] < y:
                        new_x = ((((dist**2-dist_y**2)**0.5))-dist_x).real
                    else: new_x = -((((dist**2-dist_y**2)**0.5))-dist_x).real

                    if (self.rect.center[0] < x and self.rect.center[1] < y) or (self.rect.center[0] > x and self.rect.center[1] > y):
                        new_x *= -1

                    self.move(new_x, 0)
        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for block in block_hit_list:
            if block != self:
                if self.vector.y > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                elif self.vector.y < 0:
                    self.rect.top = block.rect.bottom
                self.vector.y = 0

        box_hit_list = pygame.sprite.spritecollide(self, boxes, False)
        for box in box_hit_list:
            if box != self:
                if (self.vector.y-box.vector.y) > 0:
                    self.rect.bottom = box.rect.top
                    self.onGround = True
                    box.vector.y += box.speed
                elif (self.vector.y-box.vector.y) < 0:
                    self.rect.top = box.rect.bottom
                    box.vector.y -= box.speed
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

        if self.onGround:
            self.freefall = False

    def hp_change(self, hp):
        self.hp += hp
        if self.hp < 0:
            if self in boxes:
                for i in range(5):
                    coin = Coin(list(self.rect.midbottom))
                    self.kill()
                    coin.vector.y -= 7
                    coin.vector.x += random.choice([-2,2,2.5,-2.5,1,-1,1.5,-1.5, 1.2,-1.2,2.2,-2.2])
            self.kill()
        
            
class Creature(Gravity_thing):
    def __init__(self, position, speed, max_hp):
        super(Creature, self).__init__(position, speed, max_hp, 1)
        self.gun_ready = True
        self.max_hp = max_hp
        self.hp = max_hp
        self.direction = "right"
        self.free_flight = False
        

    def hp_bar(self):
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.max_hp, 5), 2)
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.hp, 5))


    def update(self):
        if isinstance(self, Player):
            coin_collisions = pygame.sprite.spritecollide(self, coins, False)
            for coin in coin_collisions:
                self.coins += 1
                coin.kill()

            if self.hooked[0]:
##                x,y = self.hooked[0].rect.center
##                pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]],[x,y])
##                dist_x = abs(x - self.rect.center[0])
##                dist_y = abs(y - self.rect.center[1])
##                dist = self.hooked[1]
##                pressed_keys = pygame.key.get_pressed()
##                if pressed_keys[K_SPACE]:
##                    self.hooked = [False, dist]
##
####                vector_y = self.hooked[2]
####
####                if x - self.rect.center[0] > 0:
####                    vector_y = 5
####                else: vector_y = -5
####                if self.direction == "left":
####                    vector_y *= -1
####                   
##                #vector_y += 0.3
##
##               # if event.type == pygame.MOUSEBUTTONUP:
##                x1,y1 = pygame.mouse.get_pos()
##                
##                dist_x = abs(x - x1)
##                dist_y = abs(y - y1)
##                distt = (dist_x**2+dist_y**2)**0.5
##
##                pygame.draw.rect(screen,[0,0,0],(x-dist, y-dist, dist*2, dist*2), 2)



##                if distt > dist:
##                    if x1 < x:
##                        new_y = ((dist**2 - dist_x**2)**0.5 - dist_y).real
##                    else: new_y = -((dist**2 - dist_x**2)**0.5 - dist_y).real
##
##                    if y1 < y:
##                        new_x = ((((dist**2-dist_y**2)**0.5))-dist_x).real
##                    else: new_x = -((((dist**2-dist_y**2)**0.5))-dist_x).real
##
##                    if (x1 < x and y1 < y) or (x1 > x and y1 > y):
##                        new_x *= -1
##                        new_y *= -1
##
##
##                    
##                    #print(x1, y1, new_x, new_y)
##                    
##                    pygame.draw.rect(screen,[0,0,0],(x1, y1 + new_y, 5, 5), 2)
##                    pygame.draw.rect(screen,[255,0,0],(x1 + new_x, y1, 5, 5), 2)

                    
##                    node = Node([x1,new_y], rope)
##                    node.stick([x1,new_y])
##                    node2 = Node([new_x,y1], rope)
##                    node2.stick([new_x, y1])

                
##                self.move(self.vector.x, 0)
##
##                dist_x = abs(x - (self.rect.center[0] + self.vector.x))
##                dist_y = abs(y - self.rect.center[1])
##
##                if self.rect.center[0] < x:
##                    i = 1
##                else:
##                    i = -1
##                    
##
##                #if (dist_x**2+dist_y**2)**0.5 > dist+2:
##                needed_y = (i*((((dist**2-dist_x**2)**0.5))-dist_y)).real
##                #self.move(-self.vector.x, i*((((dist**2-dist_x**2)**0.5))-dist_y))
##                #if isinstance(i*((((dist**2-dist_x**2)**0.5))-dist_y), float):
##                #print(needed_y)
##                #self.move(0, i*needed_y)
##                print("y: ", needed_y)
##
##                if not needed_y*100 in range(-1,1) and not abs(needed_y) > 30:
##                    self.move(0, needed_y)
##                else:
##                    print("X")
##                    self.move(-self.vector.x, 0)
##                
##                self.move(0, self.vector.y)
##
##                dist_x = abs(x - self.rect.center[0])
##                dist_y = abs(y - (self.rect.center[1] + self.vector.y))
##
##                if self.rect.center[0] < x:
##                    i = 1
##                else:
##                    i = -1
##
##                #print(self.direction)
##                #print(dist, dist_x, dist_y)
##                
##                #if (dist_x**2+dist_y**2)**0.5 > dist+2:
##                needed_x = (i*((((dist**2-dist_y**2)**0.5))-dist_x)).real
##                print("x: ", needed_x)
##                #print()
##                if not needed_x*100 in range(-1, 1) and not abs(needed_x) > 30:
##                    self.move(needed_x, 0)
##                else:
##                    print("Y")
##                    self.move(0, -self.vector.y)
                #self.move(i*abs(self.vector.y), 0)
                
                #dist_y = abs(y - self.rect.center[1] + abs(vector_y))
                #self.rect.move_ip(i*((((dist**2-dist_y**2)**0.5))-dist_x), vector_y)
                
##                if dist_x >= dist:
##                    if self.direction == "right":
##                        self.direction = "left"
##                    else: self.direction = "right"
##                self.hooked[2] = vector_y
                    
                self.vector.y *= 0.85

                if self.vector.y < 0:
                    self.vector.y *= 1.2
                
                self.vector.x *= 0.85
                pass

            elif self.freefall:
                pass
            else: self.vector.x = 0               

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
                        self.move(0, -14)
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


            else:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_SPACE]:
                    self.hooked = [False, 0]
                    self.freefall = True
                    self.vector *= 1.3
                
 

        else:
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
            
        self.moving()

    def shoot(self):
        if self.gun_ready:
            if self.direction == "right":
                bullet = Bullet([self.rect.midright, self.direction])
            else: bullet = Bullet([self.rect.midleft, self.direction])
            self.gun_ready = False
            pygame.time.set_timer(RELOAD, 700)


class Player(Creature):
    def __init__(self):
        super().__init__([SCREEN_WIDTH//2, SCREEN_HEIGHT//2], 8, 100)
        self.coins = 0
        self.onRope = False
        self.hooked = [False, False, 0]


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
    def __init__(self, position):
        super(Hook, self).__init__()
        x = player.rect.center[0]
        y = player.rect.center[1]-25
        self.node = None
        vector_x = (x - position[0])/40
        if vector_x > 0:
            vector_x = min(vector_x, 15)
        else: vector_x = max(vector_x, -15)
        vector_y = (y - position[1])/40
        if vector_y > 0:
            vector_y = min(vector_y, 15)
        else: vector_y = max(vector_y, -15)
        if vector_x > 0:
            vector_x = min(vector_y, 15)
        while not sum([wall.rect.collidepoint(x,y) for wall in walls]):
            #pygame.draw.line(screen, [0,0,0], [player.rect.center[0], player.rect.center[1]],[x,y])
            #pygame.display.flip()
            x -= vector_x
            y -= vector_y
        node = Node([x,y], self)
        node.stick([x,y])
        self.node = node

        dist_x = abs(x - player.rect.center[0])
        dist_y = abs(y - player.rect.center[1])
        dist = (dist_x**2+dist_y**2)**0.5
                
        player.hooked = [self.node, dist]
        
                

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
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
        if pygame.sprite.spritecollideany(self, boxes):
            self.velocity = 0.01
            

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface([80,50])
        self.surf.fill([200,200,200])
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

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

x = y = 0
for row in level:
    for col in row:
        if col == "P":
            platform = Wall([x,y], [200,200,200], walls, all_sprites)
        if col == "S":
            platform = Wall([x,y], [100,100,100], all_sprites, spikes)
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

running = True
target = player
i = -1
while running:
    i += 1
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                pygame.display.quit()
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
        elif event.type == pygame.MOUSEBUTTONUP:
              x,y = pygame.mouse.get_pos()
              hook = Hook([x,y])

    #x,y = pygame.mouse.get_pos()
    #rope.nodes[2].rect.center = [x,y]
    screen.fill((135, 206, 250))
    offset_x, offset_y = camera.update(target)
    clouds.update()
    bullets.update()
    water.update()
    for entity in all_sprites:
        if entity != player:
            entity.rect.move_ip(offset_x, offset_y)
        if not isinstance(entity, Water):
            screen.blit(entity.surf, entity.rect)

    for water_block in water:
        screen.blit(water_block.surf, water_block.rect)
    
    for gravity_thing in gravity_things:
        if pygame.sprite.spritecollideany(gravity_thing, bullets):
            gravity_thing.hp_change(-20)
        if gravity_thing != player:
            gravity_thing.update()

            
    coins_sign.kill()
    coins_sign = Sign([10,10], ['Coins: ', player.coins], 30, [0,0,0])
    for sign in signs:
        screen.blit(sign.textsurface,sign.position)
        
    pygame.display.flip()
    clock.tick(100)
