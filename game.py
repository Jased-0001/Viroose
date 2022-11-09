def Run() -> None:
    try:
        import pygame
        import sys
        import pyautogui
        import json

        import Assets.player
        import Assets.ground
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

                    #when clicking LMB, fire bullet
                    if event.key == pygame.K_LCTRL:
                        player.fire()

            #check if player is colliding with ground
            if player.isColliding(ground) and ground.isColliding(player):
                player.onGround = True
            else:
                player.onGround = False

            #draw sprites and update
            bg.draw(screen)

            player.update()
            player.draw(screen)
            ground.draw(screen)
            

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