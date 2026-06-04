# Start your code here
import pygame as pg
import random
from urllib.request import urlopen
from io import BytesIO
pg.init()

def game():
    WIDTH = 500
    HEIGHT = 225
    size = (WIDTH, HEIGHT)
    TILE = 25 # each maze cell size
    screen = pg.display.set_mode(size) 
    
    # maze
    maze_1 = [
        "####################",
        "#..o.....##...o....#",
        "#.####...##...####.#",
        "#....c.............#",
        "#.####.######c####.#",
        "#..o...##.o..##....#",
        "#.####.##....##.####",
        "#...c....o.....c...#",
        "####################"
    ]
    
    maze_2 = [
        "####################",
        "#..o....##....o....#",
        "#.####..##..####...#",
        "#...c.......c......#",
        "#.####.######.####.#",
        "#..o...##.o..##....#",
        "#.####.##....##.####",
        "#...c....o....c....#",
        "####################"
    ]
    
    maze_3 = [
        "####################",
        "#..o....###....o...#",
        "#.####.#..#.####.#.#",
        "#c.....#..#.....#c.#",
        "####.#.##.###.#.####",
        "#..o.#....c......o.#",
        "#.##.####..####.##.#",
        "#...c....##....c...#",
        "####################"
    ]
    
    maze_4 = [
        "###################",
        "#c..o.#..##..#o..c#",
        "#.##..####..####..#",
        "#..c.....##.....c.#",
        "#.####.##.##.####.#",
        "#..o..#....#..o...#",
        "#.##..####..####..#",
        "#c.....o....o....c#",
        "###################"
    ]
    
    maze_5 = [
        "####################",
        "#..o..#.....#..o...#",
        "#.##..###..###..##.#",
        "#....c.......c.....#",
        "#.####.######.####.#",
        "#..o...##...##..o..#",
        "#.##.##....##.##...#",
        "#...c....o....c....#",
        "####################"
    ]

    mazes = [maze_1, maze_2, maze_3, maze_4, maze_5]
    maze = random.choice(mazes)
    rows = len(maze) # got help
    cols = len(maze[0]) # got help
    pellets = [] # normal pellets
    big_pellets = [] # big pellets
    cherries = [] # cherries
    
    # player variables
    player = pg.image.load("pacman.png")
    player = pg.transform.scale(player, (20,20))
    player_original = player # orignal image (doesn't change)
    position = [25,25] # player position
    angle = 0 # presistent angle (got help)
    score = 0
    
    # statistic variables
    font_data = urlopen("https://codehs.com/uploads/eaece357375ac9f74fd434d4e11acd6d")
    font_file = BytesIO(font_data.read())
    anonymous_pro = pg.font.Font(font_file, 10)
    
    # ghosts
    red = pg.image.load("red_ghost.png")
    red = pg.transform.scale(red, (20,20))
    red_pos = [WIDTH-20, HEIGHT-10]
    red_speed = 1
    
    # border
    screen.fill("white")
    
    # starting animation
    start = pg.image.load("startscreen.png")
    start = pg.transform.scale(start, (WIDTH, HEIGHT))
    start_position = [0,0]
    
    # player wins screen
    win = pg.image.load("win_screen.png")
    win = pg.transform.scale(win, (WIDTH, HEIGHT))
    win_position = [0,0]
    
    # pellets
    # initialize the pellets
    # normal pellets
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] ==  ".": # dots represent pellets
                pellets.append([c*TILE + TILE//2, r*TILE + TILE//2]) # got help
    # big pellets
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "o": # o's represent big pellets (more points)
                big_pellets.append([c*TILE + TILE//2, r*TILE + TILE//2]) # got from pellets 
    
    # cherries
    
    # fruit
    cherry = pg.image.load("cherry.png")
    cherry = pg.transform.scale(cherry, (15,15))
    
    # initialize the cherries
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "c": # c's represent cherries
                cherries.append([c*TILE + TILE//2, r*TILE + TILE//2]) 
    
    # check for wall collision
    def can_move(x,y):
        # check the whole shape of the pacman
        corners = [
            (x,y),
            (x+20, y),
            (x, y+20),
            (x+20, y+20)
        ]
        for cx, cy in corners:
            col = int(cx // TILE)
            row = int(cy // TILE)
            if maze[row][col] == "#":
                return False
        return True
    
    while True:
        # bg
        pg.draw.rect(screen, "black", ((5,5), (500, 225)))
        pg.event.get()
        pressed_keys = pg.key.get_pressed()
        # movement controls
        new_x, new_y = position[0], position[1]
        
        # WASD
        if pressed_keys[pg.K_a] or pressed_keys[pg.K_LEFT]: # left
            angle = 180
            new_x -= 0.35
        elif pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]: # right
            angle = 0
            new_x += 0.35
        elif pressed_keys[pg.K_s] or pressed_keys[pg.K_DOWN]: # down
            angle = 270
            new_y += 0.35
        elif pressed_keys[pg.K_w] or pressed_keys[pg.K_UP]: # up
            angle = 90
            new_y -= 0.35
    
        # wall blocking
        if can_move(new_x, new_y):
            position[0] = new_x
            position[1] = new_y
    
        # rotate after movement (got help)
        rotated = pg.transform.rotate(player_original, angle) # got help
        screen.blit(rotated, position) # display player
    
        # draw maze
        for r in range(rows):
            for c in range(cols):
                if maze[r][c] == "#":
                    pg.draw.rect(screen, (0,0,255), (c*TILE, r*TILE, TILE, TILE))
        
        text = anonymous_pro.render(f"Score:  {score}", True, 'white')
        text_rectangle = text.get_rect()
        text_rectangle.center = (40, 10)
        screen.blit(text, text_rectangle)
        
        # pellets
        # small pellets
        # draw the pellets
        for px, py in pellets: # pellet position
            pg.draw.circle(screen, (255, 255, 222), (px, py), 2)
            
        # pellet detection (inspired from cherry detection)
        for pellet in pellets[:]: # got help
            if abs(position[0] + 10 - pellet[0]) < 10 and abs(position[1] + 10 - pellet[1]) < 10:
                pellets.remove(pellet)
                score += 10
        
        # big pellets
        for px, py in big_pellets:
            pg.draw.circle(screen, (255, 255, 0), (px, py), 4)
        
        # pellet detection (big pellets)
        for big_pellet in big_pellets[:]:
            if abs(position[0] + 10 - big_pellet[0]) < 10 and abs(position[1] + 10 - big_pellet[1]) < 10:
                big_pellets.remove(big_pellet)
                score += 50
        
        # cherries
        cherry_size = 15
        cherry_offset = cherry_size // 2 # got help
        
        for cx, cy in cherries[:]:
            screen.blit(cherry, (cx-cherry_offset, cy-cherry_offset)) # got help for the offset part
            
        for cherry_pos in cherries[:]:
            if abs(position[0]-cherry_pos[0]) < 15 and abs(position[1]-cherry_pos[1]) < 15: # check if player ate cherry (got help)
                # player ate the cherry (remove)
                cherries.remove(cherry_pos)
                score += 100
    
        # enemy follow code
        screen.blit(red, red_pos)
        
        dx = position[0] - red_pos[0]
        dy = position[1] - red_pos[1]
        
        dist = (dx**2 + dy**2) ** 0.5 # find the distance (got help)
        
        # if ghost touches player
        if dist < 15:
            print("Game Over!")
            return
        elif len(pellets) == 0 and len(big_pellets) == 0 and len(cherries) == 0: # all the cherries/pellets have been eaten (player wins)
            print("Player wins!")
            print(f"Score: {score}")
            screen.blit(win, win_position)
        
        if dist != 0:
            dx /= dist
            dy /= dist
        
        red_speed = 0.1
        red_pos[0] += dx * red_speed
        red_pos[1] += dy * red_speed
        
        pg.display.update() 

def click_to_start():
    # homepage
    size = width, height = 500, 225
    speed = [1, 1]
    screen = pg.display.set_mode(size)
    logo = pg.image.load("pacman logo.png")
    logo = pg.transform.scale(logo, (100, 65))
    rect = logo.get_rect()
    rect.x = random.randint(0, width - rect.width)
    rect.y = random.randint(0, height - rect.height)
    font_data = urlopen("https://codehs.com/uploads/eaece357375ac9f74fd434d4e11acd6d")
    font_file = BytesIO(font_data.read())
    anonymous_pro = pg.font.Font(font_file, 10)
    
    while True:
        # background
        screen.fill((255,255,255))
        # screen
        pg.draw.rect(screen, "black", (2, 2, width-4, height-4), 2) 
        
        clock = pg.time.Clock()
        # Limit to 60 frames per second
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            # click detection
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if rect.collidepoint(mouse_pos): # if user clicks logo (got help)
                    game()
                    break # exit out of the homepage loop
            
        rect.x += speed[0]
        rect.y += speed[1]
        if rect.left < 2.5 or rect.right > width-2.5:
            speed[0] = -speed[0]
        if rect.top < 2 or rect.bottom > height-2:
            speed[1] = -speed[1]
        screen.blit(logo, (rect.x, rect.y))
        pg.display.update()

WIDTH = 500
HEIGHT = 225
size = (WIDTH, HEIGHT)
screen = pg.display.set_mode(size)

# startscreen BG
start_screen = pg.image.load("startscreen.png")
start_screen = pg.transform.scale(start_screen, (275, 75))
click_start = pg.image.load("clickstart.png")
click_start = pg.transform.scale(click_start, (250, 75))
instruction = pg.image.load("instructions.png")
instruction = pg.transform.scale(instruction, (250, 75))
instruction_text = pg.image.load("instructions_text.png")
instruction_text = pg.transform.scale(instruction_text, (WIDTH/1.75, HEIGHT))

while True:
    # display the content
    screen.blit(start_screen, (115,0))
    screen.blit(click_start, (125, HEIGHT/2))
    screen.blit(instruction, (125, (HEIGHT/2)+HEIGHT/4))
    
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            if 125 <= mouse_x <= 375 and 113 <= mouse_y <= 180:
                # click to start clicked
                click_to_start()
            elif 125 <= mouse_x <= 375 and 169 <= mouse_y <= 244:
                # user clicked instructions
                screen.fill("black")
                show_instructions = True
                while show_instructions:
                    screen.blit(instruction_text, (WIDTH/4, 0)) # display instructions
                    
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_b: # if 'b' pressed
                                show_instructions = False
                                screen.fill("black")
                                pg.event.clear()
                                
                    pg.display.update()

    pg.display.update()