"""
Lab05: Loop
Royal Military College of Canada
CSE101
Dr. Yawei Liang
OCdt Flood 31226
October 13, 2024

The goal of this lab is to allow the user to guess a randomly generated number, n, and if successfully guessed within a certain threshold, increase the upper limit of the random number for the next round.
The program will allow the user to input a guess, and inform the user if the guess is too high (up arrow) or too low (down arrow).
As an added bonus, the entire program will be run in a graphical user interface using the pygame module.
"""
import math # used for advanced calculations, like logarithms and powers
import random # used for random number generation
import sys # used for getting access to objects maintained by the interpreter
import os # used for more modularity between systems
import time # used for delays

import pygame # used for GUI

pygame.init() # initializes pygame

res = (720, 720) # sets screen resolution to 720x720px
screen = pygame.display.set_mode(res) # declares screen variable (where everything else will go on top of)

screen_width = screen.get_width() # sets screen width equal to the width of the screen (720px)
screen_height = screen.get_height() # sets screen height equal to the height of the screen (720px)

current_screen = "title" # the variable which will determine current screen
current_factor = 1 # the variable which determines upper limit of n
user_text = "" # the string variable for the inputted user text

previous_guesses = ["", ""] # holds the two most recent user guesses
previous_values = ["", ""] # holds the two most recent high/low values of the last two guesses

current_guesses = 0 # how many guesses the user has taken
remaining_guesses = 0 # max guesses - current guesses (starts at 0, however)

# color palette, with variables being tuples storing RGB values
color_purple = (163, 73, 164) # secondary color used
color_green = (34, 177, 76) # back drop, primary color
color_white = (255, 255, 255) # most interactable objects and text holders
color_dark = (100, 100, 100) # button hover
color_black = (0, 0, 0) # used for outlines and text inside of white rectangles (with the exception of extra info on title screen)
color_red = (255, 98, 34) # back to menu button hover
# font palette, using default windows system fonts. integer value in brackets = size in pixels
buttonfont = pygame.font.SysFont('Gill Sans MT', 60) # for buttons
titlefont = pygame.font.SysFont('Euphemia', 120) # for main titles
displayfont = pygame.font.SysFont('OCR-A Extended', 120) # used for difficulty + current guesses display
subfont = pygame.font.SysFont('Segoe UI', 50) # used for sub titles
smallfont = pygame.font.SysFont('Verdana', 15) # used for the description

# all values are in pixels
# [x coord = 0, y coord = 1, width = 2, height = 3]
# + = right, down
# - = left, up

# title screen objects
quit_button = [screen_width / 2 - 120, screen_height / 2, 280, 60] # quit button rectangle
play_button = [screen_width / 2 - 120, screen_height / 2 - 75, 280, 60] # play button rectangle
# play screen objects
difficulty_display = [100, 100, 85, 0] # top left circle
back_to_menu_button = [screen_width / 2 - 60, screen_height - 50, 140, 45] # quit to menu button rectangle
input_box = [screen_width / 2 - 220, screen_height / 2, 450, 90] # centre main text input rectangle
remaining_guesses_box = [input_box[0] + 475, screen_height / 2, 90, 90] # middle right square
last_guess_box = [input_box[0] + 30, input_box[1] + 115, 395, 80] # first of two smaller rectangles
second_last_guess_box = [last_guess_box[0], last_guess_box[1] + 90, last_guess_box[2], last_guess_box[3]] # second of two smaller rectangles

