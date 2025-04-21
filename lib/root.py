import pygame, os, sys, time
from textwrap import fill
pygame.init()

#Consistent screen size variable
screen_size = (1280, 720)

def initialise(screen):
    load_start = time.time()
    #Global variables for reference in all functions
    global car_idle
    global music
    global menu_frames
    global menu_imgs
    global highscores_frames
    global highscores_imgs
    global settings_frames
    global settings_imgs
    global game_frames
    global game_imgs
    global tutorial_frames
    global tutorial_imgs
    global rev_num
    global revs
    global sound_effects_volume
    global music_volume
    global play_anims

    #User options
    f = open(os.path.join('data', 'saved', 'UserPreferences.txt'), "r")

    #Volume
    try: sound_effects_volume = float(f.readline().split(':')[1])
    except: sound_effects_volume = 0.4
    try: music_volume = float(f.readline().split(':')[1])
    except: music_volume = 0.05

    #Visuals
    try: play_anims = f.readline().strip().split(':')[1] == "True"
    except: play_anims = True

    f.close()

    load_sound = pygame.mixer.Sound(os.path.join('data', 'audio', 'load.wav'))
    load_sound.set_volume(sound_effects_volume)
    load_sound.play()

    menu_frames = 60
    menu_imgs = []
    highscores_frames = 60
    highscores_imgs = []
    settings_frames = 60
    settings_imgs = []
    game_frames = 150
    game_imgs = []
    tutorial_frames = 8
    tutorial_imgs = []

    if not play_anims:
        menu_frames = 1
        highscores_frames = 1
        settings_frames = 1
        game_frames = 1

    rev_num = 3
    revs = []

    #Create array of images for menu background image
    for i in range(menu_frames):
        menu_imgs.append(pygame.image.load(os.path.join("data", "background", "menu" + "{:02d}".format(i) + ".jpg")))
        #Path to compressed images
        #menu_imgs.append(pygame.image.load(os.path.join("data", "background-m", "menu" + "{:02d}".format(i) + "_" + str(56 + i) + "_11zon.jpg")))
        display_loading_screen(screen, i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    #Create array of images for highscores background image
    for i in range(highscores_frames):
        highscores_imgs.append(pygame.image.load(os.path.join("data", "background", "highscores" + "{:02d}".format(i) + ".jpg")))
        display_loading_screen(screen, menu_frames + i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    #Create array of images for settings background image
    for i in range(settings_frames):
        settings_imgs.append(pygame.image.load(os.path.join("data", "background", "settings" + "{:02d}".format(i) + ".jpg")))
        display_loading_screen(screen, menu_frames + highscores_frames + i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    #Create array of images for game background image
    for i in range(game_frames):
        game_imgs.append(pygame.image.load(os.path.join("data", "background", "game" + "{:03d}".format(i) + ".jpg")))
        display_loading_screen(screen, menu_frames + highscores_frames + settings_frames + i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    #Create array of images for tutorial
    for i in range(tutorial_frames):
        tutorial_imgs.append(pygame.image.load(os.path.join("data", "tutorial", "slide" + str(i + 1) + ".png")))
        display_loading_screen(screen, menu_frames + highscores_frames + settings_frames + game_frames + i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    #Create array of rev sounds
    for i in range(rev_num):
        revs.append(os.path.join('data', 'audio', 'rev' + str(i + 1) + '.wav'))
        display_loading_screen(screen, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + i + 1, menu_frames + highscores_frames + settings_frames + game_frames + tutorial_frames + rev_num)

    music = pygame.mixer.Sound(os.path.join('data', 'audio', 'songs', 'dark_valley.mp3'))
    music.set_volume(music_volume)
    music.play(-1)

    car_idle = pygame.mixer.Sound(os.path.join('data', 'audio', 'car idle.wav'))
    car_idle.set_volume(sound_effects_volume)
    car_idle.play(-1)

    time.sleep(max(0, 1 - (time.time() - load_start)))

#Function for access from other files to save user preferences
def save():
    f = open(os.path.join('data', 'saved', 'UserPreferences.txt'), "w")
    f.write('sound_effects_volume:' + str(sound_effects_volume) + '\n')
    f.write('music_volume:' + str(music_volume) + '\n')
    f.write('play_anims:' + str(play_anims) + '\n')
    f.close()

def display_loading_screen(screen, current, max):
    pb = progress_bar(700, 40, (screen_size[0] - 700) / 2, 520, (0, 0, 0), max)
    pb.current = current
    #Blit loading screen
    screen.fill((255, 255, 255))
    #Warning messages
    warning_text = fill("This product does not endorse the behaviours presented within it. Under Australian federal law, it is a felony to engage in street racing and other related activities. The developers and distributors claim no responsibility for illegal conduct as a result of playing DRAGTYPING.", 74)
    wanring_text2 = fill("EPILEPSY WARNING: This product may contain rapid flashing graphics. Photosensitive players are advised to consult a medical professional before continuing.", 74)
    #Blit warning messages across multiple lines using custom function
    render_multi_line(screen, warning_text, 50, 230, 30)
    render_multi_line(screen, wanring_text2, 50, 390, 30)
    #screen.blit(loading_text2, (50, 650))
    pb.draw(screen)
    pygame.display.flip()
    #Allow user to quit while loading
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update_UI(events, buttons=[], sliders=[], toggles=[], textboxes=[]):
    for event in events:
            #Breaking out of the loop if window closed
            if event.type == pygame.QUIT:
                pygame.quit()
                save()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    #Call button function if hovered
                    if button.hovered:
                        if button.argument:
                            button.func(button.argument)
                        else:
                            button.func()
                click_pos = pygame.mouse.get_pos()
                #Change slider position based on mouse movement if hovered
                for slider in sliders:
                    if slider.hovered:
                        slider.initial_value = slider.value
                        slider.active = True
                        slider.click_pos = click_pos
                #Change toggle state if hovered
                for toggle in toggles:
                    if toggle.hovered:
                        toggle.state = not toggle.state

            if event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.active = False

            if event.type == pygame.MOUSEMOTION:
                #Update hover for all UI elements when mouse moved
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.update_hover(pos)
                for slider in sliders:
                    slider.update_hover(pos)
                    if slider.active:
                        slider.update_slider(slider.initial_value, slider.click_pos, pos)
                for toggle in toggles:
                    toggle.update_hover(pos)

class progress_bar():
    def __init__(self, width, height, x, y, colour, maxValue, segments=1):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.colour = colour
        self.current = 0
        self.max = maxValue
        self.segments = segments

    def draw(self, screen):
        #2 rectangles, one for border one for actual progress
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, self.width * max(min(self.current / self.max, 1), 0), self.height), 0, 3)
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height), 3, 3)
        #Draw lines to separate bar into segments
        for i in range(self.segments - 1):
            pygame.draw.rect(screen, self.colour, (pygame.Rect(self.x + self.width / (self.segments) * (i + 1), self.y, 3, self.height)))

class text_button():
    def __init__(self, size, colour, text):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.size = size
        self.colour = colour
        self.text = text
        self.hovered = False
        self.pressed = False
        self.func = None
        self.argument = None

    def update_hover(self, pos):
        #check if pos is within bounds of button
        #call on mouse movement event
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        #Alternative colours based on pressed down, hovered etc
        if self.pressed:
            c = (80, 80, 80)
        else:
            c = self.colour
        #Correspond number value to one of the fonts
        if self.size > 35:
            title_text = larger_font.render(self.text, True, c)
        elif self.size > 25:
            title_text = large_font.render(self.text, True, c)
        else:
            title_text = medium_font.render(self.text, True, c)

        if not self.pressed and self.hovered:
            title_text.set_alpha(127)

        self.width = title_text.get_width()
        self.height = title_text.get_height()
        #blitting text in centre of rectangle
        screen.blit(title_text, (self.x + self.width / 2 - title_text.get_width() / 2, self.y + self.height / 2 - title_text.get_height() / 2))

class slider():
    def __init__(self, width, height, value, main_colour, accent_colour):
        self.width = width
        self.height = height
        self.slider_pos_height = height * 1.4
        self.slider_pos_width = self.slider_pos_height / 21 * 9
        self.x = 0
        self.y = 0
        self.main_colour = main_colour
        self.accent_colour = accent_colour
        self.active = False
        self.hovered = False
        self.value = value
        self.slider_pos = 0
        self.initial_value = 0
        self.click_pos = 0

    def update_hover(self, pos):
        #check cursor position against own position, taking into account dimensions
        if pos[0] > self.slider_pos and pos[0] < self.slider_pos + self.slider_pos_width and pos[1] > self.y - self.height * 0.2 and pos[1] < self.y - self.height * 0.2 + self.slider_pos_height:
            self.hovered = True
        else:
            self.hovered = False

    def update_slider(self, initial_pos, click_pos, new_pos):
        #set value of slider based on cursor movement (only calls on mousedown)
        self.value = max(min(initial_pos + (new_pos[0] - click_pos[0]) / self.width, 1), 0)

    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        self.slider_pos = self.x + self.value * self.width - self.slider_pos_width / 2
        colour = self.accent_colour
        if self.hovered:
            colour = (150, 150, 150)
        #3 rectangles - one for border, one for slider position, one for slider background
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.x, self.y, self.slider_pos - self.x, self.height))
        pygame.draw.rect(screen, self.main_colour, pygame.Rect(self.x, self.y, self.width, self.height), 3, 5)
        pygame.draw.rect(screen, colour, pygame.Rect(self.slider_pos, self.y - self.height * 0.2, self.slider_pos_width, self.slider_pos_height), 0, 3)

