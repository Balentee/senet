import pygame
from pygame import mixer
from pygame.locals import *  # para VIDEORESIZE
import button
import os
import random

pygame.init()

# criar janela
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
width, height = info.current_w, info.current_h

window = pygame.display.set_mode((width, height - 60), pygame.RESIZABLE)       # display da janela
pygame.display.set_caption("Senet Game by Balente & Skimmer")   # titulo da janela

# game variables
game_start = False
game_pause = False
menu_state = "main"
sticks = 0

# cores
white = (255, 255, 255)

# fontes
arial = pygame.font.SysFont("arialblack", 25)

# imagens
background = pygame.image.load("img/background.png").convert_alpha()
start_img = pygame.image.load("img/button_start.png")
resume_img = pygame.image.load("img/button_resume.png").convert_alpha()
quit_img = pygame.image.load("img/button_quit.png").convert_alpha()
tabuleiro_img = pygame.image.load("img/tabuleiro.png").convert_alpha()
white_img = pygame.image.load("img/cone.png").convert_alpha()
black_img = pygame.image.load("img/spool.png").convert_alpha()
um = pygame.image.load("img/1.png").convert_alpha()
dois = pygame.image.load("img/2.png").convert_alpha()
tres = pygame.image.load("img/3.png").convert_alpha()
quatro = pygame.image.load("img/4.png").convert_alpha()
cinco = pygame.image.load("img/5.png").convert_alpha()

# som
mixer.music.load("audio/background.wav")
mixer.music.play(-1)  # loop infinito

# criar butões
start_button = button.Button(850, 400, start_img, 1)
resume_button = button.Button(800, 400, resume_img, 1)
quit_button = button.Button(830, 600, quit_img, 1)
throw_button = button.Button(0, 200, quit_img, 1)

# peças do jogo (TABULEIRO --> 3*10 -> 30 linha 1 começa (0, 0) e acaba (0,10) ver notas.txt
white_pieces = ['cone', 'cone', 'cone', 'cone', 'cone']
white_location = [(0, 0), (2, 0), (4, 0), (6, 0), (8, 0)]
black_pieces = ['spool', 'spool', 'spool', 'spool', 'spool']
black_location = [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)]
piece_list = ['cone', 'spool']

# quem joga variavel:
# 0 - branca sem select / 1 - branca com select
# 2 - preta sem select / 3 - preta com select
turn_step = 0
selection = 100  # variavel para usar comoo flag de peça selecionada
valid_moves = []  # check ações válidas

# definitions
# funcao mostrar_texto
def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

# funcao rand dos paus
def throw_sticks():
    num_move = random.randint(1, 5)
    print(num_move)
    return num_move

