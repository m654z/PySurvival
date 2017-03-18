import pygame
import sys
import random
import time
from pygame.locals import *

# Lists and stuff
animals = ["deer", "moose", "bear", "duck", "rabbit", "reindeer"]
log = "You find yourself in a strange forest."

# Resources
wood = 0
food = 5
seeds = 0
fpt = 0 # Food per turn
wool = 0
heat = 40
hpt = 1 # Heat (lost) per turn

# Stats
turn = 0
moves = 5
moved = False
has_house = False
house_pos = [0,0]
season = "Summer"
winter = False
running = True # If this is off it plays the end sequence thing
ttw = 50 # Turns to winter
clothes = False

# Tilemap tiles
WATER = 0
DIRT = 1
GRASS = 2
FOREST = 3
HOUSE = 4
FARM = 5
PASTURE = 6
COTTAGE = 7
CLOUD = 10

# ------ Map settings ------
TILESIZE = 40
MAPWIDTH = 20
MAPHEIGHT = 10
# --------------------------

# Cloud stuff
cloudx = -200
cloudy = random.randint(0, MAPHEIGHT*TILESIZE)
cloudClock = pygame.time.Clock()

# Generate the tilemap
tilemap = [[random.randint(0, 3) for e in range(MAPWIDTH)] for e in range(
    MAPHEIGHT)]
tilemap[0][0] = 3 # Make sure that the starting position is a forest

# Textures for the tiles
textures = {
    WATER: pygame.image.load("water.png"),
    DIRT: pygame.image.load("dirt.png"),
    GRASS: pygame.image.load("grass.png"),
    FOREST: pygame.image.load("forest.png"),
    HOUSE: pygame.image.load("house.png"),
    FARM: pygame.image.load("farm.png"),
    PASTURE: pygame.image.load("pasture.png"),
    COTTAGE: pygame.image.load("cottage.png"),
    CLOUD: pygame.image.load("cloud.png")
}

winter_textures = {
    WATER: pygame.image.load("snow_water.png"),
    DIRT: pygame.image.load("dirt.png"),
    GRASS: pygame.image.load("snow_grass.png"),
    FOREST: pygame.image.load("snow_forest.png"),
    HOUSE: pygame.image.load("house.png"),
    FARM: pygame.image.load("farm.png"),
    PASTURE: pygame.image.load("snow_pasture.png"),
    COTTAGE: pygame.image.load("snow_cottage.png"),
    CLOUD: pygame.image.load("cloud.png")
}

# The Unit class
class Unit:
    TILESIZE = TILESIZE
    def __init__(self, name, pos, graphic, display):
        self.name = name
        self.pos = pos
        self.graphic = graphic
        self.display = display

    def move(self, pos):
        self.pos = pos

    def draw(self):
        image = pygame.image.load(self.graphic).convert_alpha()
        self.display.blit(image,(self.pos[0]*TILESIZE,self.pos[1]*TILESIZE)) 

# Set everything up
pygame.init()
icon = pygame.image.load("icon.png")
pygame.display.set_caption("PySurvival")
pygame.display.set_icon(icon)
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE+100))

# Fonts
large_font = pygame.font.SysFont("monospace", 20)
font = pygame.font.SysFont("monospace", 15)
small_font = pygame.font.SysFont("monospace", 9)

def text():
    # This function renders and displays all the text
    lblFood = font.render("Food: {}".format(food), 1, (255,255,255))
    lblFpt = font.render("Food per turn: {}".format(fpt-1), 1, (255,255,255))
    lblWood = font.render("Wood: {}".format(wood), 1, (255,255,255))
    lblSeeds = font.render("Seeds: {}".format(seeds), 1, (255,255,255))
    lblWool = font.render("Wool: {}".format(wool), 1, (255,255,255))
    lblMoves = font.render("Moves: {}".format(moves), 1, (255,255,255))
    lblTurn = font.render("Turn: {}".format(turn), 1, (255,255,255))
    lblHeat = font.render("Heat: {}|Heat loss: {}".format(heat, hpt), 1, (255,255,255))
    lblSeason = font.render(season, 1, (255,255,255))
    lblLog = small_font.render(log, 1, (255,255,255))
    DISPLAYSURF.blit(lblFood, (5,400))
    DISPLAYSURF.blit(lblFpt, (5, 420))
    DISPLAYSURF.blit(lblWood, (5, 440))
    DISPLAYSURF.blit(lblSeeds, (5, 460))
    DISPLAYSURF.blit(lblWool, (5, 480))
    DISPLAYSURF.blit(lblMoves, (200, 440))
    DISPLAYSURF.blit(lblTurn, (200, 460))
    DISPLAYSURF.blit(lblSeason, (200, 420))
    DISPLAYSURF.blit(lblLog, (200,400))
    DISPLAYSURF.blit(lblHeat, (200, 480))

def end():
    # Ending stuff, pretty ugly right now
    DISPLAYSURF.fill(Color("black"))
    lblEnd1 = large_font.render("A ship comes to rescue you!", 1, (255,255,255))
    lblEnd2 = large_font.render("Thank you for playing!", 1, (255,255,255))
    DISPLAYSURF.blit(lblEnd1, (0, 0))
    pygame.display.update()
    time.sleep(4)
    DISPLAYSURF.fill(Color("black"))
    DISPLAYSURF.blit(lblEnd2, (0, 0))
    pygame.display.update()
    time.sleep(4)
    pygame.quit()
    sys.exit()

