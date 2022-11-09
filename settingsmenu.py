def Run() -> None:
    #try:
        import pygame
        import sys
        import pyautogui
        import json
        import os

        import Assets.background
        import Assets.button

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

            RPC.update(state="Settings. . .", details="smiley circle", large_image="512_player", large_text="Viroose")

        pygame.init()

        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Viroose")
        icon = pygame.image.load("gfx/icon.png")
        pygame.display.set_icon(icon)
        bg = Assets.background.BG()

        clock = pygame.time.Clock()

        inSettingsMnu = True

        while inSettingsMnu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in buttonGroup:
                            if button.rect.collidepoint(event.pos):
                                if button.text == "Return":
                                    inSettingsMnu = False
                                button.doAction()

            buttonGroup = pygame.sprite.Group()

            def setRanMove():
                meta["settings"]["randomMovement"] = not meta["settings"]["randomMovement"]
                with open("meta.json", "w") as f:
                    json.dump(meta, f, indent=4)

            def setMenuPlayerSpin():
                meta["settings"]["menuPlayerSpin"] = not meta["settings"]["menuPlayerSpin"]
                with open("meta.json", "w") as f:
                    json.dump(meta, f, indent=4)

            #row 1
            ranMoveBttn = buttonGroup.add(Assets.button.Button(text=f"Random Movement: {meta['settings']['randomMovement']}", xy=(210, 120), image="gfx/bttn.png", text_size=10, action=lambda: setRanMove()))
            menuPlayerRotation = buttonGroup.add(Assets.button.Button(text=f"Menu Player Spins: {meta['settings']['menuPlayerSpin']}", xy=(210, 240), image="gfx/bttn.png", text_size=10, action=lambda: setMenuPlayerSpin()))
            #restart needed warning
            RestartNeeded = pygame.font.SysFont("Verdana", 10).render("Restart needed", True, (255, 0, 0))
            #
            Nonebutton = buttonGroup.add(Assets.button.Button(text="none", xy=(210, 360), image="gfx/bttn.png", text_size=32))

            #row 2
            Nonebutton = buttonGroup.add(Assets.button.Button(text="none", xy=(430, 120), image="gfx/bttn.png", text_size=30))
            Nonebutton = buttonGroup.add(Assets.button.Button(text="none", xy=(430, 240), image="gfx/bttn.png", text_size=32))
            returnBttn = buttonGroup.add(Assets.button.Button(text="Return", xy=(430, 360), image="gfx/bttn.png", text_size=32, action=lambda: print("", end="")))

            #draw sprites and update
            bg.draw(screen)

            buttonGroup.draw(screen)
            screen.blit(RestartNeeded, (200, 260))
            
            pygame.display.flip()
            clock.tick(60)

            #set game title to show FPS
            pygame.display.set_caption(f"Viroose {version} - FPS: {str(int(clock.get_fps()))} | Delta Time: {str(clock.get_time() / 1000)}s")

            if drpEnabled:
                RPC.update(state="Settings. . .", details="smiley circle", large_image="512_player", large_text="Viroose")
    #except Exception as e:
    #    #pyautogui error box
    #    pyautogui.alert("An error has occured: " + str(e))
    #    pass

if __name__ == "__main__":
    Run()