def Run() -> None:
    try:
        import pygame
        import sys
        import pyautogui
        import json
        import random
        import os

        import Assets.button
        import Assets.background
        import Assets.enemy

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

            RPC.update(state="Died!", details="smiley circle", large_image="512_player", large_text="Viroose")


        pygame.init()

        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Viroose")
        #icon = pygame.image.load("gfx/icon.png")
        #pygame.display.set_icon(icon)

        bg = Assets.background.BG()

        clock = pygame.time.Clock()

        #have enemy bounce around the screen
        enemy = Assets.enemy.Enemy(X=random.randint(200,430), Y=random.randint(240,370), Xvel=random.randint(5,10), Yvel=random.randint(5,10))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.text == "Return to Menu":
                                    return
                                button.doAction()

            #text in the center of the screen
            font = pygame.font.SysFont("Arial", 50, bold=True)
            text = font.render("You died!", True, (0, 0, 0))

            #rotate and scale text
            text = pygame.transform.scale(text, (text.get_width() + 10, text.get_height() + 10))
            text = pygame.transform.rotate(text, 5)
            text = text.convert_alpha()

            #add "Return" button
            buttons = pygame.sprite.Group()
            ReturnBtn = buttons.add(Assets.button.Button(text="Return to Menu", xy=(320, 240), image="gfx/bttn.png", text_size=15, action=lambda: print("", end="")))

            #draw sprites and update
            bg.draw(screen)
            buttons.draw(screen)
            screen.blit(text, (50, 50))

            #update enemy
            enemy.update()
            enemy.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

            #set game title to show FPS
            pygame.display.set_caption(f"Viroose {version} - FPS: {str(int(clock.get_fps()))} | Delta Time: {str(clock.get_time() / 1000)}s")

            if drpEnabled:
                RPC.update(state="Died!", details="smiley circle", large_image="512_player", large_text="Viroose")
    except Exception as e:
        #pyautogui error box
        pyautogui.alert("An error has occured: " + str(e))
        pass

if __name__ == "__main__":
    Run()