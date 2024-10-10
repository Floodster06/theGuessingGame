import math
import random
import pygame
import sys

# random.randint(0, n)
# includes 0 and n

pygame.init()

res = (720, 720)
screen = pygame.display.set_mode(res)

current_screen = "title"

# palette
color_purple = (163, 73, 164)
color_green = (34, 177, 76)
color_white = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_black = (0, 0, 0)

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



smallfont = pygame.font.SysFont('Gill Sans MT', 60)
titlefont = pygame.font.SysFont('Euphemia', 120)
displayfont = pygame.font.SysFont('OCR-A Extended', 120)
subfont = pygame.font.SysFont('Segoe UI', 50)

text_quit = smallfont.render('Quit', True, color_black)
text_play = smallfont.render('Play', True, color_black)
text_title = titlefont.render('Guessing Game', True, color_black)
text_author = subfont.render('Flood M.L., 31226', True, color_purple)
title_display_1 = titlefont.render("Guessing", True, color_black)
title_display_2 = titlefont.render("Game", True, color_black)

quit_button_rect = pygame.draw.rect(screen, color_dark,[quit_button[0], quit_button[1], quit_button[2], quit_button[3]])  # quit button
play_button_rect = pygame.draw.rect(screen, color_dark,[play_button[0], play_button[1], play_button[2], play_button[3]])  # play button

def title_screen(condition):

    global quit_button_rect
    global play_button_rect


    if (condition == "hovering_play"):

        quit_button_rect = pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])
        play_button_rect = pygame.draw.rect(screen, color_dark, [play_button[0], play_button[1], play_button[2], play_button[3]])

    elif (condition == "hovering_quit"):

        quit_button_rect = pygame.draw.rect(screen, color_dark, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])
        play_button_rect = pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]])

    else:

        quit_button_rect = pygame.draw.rect(screen, color_white, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]])  # quit button
        play_button_rect = pygame.draw.rect(screen, color_white, [play_button[0], play_button[1], play_button[2], play_button[3]])  # play button

    pygame.draw.rect(screen, color_black, [quit_button[0], quit_button[1], quit_button[2], quit_button[3]], 5)
    pygame.draw.rect(screen, color_black, [play_button[0], play_button[1], play_button[2], play_button[3]], 5)

    screen.blit(text_title, (screen_width / 2 - 325, screen_height - 700))
    screen.blit(text_author, (screen_width / 2 - 325, screen_height - 650))

    screen.blit(text_quit, (quit_button[0] + 100, quit_button[1] + 10))
    screen.blit(text_play, (play_button[0] + 100, play_button[1] + 10))






def play_screen(factor):

    pygame.draw.circle(screen, color_purple, [difficulty_display[0], difficulty_display[1]], difficulty_display[2])
    pygame.draw.circle(screen, color_black, [difficulty_display[0], difficulty_display[1]], difficulty_display[2], 5)
    pygame.draw.rect(screen, color_white, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]])
    pygame.draw.rect(screen, color_black, [back_to_menu_button[0], back_to_menu_button[1], back_to_menu_button[2], back_to_menu_button[3]], 3)


    n = random.randint(1, int(math.pow(10, factor)))
    maxNumGuesses = int(math.log(n) / math.log(10)) * 3 + 2

    print("n = " , n)
    print("factor = " , factor)
    print("max guesses = " , maxNumGuesses)

    factor_display = displayfont.render(str(factor), True, color_black)

    screen.blit(factor_display, (difficulty_display[0] - 25, difficulty_display[1] - 45))

    screen.blit(title_display_1, (difficulty_display[0] + 150, difficulty_display[1] - 75))
    screen.blit(title_display_2, (difficulty_display[0] + 210, difficulty_display[1] - 0))


    '''
    guesses = 0

    playing = True
    while (playing):

        guess = int(input("Guess a number: "))
        guesses += 1

        if (guess == n):

            print("You won in " + str(guesses) + " guesses!")

            if guesses < maxNumGuesses:
                factor += 1

            play_again = input("Would you like to play again? (y/n)")
            if (play_again == "y"):

                play_screen(factor)
            elif (play_again == "n"):

                playing = False
                sys.exit(0)


        elif (guess > n):

            print("Too high!")
        elif (guess < n):

            print("Too low!")
    '''










def quit_button_function():

    pygame.quit()

def play_button_function():

    global current_screen

    current_screen = "play"

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
            if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom:

                quit_button_function()
            elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom:

                play_button_function()


    screen.fill(color_green)

    mouse = pygame.mouse.get_pos()

    if (current_screen == "title"):

        if quit_button_rect.left <= mouse[0] <= quit_button_rect.right and quit_button_rect.top <= mouse[1] <= quit_button_rect.bottom:

            title_screen("hovering_quit")

        elif play_button_rect.left <= mouse[0] <= play_button_rect.right and play_button_rect.top <= mouse[1] <= play_button_rect.bottom:

            title_screen("hovering_play")

        else:

            title_screen("default")

    elif (current_screen == "play"):




        play_screen(1)






    pygame.display.update()






    pygame.display.update()
