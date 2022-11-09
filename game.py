def Run() -> None:
    try:
        import pygame
        import sys
        import pyautogui
        import json
        import os

        import Assets.player
        import Assets.ground
        import Assets.background
        import Assets.enemy

        import deathscreen

        with open("meta.json") as f:
            meta = json.load(f)
            
        version = meta["version"]

        drpEnabled = meta["settings"]["DiscordRichPresence"]

        try:
            import pypresence
        except:
            print("pypresence not installed, disabling Discord Rich Presence")
            drpEnabled = False

        if drpEnabled:
            client_id = "1039669275973144586"
            RPC = pypresence.Presence(client_id)
            RPC.connect()

            RPC.update(state="Playing. . .", details="smiley circle", large_image="512_player", large_text="Viroose")


        pygame.init()

        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Viroose")
        #icon = pygame.image.load("gfx/icon.png")
        #pygame.display.set_icon(icon)

        player = Assets.player.Player()
        ground = Assets.ground.Ground()
        bg = Assets.background.BG()

        #enemy group
        enemyGroup = pygame.sprite.Group()

        enemy = Assets.enemy.Enemy(X=pygame.display.get_surface().get_width() - 50, Y=240, Xvel=5, Yvel=5)
        enemyGroup.add(enemy)

        enemy2 = Assets.enemy.Enemy(X=4, Y=44, Xvel=0, Yvel=8)
        enemyGroup.add(enemy2)

        enemy3 = Assets.enemy.Enemy(X=45, Y=240, Xvel=5, Yvel=5)
        enemyGroup.add(enemy3)

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    #movement
                    if event.key == pygame.K_SPACE:
                        #jump
                        player.jump(meta["settings"]["randomMovement"])

                    if event.key == pygame.K_a:
                        #add -5 to x velocity
                        player.Xvel -= 5

                    if event.key == pygame.K_d:
                        #add 5 to x velocity
                        player.Xvel += 5

                    if event.key == pygame.K_w:
                        #jump
                        player.jump(meta["settings"]["randomMovement"])

                    if event.key == pygame.K_s:
                        #fall 
                        player.fall(meta["settings"]["randomMovement"])

                    #when clicking LMB spawn enemy
                    #if event.key == pygame.K_e:
                    

            #check if player is colliding with ground
            if player.isColliding(ground) and ground.isColliding(player):
                player.onGround = True
            else:
                player.onGround = False

            #if enemies are colliding with ground
            for enemy in enemyGroup:
                if enemy.isColliding(ground) and ground.isColliding(enemy):
                    enemy.onGround = True
                else:
                    enemy.onGround = False

            #check if player is colliding with enemy
            for enemy in enemyGroup:
                if player.isColliding(enemy) and enemy.isColliding(player):
                    player.HP -= .5
                    enemy.HP -= 1

            #if player is dead, go to death screen
            if player.HP <= 0:
                deathscreen.Run()
            
            #draw sprites and update
            bg.draw(screen)

            #draw HP bar on top left of screen with 175px width and 17px height
            pygame.draw.rect(screen, (255, 0, 0), (3, 3, 175, 17))
            pygame.draw.rect(screen, (0, 255, 0), (3, 3, player.HP * 1.75, 17))
            #add border
            pygame.draw.rect(screen, (0, 0, 0), (3, 3, 175, 17), 1)
            #draw HP text on top left of screen, in the middle of the HP bar
            font = pygame.font.SysFont("Arial", 15)
            text = font.render(f"HP: {player.HP}", True, (0, 0, 0))

            #if enemy is dead, remove it from the group
            for enemy in enemyGroup:
                if enemy.HP <= 0:
                    enemyGroup.remove(enemy)

            #update sprites
            player.update()
            enemyGroup.update()

            #draw sprites
            player.draw(screen)
            ground.draw(screen)
            enemyGroup.draw(screen)

            #draw HP HUD
            screen.blit(text, (3 + 175 / 2 - text.get_width() / 2, 3 + 17 / 2 - text.get_height() / 2))
            
            pygame.display.flip()
            clock.tick(60)

            #set game title to show FPS
            pygame.display.set_caption(f"Viroose {version} - FPS: {str(int(clock.get_fps()))} | Delta Time: {str(clock.get_time() / 1000)}s")

            if drpEnabled:
                RPC.update(state="Playing. . .", details="smiley circle", large_image="512_player", large_text="Viroose")
    except Exception as e:
        #pyautogui error box
        pyautogui.alert("An error has occured: " + str(e))
        pass

if __name__ == "__main__":
    Run()