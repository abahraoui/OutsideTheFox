import pygame
from pygame.locals import *
import sys
import button
import pickle

pygame.init()


# Event handler.
def events():
    global scroll_left
    global scroll_right
    global scroll_speed
    global level
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                scroll_left = True
            if event.key == K_RIGHT:
                scroll_right = True
            if event.key == K_LSHIFT:
                scroll_speed = 5
            if event.key == K_UP:
                level += 1
            if event.key == K_DOWN and level > 0:
                level -= 1

        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                scroll_left = False
            if event.key == K_RIGHT:
                scroll_right = False
            if event.key == K_LSHIFT:
                scroll_speed = 1


# Draws and makes the background scrollable.
def draw_bg():
    screen.fill('crimson')
    width = bg.get_width()
    for x in range(4):
        screen.blit(bg, ((x * width) - scroll * 0.5, 0))
        screen.blit(md, ((x * width) - scroll * 0.8, 300))
        screen.blit(md, ((x * width) - scroll * 0.8 + 400, 300))
        screen.blit(md, ((x * width) - scroll * 0.8 + 780, 300))


# Draws the grid.
def draw_grid():
    for col in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (col * TILE_SIZE - scroll, 0), (col * TILE_SIZE - scroll, H))

    for row in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (W, row * TILE_SIZE))


# Draw each tile based on position in the grid.
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tiles_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# Helper function to draw some text.
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Saves and loads level data using pickle.
def save_and_load():
    global world_data
    global scroll
    if save_button.draw(screen):
        pickle_out = open(f'level_data/level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()
        print(f'Saved Level {level}.')
    if load_button.draw(screen):
        scroll = 0
        world_data = []
        pickle_in = open(f'level_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)


# Highlights the selected tile in the editor.
def highlight_tile():
    global current_tile
    button_count = 0
    for button_count, button in enumerate(button_list):
        if button.draw(screen):
            current_tile = button_count
    pygame.draw.rect(screen, 'magenta', button_list[current_tile].rect, 3)


# Makes the side and lower part of the GUI visible.
def draw_GUI():
    pygame.draw.rect(screen, '#E6E6FA', (W, 0, SIDE_MARGIN, H))
    pygame.draw.rect(screen, '#E6E6FA', (0, H, W + SIDE_MARGIN, LOWER_MARGIN))
    draw_text(f"level: {level}", font, 'navy', 0, H + 20)


# Changes the scroll direction of the world.
def change_scroll_direction():
    global scroll
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - W:
        scroll += 5 * scroll_speed


# Places and deletes tiles based on their relative mouse position in the grid.
def place_n_delete_tiles():
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    if pos[0] < W and pos[1] < H:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1


# Init variables
W, H = 1280, 720
LOWER_MARGIN, SIDE_MARGIN = 100, 300
FPS = 120
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((W + SIDE_MARGIN, H + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

# Scroll variables.
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# Grid variables.
ROWS = 16
MAX_COLS = 150
TILE_SIZE = H // ROWS
TILE_TYPES = 26
current_tile = 0
level = 0

# Loads background.
bg = pygame.image.load('../assets/back.png').convert_alpha()
bg = pygame.transform.scale(bg, (W, H))
md = pygame.image.load('../assets/middle.png').convert_alpha()
md = pygame.transform.scale(md, (500, 450))

# Loads the tiles for the level editor.
tiles_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'../assets/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img.set_colorkey((0, 0, 0))
    tiles_list.append(img)

# Init the world_data list.
world_data = []
for i in range(ROWS):
    row = [-1] * MAX_COLS
    world_data.append(row)

# Init some GUI variables.
font = pygame.font.Font('../assets/joystix monospace.otf', 32)
save_text = font.render('Save', True, 'yellow', 'teal')
save_button = button.Button(W // 2, H + LOWER_MARGIN - 50, save_text, 1, 'yellow', 'teal')
load_text = font.render('Load', True, 'yellow', 'teal')
load_button = button.Button(W // 2 + 200, H + LOWER_MARGIN - 50, load_text, 1, 'yellow', 'teal')

# Makes all tiles into buttons.
button_list = []
button_col = 0
button_row = 0
for x in range(len(tiles_list)):
    tile_button = button.Button(W + (75 * button_col) + 50, 75 * button_row + 50, tiles_list[x], 1, "black", "black")
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

while True:
    events()
    draw_bg()
    draw_grid()
    draw_world()
    draw_GUI()
    highlight_tile()
    place_n_delete_tiles()
    change_scroll_direction()
    save_and_load()
    pygame.display.update()
    clock.tick(FPS)
