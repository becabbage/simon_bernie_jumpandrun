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


while game_is_running:
    screen.blit(background_image,(0,0))
    draw_grid()
    draw_grid_labels()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running=False
    pygame.display.update()

pygame.quit()
