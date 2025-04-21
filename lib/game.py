import os, sys, time, random, math
import pygame
from lib import root
from lib import postgame

def game(screen, clock, race_length):
    #Generating word bank from text file
    with open(os.path.join('data', 'words', 'english1000.txt')) as f:
        data = f.read()
        word_bank = data.split('\n')

    class word():
        def __init__(self):
            self.word = random.choice(word_bank)

        def draw(self, screen, x, y):
            self.text = root.medium_font.render(self.word, True, (255, 255, 255))
            self.x = x
            self.y = y
            screen.blit(self.text, (x, y))

    #Pause screen, called when escape pressed
    def pause(screen, clock, race_start):
        pause_start = time.time()
        s = pygame.Surface(root.screen_size, pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        pygame.display.flip()
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                #Exit when any key pressed
                if event.type == pygame.KEYDOWN:
                    return race_start + (time.time() - pause_start)

    #Single function to handle displaying all GUI
    def redraw_win(screen):
        screen.fill((255, 255, 255))
        screen.blit(root.game_imgs[math.floor(background_counter) % len(root.game_imgs)], (0, 0))
        
        #Text box + custom cursor typing indicator using sine
        position = [50, root.screen_size[1] - 100]

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(position[0], position[1], 300, 50), 3, 3)
        text_input = root.medium_font.render(current_word, True, (255, 255, 255))
        screen.blit(text_input, (position[0] + 20, position[1] + 11))
        pygame.draw.rect(screen, (abs(int(255 * math.sin(frame_counter/10))), abs(int(255 * math.sin(frame_counter/10))), abs(int(255 * math.sin(frame_counter/10)))), pygame.Rect(position[0] + 25 + len(current_word) * 16, position[1] + 11, 3, 30))

        #Words to type
        prev_width = 0
        prev_x = 0
        for i, word in enumerate(words):
            word.draw(screen, 50 + prev_x + prev_width, 570)
            prev_width = word.text.get_width()
            prev_x = word.x

        #Current gear display
        t = str(current_gear) + "th"
        if current_gear == 1:
            t = "1st"  
        elif current_gear == 2:
            t = "2nd"
        elif current_gear == 3:
            t = "3rd"
        throttle_bar.draw(screen)

        gear_text = root.medium_font.render(t + " GEAR", True, (255, 255, 255))
        screen.blit(gear_text, ((root.screen_size[0] - gear_text.get_width()) / 2, root.screen_size[1] - 90))

        #Race progress display
        race_progress_text = root.medium_font.render(str(round(distance)) + " / " + str(race_length), True, (255, 255, 255))
        screen.blit(race_progress_text, ((root.screen_size[0] - race_progress_text.get_width()) / 2, 80))
        race_progress.draw(screen)
        
    words = []
    max_words = 10
    current_word = ""

    current_gear = 1
    throttle = 1
    distance = 0
    race_progress = root.progress_bar(1200, 30, 40, 40, (255, 255, 255), race_length, int(race_length / 500))
    throttle_bar = root.progress_bar(300, 50, root.screen_size[0] - 375, root.screen_size[1] - 100, (255, 255, 255), 2, 2)

    backspace_pressed = time.time() * 2
    background_counter = 0
    frame_counter = 0
    race_end = False
    end_animation_length = 3
    run = True

    last_boost = time.time()
    race_start = time.time()
    while run:
        if len(words) < max_words:
            words.append(word())

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                root.save()
                sys.exit()

            if event.type == pygame.KEYDOWN and not race_end:
                #Pause
                if event.key == 27:
                    race_start = pause(screen, clock, race_start)

                #Checking for number keys (shifting gears)
                if event.key >= 49 and event.key <= 54:
                    gear_to = event.key - 48
                    if throttle > gear_to:
                        current_gear = gear_to

                #Checking for spacebar or enter pressed
                elif event.key == 32 or event.key == 13 or event.key == 10:
                    for w in words:
                        if w.word == current_word:
                            current_word = ""
                            words.remove(w)
                            throttle = min(current_gear + 2, throttle + (0.225 * (7 - current_gear)))
                            last_boost = time.time()
                            rev = pygame.mixer.Sound(random.choice(root.revs))
                            rev.set_volume(1 * root.sound_effects_volume)
                            rev.play(0, 0, 100)

                #Checking for backspace pressed
                elif event.key == 8:
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        current_word = ''
                    else:
                        backspace_pressed = time.time()
                        current_word = current_word[:-1]

                #Checking keycode is within typable ASCII characters
                elif ((event.key >= 97 and event.key <= 122) or event.key == 39) and len(current_word) < 16:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        #Shifting ASCII keycode by 32 positions if shift is held down
                        current_word += chr(event.key - 32)
                    else:
                        current_word += chr(event.key)

            if event.type == pygame.KEYUP:
                backspace_pressed = time.time() * 2

        #Handling for backspace being held down for more than half a second
        if time.time() - backspace_pressed > .5:
            current_word = current_word[:-1]

        #Number value for reference in background changing
        if root.play_anims:
            if background_counter < len(root.game_imgs) - throttle:
                background_counter += throttle
            else:
                background_counter = 0

        #Number value for other reference
        if frame_counter < 60:
            frame_counter += 1
        else:
            frame_counter = 0

        redraw_win(screen)

        if race_end:
            #Race end animation
            opacity = (time.time() - race_end_timestamp) / end_animation_length
            throttle *= 0.98

            s = pygame.Surface(root.screen_size)
            s.set_alpha(min(1, opacity) * 255)
            s.fill((255,255,255))
            screen.blit(s, (0,0)) 

            if opacity > 1:
                run = False
        else:
            #Slow down car if user stops typing, taking into account last time word was typed and the current gear
            last_boost_factor = 0.75 - min(0.75, time.time() - last_boost)
            current_gear_factor = 1 - (7 - current_gear) / 700
            current_gear_factor = current_gear_factor + (1 - current_gear_factor) * last_boost_factor
            throttle = max(current_gear, throttle * current_gear_factor)
            #Increase distance travelled and update race progress bar
            distance = min(distance + throttle, race_length)
            race_progress.current = distance
            #End race
            if distance >= race_length:
                race_end = True
                race_end_timestamp = time.time()
                race_time = race_end_timestamp - race_start

        #Update throttle bar value
        throttle_bar.current = throttle - current_gear

        pygame.display.flip()
        clock.tick(30)
    
    postgame.postgame(screen, clock, race_time, race_length)
    return