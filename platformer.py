#from pygame.locals import *
import pygame

pygame.init()

# Konstanten
WINDOW_HEIGHT=1000
WINDOW_WIDTH=1000
FONT_SIZE_SMALL = 15
WHITE=(255,255,255)
BLACK=(0,0,0)

screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Platformer Tutorial")

tile_size=50
game_is_running=True

background_image=pygame.image.load('res/sky.png')

###################### FUNCTIONS #########################

def draw_text(text, pos, font, color=BLACK, background=WHITE, anchor='center'):
    text_surface = font.render(text, True, color, background)
    offset_y=0
    offset_x=0
    if anchor == 'center':
        offset_x = text_surface.get_width() / 2
        offset_y = text_surface.get_height() / 2
    elif anchor == 'left':
        offset_x = 0
        offset_y = text_surface.get_height() / 2
    elif anchor == 'top':
        offset_x = text_surface.get_width() / 2
        offset_y = 0
    screen.blit(text_surface, (pos[0] - offset_x, pos[1] - offset_y))

def draw_grid_labels():
    myfont = pygame.font.Font(None, FONT_SIZE_SMALL) 
    draw_text("(x,y)", (FONT_SIZE_SMALL, tile_size/2), myfont, BLACK, WHITE, 'center')

    # Y-Koordinaten am linken Rand
    for y_label in range(1, WINDOW_HEIGHT // tile_size):
        grid_label_text = f"(0,{y_label * tile_size})"
        y_pos = y_label * tile_size
        draw_text(grid_label_text, (FONT_SIZE_SMALL, y_pos), myfont, BLACK, WHITE, 'left')

    # X-Koordinaten am oberen Rand
    for x_label in range(1, WINDOW_WIDTH // tile_size):
        grid_label_text = f"({x_label * tile_size},0)"
        x_pos = x_label * tile_size
        draw_text(grid_label_text, (x_pos, FONT_SIZE_SMALL), myfont, BLACK, WHITE, 'top')

def draw_grid():
    for line in range(0,int(WINDOW_WIDTH/tile_size)):
        pygame.draw.line(screen,WHITE,(0,line*tile_size),(WINDOW_WIDTH,line*tile_size),1)
        pygame.draw.line(screen,WHITE,(line*tile_size,0),(line*tile_size,WINDOW_HEIGHT),1)

###################### CLASSES #########################

class World():
    def __init__(self, data):
        self.tile_list = []

        dirt_image=pygame.image.load('res/dirt.png')
        grass_image=pygame.image.load('res/grass.png')

        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile==1:
                    img = pygame.transform.scale(dirt_image, (tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==2:
                    img = pygame.transform.scale(grass_image, (tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def print_tile_list(self):
        print(self.tile_list)

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0], 
[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0], 
[0, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0], 
[0, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2], 
[0, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[2, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Player:
    def __init__(self,x ,y) -> None:
        #img = pygame.image.load('res/guy1.png')
        #self.image = pygame.transform.scale(img, (40, 80))
        #self.rect = self.image.get_rect()
        # self.jumped = False
        self.player_jumped = False
        self.counter=0
        self.index=0
        self.images_right=[]
        self.images_left=[]
        self.direction=0
        for num in range(1,5):
            img_right=pygame.image.load(f'res/guy{num}.png')
            img_right=pygame.transform.scale(img_right,(40,80))
            img_left=pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x = x  # Linke Ecke von Player-Rect
        self.rect.y = y # Linke Ecke von Player-Rect
        self.vel_y = 0
        self.vel_x = 5
        self.width=self.image.get_width()
        self.height=self.image.get_height()

    def print_player_debug_info(self) -> None:
        print(f'X: {self.rect.x} Y: {self.rect.y} vel_x: {self.vel_x} vel-y: {self.vel_y}')

    def update(self) -> None:
        walking_cooldown=5
        dx = 0
        dy = 0

        #get keypressesey
        key = pygame.key.get_pressed()
  
        if key[pygame.K_LEFT] and self.rect.x>0:
            dx-=self.vel_x
            self.counter += 1
            self.direction = -1

        if key[pygame.K_RIGHT] and (self.rect.x<WINDOW_WIDTH - self.rect.width): 
            dx+=self.vel_x
            self.counter += 1
            self.direction = 1

        # Jumping
        if (self.player_jumped == False) and key[pygame.K_SPACE]:
            self.vel_y=-15
            self.player_jumped=True

        # Jumping motion
        if key[pygame.K_SPACE]==False:
            self.player_jumped=False
        
        # Handle Animation

        if self.counter > walking_cooldown:
            self.counter = 0    
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # TODO: check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0



        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # stop the player from falling below ground
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            dy = 0


        #draw player onto screen
        screen.blit(self.image, self.rect)

        pygame.draw.rect(screen,WHITE,self.rect,width=2)

world=World(world_data)
world.print_tile_list()
player=Player(500,500)
fps=60
clock=pygame.time.Clock()

#################################################################
# GAME LOOP
#################################################################

while game_is_running:
    clock.tick(fps)
    screen.blit(background_image,(0,0))
    #draw_grid()
    #draw_grid_labels()
    world.draw()
    player.print_player_debug_info()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running=False

    pygame.display.update()

pygame.quit()
