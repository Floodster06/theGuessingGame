import math
import random
import time

import pygame


# random.randint(0, n)
# includes 0 and n

pygame.init()

res = (720, 720)
screen = pygame.display.set_mode(res)

current_screen = "title"
current_factor = 1
user_text = ""
input_active = False

previous_guesses = ["", ""]

current_guesses = 0
remaining_guesses = 0


# palette
color_purple = (163, 73, 164)
color_green = (34, 177, 76)
color_white = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_black = (0, 0, 0)
color_red = (255, 98, 34)
color_active = (64, 226, 255)

input_box_color = color_white

screen_width = screen.get_width()
screen_height = screen.get_height()

# [x coord = 0, y coord = 1, width = 2, height = 3]
# + = right, down
# - = left, up

# title screen
quit_button = [screen_width / 2 - 120, screen_height / 2, 280, 60]
play_button = [screen_width / 2 - 120, screen_height / 2 - 75, 280, 60]

# play screen
difficulty_display = [100, 100, 85, 0]
back_to_menu_button = [screen_width / 2 - 60, screen_height - 50, 140, 45]
input_box = [screen_width / 2 - 220, screen_height / 2, 450, 90]
remaining_guesses_box = [input_box[0] + 475, screen_height / 2, 90, 90]



buttonfont = pygame.font.SysFont('Gill Sans MT', 60)
titlefont = pygame.font.SysFont('Euphemia', 120)
displayfont = pygame.font.SysFont('OCR-A Extended', 120)
subfont = pygame.font.SysFont('Segoe UI', 50)
smallfont = pygame.font.SysFont('Verdana', 15)

text_quit = buttonfont.render('Quit', True, color_black)
text_play = buttonfont.render('Play', True, color_black)
text_title = titlefont.render('Guessing Game', True, color_black)
text_author = subfont.render('Flood M.L., 31226', True, color_purple)
title_display_1 = titlefont.render("Guessing", True, color_black)
title_display_2 = titlefont.render("Game", True, color_black)

description_text_L0 = smallfont.render("Welcome to the Guessing Game!", True, color_purple)
description_text_L1 = smallfont.render("The game challenges you to guess a random number, with difficulty increasing as you succeed.", True, color_purple)
description_text_L2 = smallfont.render("A random number will be within 1 and a specified upper limit. You need to guess this number.", True, color_purple)
description_text_L3 = smallfont.render("The game will let you know if your guess is low or high. Guess until you find the number.", True, color_purple)
description_text_L4 = smallfont.render("If you guess the number in less attempts than a threshold, the upper limit will increase.", True, color_purple)
description_text_L5 = smallfont.render("If an invalid guess is entered, you will be told. Invalid entries still count as a guess.", True, color_purple)
description_text_L6 = smallfont.render("Bonne chance, and have fun!", True, color_purple)

extra_info_text = subfont.render("CSE101 |  Dr. Y Liang  | 10/28/24", True, color_black)
guess_input_box_label_text = buttonfont.render('GUESS:', True, color_black)



quit_button_rect = pygame.draw.rect(screen, color_dark,[quit_button[0], quit_button[1], quit_button[2], quit_button[3]])  # quit button
play_button_rect = pygame.draw.rect(screen, color_dark,[play_button[0], play_button[1], play_button[2], play_button[3]])  # play button
back_to_menu_button_rect = pygame.draw.rect(screen, color_white, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]])
input_box_rect = pygame.draw.rect(screen, color_white, [input_box[0], input_box[1], input_box[2], input_box[3]])

winning_sound = pygame.mixer.Sound('winning_sound.mp3')


def title_screen(condition):

    global quit_button_rect
    global play_button_rect


    if condition == "hovering_play":

        quit_button_rect = pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])
        play_button_rect = pygame.draw.rect(screen, color_dark, [play_button[0], play_button[1], play_button[2], play_button[3]])

    elif condition == "hovering_quit":

        quit_button_rect = pygame.draw.rect(screen, color_dark, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])
        play_button_rect = pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]])

    else:

        quit_button_rect = pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])  # quit button
        play_button_rect = pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]])  # play button

    pygame.draw.rect(screen, color_black, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]], 5)
    pygame.draw.rect(screen, color_black, [play_button[0], play_button[1], play_button[2], play_button[3]], 5)

    screen.blit(text_author, (screen_width / 2 - 170, screen_height - 625))
    screen.blit(text_title, (screen_width / 2 - 325, screen_height - 700))

    screen.blit(description_text_L0, (screen_width / 2 - 100, screen_height - 280))
    screen.blit(description_text_L1, (screen_width / 2 - 360, screen_height - 240))
    screen.blit(description_text_L2, (screen_width / 2 - 350, screen_height - 220))
    screen.blit(description_text_L3, (screen_width / 2 - 335, screen_height - 200))
    screen.blit(description_text_L4, (screen_width / 2 - 330, screen_height - 180))
    screen.blit(description_text_L5, (screen_width / 2 - 315, screen_height - 160))
    screen.blit(description_text_L6, (screen_width / 2 - 85, screen_height - 120))

    screen.blit(extra_info_text, (screen_width / 2 - 320, screen_height - 70))








    screen.blit(text_quit, (quit_button[0] + 100, quit_button[1] + 10))
    screen.blit(text_play, (play_button[0] + 100, play_button[1] + 10))


