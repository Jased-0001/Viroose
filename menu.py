import pygame
import sys
import random
import json
import os

import game
import settingsmenu

import Assets.button
import Assets.background

with open("meta.json") as f:
    meta = json.load(f)
        
version = meta["version"]

drpEnabled = meta["settings"]["DiscordRichPresence"]

try:
    import pypresence
except:
    print("pypresence not installed, disabling Discord Rich Presence")
    drpEnabled = False

#discord rich presence
if drpEnabled:
    client_id = "1039669275973144586"
    RPC = pypresence.Presence(client_id)  # Initialize the client class
    RPC.connect() # Start the handshake loop

    #set discord rich presence
    RPC.update(state="In Menu", details="smiley circle", large_image="512_player", large_text="Viroose")

pygame.init()

inGame = False

#get random MOTD
MOTD = open("MOTD.txt", "r")
MOTD = MOTD.readlines()
MOTD = random.choice(MOTD)[0:-1]
#filter null characters

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Viroose")
icon = pygame.image.load("gfx/icon.png")
pygame.display.set_icon(icon)

BG = Assets.background.BG()

clock = pygame.time.Clock()

p1Rand = (random.randint(25, 200), random.randint(25, 200))
p2Rand = (random.randint(25, 200), random.randint(25, 200))

if meta["settings"]["menuPlayerSpin"]:
    #random rotation
    RTT1 = random.randint(0, 1)
    RTT2 = random.randint(0, 1)
    rotation1 = random.randint(-360, 360)
    rotation2 = random.randint(-360, 360)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        #if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        button.doAction()

    buttons = pygame.sprite.Group()
    playbutton = buttons.add(Assets.button.Button(text="Play", xy=(320, 130), image="gfx/bttn.png", text_size=32, action=lambda: game.Run()))
    Nonebutton = buttons.add(Assets.button.Button(text="Settings", xy=(320, 240), image="gfx/bttn.png", text_size=30, action=lambda: settingsmenu.Run()))
    exitbutton = buttons.add(Assets.button.Button(text="Exit", xy=(320, 350), image="gfx/bttn.png", text_size=32, action=lambda: sys.exit()))

    #draw name on right side
    ArialBold = pygame.font.SysFont("Arial", 50, bold=True)
    text_surface = ArialBold.render("Viroose", True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center = (320, 55)
    #display MOTD on bottom left in yellow
    ComicSans = pygame.font.SysFont("Comic Sans MS", 20)
    MOTD_surface = ComicSans.render(MOTD, True, (255,255,0))
    MOTD_rect = MOTD_surface.get_rect()
    MOTD_rect.center = (320, 450)

    #draw two players on each side, both with random sizes
    player1 = pygame.image.load("gfx/player.png")
    player1 = pygame.transform.scale(player1, p1Rand)
    player1_rect = player1.get_rect()
    player1_rect.center = (500, 240)

    player2 = pygame.image.load("gfx/player.png")
    player2 = pygame.transform.scale(player2, p2Rand)
    player2_rect = player2.get_rect()
    player2_rect.center = (100, 240)

    #spin player1 and player2
    #if rotation is negative, it will spin clockwise
    #if rotation is positive, it will spin counter-clockwise
    if meta["settings"]["menuPlayerSpin"]:
        if RTT1 == 0:
            rotation1 -= 1
        else:
            rotation1 += 1

        if RTT2 == 0:
            rotation2 -= 1
        else:
            rotation2 += 1

        #if rotation is greater than 360, reset it to 0
        if rotation1 > 360:
            rotation1 = 0
        if rotation2 > 360:
            rotation2 = 0
        if rotation1 < -360:
            rotation1 = 0
        if rotation2 < -360:
            rotation2 = 0

        player1 = pygame.transform.rotate(player1, rotation1)
        player2 = pygame.transform.rotate(player2, rotation2)
    else:
        pass

    BG.draw(screen)
    buttons.draw(screen)
    screen.blit(text_surface, text_rect)
    screen.blit(MOTD_surface, MOTD_rect)
    screen.blit(player1, player1_rect)
    screen.blit(player2, player2_rect)

    
    pygame.display.flip()
    clock.tick(60)

    #set game title to show FPS
    #spf = seconds per frame
    pygame.display.set_caption(f"Viroose {version} - FPS: {str(int(clock.get_fps()))} | Delta Time: {str(clock.get_time() / 1000)}s")

    if drpEnabled:
        #set discord rich presence
        RPC.update(details="smiley circle", large_image="512_player", large_text="Viroose")