class toggle():
    def __init__(self, width, height, x, y, state):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hovered = False
        self.state = state

    def update_hover(self, pos):
        #check if pos is within bounds of button
        #call on mouse movement event
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, screen):
        #Change colour based on hover state etc
        c = (255, 255, 255)
        if self.hovered:
            c = (150, 150, 150)
        x = self.x
        if self.state:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.x, self.y, self.width, self.height))
            x += self.width / 2
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height), 3, 5)
        pygame.draw.rect(screen, c, pygame.Rect(x, self.y - self.height * 0.1, self.width / 2, self.height * 1.2), 0, 3)
        screen.blit(medium_font.render(str(self.state), True, (150, 150, 150)), (self.x + self.width + 15, self.y))
    
class score_display():
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.position = 0

    def draw(self, screen, offsetX, offsetY):
        #Display 3 text objects - position, name, score
        screen.blit(medium_font.render(str(self.position + 1), True, (255, 255, 255)), (offsetY - 50, offsetX + self.position * 50))
        screen.blit(medium_font.render(self.name, True, (255, 255, 255)), (offsetY, offsetX + self.position * 50))
        screen.blit(medium_font.render(self.score + 's', True, (120, 120, 120)), (offsetY + 300, offsetX + self.position * 50))

#Custom function for rendering multiple lines
def render_multi_line(screen, text, x, y, fsize):
    lines = text.splitlines()
    for i, v in enumerate(lines):
        line = medium_font.render(v, True, (0, 0, 0))
        screen.blit(line, ((screen_size[0] - line.get_width()) / 2, y + fsize*i))

#Colours dictionary for easy access and modification
colours = {
    "background": (255, 255, 255),
    "text": (130, 130, 130),
    "activetext": (255, 255, 255),
    "incorrecttext": (255, 140, 140),
    "textbox": (240, 240, 240),
    "accent": (180, 250, 30)
}

#Fonts
medium_font = pygame.font.Font(os.path.join("data", "fonts", "AzeretMono-SemiBold.ttf"), 25)
large_font = pygame.font.Font(os.path.join("data", "fonts", "AzeretMono-SemiBold.ttf"), 45)
larger_font = pygame.font.Font(os.path.join("data", "fonts", "AzeretMono-SemiBold.ttf"), 75)
super_font = pygame.font.Font(os.path.join("data", "fonts", "AzeretMono-SemiBold.ttf"), 150)