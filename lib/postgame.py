import os, sys, math, time
import pygame
from lib import root

heading = root.large_font.render("RACE COMPLETE", True, (0, 0, 0))
name_heading = root.medium_font.render("Enter Your Name", True, (0, 0, 0))
def postgame(screen, clock, race_time, race_length):
    save_button = root.text_button(25, (0, 0, 0), "Save to Highscores")
    def save_button_function(name, race_time):
        f = open(os.path.join('data', 'saved', 'Highscores.txt'), "a")
        f.write(name + ':' + str(round(race_time, 2)) + ':' + str(race_length) + '\n')
        f.close()
        global run
        run = False
    save_button.func = save_button_function

    exit_button = root.text_button(25, (0, 0, 0), "Exit Without Saving")
    def exit_button_function(name, race_time):
        global run
        run = False
    exit_button.func = exit_button_function

    buttons = [save_button, exit_button]

    current_word = ""
    frame_counter = 0
    def redraw_win(screen, race_time):
        screen.fill((255, 255, 255))
        score = root.super_font.render(str(round(race_time, 2)) + 's', True, (0, 0, 0))

        screen.blit(heading, (75, 170))
        screen.blit(score, (75, 250))

        #Text box
        width, height = 400, 50
        position = [root.screen_size[0] - 75 - width, 340]
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(position[0], position[1], width, height), 3, 3)
        text_input = root.medium_font.render(current_word, True, (0, 0, 0))
        screen.blit(text_input, (position[0] + 20, position[1] + 11))
        pygame.draw.rect(screen, (abs(int(255 * math.sin(frame_counter/10))), abs(int(255 * math.sin(frame_counter/10))), abs(int(255 * math.sin(frame_counter/10)))), pygame.Rect(position[0] + 25 + len(current_word) * 16, position[1] + 11, 3, 30))

        screen.blit(name_heading, (position[0], position[1] - 40))    

        exit_button.draw(screen, 75, 620)
        save_button.draw(screen, root.screen_size[0] - save_button.width - 75, 620)
        
    global run
    run = True
    name = "Anonymous"

    backspace_pressed = time.time() * 2
    save_button.hovered = False
    exit_button.hovered = False

    redraw_win(screen, race_time)
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            #Breaking out of the loop if window closed
            if event.type == pygame.QUIT:
                pygame.quit()
                root.save()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #Checking keycode is within typable ASCII characters
                if ((event.key >= 97 and event.key <= 122) or event.key == 39) and len(current_word) < 16:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        #Shifting ASCII keycode by 32 positions if shift is held down
                        current_word += chr(event.key - 32)
                    else:
                        current_word += chr(event.key)
                #Checking for backspace pressed
                elif event.key == 8:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        current_word = ''
                    else:
                        backspace_pressed = time.time()
                        current_word = current_word[:-1]

            if event.type == pygame.KEYUP:
                backspace_pressed = time.time() * 2

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.hovered:
                        button.func(name, race_time)

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.update_hover(pos)
            
            name = current_word

        #Handling for backspace being held down for more than half a second
        if time.time() - backspace_pressed > .5:
            current_word = current_word[:-1]

        if frame_counter < 60:
            frame_counter += 1
        else:
            frame_counter = 0
        
        redraw_win(screen, race_time)
        pygame.display.flip()
        clock.tick(30)
    
    return