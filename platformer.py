#from pygame.locals import *
import pygame

pygame.init()

# Konstanten
WINDOW_HEIGHT=1000
WINDOW_WIDTH=1000
FONT_SIZE_SMALL = 15
WHITE=(255,255,255)
BLACK=(0,0,0)

# Camera offset
camera_x = 0

screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Platformer Tutorial")

tile_size=50
game_over=0 # 0 = False, 1 = True

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
        self.reset_world(data)

    def reset_world(self, data):
        blob_group.empty()
        lava_group.empty()
        dirt_image=pygame.image.load('res/dirt.png')
        grass_image=pygame.image.load('res/grass.png')
        lava_group
        self.tile_list = []
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
                if tile==3:
                    # create a enemy based on the Enemy class. Position the enemy based on the col_count and row_count 
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile==6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + int(tile_size//2) )
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - camera_x, tile[1].y))

    def print_tile_list(self):
        print(self.tile_list)

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], 
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
[0, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[2, 0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Button():
    def __init__(self, x, y, image, shortcut_key:pygame.key) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.shortcut_key = shortcut_key

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        key = pygame.key.get_pressed()

        if key[self.shortcut_key]:
            action = True

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Player:
    def __init__(self,x ,y) -> None:
        self.reset(x,y)

    def reset(self,x,y) -> None:
        self.player_jumped = False
        self.in_air = True
        self.counter=0
        self.index=0
        self.images_right=[]
        self.images_left=[]
        self.direction=0
        for num in range(1,5):
            img_left=pygame.image.load(f'res/resized_van{num}.png')
            img_left=pygame.transform.scale(img_left,(40,80))
            img_right=pygame.transform.flip(img_left,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image=pygame.image.load(f'res/ghost.png')
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x = x  # Linke Ecke von Player-Rect
        self.rect.y = y # Linke Ecke von Player-Rect
        self.vel_y = 0
        self.vel_x = 300  # Pixel pro Sekunde
        self.width=self.image.get_width()
        self.height=self.image.get_height()

    def print_player_debug_info(self) -> None:
        print(f'X: {self.rect.x} Y: {self.rect.y} vel_x: {self.vel_x} vel-y: {self.vel_y}')

    def update(self, game_over, delta_time) -> int:
        walking_cooldown=0.1  # Sekunden zwischen Animationsframes
        dx = 0
        dy = 0
        is_moving = False

        #get keypresses
        key = pygame.key.get_pressed()
        if game_over == 0:
            if key[pygame.K_LEFT]:
                dx -= self.vel_x * delta_time
                self.direction = -1
                is_moving = True

            if key[pygame.K_RIGHT]: 
                dx += self.vel_x * delta_time
                self.direction = 1
                is_moving = True

            # Jumping
            if (self.player_jumped == False) and key[pygame.K_SPACE] and (self.in_air == False):
                self.vel_y = -750  # Pixel pro Sekunde
                self.player_jumped = True
                self.in_air = True

            # Jumping motion
            if key[pygame.K_SPACE] == False:
                self.player_jumped = False
            
            # Handle Animation
            if is_moving:
                self.counter += delta_time
                if self.counter > walking_cooldown:
                    self.counter -= walking_cooldown    
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
            else:
                self.counter = 0
                self.index = 0
            
            # Update image based on direction
            if self.direction == 1:
                self.image = self.images_right[self.index]
            elif self.direction == -1:
                self.image = self.images_left[self.index]

            # Gravity
            self.vel_y += 2500 * delta_time  # Pixel pro Sekunde pro Sekunde (Beschleunigung)
            if self.vel_y > 500:  # Max fall speed in Pixel pro Sekunde
                self.vel_y = 500
            dy += self.vel_y * delta_time
            self.in_air = True

            # check for collision
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
                        self.in_air = False

            # add collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                print('collision with enemy')
                game_over = 1
            
            # add collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                print('collision with lava')
                game_over = 1

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            
            # Calculate map width based on world_data
            map_width = len(world_data[0]) * tile_size
            
            # Keep player within map boundaries
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > map_width:
                self.rect.right = map_width

            # stop the player from falling below ground
            if self.rect.bottom > WINDOW_HEIGHT:
                self.rect.bottom = WINDOW_HEIGHT
                dy = 0
                self.in_air = False

        #draw player onto screen
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

        # This draws the player rectangle
        #pygame.draw.rect(screen, WHITE, self.rect, width=2)

        return game_over

class Enemy(pygame.sprite.Sprite):
    '''
        Create Enemy class here that is a child class of pygame.sprite.Sprite
        it should have a constructor that takes an x and y position
        it should have a method update that moves the enemy towards the player
        it should have a method draw that draws the enemy on the screen
        it should have a method collide that checks if the enemy collides with the player
        it should have a method reset that resets the enemy to a random position
        it should load the image 'res/blob.png'
    '''
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image_left = pygame.image.load('res/blob.png')
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.move_direction = 1
        self.move_counter = 0

    def update(self) -> None:
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter >= 50:
            self.move_direction *= -1
            self.move_counter = 0
            if self.move_direction == 1:
                self.image = self.image_right
            else:
                self.image = self.image_left
        elif self.move_counter == 25:
            self.rect.x = self.start_x

    def draw(self) -> None:
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def collide(self) -> None:
        pass

    def reset(self) -> None:
        self.rect.x = self.start_x
        self.move_counter = 0
        self.move_direction = 1
        self.image = self.image_right

class Lava(pygame.sprite.Sprite):
    '''
        Create a class called Lava that is a child class of pygame.sprite.Sprite
        it should have a constructor that takes an x and y position
        it should have a method update that checks if the player collides with the lava
        it should have a method draw that draws the lava on the screen
        it should have a method reset that resets the lava to a random position
        it should load the image 'res/lava.png' and scale it to the tile size
    '''
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('res/lava.png'), (tile_size, tile_size/2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self) -> None:
        pass

    def draw(self) -> None:
        screen.blit(self.image, self.rect)

    def reset(self) -> None:
        pass

blob_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
world=World(world_data)
# world.print_tile_list() # this prints the tile list of the world
player=Player(500,500)

fps=60
clock=pygame.time.Clock()
restart_button=Button(300,250,pygame.image.load('res/restart_button.png'),pygame.K_r)
quit_button=Button(600,250,pygame.image.load('res/quit_button.png'),pygame.K_q)

#################################################################
# GAME LOOP
#################################################################

while game_is_running:
    delta_time = clock.tick(fps) / 1000.0  # Convert milliseconds to seconds
    screen.blit(background_image,(0,0))
    #draw_grid()
    #draw_grid_labels()
    
    # Update camera to follow player
    map_width = len(world_data[0]) * tile_size
    camera_x = player.rect.x - WINDOW_WIDTH // 2 + player.rect.width // 2
    camera_x = max(0, camera_x)  # Don't go past left edge
    camera_x = min(camera_x, map_width - WINDOW_WIDTH)  # Don't go past right edge
    
    world.draw()
    # Draw lava with camera offset
    for lava in lava_group:
        screen.blit(lava.image, (lava.rect.x - camera_x, lava.rect.y))
    # Draw enemies with camera offset
    for blob in blob_group:
        blob.draw()

    #print(f'Game Over: {game_over}')

    if game_over == 0:
        #lava_group.update()
        blob_group.update()
        # player.print_player_debug_info() # this is to print the players position and velocity
        game_over=player.update(game_over, delta_time)

    if game_over == 1:
        screen.blit(player.dead_image, (player.rect.x - camera_x, player.rect.y))
        player.rect.y -= 5  # Move the dead image upwards
        if player.rect.y + player.rect.height < 0:  # Check if the image is out of the screen
            if restart_button.draw() == True:
                screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))
                world.reset_world(world_data)
                player.reset(500,500)
                game_over = 0
            if quit_button.draw() == True:
                game_is_running = False
                game_over = 0
            #game_is_running = False  # End the game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running=False

    pygame.display.update()

pygame.quit()
