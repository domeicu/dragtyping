import os, sys
import pygame
from lib import root

race_length_heading = root.large_font.render("Race Length", True, (255, 255, 255))
def highscores(screen, clock):
    #Global variables that need to be accessed within functions
    #Not great practice, but required - class field functions can't take unique parameters
    global run
    global scores_display_objects
    global scores
    global buttons
    global race_length
    run = True
    scores_display_objects = []
    scores = []
    buttons = []
    race_length = "1000"

    #Loading proper image if play_anims False (won't be loaded otherwise)
    if root.play_anims:
        img = root.highscores_imgs[-1]
    else:
        img = pygame.image.load(os.path.join("data", "background", "highscores59.jpg"))

    #Defining sort keys
    def return_name(obj):
        name = obj.name
        #Handling filler scores
        if name == ".................":
            return "zzzzzzzzzzzzzzzzzz"
        return obj.name
    
    def return_score(obj):
        #Handling filler scores
        try: return (float(obj.score))
        except: return (9999999999)

    #Insertion sort function which takes a sorting key parameter
    def insertion_sort(array, sort_key):
        for step in range(1, len(array)):
            key = array[step]
            j = step - 1
            #Compare key with each element on the left of it until an element smaller than it is found
            while j >= 0 and sort_key(key) < sort_key(array[j]):
                array[j + 1] = array[j]
                j = j - 1
            #Place key after the element just smaller than it.
            array[j + 1] = key

    #Defining buttons
    back_button = root.text_button(25, (255, 255, 255), "Back")
    def back_button_function():
        global run
        #Set run to False => breaks out of function, returns to menu
        run = False
    back_button.func = back_button_function

    def race_length_button_function(button):
        global race_length
        global buttons
        #Set global race_length value
        race_length = button.text[:-1]
        #Unpress all buttons, press current button
        for b in buttons:
            b.pressed = False
        button.pressed = True
        #Reload scores into display objects
        load_scores(race_length)

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

    #Load scores function with pseudo linear search for race length
    def load_scores(race_length):
        global scores_display_objects
        global scores
        #Open file
        f = open(os.path.join('data', 'saved', 'Highscores.txt'), "r")
        fl = f.readline()
        scores = []
        scores_display_objects = []
        #Read line by line from file into array
        #Creates an array of arrays
        #Example of one element - ['Domenic', '18.63', '1000']
        while fl:
            scores.append(fl.strip().split(':'))
            fl = f.readline()
        #Create 10 score display objects
        #Creates filler values where file does not contain enough entries
        for i in range(10):
            try:
                if scores[i][2] == race_length:
                    obj = root.score_display(scores[i][0], scores[i][1])
                else:
                    obj = root.score_display(".................", "...")  
            except:
                obj = root.score_display(".................", "...")
            scores_display_objects.append(obj)

        #Sort twice, first by name (secondary sort)
        #Then by score (primary sort)
        insertion_sort(scores_display_objects, return_name)
        insertion_sort(scores_display_objects, return_score)
        
    load_scores(race_length)

    heading = root.larger_font.render("Highscores", True, (255, 255, 255))

    max_scores_to_display = 10
    def redraw_win(screen):
        screen.fill((255, 255, 255))
        screen.blit(img, (0, 0))
        #Draw all buttons
        back_button.draw(screen, 75, 30)
        l500_button.draw(screen, 75, 400)
        l1000_button.draw(screen, 175, 400)
        l5000_button.draw(screen, 275, 400)
        l10000_button.draw(screen, 375, 400)
        screen.blit(race_length_heading, (75, 320))
        #Display score objects
        for i in range(min(len(scores_display_objects), max_scores_to_display)):
            scores_display_objects[i].position = i
            scores_display_objects[i].draw(screen, 120, 750)
        screen.blit(heading, (75, 100))

    while run:        
        redraw_win(screen)
        pygame.display.flip()
        clock.tick(30)
        root.update_UI(pygame.event.get(), buttons)
    
    return