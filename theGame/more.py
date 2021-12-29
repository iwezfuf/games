import random
import pygame
import pygame.freetype
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
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
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP                                          PP",
        "PP                                     B    PP",
        "PP                                          PP",
        "PP                    PPPPPPPPPPP           PP",
        "PP                                          PP",
        "PP               WWWWWWWWW                  PP",
        "PP                WWWWWW                    PP",
        "PP PPPPPPPPPPPPPPPWWWWW                     PP",
        "PP                                          PP",
        "PP                    B     SSSSSSS         PP",
        "PP                 PPPPPP                   PP",
        "PP          1                               PP",
        "PP         PPPPPPP                          PP",
        "PP                      3                   PP",
        "PP                     PPPPPP               PP",
        "PP          B                               PP",
        "PP   PPPPPPPPPPP                            PP",
        "PP                       B                  PP",
        "PP                 PPPPPPPPPPP  P  WWWWWWW  PP",
        "PP                              P  WWWWWWW  PP",
        "PP                              P  WWWWWWW  PP",
        "PP                              P  WWWWWWW  PP",
        "PP                              P  WWWWWWW  PP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]


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
    def __init__(self, position, speed, max_hp):
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
        self.inWater = False
        all_sprites.add(self)
        gravity_things.add(self)


    def move(self, x, y):
        self.vector.x += x
        self.vector.y += y
        if x > 0:
            self.direction = "right"
        elif x < 0:
            self.direction = "left"

    def gravity(self):
        #if not self.onGround:
            self.vector += gravity
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
            
        if self.vector.y > 0:
            self.vector -= friction_y
        if self.vector.y < 0:
            self.vector += friction_y
        if self.vector.x > 0:
            self.vector -= friction_x
        if self.vector.x < 0:
            self.vector += friction_x
                

    def moving(self):
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
##        if isinstance(self, Node):
##            dist_x1, dist_x2, dist_y1, dist_y2 = self.dist()
##            if dist_x1 > 70:
##                index = self.rope.nodes.index(self)
##                the_node = self.rope.nodes[index-1]
##                if self.vector.x > 0:
##                    the_node.move(the_node.speed, 0)
##                else: the_node.move(-the_node.speed, 0)
##            if dist_x2 > 70:
##                index = self.rope.nodes.index(self)
##                the_node = self.rope.nodes[index+1]
##                if self.vector.x > 0:
##                    the_node.move(the_node.speed, 0)
##                else: the_node.move(-the_node.speed, 0)

        if isinstance(self, Node):
            dist_x1, dist_x2, dist_y1, dist_y2 = self.dist()
            #if dist_y1 <= 0 and dist_y2 <= 0:
            self.rect.move_ip(-dist_x1/10,0)
            self.rect.move_ip(-dist_x2/10,0)
            self.rect.move_ip(0, -dist_y1)
            self.rect.move_ip(0, -dist_y2)
##        if isinstance(self, Node):
##            index = self.rope.nodes.index(self)
##            the_node = self.rope.nodes[index-1]
##            the_node.move(self.vector.x,0)
##            if self.rect.left - the_node.rect.left > 70:
##                self.vector.x = -2
##            elif self.rect.left - the_node.rect.left < 70:
##                self.vector.x = 2
##            if index > len(self.rope.nodes):
##                self.rect.move_ip(self.vector.x, 0)
            
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
                if self.vector.x > 0:
                    self.rect.right = box.rect.left
                    box.rect.move_ip(box.speed,0)
                    #box.vector.x += box.speed
                elif self.vector.x < 0:
                    self.rect.left = box.rect.right
                    box.rect.move_ip(-box.speed,0)
                    #box.vector.x -= box.speed
 

        self.rect.move_ip(0, self.vector.y)
        
##        if isinstance(self, Node):
##            dist_x1, dist_x2, dist_y1, dist_y2 = self.dist()
##            if dist_y1 > 70:
##                index = self.rope.nodes.index(self)
##                the_node = self.rope.nodes[index-1]
##                if self.vector.y > 0:
##                    the_node.move(0, the_node.speed)
##                else: the_node.move(0, -the_node.speed)
##            if dist_y2 > 70:
##                index = self.rope.nodes.index(self)
##                the_node = self.rope.nodes[index+1]
##                if self.vector.y > 0:
##                    the_node.move(0, the_node.speed)
##                else: the_node.move(0, -the_node.speed)

