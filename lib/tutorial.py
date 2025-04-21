import os, sys
import pygame
from lib import root

def tutorial(screen, clock):
    global tutorial_index
    global run
    run = True

    back_button = root.text_button(25, (255, 255, 255), "Back")
    def back_button_function():
        global run
        run = False
    back_button.func = back_button_function

    more_button = root.text_button(25, (255, 255, 255), "More Help ↗")
    def more_button_function():
        os.startfile('https://www.dome.icu/dragtyping')
    more_button.func = more_button_function

    previous_button = root.text_button(45, (255, 255, 255), "←")
    def previous_button_function():
        global tutorial_index
        if tutorial_index > 0:
            tutorial_index -= 1
        else:
            tutorial_index = len(tutorial_slideshow) - 1
    previous_button.func = previous_button_function

    next_button = root.text_button(45, (255, 255, 255), "→")
    def next_button_function():
        global tutorial_index
        if tutorial_index < len(tutorial_slideshow) - 1:
            tutorial_index += 1
        else:
            tutorial_index = 0
    next_button.func = next_button_function

    buttons = [back_button, more_button, previous_button, next_button]

    if root.play_anims:
        img = root.menu_imgs[-1]
    else:
        img = root.game_imgs[-1]

    tutorial_slideshow = root.tutorial_imgs
    tutorial_index = 0

    def redraw_win(screen):
        screen.fill((255, 255, 255))
        screen.blit(img, (0, 0))
        screen.blit(tutorial_slideshow[tutorial_index], ((1280 - 849) / 2, (720 - 480) / 2))
        back_button.draw(screen, 75, 30)
        more_button.draw(screen, 1030, root.screen_size[1] - 100)
        previous_button.draw(screen, (1280 - 849) / 2 - previous_button.width - 50, root.screen_size[1] / 2 - 50)
        next_button.draw(screen, (1280 - 849) / 2 + 849 + 50, root.screen_size[1] / 2 - 50)
        slide_counter = root.medium_font.render(str(tutorial_index + 1) + '/' + str(len(tutorial_slideshow)), True, (255, 255, 255))
        screen.blit(slide_counter, ((root.screen_size[0] - slide_counter.get_width()) / 2, root.screen_size[1] - 100))

    while run:        
        redraw_win(screen)
        pygame.display.flip()
        clock.tick(30)
        root.update_UI(pygame.event.get(), buttons)

    return