def play_screen(condition):

    global back_to_menu_button_rect
    global input_box_color
    global current_factor
    global remaining_guesses

    remaining_guesses = maxNumGuesses - current_guesses



    pygame.draw.circle(screen, color_purple, [difficulty_display[0], difficulty_display[1]], difficulty_display[2])
    pygame.draw.circle(screen, color_black, [difficulty_display[0], difficulty_display[1]], difficulty_display[2], 5)

    pygame.draw.rect(screen, color_white, [input_box[0], input_box[1], input_box[2], input_box[3]])
    pygame.draw.rect(screen, color_black, [input_box[0], input_box[1], input_box[2], input_box[3]], 5)

    pygame.draw.rect(screen, color_purple, [remaining_guesses_box[0], remaining_guesses_box[1], remaining_guesses_box[2], remaining_guesses_box[3]])
    pygame.draw.rect(screen, color_black, [remaining_guesses_box[0], remaining_guesses_box[1], remaining_guesses_box[2], remaining_guesses_box[3]], 5)

    user_input_text = subfont.render(user_text, True, color_black)
    screen.blit(user_input_text, (input_box[0] + 25, input_box[1] + 15))
    screen.blit(guess_input_box_label_text, (input_box[0] + 160, input_box[1] - 40))



    if condition == "hovering_back_to_menu":

        pygame.draw.rect(screen, color_red, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]])
        pygame.draw.rect(screen, color_black, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]], 3)
    else:
        pygame.draw.rect(screen, color_white, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]])
        pygame.draw.rect(screen, color_black, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]], 3)

    if condition == "win":

        winning_sound.play()
        time.sleep(0.5)
        winning_sound.stop()






    factor_display = displayfont.render(str(current_factor), True, color_black)
    remaining_guesses_display = displayfont.render(str(remaining_guesses), True, color_black)
    screen.blit(factor_display, (difficulty_display[0] - 25, difficulty_display[1] - 45))
    screen.blit(remaining_guesses_display, (remaining_guesses_box[0] + 25, remaining_guesses_box[1] + 5))

    screen.blit(title_display_1, (difficulty_display[0] + 150, difficulty_display[1] - 75))
    screen.blit(title_display_2, (difficulty_display[0] + 210, difficulty_display[1] - 0))

    screen.blit(text_quit, (back_to_menu_button[0] + 25, back_to_menu_button[1] + 5))







def new_numbers():

    global n
    global maxNumGuesses
    global current_guesses

    current_guesses = 0
    n = random.randint(1, int(math.pow(10, current_factor)))
    maxNumGuesses = int(math.log(n) / math.log(10)) * 3 + 2




def game():

    global current_factor
    global current_guesses
    global user_text
    global remaining_guesses

    current_guesses += 1

    print("n = " , n)
    print("factor = " , current_factor)
    print("max guesses = " , maxNumGuesses)
    print("current guesses = ", current_guesses)


    if int(user_text) == n:

        play_screen("win")
        print("win")

        if current_guesses < maxNumGuesses:

            current_factor += 1
        
        new_numbers()
        current_guesses = 0


    elif int(user_text) > n:

        play_screen("high")
        print("high")


    elif int(user_text) < n:

        play_screen("low")
        print("low")

    user_text = ""

def quit_button_function():

    pygame.quit()

def play_button_function():

    global current_screen

    current_screen = "play"

def back_to_menu_function():

    global current_factor
    global current_screen
    global user_text

    user_text = ""
    current_screen = "title"
    current_factor = 1

def user_guess():

    global user_text
    global current_guesses

    if not user_text.isnumeric():

        user_text = "Non-numeric input."
        current_guesses += 1
    else:

        game()






# [x coord = 0, y coord = 1, width = 2, height = 3]
# + = right, down
# - = left, up

# main loop

while True:

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:

            quit_button_function()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom and current_screen == "title":

                quit_button_function()
            elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom and current_screen == "title":

                new_numbers()
                play_button_function()
            elif back_to_menu_button_rect.left <= mouse[0] <= back_to_menu_button_rect.right and back_to_menu_button_rect.top <= mouse[1] <= back_to_menu_button_rect.bottom and current_screen == "play":

                back_to_menu_function()

        if ev.type == pygame.KEYDOWN and current_screen == "play":

            if ev.key == pygame.K_BACKSPACE and user_text != "":

                user_text = user_text[:-1]
            elif ev.key == pygame.K_RETURN:

                user_guess()
            else:

                user_text += ev.unicode




    screen.fill(color_green)

    mouse = pygame.mouse.get_pos()






    if current_screen == "title":

        if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom:

            title_screen("hovering_quit")

        elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom:

            title_screen("hovering_play")

        else:

            title_screen("default")

    elif current_screen == "play":

        if back_to_menu_button_rect.left <= mouse[0] <= back_to_menu_button_rect.right and back_to_menu_button_rect.top <= mouse[1] <= back_to_menu_button_rect.bottom:

            play_screen("hovering_back_to_menu")
        else:

            play_screen("default")












    pygame.display.update()






    pygame.display.update()
