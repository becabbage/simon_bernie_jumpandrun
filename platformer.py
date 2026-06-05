#from pygame.locals import *
import pygame
from level_manager import get_map_files, load_level, get_level_name

pygame.init()

# Konstanten für die virtuelle Spielgröße
GAME_WIDTH = 1000
GAME_HEIGHT = 1000
FONT_SIZE_SMALL = 15
WHITE=(255,255,255)
BLACK=(0,0,0)

# Camera offset
camera_x = 0

# Ermittle verfügbare Bildschirmgröße
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Berechne optimale Fenstergröße
# Maximal 1200x1200, mindestens 600x600
max_size = min(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 1200)
min_size = 600

if GAME_WIDTH > max_size:
    # Skaliere runter wenn Bildschirm zu klein
    scale = max_size / GAME_WIDTH
elif GAME_WIDTH < min_size and SCREEN_WIDTH >= GAME_WIDTH and SCREEN_HEIGHT >= GAME_HEIGHT:
    # Skaliere hoch wenn Bildschirm groß genug
    scale = min(1.2, min_size / GAME_WIDTH)
else:
    # Verwende 1:1 wenn möglich
    scale = 1.0

WINDOW_WIDTH = int(GAME_WIDTH * scale)
WINDOW_HEIGHT = int(GAME_HEIGHT * scale)

# Vollbild-Modus
is_fullscreen = False
fullscreen_width = SCREEN_WIDTH
fullscreen_height = SCREEN_HEIGHT