# funcao peças
def draw_pieces():
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'cone':
            window.blit(white_img, (white_location[i][0] * 98 + 485, white_location[i][1] * 98 + 380))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(window, 'red', [white_location[i][0] * 98 + 468, white_location[i][1] * 100 + 377,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        if black_pieces[i] == 'spool':
            window.blit(black_img, (black_location[i][0] * 98 + 485, black_location[i][1] * 98 + 380))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(window, 'blue', [black_location[i][0] * 98 + 468, black_location[i][1] * 100 + 377,
                                                  100, 100], 2)

# funcao jogadas possiveis TODO: Fazer esta função
def check_options(n, pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    print("your number: " + str(n))
    if n != 0:
        print("running options")
        for i in range(len(pieces)):
            location = locations[i]
            if turn == 'cone':
                moves_list = check_moves(n, location, turn)
            if turn == 'spool':
                moves_list = check_moves(n, location, turn)
            all_moves_list.append(moves_list)  # um 'tab' a faltar aqui custou uma direta a rever código
        print(all_moves_list)
    return all_moves_list

# ver moves do cone
def check_moves(n, position, turn):
    moves_list = []
    print('My [' + str(position[0]) + ',' + str(position[1]) + ']')
    # number of moves = n
    if turn == 'cone':
        # se linha 1 ou 3
        if position[1] == 0 or position[1] == 2:
            if (position[0] + n, position[1]) not in white_location:
                print(" this shit " + str(position[0]) + "-" + str(position[1]))
                # se for passar da linha 1 para linha 2 do tabuleiro
                if (position[0] + n) > 9:
                    linechange = (position[0] + n - 9) - 1  # menos 1 devido a se andar +1 em y e nao em x
                    print("this is" + str(linechange))
                    moves_list.append((9 - linechange, position[1] + 1))
                    print(" wtf + " + str(moves_list))
                # sem trocas de linha:
                if 0 <= position[0] + n <= 9:
                    moves_list.append((position[0] + n, position[1]))
                    print(" wtf + " + str(moves_list))
        # se linha 2
        if position[1] == 1:
            if (position[0] + n, position[1]) not in white_location:
                # se for passar da linha 2 para a linha 3 do tabuleiro
                if position[0] - n < 0:
                    linechange = (- n) - 1  # menos 1 devido ao quadrado que se anda em coluna dado ao y
                    moves_list.append((position[0] - linechange, position[1] + 1))
                # se ficar na mesma linha: (linha 2 anda para a esquerda)
                else:
                    moves_list.append((position[0] - n, position[1]))

    else:
        # se linha 1 ou 3
        if position[1] == 0 or position[1] == 2:
            if (position[0] + n, position[1]) not in black_location:
                # se for passar da linha 1 para linha 2 do tabuleiro
                if position[0] + n > 9:
                    linechange = (position[0] + n - 9) - 1  # menos 1 devido a se andar +1 em y e nao em x
                    moves_list.append((9 - linechange, position[1] + 1))
                # sem trocas de linha:
                if 0 <= position[0] + n <= 9:
                    moves_list.append((position[0] + n, position[1]))

        # se linha 2
        if position[1] == 1:
            if (position[0] + n, position[1]) not in black_location:
                # se for passar da linha 2 para a linha 3 do tabuleiro
                if position[0] - n < 0:
                    linechange = (- n) - 1  # menos 1 devido ao quadrado que se anda em coluna dado ao y
                    moves_list.append((position[0] - linechange, position[1] + 1))
                # se ficar na mesma linha: (linha 2 anda para a esquerda)
                moves_list.append((position[0] - n, position[1]))

    return moves_list

# calcula movimentos válidos
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

# apresenta movimentos válidos no ecrã
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(window, color, (moves[i][0] * 98 + 512, moves[i][1] * 98 + 421), 5)


# options
if sticks == 0:
    sticks = 3
black_options = check_options(sticks, black_pieces, black_location, 'spool')
white_options = check_options(sticks, white_pieces, white_location, 'cone')

# loop do jogo
running = True
while running:
    window.blit(background, (0, 0))

    if menu_state == "main":
        if start_button.draw(window):
            game_start = True

    if game_start:
        # verificar se o jogo está pausado
        if game_pause:
            menu_state = "pausa"
            # verificar menu
            if menu_state == "pausa":
                if resume_button.draw(window):
                    game_pause = False
                # TODO: botão de guardar (que vai guardar estado atual do jogo num ficheiro)
                # nao esquecer o -- menu_state == "save" para depois fazer menu save com if
                if quit_button.draw(window):
                    running = False

        else:
            display_text("Press esc to menu", arial, white, 0, 0)
            if throw_button.draw(window) and sticks == 0:
                sticks = throw_sticks()
            if sticks == 1:
                window.blit(um, (0, 50))
            if sticks == 2:
                window.blit(dois, (0, 50))
            if sticks == 3:
                window.blit(tres, (0, 50))
            if sticks == 4:
                window.blit(quatro, (0, 50))
            if sticks == 5:
                window.blit(cinco, (0, 50))

            # ok esta parte é preciso mesmo comentar:
            # basicamente esta parte do codigo permite alterar o tamanho da janela e manter o tabuleiro centrado
            # os números estranhos são a 'razão' para ficarem sempre centrados em relacao à janela
            x_tabuleiro = 1.2990  # escala x relacao tabuleiro janela
            y_tabuleiro = 1.5104  # escala y relacao tabuleiro janela
            window.blit(tabuleiro_img, (width - width / x_tabuleiro, height - height / y_tabuleiro))
            # window.blit(white_img, (485, 380))
            draw_pieces()
            if selection != 100:
                valid_moves = check_valid_moves()
                draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not game_pause:  # se o jogo nao está pausado
                    game_pause = True  # se clicar esc pausa
                else:           # se estiver pausado
                    game_pause = False  # esc volta ao jogo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and sticks != 0:
            x_coord = (event.pos[0] // 98) - 5
            y_coord = (event.pos[1] // 98) - 4
            click_coords = (x_coord, y_coord)
            print("where:" + str(click_coords))
            # if white turn:
            if turn_step <= 1:
                if click_coords in white_location:
                    selection = white_location.index(click_coords)
                    print("here" + str(selection))
                    swap_w_white = click_coords
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_location[selection] = click_coords
                    if click_coords in black_location:
                        black_piece = black_location.index(click_coords)
                        black_location[black_piece] = swap_w_white
                    black_options = check_options(sticks, black_pieces, black_location, 'spool')
                    white_options = check_options(sticks, white_pieces, white_location, 'cone')
                    turn_step = 2
                    selection = 100
                    sticks = 0
                    valid_moves = []
                # if black turn
                if turn_step > 1:
                    if click_coords in black_location:
                        selection = black_location.index(click_coords)
                        swap_w_black = click_coords
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_location[selection] = click_coords
                        if click_coords in white_location:
                            white_piece = white_location.index(click_coords)
                            black_location[white_piece] = swap_w_black
                        black_options = check_options(sticks, black_pieces, black_location, 'spool')
                        white_options = check_options(sticks, white_pieces, white_location, 'cone')
                        turn_step = 0
                        selection = 100
                        sticks = 0
                        valid_moves = []
        if selection != 100:
            print('[' + str(white_options) + ']' + ' [' + str(black_options) + ']')

        if event.type == VIDEORESIZE:
            width, height = event.w, event.h

        if event.type == pygame.QUIT:  # dar funcionalidade ao x da janela para sair
            running = False

    # Game logic and updates go here
        # Rendering the screen
    # window.fill((250, 200, 100))  # Fill the window with color
        # Draw your game objects here using pygame.draw and other functions
    pygame.display.update()  # Update the window display

pygame.quit()

# TODO: https://youtube.com/shorts/WWIo6jvC5xA?feature=share ~ detalhe nice