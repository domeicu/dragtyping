import os, sys, math
import pygame
from lib import root

heading = root.larger_font.render("Pre", True, (255, 255, 255))
heading2 = root.larger_font.render("Game", True, (255, 255, 255))
race_length_heading = root.large_font.render("Select Race Length", True, (255, 255, 255))
start = root.large_font.render("Press SPACE to START", True, (255, 255, 255))

def pregame(screen, clock):
    global run
    global race_length
    global buttons
    run = True
    buttons = []

    frame_counter = 0
    race_length = 1000

    back_button = root.text_button(25, (255, 255, 255), "Back")
    def back_button_function():
        global run
        run = False
    back_button.func = back_button_function

    def race_length_button_function(button):
        global race_length
        global buttons
        race_length = int(button.text[:-1])
        for b in buttons:
            b.pressed = False
        button.pressed = True

    l500_button = root.text_button(25, (255, 255, 255), "500m")
    l500_button.func = race_length_button_function
    l500_button.argument = l500_button

    l1000_button = root.text_button(25, (255, 255, 255), "1000m")
    l1000_button.pressed = True
    l1000_button.func = race_length_button_function
    l1000_button.argument = l1000_button

    l5000_button = root.text_button(25, (255, 255, 255), "5000m")
    l5000_button.func = race_length_button_function
    l5000_button.argument = l5000_button

    l10000_button = root.text_button(25, (255, 255, 255), "10000m")
    l10000_button.func = race_length_button_function
    l10000_button.argument = l10000_button

    buttons = [back_button, l500_button, l1000_button, l5000_button, l10000_button]

    if root.play_anims:
        img = root.menu_imgs[-1]
    else:
        img = root.game_imgs[-1]

    def redraw_win(screen):
        screen.blit(img, (0, 0))
        back_button.draw(screen, 75, 30)
        l500_button.draw(screen, 600, 200)
        l1000_button.draw(screen, 700, 200)
        l5000_button.draw(screen, 800, 200)
        l10000_button.draw(screen, 900, 200)
        start.set_alpha(abs(255 * math.sin(frame_counter/10)))
        screen.blit(heading, (75, 100))
        screen.blit(heading2, (75, 190))
        screen.blit(race_length_heading, (600, 120))
        screen.blit(start, ((root.screen_size[0] - start.get_width()) / 2, root.screen_size[1] - 100))

    while run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return race_length

        if frame_counter < 60:
            frame_counter += 1
        else:
            frame_counter = 0

        redraw_win(screen)
        pygame.display.flip()
        clock.tick(30)
        root.update_UI(pygame.event.get(), buttons)

    return