# Erstelle echtes Fenster und virtuelle Spieloberfläche
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

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
    game_surface.blit(text_surface, (pos[0] - offset_x, pos[1] - offset_y))

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
        coin_group.empty()
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
                if tile==4 or tile==5:
                    # Create coins at positions marked with 4 or 5
                    coin = Coin(col_count * tile_size, row_count * tile_size)
                    coin_group.add(coin)
                if tile==6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + int(tile_size//2) )
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            game_surface.blit(tile[0], (tile[1].x - camera_x, tile[1].y))

    def print_tile_list(self):
        print(self.tile_list)


def select_level():
    """
    Display a level selection dialog in a Pygame window.
    
    Returns:
        Tuple of (level_name, world_data)
    """
    map_files = get_map_files()
    
    if not map_files:
        print("ERROR: Keine .map Dateien gefunden!")
        print("Bitte erstelle mindestens eine .map Datei im Spieleverzeichnis.")
        exit(1)
    
    # Create a dedicated selection window
    pygame.display.set_caption("Level Auswahl")
    clock = pygame.time.Clock()
    
    # Fonts for the dialog
    title_font = pygame.font.Font(None, 60)
    level_font = pygame.font.Font(None, 40)
    hint_font = pygame.font.Font(None, 25)
    
    # Calculate level button positions
    level_names = [get_level_name(f) for f in map_files]
    button_width = 300
    button_height = 60
    button_spacing = 20
    total_height = len(map_files) * (button_height + button_spacing) + 100
    
    selected_index = 0
    selection_done = False
    
    while not selection_done:
        clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            
            if event.type == pygame.KEYDOWN:
                # Number keys (1-9) to select levels
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_1
                    if num < len(map_files):
                        selected_index = num
                
                # Arrow keys for navigation
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(map_files)
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(map_files)
                
                # Enter to confirm
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selection_done = True
            
            # Mouse click detection
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_y = event.pos[1]
                for i in range(len(map_files)):
                    button_y = 150 + i * (button_height + button_spacing)
                    if button_y <= mouse_y <= button_y + button_height:
                        selected_index = i
                        selection_done = True
                        break
        
        # Draw the dialog window
        game_surface.fill((70, 130, 180))  # Steel blue background
        
        # Draw title
        title_text = title_font.render("Level Auswahl", True, WHITE)
        title_rect = title_text.get_rect(center=(GAME_WIDTH // 2, 30))
        game_surface.blit(title_text, title_rect)
        
        # Draw level buttons
        for i, level_name in enumerate(level_names):
            button_y = 150 + i * (button_height + button_spacing)
            button_x = GAME_WIDTH // 2 - button_width // 2
            
            # Highlight selected level
            if i == selected_index:
                color = (255, 200, 0)  # Gold for selected
                pygame.draw.rect(game_surface, color, (button_x, button_y, button_width, button_height))
                pygame.draw.rect(game_surface, WHITE, (button_x, button_y, button_width, button_height), 3)
            else:
                color = (100, 150, 200)  # Lighter blue for unselected
                pygame.draw.rect(game_surface, color, (button_x, button_y, button_width, button_height))
                pygame.draw.rect(game_surface, WHITE, (button_x, button_y, button_width, button_height), 2)
            
            # Draw level number and name
            level_text = level_font.render(f"{i+1}. {level_name}", True, BLACK)
            text_rect = level_text.get_rect(center=(GAME_WIDTH // 2, button_y + button_height // 2))
            game_surface.blit(level_text, text_rect)
        
        # Draw instructions
        hint_text = hint_font.render("Zahlen/Pfeile zum Wählen, Enter zum Bestätigen", True, WHITE)
        hint_rect = hint_text.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT - 40))
        game_surface.blit(hint_text, hint_rect)
        
        # Scale and display
        scale_x = WINDOW_WIDTH / GAME_WIDTH
        scale_y = WINDOW_HEIGHT / GAME_HEIGHT
        scale_factor = min(scale_x, scale_y)
        scaled_width = int(GAME_WIDTH * scale_factor)
        scaled_height = int(GAME_HEIGHT * scale_factor)
        offset_x = (WINDOW_WIDTH - scaled_width) // 2
        offset_y = (WINDOW_HEIGHT - scaled_height) // 2
        scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
        screen.fill(BLACK)
        screen.blit(scaled_surface, (offset_x, offset_y))
        pygame.display.update()
    
    # Load the selected level
    selected_file = map_files[selected_index]
    level_name = get_level_name(selected_file)
    world_data = load_level(selected_file)
    
    return level_name, world_data


# Load level from selection dialog
level_name, world_data = select_level()

# Set window title with level name
pygame.display.set_caption(f"Platformer - Level: {level_name}")

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
        game_surface.blit(self.image, (self.rect.x, self.rect.y))

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
        self.direction=1
        self.total_coins = len(coin_group)
        self.coins_collected = 0
        for num in range(1,5):
            img_left=pygame.image.load(f'res/resized_van{num}.png')
            img_left=pygame.transform.scale(img_left,(40,80))
            img_right=pygame.transform.flip(img_left,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image=pygame.image.load(f'res/ghost.png')
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        # Verwende Float-Positionen für präzise Bewegung
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.vel_y = 0.0
        self.vel_x = 300.0  # Pixel pro Sekunde
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
                if tile[1].colliderect(self.x + dx, self.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.x, self.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.y
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - (self.y + self.height)
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
            
            # collect coins
            collected_coins = pygame.sprite.spritecollide(self, coin_group, False)
            for coin in collected_coins:
                coin.collect()
                self.coins_collected += 1
                print(f'Coin collected! Total: {self.coins_collected}/{self.total_coins}')

            #update player coordinates (Float-Positionen)
            self.x += dx
            self.y += dy
            
            # Calculate map width based on world_data
            map_width = len(world_data[0]) * tile_size
            
            # Keep player within map boundaries
            if self.x < 0:
                self.x = 0
            if self.x + self.width > map_width:
                self.x = map_width - self.width

            # stop the player from falling below ground
            if self.y + self.height > GAME_HEIGHT:
                self.y = GAME_HEIGHT - self.height
                self.vel_y = 0
                self.in_air = False
            
            # Sync rect with float positions for rendering
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        #draw player onto screen
        game_surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

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
        game_surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))

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
        game_surface.blit(self.image, self.rect)

    def reset(self) -> None:
        pass

class Coin(pygame.sprite.Sprite):
    '''
    Coin class representing collectible multivitamin juices
    '''
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('res/multivitaminsaft.png'), (int(tile_size * 0.6), int(tile_size * 0.6)))
        self.rect = self.image.get_rect()
        self.rect.center = (x + tile_size // 2, y + tile_size // 2)
        self.collected = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        if not self.collected:
            game_surface.blit(self.image, self.rect)

    def collect(self) -> None:
        self.collected = True
        self.kill()

blob_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
world=World(world_data)
# world.print_tile_list() # this prints the tile list of the world
# Start player at the left end of the level
PLAYER_START_X = 10
PLAYER_START_Y = 900
player=Player(PLAYER_START_X, PLAYER_START_Y)

fps=60
clock=pygame.time.Clock()
restart_button=Button(300,250,pygame.image.load('res/restart_button.png'),pygame.K_r)
quit_button=Button(600,250,pygame.image.load('res/quit_button.png'),pygame.K_q)

#################################################################
# GAME LOOP
#################################################################

while game_is_running:
    delta_time = clock.tick(fps) / 1000.0  # Convert milliseconds to seconds
    game_surface.blit(background_image,(0,0))
    #draw_grid()
    #draw_grid_labels()
    
    # Update camera to follow player
    map_width = len(world_data[0]) * tile_size
    camera_x = player.rect.x - WINDOW_WIDTH // 2 + player.rect.width // 2
    camera_x = max(0, camera_x)  # Don't go past left edge
    camera_x = min(camera_x, map_width - WINDOW_WIDTH)  # Don't go past right edge
    
    world.draw()
    # Draw coins with camera offset
    for coin in coin_group:
        if not coin.collected:
            game_surface.blit(coin.image, (coin.rect.x - camera_x, coin.rect.y))
    # Draw lava with camera offset
    for lava in lava_group:
        game_surface.blit(lava.image, (lava.rect.x - camera_x, lava.rect.y))
    # Draw enemies with camera offset
    for blob in blob_group:
        blob.draw()
    
    # Draw coin counter
    if game_over == 0:
        coin_font = pygame.font.Font(None, 35)
        coin_text = coin_font.render(f"Coins: {player.coins_collected}/{player.total_coins}", True, WHITE)
        game_surface.blit(coin_text, (10, 10))

    #print(f'Game Over: {game_over}')

    if game_over == 0:
        #lava_group.update()
        blob_group.update()
        # player.print_player_debug_info() # this is to print the players position and velocity
        game_over=player.update(game_over, delta_time)

    if game_over == 1:
        game_surface.blit(player.dead_image, (player.rect.x - camera_x, player.rect.y))
        player.rect.y -= 5  # Move the dead image upwards
        if player.rect.y + player.rect.height < 0:  # Check if the image is out of the screen
            if restart_button.draw() == True:
                game_surface.blit(player.image, (player.rect.x - camera_x, player.rect.y))
                world.reset_world(world_data)
                player.reset(PLAYER_START_X, PLAYER_START_Y)
                game_over = 0
            if quit_button.draw() == True:
                game_is_running = False
                game_over = 0
            #game_is_running = False  # End the game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                # Toggle Vollbild-Modus
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((fullscreen_width, fullscreen_height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Skaliere die virtuelle Spieloberfläche auf das echte Fenster
    current_width = fullscreen_width if is_fullscreen else WINDOW_WIDTH
    current_height = fullscreen_height if is_fullscreen else WINDOW_HEIGHT
    
    # Berechne Skalierung mit Seitenverhältnis für Vollbild
    if is_fullscreen:
        scale_x = current_width / GAME_WIDTH
        scale_y = current_height / GAME_HEIGHT
        scale_factor = min(scale_x, scale_y)
        scaled_width = int(GAME_WIDTH * scale_factor)
        scaled_height = int(GAME_HEIGHT * scale_factor)
        offset_x = (current_width - scaled_width) // 2
        offset_y = (current_height - scaled_height) // 2
        scaled_surface = pygame.transform.scale(game_surface, (scaled_width, scaled_height))
        screen.fill(BLACK)  # Schwarze Balken
        screen.blit(scaled_surface, (offset_x, offset_y))
    else:
        scaled_surface = pygame.transform.scale(game_surface, (current_width, current_height))
        screen.blit(scaled_surface, (0, 0))
    
    pygame.display.update()

pygame.quit()
