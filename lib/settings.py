import os, sys
import pygame
from lib import root

def settings(screen, clock):
    global run
    run = True

    if root.play_anims:
        img = root.settings_imgs[-1]
    else:
        img = pygame.image.load(os.path.join("data", "background", "settings59.jpg"))

    back_button = root.text_button(25, (255, 255, 255), "Back")
    def back_button_function():
        global run
        run = False
    back_button.func = back_button_function

    buttons = [back_button]

    sfx_slider = root.slider(root.screen_size[0] * 0.6, 30, root.sound_effects_volume, (255, 255, 255), (255, 255, 255))
    music_slider = root.slider(root.screen_size[0] * 0.6, 30, root.music_volume, (255, 255, 255), (255, 255, 255))

    sliders = [sfx_slider, music_slider]

    animations_toggle = root.toggle(100, 30, root.screen_size[0] * 0.7, 255, root.play_anims)

    toggles = [animations_toggle]

    heading = root.larger_font.render("Settings", True, (255, 255, 255))
    sfx_label = root.medium_font.render("SFX Volume", True, (255, 255, 255))
    music_label = root.medium_font.render("Music Volume", True, (255, 255, 255))
    animations_label = root.medium_font.render("Play Animations", True, (255, 255, 255))

    def redraw_win(screen):
        screen.fill((255, 255, 255))
        screen.blit(img, (0, 0))
        back_button.draw(screen, 75, 30)
        sfx_slider.draw(screen, 75, 255)
        music_slider.draw(screen, 75, 350)
        animations_toggle.draw(screen)

        screen.blit(sfx_label, (75, 220))
        screen.blit(music_label, (75, 315))
        screen.blit(animations_label, (root.screen_size[0] * 0.7, 220))
        screen.blit(heading, (75, 100))

    while run:
        root.sound_effects_volume = sfx_slider.value
        root.music_volume = music_slider.value
        root.car_idle.set_volume(root.sound_effects_volume)
        root.music.set_volume(root.music_volume)

        root.play_anims = animations_toggle.state
        
        redraw_win(screen)
        pygame.display.flip()
        clock.tick(30)
        root.update_UI(pygame.event.get(), buttons, sliders, toggles)

    return