# text renders with the string displayed, antialiasing = True, designated color.
# title page text renders
text_quit = buttonfont.render('Quit', True, color_black) # quit button text
text_play = buttonfont.render('Play', True, color_black) # play button text
text_title = titlefont.render('Guessing Game', True, color_black) # main title
text_author = subfont.render('Flood M.L., 31226', True, color_purple) # author subtext
extra_info_text = subfont.render("CSE101 |  Dr. Y Liang  | 10/28/24", True, color_black) # info at bottom text
# description (on title page) text renders
description_text_L0 = smallfont.render("Welcome to the Guessing Game!", True, color_purple) # line 1
description_text_L1 = smallfont.render("The game challenges you to guess a random number, with difficulty increasing as you succeed.", True, color_purple) # line 2
description_text_L2 = smallfont.render("A random number will be within 1 and a specified upper limit. You need to guess this number.", True, color_purple) # line 3
description_text_L3 = smallfont.render("The game will say if your guess is low (down arrow) or high (up arrow). Guess until you get it.", True, color_purple) # line 4
description_text_L4 = smallfont.render("If you guess the number in less attempts than a threshold, the upper limit will increase.", True, color_purple) # line 5
description_text_L5 = smallfont.render("If an invalid guess is entered, you will be told. Invalid entries still count as a guess.", True, color_purple) # line 6
description_text_L6 = smallfont.render("Bonne chance, and have fun!", True, color_purple) # line 7
# game page text renders
title_display_1 = titlefont.render("Guessing", True, color_black) # top half of title
title_display_2 = titlefont.render("Game", True, color_black) # bottom half of title
guess_input_box_label_text = buttonfont.render('GUESS:', True, color_black) # text above input box

# defining button rectangles for easier coordinate mapping; doesn't actually draw any shapes
quit_button_rect = pygame.draw.rect(screen, color_white,[quit_button[0], quit_button[1], quit_button[2], quit_button[3]]) # quit button (title screen)
play_button_rect = pygame.draw.rect(screen, color_white,[play_button[0], play_button[1], play_button[2], play_button[3]]) # play button (title screen)
back_to_menu_button_rect = pygame.draw.rect(screen, color_white, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]]) # quit to menu button (play screen)

# function for getting absolute paths to resources on any machine
def resource_path(relative_path):

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# defining other types of required elements for the game
default_dash = pygame.image.load(resource_path('dash.png')) # default symbol
too_low_arrow = pygame.image.load(resource_path('down_arrow.png')) # too low symbol
too_high_arrow = pygame.image.load(resource_path('up-arrow.png')) # too high symbol
winning_sound = pygame.mixer.Sound(resource_path('winning_sound.mp3')) # sound for when you guess n correctly

# displays the title screen, depending on given condition
def title_screen(condition):

    if condition == "hovering_play": # if user is hovering over the play button

        pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]]) # render the quit button as white
        pygame.draw.rect(screen, color_dark, [play_button[0], play_button[1], play_button[2], play_button[3]]) # render the play button as darker

    elif condition == "hovering_quit": # if user is hovering over the quit button

        pygame.draw.rect(screen, color_dark, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]]) # render the quit button as darker
        pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]]) # render the play button as white

    else: # if the user isn't hovering any buttons

        pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])  # render quit button as white
        pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]])  # render play button as white

    # always render the borders for the buttons
    pygame.draw.rect(screen, color_black, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]], 5) # quit button black border
    pygame.draw.rect(screen, color_black, [play_button[0], play_button[1], play_button[2], play_button[3]], 5) # play button black border

    screen.blit(text_title, (screen_width / 2 - 325, screen_height - 700))  # displays main title
    screen.blit(text_author, (screen_width / 2 - 170, screen_height - 625)) # displays author text
    # displays description text
    screen.blit(description_text_L0, (screen_width / 2 - 100, screen_height - 280)) # line 1
    screen.blit(description_text_L1, (screen_width / 2 - 360, screen_height - 240)) # line 2
    screen.blit(description_text_L2, (screen_width / 2 - 350, screen_height - 220)) # line 3
    screen.blit(description_text_L3, (screen_width / 2 - 353, screen_height - 200)) # line 4
    screen.blit(description_text_L4, (screen_width / 2 - 330, screen_height - 180)) # line 5
    screen.blit(description_text_L5, (screen_width / 2 - 315, screen_height - 160)) # line 6
    screen.blit(description_text_L6, (screen_width / 2 - 85, screen_height - 120)) # line 7

    screen.blit(extra_info_text, (screen_width / 2 - 320, screen_height - 70)) # displays extra info text

    screen.blit(text_quit, (quit_button[0] + 100, quit_button[1] + 10)) # displays quit button text
    screen.blit(text_play, (play_button[0] + 100, play_button[1] + 10)) # displays play button text

