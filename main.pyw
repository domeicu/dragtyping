import os, time, random
import pygame
from lib import root
from lib import settings
from lib import highscores
from lib import tutorial
from lib import pregame
from lib import game

pygame.init()

screen = pygame.display.set_mode(root.screen_size)
display = pygame.Surface(root.screen_size)
pygame.Surface.convert_alpha(display)

pygame.display.set_caption("dragtyping")
pygame.display.set_icon(pygame.Surface((1, 1)))
clock = pygame.time.Clock()

title_text = root.larger_font.render("dragtyping", True, (255, 255, 255))

#Define buttons
play_button = root.text_button(35, (255, 255, 255), "Play")
def play_button_function():
    #Animated transition to camera angle of game animation
    if root.play_anims:
        for i in range(root.menu_frames):
            clock.tick(30)
            screen.fill((255, 255, 255))
            screen.blit(root.menu_imgs[i], (0, 0))
            pygame.display.flip()

    race_length = pregame.pregame(screen, clock)
    #Play white flash transition if player finished race
    if race_length:
        game.game(screen, clock, race_length)

        global load_time
        load_time = time.time()
    else:
        #Play animated transition if play_anims setting is true
        if root.play_anims:
            for i in range(root.menu_frames - 1, 0, -1):
                clock.tick(30)
                screen.fill((255, 255, 255))
                screen.blit(root.menu_imgs[i], (0, 0))
                pygame.display.flip()
    
    for button in buttons:
        button.hovered = False

play_button.func = play_button_function

settings_button = root.text_button(25, (255, 255, 255), "Settings")
def settings_button_function():
    #Play animated transition if play_anims setting is true
    if root.play_anims:
        for i in range(root.settings_frames):
            screen.fill((255, 255, 255))
            screen.blit(root.settings_imgs[i], (0, 0))
            pygame.display.flip()
            clock.tick(30)

    settings.settings(screen, clock)

    #Play animated transition if play_anims setting is true
    if root.play_anims:
        if root.menu_frames < 3:
            root.save()
            root.music.stop()
            root.car_idle.stop()
            root.initialise(screen)

        for i in range(root.settings_frames - 1, 0, -1):
            screen.fill((255, 255, 255))
            screen.blit(root.settings_imgs[i], (0, 0))
            pygame.display.flip()
            clock.tick(30)

    for button in buttons:
        button.hovered = False

settings_button.func = settings_button_function

highscores_button = root.text_button(25, (255, 255, 255), "Highscores")
def highscores_button_function():
    #Play animated transition if play_anims setting is true
    if root.play_anims:
        for i in range(root.highscores_frames):
            clock.tick(30)
            screen.fill((255, 255, 255))
            screen.blit(root.highscores_imgs[i], (0, 0))
            pygame.display.flip()

    highscores.highscores(screen, clock)
    
    #Play animated transition if play_anims setting is true
    if root.play_anims:
        for i in range(root.highscores_frames - 1, 0, -1):
            clock.tick(30)
            screen.fill((255, 255, 255))
            screen.blit(root.highscores_imgs[i], (0, 0))
            pygame.display.flip()

    for button in buttons:
        button.hovered = False

highscores_button.func = highscores_button_function

tutorial_button = root.text_button(25, (255, 255, 255), "Tutorial")
def tutorial_button_function():
    #Play animated transition if play_anims setting is true
    if root.play_anims:
        for i in range(root.menu_frames):
            clock.tick(30)
            screen.fill((255, 255, 255))
            screen.blit(root.menu_imgs[i], (0, 0))
            pygame.display.flip()

    tutorial.tutorial(screen, clock)

    #Play animated transition if play_anims setting is true
    if root.play_anims:
        for i in range(root.menu_frames - 1, 0, -1):
            clock.tick(30)
            screen.fill((255, 255, 255))
            screen.blit(root.menu_imgs[i], (0, 0))
            pygame.display.flip()
    for button in buttons:
        button.hovered = False

tutorial_button.func = tutorial_button_function

quit_button = root.text_button(25, (255, 255, 255), "Quit")
def quit_button_function():
    global run
    run = False
quit_button.func = quit_button_function

buttons = [play_button, settings_button, highscores_button, tutorial_button, quit_button]

root.initialise(screen)

load_time = time.time()
run = True
while run:
    root.update_UI(pygame.event.get(), buttons)

    screen.fill((255, 255, 255))
    screen.blit(root.menu_imgs[0], (0, 0))

    #Draw all text, buttons
    screen.blit(title_text, (75, 200))
    play_button.draw(screen, 75, 320)
    settings_button.draw(screen, 75, 410)
    highscores_button.draw(screen, 75, 460)
    tutorial_button.draw(screen, 75, 510)
    quit_button.draw(screen, 75, 560)

    #White flash animation handling
    opacity = (time.time() - load_time) / 1
    s = pygame.Surface(root.screen_size)
    s.set_alpha(max(0, 1 - opacity) * 255)
    s.fill((255,255,255))
    screen.blit(s, (0,0))

    pygame.display.flip()
    clock.tick(30)

root.save()