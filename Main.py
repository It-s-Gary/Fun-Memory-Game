import pygame
import sys
import random
pygame.init()
Screen_width = 900
Screen_Height = 800
Tile_size = 100
hide_timer = None
score = 0
screen = pygame.display.set_mode((Screen_width, Screen_Height))
tile_img = [pygame.image.load("Cookie.png").convert(), 
            pygame.image.load("Apple.png").convert(),  
            pygame.image.load("Circle.png").convert(),  
            pygame.image.load("Screen.png").convert(), 
            pygame.image.load("Three.png").convert(),
            pygame.image.load("icon_bell.png").convert(),
            pygame.image.load("icon_bone.png").convert(),
            pygame.image.load("icon_boots.png").convert(),
            pygame.image.load("icon_brain.png").convert(),
            pygame.image.load("icon_brush.png").convert(),
            pygame.image.load("icon_call.png").convert(),
            pygame.image.load("icon_crate.png").convert(),
            pygame.image.load("icon_gear.png").convert(),
            pygame.image.load("icon_hammer.png").convert(),
            pygame.image.load("icon_hand.png").convert(),
            pygame.image.load("icon_hat.png").convert(),
            pygame.image.load("icon_heart.png").convert(),
            pygame.image.load("icon_trap.png").convert(),
            pygame.image.load("icon_tree.png").convert(),
            pygame.image.load("icon_trophy.png").convert(),
            pygame.image.load("robot.png").convert(),
            ]

scaled_tiles = []

font = pygame.font.Font(None, 48)

matched = set()


for img in tile_img:
    scaled = pygame.transform.scale(img, (Tile_size, Tile_size))
    scaled_tiles.append(scaled)
height = 750
width = 600
rows = height // Tile_size
cols = width // Tile_size
total_tiles = rows * cols  
indices = [i % len(scaled_tiles) for i in range(total_tiles)] 
random.shuffle(indices)
count = 0
grid = [[0 for _ in range(cols)] for _ in range(rows)]
grid2 = []
revealed = [[False for _ in range(cols)] for _ in range(rows)]
Spacing = 8
first_click = None
second_click = None
for row in range(rows):
    for col in range(cols):
        grid[row][col] = indices[count]
        count += 1

for row in range(rows):
    row_rects = []
    for col in range(cols):

        rect = pygame.Rect(
            col * (Tile_size + Spacing) + 50, row * (Tile_size + Spacing) + 40, Tile_size, Tile_size)

        row_rects.append(rect)
    grid2.append(row_rects)


running = True
while running:
    text_surface = font.render(f"Score {score}", True, "white")
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in range(rows):
                for col in range(cols):
                    if grid2[row][col].collidepoint(mouse_x, mouse_y):
                        if (row, col) in matched:
                            continue
                        if first_click is None:
                            first_click = (row, col)
                            revealed[row][col] = True

                        elif second_click is None and (row, col) != first_click:
                            second_click = (row, col)
                            revealed[row][col] = True
    screen.fill("blue")

    if first_click and second_click:
        r1, c1 = first_click
        r2, c2 = second_click
        if grid[r1][c1] == grid[r2][c2]:

            score += 2
            first_click = None
            second_click = None
            matched.add((r1, c1))  
            matched.add((r2, c2))
        elif hide_timer is None:
            hide_timer = pygame.time.get_ticks()
    if hide_timer and pygame.time.get_ticks() - hide_timer > 1000:  
        revealed[r1][c1] = False
        revealed[r2][c2] = False
        first_click = None
        second_click = None
        hide_timer = None
    for row in range(rows):
        for col in range(cols):
                x = col * (Tile_size + Spacing) + 50
                y = row * (Tile_size + Spacing) + 40
                tile_index = grid[row][col]
                screen.blit(scaled_tiles[tile_index], (x, y))
                if not revealed[row][col]:  
                    pygame.draw.rect(screen, "black", grid2[row][col], 0)
    screen.blit(text_surface, (700, 300))
    

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
sys.exit()