# displays the screen when playing, based on the given condition
def play_screen(condition):

    # globalises variables so they can be edited within the function
    global current_factor # current factor
    global remaining_guesses # remaining guesses until you reach max num guesses threshold

    remaining_guesses = maxNumGuesses - current_guesses # remaining guesses = maxNumGuesses - amount of guessed guesses

    # rendering of all on screen shapes
    # top left circle used as background for current factor
    pygame.draw.circle(screen, color_purple, [difficulty_display[0], difficulty_display[1]], difficulty_display[2]) # main circle
    pygame.draw.circle(screen, color_black, [difficulty_display[0], difficulty_display[1]], difficulty_display[2], 5) # border
    # main text input box in centre of screen
    pygame.draw.rect(screen, color_white, [input_box[0], input_box[1], input_box[2], input_box[3]]) # main rectangle
    pygame.draw.rect(screen, color_black, [input_box[0], input_box[1], input_box[2], input_box[3]], 5) # border
    # guessed guesses box on middle right of screen
    pygame.draw.rect(screen, color_purple, [remaining_guesses_box[0], remaining_guesses_box[1], remaining_guesses_box[2], remaining_guesses_box[3]]) # main square
    pygame.draw.rect(screen, color_black, [remaining_guesses_box[0], remaining_guesses_box[1], remaining_guesses_box[2], remaining_guesses_box[3]], 5) # border
    # most recent guess box below input box
    pygame.draw.rect(screen, color_white, [last_guess_box[0], last_guess_box[1], last_guess_box[2], last_guess_box[3]]) # main rectangle
    pygame.draw.rect(screen, color_black, [last_guess_box[0], last_guess_box[1], last_guess_box[2], last_guess_box[3]], 3) # border
    # second most recent guess box below input box
    pygame.draw.rect(screen, color_white, [second_last_guess_box[0], second_last_guess_box[1], second_last_guess_box[2], second_last_guess_box[3]]) # main rectangle
    pygame.draw.rect(screen, color_black, [second_last_guess_box[0], second_last_guess_box[1], second_last_guess_box[2], second_last_guess_box[3]], 3) # border


    user_input_text = subfont.render(user_text, True, color_black) # the text renderer for the text the user is typing

    screen.blit(user_input_text, (input_box[0] + 25, input_box[1] + 15)) # displays the user's typed guess
    screen.blit(guess_input_box_label_text, (input_box[0] + 160, input_box[1] - 40))  # displays the text above text input box

    # checks if most recent guess was too high or low and displays arrow accordingly
    match previous_values[0]: # parameter = previous_values[0]
        case "low": # if guess was low

            screen.blit(too_low_arrow, (last_guess_box[0] + 400, last_guess_box[1])) # display down arrow image
        case "high": # if guess was high

            screen.blit(too_high_arrow, (last_guess_box[0] + 400, last_guess_box[1])) # display up arrow image
        case _: # if the value is empty

            screen.blit(default_dash, (last_guess_box[0] + 400, last_guess_box[1])) # display dash image
    # checks if second most recent guess was too high or low and displays arrow accordingly
    match previous_values[1]: # parameter = previous_values[1]
        case "low":

            screen.blit(too_low_arrow, (second_last_guess_box[0] + 400, second_last_guess_box[1]))
        case "high":

            screen.blit(too_high_arrow, (second_last_guess_box[0] + 400, second_last_guess_box[1]))
        case _:

            screen.blit(default_dash, (second_last_guess_box[0] + 400, second_last_guess_box[1]))


    if condition == "hovering_back_to_menu": # if user is hovering over the quit back to menu button

        pygame.draw.rect(screen, color_red, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]]) # color the quit button red
    else: # if user is not hovering over the quit back to menu button
        pygame.draw.rect(screen, color_white, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]]) # color the quit button white

    pygame.draw.rect(screen, color_black,[back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]],3) # draw the border around the quit button


    if condition == "win": # if the user guesses n correctly

        winning_sound.play() # play victory sound
        time.sleep(0.75) # pause game for 0.5 seconds to allow sound to play
        winning_sound.stop() # stop victory sound


    factor_display = displayfont.render(str(current_factor), True, color_black) # renders the current factor
    remaining_guesses_display = displayfont.render(str(current_guesses), True, color_black) # renders the amount of user guesses

    screen.blit(factor_display, (difficulty_display[0] - 25, difficulty_display[1] - 45)) # displays the current factor
    screen.blit(remaining_guesses_display, (remaining_guesses_box[0] + 25, remaining_guesses_box[1] + 5)) # displays the amount of user guesses

    screen.blit(title_display_1, (difficulty_display[0] + 150, difficulty_display[1] - 75)) # displays the first half of the title
    screen.blit(title_display_2, (difficulty_display[0] + 210, difficulty_display[1] - 0)) # displays the second half of the title
    screen.blit(text_quit, (back_to_menu_button[0] + 25, back_to_menu_button[1] + 5)) # displays the text over the quit button

    last_guess_text = subfont.render(previous_guesses[0], True, color_black) # renders the most recent guess
    second_last_guess_text = subfont.render(previous_guesses[1], True, color_black) # renders the second most recent guess

    screen.blit(last_guess_text, (last_guess_box[0] + 5, last_guess_box[1])) # displays most recent guess
    screen.blit(second_last_guess_text, (second_last_guess_box[0] + 5, second_last_guess_box[1])) # displays second most recent guess