##        if isinstance(self, Node):
##            index = self.rope.nodes.index(self)
##            the_node = self.rope.nodes[index-1]
##            the_node.move(self.vector.y,0)
##            print(self.rect.top - the_node.rect.top)
##            if self.rect.top - the_node.rect.top > 70:
##                self.vector.y = -2
##            elif self.rect.top - the_node.rect.top < 70:
##                self.vector.y = 2
##            if index > len(self.rope.nodes):
##                self.rect.move_ip(0, self.vector.y)

                
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
                if self.vector.y > 0:
                    self.rect.bottom = box.rect.top
                    self.onGround = True
                    #box.vector.y -= box.speed
                elif self.vector.y < 0:
                    self.rect.top = box.rect.bottom
                    #box.vector.y -= box.speed
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
        super(Creature, self).__init__(position, speed, max_hp)
        self.gun_ready = True
        self.max_hp = max_hp
        self.hp = max_hp
        self.direction = "right"
        

    def hp_bar(self):
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.max_hp, 5), 2)
        pygame.draw.rect(screen,[255,0,0],(self.rect.left-self.max_hp*0.25+self.rect.width//2, self.rect.top-30, 0.5*self.hp, 5))


    def update(self):
        self.vector.x = 0
        if isinstance(self, Player):
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP] and self.onGround:
                self.move(0, -14)
                self.onGround = False
            if pressed_keys[K_DOWN] and self.onGround:
                self.move(0,-10)
            if pressed_keys[K_DOWN]:
                self.move(8,0)
            if pressed_keys[K_LEFT]:
                self.move(-self.speed, 0)
            if pressed_keys[K_RIGHT]:
                self.move(self.speed, 0)
            if pressed_keys[K_SPACE]:
                self.shoot()

            coin_collisions = pygame.sprite.spritecollide(self, coins, False)
            for coin in coin_collisions:
                self.coins += 1
                coin.kill()
                

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


class Coin(Gravity_thing):
    def __init__(self, position):
        super(Coin, self).__init__(position, 10, 5000)
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
        super(Box, self).__init__(position, speed, max_hp)
        boxes.add(self)
        
    def update(self):
        self.moving()
        self.vector.x = 0

class Soldier(Creature):
    def __init__(self, position, path):
        super().__init__(position, 3, 50)
        self.left = position
        self.right = path


class Node(Gravity_thing):
    def __init__(self, position, rope):
        super(Node, self).__init__(position, 1, 5000)
        self.surf = pygame.Surface([5,5])
        self.surf.fill([176, 134, 18])
        self.rect = self.surf.get_rect(bottomleft=position)
        self.rope = rope
        gravity_things.add(self)
        boxes.add(self)

    def update(self):
        self.moving()
        self.vector.x = 0

    def dist(self):
        index = self.rope.nodes.index(self)
        dist_x1 = self.rect.left - self.rope.nodes[index-1].rect.left
        dist_y1 = self.rect.top - self.rope.nodes[index-1].rect.top
        if index == 0:
            dist_x1 = dist_y1 = 0.01
        try:
            dist_x2 = self.rect.left - self.rope.nodes[index+1].rect.left
            dist_y2 = self.rect.top - self.rope.nodes[index+1].rect.top
        except IndexError:
            dist_x2 = dist_y2 = 0.01
        return dist_x1, dist_x2, dist_y1, dist_y2

##    def dist(self):
##        index = self.rope.nodes.index(self)
##        try:
##            dist_x = self.rect.left - self.rope.nodes[index-1].rect.left
##            dist_y = self.rect.top - self.rope.nodes[index-1].rect.top
##        except IndexError:
##            dist_x = dist_y = 0
##        if index == 0:
##            dist_x = dist_x = 0
##        return dist_x, dist_y
##

class Rope(pygame.sprite.Sprite):
    def __init__(self, position, lenght):
        super(Rope, self).__init__()
        self.position = position
        self.lenght = lenght
        self.nodes = []
        #all_sprites.add(self)
        for i in range(lenght):
            node = Node([position[0]+i*60,position[1]], self)
            self.nodes.append(node)

##    def update(self):
##        for i in range(len(self.nodes)-1):
##            node1 = self.nodes[i]
##            node2 = self.nodes[i+1]
##            dist = abs(node1.rect.left - node2.rect.left)
##            if dist > 60:
##                pass
                
                #node1.rect.left = node2.rect.left+10
                #node1.vector.x -= 5
                #node2.vector.x -= 5

                


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
player = Player()
coins_sign = Sign([10,10], ['Coins: ', player.coins], 30, [0,0,0])
rope = Rope([100,200], 8)

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
            
        x += TILE_SIZE
    y += TILE_SIZE
    x = 0

clock = pygame.time.Clock()

running = True
target = player
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                pygame.display.quit()
        elif event.type == QUIT:
            running = False
            pygame.display.quit()
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        elif event.type == RELOAD:
            player.gun_ready = True
    pygame.mouse.get_pressed
    x,y = pygame.mouse.get_pos()
    rope.nodes[7].rect.center = [x,y]
            
    screen.fill((135, 206, 250))
    offset_x, offset_y = camera.update(target)
    clouds.update()
    bullets.update()
    water.update()
    rope.update()
    for entity in all_sprites:
        if entity != player:
            entity.rect.move_ip(offset_x, offset_y)
        screen.blit(entity.surf, entity.rect)
    
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
    clock.tick(60)