# Set up a unit called player
player = Unit("player", [0,0], "player.png", DISPLAYSURF)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Keydown event
        elif event.type == KEYDOWN:
            if moves == 0:
                # This code runs once every turn
                turn += 1
                moves = 5
                food += fpt
                food -= 1
                ttw -= 1
    
            if food < 1:
                # If you don't have any food you lose!
                pygame.quit()
                sys.exit()

            if food < 3:
                log = "You're hungry."

            if winter == True:
                # Check if it's summer again
                if ttw == 0:
                    winter = False
                    season = "Summer"
                    running = False

            if ttw == 0:
                # Check if it's winter
                season = "Winter"
                winter = True
                fpt = fpt / 2 # During winter you make less food
                ttw = 50
                hpt = 3 # Also, you lose 3 heat per turn without any clothes
                    
            # Handle arrow keys
            if event.key == K_RIGHT and player.pos[0] < MAPWIDTH - 1:
                if not tilemap[player.pos[1]][player.pos[0]+1] == WATER:
                    player.pos[0] += 1
                    moved = True

            elif event.key == K_LEFT and player.pos[0] > 0:
                if not tilemap[player.pos[1]][player.pos[0]-1] == WATER:
                    player.pos[0] -= 1
                    moved = True

            elif event.key == K_UP and player.pos[1] > 0:
                if not tilemap[player.pos[1]-1][player.pos[0]] == WATER:
                    player.pos[1] -= 1
                    moved = True

            elif event.key == K_DOWN and player.pos[1] < MAPHEIGHT - 1:
                if not tilemap[player.pos[1]+1][player.pos[0]] == WATER:
                    player.pos[1] += 1
                    moved = True

            # Chop a forest
            elif event.key == K_c:
                if tilemap[player.pos[1]][player.pos[0]] == 3:
                    wood += 10
                    tilemap[player.pos[1]][player.pos[0]] = 2
                    food -= 1
                    moved = True
                    if food < 1:
                        pygame.quit()
                        sys.exit()

            # Build a house (+1 fpt)
            elif event.key == K_1:
                if wood > 19 and has_house == False:
                    wood -= 20
                    tilemap[player.pos[1]][player.pos[0]] = 4
                    moved = True
                    has_house = True
                    house_pos = player.pos
                    fpt += 1

            # Build a farm (+1 fpt)
            elif event.key == K_2:
                if wood > 39 and seeds > 4 and tilemap[player.pos[1]][player.pos[0]] == 1:
                    wood -= 40
                    seeds -= 5
                    tilemap[player.pos[1]][player.pos[0]] = 5
                    moved = True
                    fpt += 1

            # Build a pasture
            elif event.key == K_3:
                if wood > 19:
                    wood -= 20
                    if tilemap[player.pos[1]][player.pos[0]] == 2:
                        tilemap[player.pos[1]][player.pos[0]] = 6
                        moved = True

            # Build a cottage
            elif event.key == K_4:
                if wood > 29:
                    wood -= 30
                    if tilemap[player.pos[1]][player.pos[0]] == 3:
                        tilemap[player.pos[1]][player.pos[0]] = 7
                        moved = True

            # Make clothes
            elif event.key == K_0:
                if wool > 9 and clothes == False:
                    wool -= 10
                    clothes = True
                    moved = True
                    hpt -= 1

            # Hunt
            elif event.key == K_h:
                if tilemap[player.pos[1]][player.pos[0]] == 3:
                    if random.randint(0, 1) == 1:
                        food +=  3
                        log = "You caught a {}.".format(random.choice(animals))

                    else:
                        food -= 1
                        log = "Your hunting trip was unsuccesful."

                    moved = True

            # Search for seeds
            elif event.key == K_s:
                if tilemap[player.pos[1]][player.pos[0]] == 2:
                    if random.randint(0, 2) == 2:
                        seeds += 3

                    moved = True

            # Get wool from a pasture
            elif event.key == K_w:
                if tilemap[player.pos[1]][player.pos[0]] == 6:
                    wool += 1
                    food -= 2
                    log = "You sheared some sheep."
                    moved = True

            # Gain heat in a house or a cottage
            elif event.key == K_a:
                if tilemap[player.pos[1]][player.pos[0]] == 4 or tilemap[player.pos[1]][player.pos[0]] == 7:
                    if winter == True:
                        if heat < 36 and wood > 4:
                            heat += 5
                            wood -= 2
                            moved = True
                    else:
                        if heat < 36 and wood > 0:
                            heat += 5
                            wood -= 1
                            moved = True

            # Reset the map
            elif event.key == K_F5:
                tilemap = [[random.randint(0, 3) for e in range(MAPWIDTH)] for e in range(MAPHEIGHT)]
                tilemap[0][0] = 3

            if moved == True:
                moves -= 1
                moved = False
                if tilemap[player.pos[1]][player.pos[0]] == 4 or tilemap[player.pos[1]][player.pos[0]] == 7:
                    # If you're in a house or cottage, don't take any heat away
                    pass
                else:
                    if heat < 1:
                        # If you're cold, you lose 5 food per turn
                        food -= 5
                    else:
                        heat -= hpt
    if winter == False:
        # Draw the map
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(textures[tilemap[row][column]],
                                 (column*TILESIZE, row*TILESIZE))
    else:
        # Draw the winter textures
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                DISPLAYSURF.blit(winter_textures[tilemap[row][column]],
                                 (column*TILESIZE, row*TILESIZE))
    

    # Draw the cloud
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(),(cloudx,cloudy))
    cloudx += 1
    if cloudx > MAPWIDTH*TILESIZE:
        cloudy = random.randint(0, MAPHEIGHT*TILESIZE)
        cloudx = -200
    # Draw the player
    player.draw()
    pygame.display.update()
    cloudClock.tick(24)
    DISPLAYSURF.fill(Color("black"))
    text()

end()