# function for generating new values
def new_numbers():

    # globalises values so they can be edited + accessed outside the function
    global n
    global maxNumGuesses
    global current_guesses

    current_guesses = 0 # sets times the user has guessed to 0
    n = random.randint(1, int(math.pow(10, current_factor))) # generates a random new n value, from 1 to 10^factor
    maxNumGuesses = int(math.log(n) / math.log(10)) * 3 + 2 # generates a new max number of guesses, based on provided mathematical formula

# main game function
def game():

    # globalises values so they can be edited + accessed outside the function
    global current_factor
    global current_guesses
    global user_text
    global remaining_guesses
    global previous_guesses
    global previous_values

    current_guesses += 1 # accumulates user guesses by 1


    if current_guesses == 1: # if it's the users first guess

        previous_guesses[0] = user_text # the most recent guess is the current guess
    else: # if its not the users first guess

        previous_values[1] = previous_values[0] # the old most recent data point is now the second most data point
        previous_guesses[1] = previous_guesses[0] # the old most recent guess is now the second most recent guess
        previous_guesses[0] = user_text # the most recent guess is the current guess


    if int(user_text) == n: # if the guess is the same as n

        play_screen("win") # run play screen function with win condition

        if current_guesses <= maxNumGuesses: # if the times it took for the user to guess was less than the max

            current_factor += 1 # increase the difficulty level - aka the factor - by 1
        
        new_numbers() # generate new numbers
        previous_guesses = ["", ""] # empty previous guesses array
        previous_values = ["", ""] # empty previous guess values array
    elif int(user_text) > n: # else if the users guess is higher than n

        previous_values[0] = "high" # assign 'high' into array as the most recent data point
        play_screen("high") # run play screen function
    elif int(user_text) < n: # else if the users guess is lower than n

        previous_values[0] = "low" # assign 'low' into array as the most recent data point
        play_screen("low") # run play screen function

    user_text = "" # reset user text input to empty

# function that checks user's guess before entering it into system
def user_guess():

    # globalisation to allow modification
    global user_text
    global current_guesses

    if not user_text.isnumeric(): # if the inputted next is not an integer value (eg. "-1" or "knucklehead" or "900s")

        user_text = "Non-numeric input." # set text in input box to this
        current_guesses += 1 # increase guesses by 1 still
    elif int(user_text) > math.pow(10, current_factor) or int(user_text) < 1: # if the guess is outside of the current range

        user_text = "Out of range." # set text in input box to this
        current_guesses += 1 # increase guesses by 1 still
    else: # if guess is valid

        game() # run game function

# function for when title screen quit button is pressed
def quit_button_function():

    pygame.quit() # kills GUI
    sys.exit("Quit game.") # exits program

# function for when title screen play button is pressed
def play_button_function():

    global current_screen # allows variable to be edited

    current_screen = "play" # sets current screen to 'play'

# function for when play screen quit button is pressed
def back_to_menu_function():

    # globalises necessary variables
    global current_factor
    global current_screen
    global user_text
    global previous_guesses
    global previous_values

    user_text = "" # emptys inputted text
    previous_guesses = ["", ""]  # empty previous guesses array
    previous_values = ["", ""]  # empty previous guess values array
    current_screen = "title" # sets current screen to 'title'
    current_factor = 1 # resets factor to 1

# main loop
while True: # will always run as long as program isnt quit

    for ev in pygame.event.get(): # if an event, 'ev', happens

        if ev.type == pygame.QUIT: # if the ev is clicking the X in the top right

            quit_button_function() # run the quit button function

        if ev.type == pygame.MOUSEBUTTONDOWN: # if the ev is a mouse click

            if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom and current_screen == "title": # if the mouse coords are within the quit button dimensions and on the title screen

                quit_button_function() # run the quit button function
            elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom and current_screen == "title": # if the mouse coords are within the play button dimensions and on the title screen

                new_numbers() # generate new numbers
                play_button_function() # run the play button function
            elif back_to_menu_button_rect.left <= mouse[0] <= back_to_menu_button_rect.right and back_to_menu_button_rect.top <= mouse[1] <= back_to_menu_button_rect.bottom and current_screen == "play": # if the mouse coords are within the quit to menu button dimensions and on the play screen

                back_to_menu_function() # run the back to menu function

        if ev.type == pygame.KEYDOWN and current_screen == "play": # if the ev is a key click and the screen is on play

            if ev.key == pygame.K_BACKSPACE and user_text != "": # if the key was the backspace key and the current text isnt empty

                user_text = user_text[:-1] # delete the end value of the text
            elif ev.key == pygame.K_RETURN: # if the key was the enter key

                user_guess() # check the user guess
            else: # if it was any other key

                user_text += ev.unicode # append user_text with the unicode value of the event key


    screen.fill(color_green) # fill the back drop with green


    mouse = pygame.mouse.get_pos() # get the coordinates of the mouse


    if current_screen == "title": # if the current screen is the title screen

        if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom: # if the mouse is within the quit button dimensions

            title_screen("hovering_quit") # run title screen with condition of 'hovering_quit'
        elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom: # if the mouse is within the play button dimensions

            title_screen("hovering_play") # run title screen with condition of 'hovering_play'
        else:  # if the mouse is not within any button dimensions

            title_screen("default") # run title screen with the default condition

    elif current_screen == "play": # else if the current screen is the play screen

        if back_to_menu_button_rect.left <= mouse[0] <= back_to_menu_button_rect.right and back_to_menu_button_rect.top <= mouse[1] <= back_to_menu_button_rect.bottom: # if the mouse is within the quit to menu button dimensions

            play_screen("hovering_back_to_menu") # run play screen with the 'hovering_back_to_menu' condition
        else:  # if the mouse is not within any button dimensions

            play_screen("default") # run play screen with the 'default' condition

    pygame.display.update() # update the GUI display

# A sample output is not possible within the code for the program due to everything being done within a GUI.
# A PDF will be uploaded alongside the program executable and code with sample output screenshots.