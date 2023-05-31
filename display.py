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

# menu variables and states
game_start = False
game_pause = False
game_bot = False
menu_state = "main"

# game variables
sticks = 0
swap_w_white = 0
swap_w_black = 0
white_pontuation = 0
black_pontuation = 0
inputt = ' '
wrt = 1

# cores
white = (255, 255, 255)

# fontes
arial = pygame.font.SysFont("arialblack", 25)

# imagens
background = pygame.image.load("img/background.png").convert_alpha()
title = pygame.image.load("img/title.png").convert_alpha()
bybalente = pygame.image.load("img/by Balente.png").convert_alpha()
start_img = pygame.image.load("img/button_start.png").convert_alpha()
load_img = pygame.image.load("img/button_load.png").convert_alpha()
rules_img = pygame.image.load("img/button_rules.png").convert_alpha()
resume_img = pygame.image.load("img/button_resume.png").convert_alpha()
quit_img = pygame.image.load("img/button_quit.png").convert_alpha()
tabuleiro_img = pygame.image.load("img/tabuleiro.png").convert_alpha()
roll_img = pygame.image.load("img/button_roll.png").convert_alpha()
white_img = pygame.image.load("img/cone.png").convert_alpha()
black_img = pygame.image.load("img/spool.png").convert_alpha()
sticks_img = pygame.image.load("img/sticks.png").convert_alpha()
um = pygame.image.load("img/1.png").convert_alpha()
dois = pygame.image.load("img/2.png").convert_alpha()
tres = pygame.image.load("img/3.png").convert_alpha()
quatro = pygame.image.load("img/4.png").convert_alpha()
cinco = pygame.image.load("img/5.png").convert_alpha()
pvp_img = pygame.image.load("img/button_pvp_game.png").convert_alpha()
bot_img = pygame.image.load("img/button_bot_game.png").convert_alpha()
back_img = pygame.image.load("img/button_back.png").convert_alpha()
input_img = pygame.image.load("img/input.png").convert_alpha()
player1_img = pygame.image.load("img/Player_1.png").convert_alpha()
player2_img = pygame.image.load("img/Player_2.png").convert_alpha()
ok_img = pygame.image.load("img/OK.png").convert_alpha()
save_img = pygame.image.load("img/button_save.png").convert_alpha()
quit_to_menu_img = pygame.image.load("img/button_quit_to_menu.png").convert_alpha()
parchment_img = pygame.image.load("img/parchment.png").convert_alpha()

# som
mixer.music.load("audio/background.wav")
mixer.music.play(-1)  # loop infinito

# criar butões
start_button = button.Button(171, 888, start_img, 1)
load_button = button.Button(611, 888, load_img, 1)
rules_button = button.Button(1034, 888, rules_img, 1)
quit_start_button = button.Button(1454, 888, quit_img, 1)
pvp_game_button = button.Button(538, 544, pvp_img, 1)
bot_game_button = button.Button(1100, 544, bot_img, 1)
back_start_button = button.Button(820, 725, back_img, 1)
throw_button = button.Button(78, 371, roll_img, 1)
back_name_button = button.Button(600, 725, back_img, 1)
ok_button = button.Button(920, 725, ok_img, 1)
resume_button = button.Button(819, 374, resume_img, 1)
save_button = button.Button(819, 493, save_img, 1)
rules_pause_button = button.Button(819, 612, rules_img, 1)
quit_to_menu_button = button.Button(819, 731, quit_to_menu_img, 1)
quit_pause_button = button.Button(819, 850, quit_img, 1)


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

# funções
# funcao mostrar_texto
def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

# funcao lançar os paus
def throw_sticks():
    num_move = random.randint(1, 5)
    return num_move

# funcao desenhar peças + quadrado de selecao
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

# funcao jogadas possiveis
def check_options(n, pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    if n != 0:
        for i in range(len(pieces)):
            location = locations[i]
            if turn == 'cone':
                moves_list = check_moves(n, location, turn)
            if turn == 'spool':
                moves_list = check_moves(n, location, turn)
            all_moves_list.append(moves_list)  # um 'tab' a faltar aqui custou uma direta a rever código

    # todos os moves que uma peça pode fazer dependendo da turn
    for x in all_moves_list:
        break
        # twos = two_in_a_row(n, x, turn)
        # threes = three_in_a_row(n, x, turn)


    return all_moves_list

# funcao calcula jogadas possiveis
def check_moves(n, position, turn):
    moves_list = []  # IMPRT: além d iniciar se n houver posição pra mover devolv vazio important para os movs funcionar
    # number of moves = n = sticks
    # pairs = two_in_a_row(n, position, turn)
    # threes = three_in_a_row(n, position, turn)
    # threes = False

    # vez das brancas
    if turn == 'cone':
        # se linha 1
        if position[1] == 0:
            if (position[0] + n, position[1]) not in white_location:
                # se for passar da linha 1 para linha 2 do tabuleiro
                if (position[0] + n) > 9:
                    linechange = (position[0] + n - 9) - 1  # menos 1 devido a se andar +1 em y e nao em x
                    if (9 - linechange, position[1] + 1) not in white_location:
                        if (9 - linechange, position[1] + 1) == (5, 1) and (5, 1) in black_location:
                            pass
                        elif (9 - linechange, position[1] + 1) not in white_location:
                            moves_list.append((9 - linechange, position[1] + 1))

                # sem trocas de linha:
                if 0 <= position[0] + n <= 9:
                    moves_list.append((position[0] + n, position[1]))

        # se linha 2
        if position[1] == 1:
            if (position[0] - n, position[1]) not in white_location:
                if (position[0] - n, position[1]) == (5, 1) and (position[0] - n, position[1]) in black_location:
                    pass
                else:
                    # se for passar da linha 2 para a linha 3 do tabuleiro
                    if position[0] - n < 0:
                        linechange = -(position[0] - n) - 1  # menos 1 devido ao quadrado que se anda em coluna dado ao y
                        if (0 + linechange, position[1] + 1) not in white_location:
                            moves_list.append((0 + linechange, position[1] + 1))
                    # se ficar na mesma linha: (linha 2 anda para a esquerda)
                    if 0 <= position[0] - n <= 9:
                        moves_list.append((position[0] - n, position[1]))

        # se linha 3
        if position[1] == 2:
            if (position[0] + n, position[1]) not in white_location:
                if 0 <= position[0] + n <= 4:
                    moves_list.append((position[0] + n, position[1]))
                # SE FOR PARA A CASA DA BELEZA
                if (position[0] + n, position[1]) == (5, 2) and (position[0] + n, position[1]) not in black_location:
                    moves_list.append((position[0] + n, position[1]))
                # A PARTIR DAQUI PODIA SER MAIS RESUMIDO MAIS FICA MAIS EXPLICITO ASSIM
                # SE ESTIVER NA CASA DA BELEZA
                if (position[0], position[1]) == (5, 2):
                    if n == 5:
                        moves_list.append((position[0], position[1]))
                    # SE CASA DAS AGUAS
                    if (position[0] + n, position[1]) == (6, 2):
                        moves_list.append((6, 2))
                    # SE FOR PARA CASA DOS TRES JUIZES
                    if (position[0] + n, position[1]) == (7, 2):
                        if n == 2:
                            moves_list.append((position[0] + n, position[1]))
                    # SE FOR PARA CASA DOS DOIS JUIZES
                    if (position[0] + n, position[1]) == (8, 2):
                        if n == 3:
                            moves_list.append((position[0] + n, position[1]))
                    # SE FOR PARA CASA DE HORUS
                    if (position[0] + n, position[1]) == (9, 2):
                        if n == 4:
                            moves_list.append((position[0] + n, position[1]))

    # TODO PONTOS + NOMES
    # vez das pretas
    if turn == 'spool':
        # se linha 1
        if position[1] == 0:
            if (position[0] + n, position[1]) not in black_location:
                # se for passar da linha 1 para linha 2 do tabuleiro
                if position[0] + n > 9:
                    linechange = (position[0] + n - 9) - 1  # menos 1 devido a se andar +1 em y e nao em x
                    if (9 - linechange, position[1] + 1) == (5, 1) and (5, 1) in white_location:
                        pass
                    elif (9 - linechange, position[1] + 1) not in black_location:
                        moves_list.append((9 - linechange, position[1] + 1))
                # sem trocas de linha:
                if 0 <= position[0] + n <= 9:
                    moves_list.append((position[0] + n, position[1]))

        # se linha 2
        if position[1] == 1:
            if (position[0] - n, position[1]) not in black_location:
                if (position[0] - n, position[1]) == (5, 1) and (position[0] - n, position[1]) in white_location:
                    pass
                else:
                    # se for passar da linha 2 para a linha 3 do tabuleiro
                    if position[0] - n < 0:
                        linechange = -(position[0] - n) - 1  # menos 1 devido ao quadrado que se anda em coluna dado ao y
                        if (0 + linechange, position[1] + 1) not in black_location:
                            moves_list.append((0 + linechange, position[1] + 1))
                    # se ficar na mesma linha: (linha 2 anda para a esquerda)
                    if 0 <= position[0] - n <= 9:
                        moves_list.append((position[0] - n, position[1]))

        # se linha 3
        if position[1] == 2:
            if (position[0] + n, position[1]) not in black_location:
                if 0 <= position[0] + n <= 4:
                    moves_list.append((position[0] + n, position[1]))
                # SE FOR PARA A CASA DA BELEZA
                if (position[0] + n, position[1]) == (5, 2) and (position[0] + n, position[1]) not in white_location:
                    moves_list.append((position[0] + n, position[1]))
                # SE ESTIVER NA CASA DA BELEZA
                if (position[0], position[1]) == (5, 2):
                    if n == 5:
                        moves_list.append((position[0], position[1]))
                    # SE CASA DAS AGUAS
                    if (position[0] + n, position[1]) == (6, 2):
                        moves_list.append((position[0] + n, position[1]))
                    # SE FOR PARA CASA DOS TRES JUIZES
                    if (position[0] + n, position[1]) == (7, 2):
                        if n == 2:
                            moves_list.append((position[0] + n, position[1]))
                    # SE FOR PARA CASA DOS DOIS JUIZES
                    if (position[0] + n, position[1]) == (8, 2):
                        if n == 3:
                            moves_list.append((position[0] + n, position[1]))
                    # SE FOR PARA CASA DE HORUS
                    if (position[0] + n, position[1]) == (9, 2):
                        if n == 4:
                            moves_list.append((position[0] + n, position[1]))

    return moves_list

# funcao movimentos válidos
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

# funcao apresenta movimentos válidos (ponto para onde se mover)
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(window, color, (moves[i][0] * 98 + 512, moves[i][1] * 98 + 421), 5)

# funcoes REGRAS
# funcao two_in_a_row → se duas juntas, nao pode substituir mas pode passar à frente
def two_in_a_row(n, position, turn):
    # a funcao deve ser capaz de retornar false se for possivel saltar o pair, pois este n influencia isso
    there_are = 0
    maxim = n + 1  # n + 1, pois a casa onde calha o n pode ser a primeira peça de um par, entao tem de ler essa + 1
    # for i in maxim porque maxim é o num de casas à frente que pode influenciar a jogada com um par
    for i in range(maxim):
        i += 1
        if turn == 'cone':
            # se linha 1
            if position[1] == 0:
                # se passar de linha e tiver um par:
                if (position[0] + i) > 9:
                    linechange = (position[0] + i - 9) - 1  #TODO rever condicao aqui
                    if (9 - linechange, position[1] + 1) in black_location:
                        there_are += 1
                # se estiver na mesma linha e tiver par
                if 0 <= position[0] + i <= 9:
                    if (position[0] + i, position[1]) in black_location:
                        there_are += 1
                # não há par? entao reinicializar na variavel
                else:
                    there_are = 0
            # se linha 2
            if position[1] == 1:
                if (position[0] - i, position[1]) in black_location:
                    there_are += 1
                else:
                    there_are = 0  # se estiverem separados volta ao 0 e mais importante, se conseguir saltar o par dá false
            # se linha 3
            if position[1] == 2:
                if (position[0] + i, position[1]) in black_location:
                    there_are += 1
                else:
                    there_are = 0

        if turn == 'spool':
            # se linha 1
            if position[1] == 0:
                # se passar de linha e tiver um par:
                if (position[0] + i) > 9:
                    linechange = (position[0] + i - 9) - 1  # TODO rever condicao aqui
                    if (9 - linechange, position[1] + 1) in white_location:
                        there_are += 1
                # se estiver na mesma linha e tiver par
                if 0 <= position[0] + i <= 9:
                    if (position[0] + i, position[1]) in white_location:
                        there_are += 1
                # não há par? entao reinicializar na variavel
                else:
                    there_are = 0
            # se linha 2
            if position[1] == 1:
                if (position[0] - i, position[1]) in white_location:
                    there_are += 1
                else:
                    there_are = 0  # se estiverem separados volta ao 0 e mais importante, se conseguir saltar o par dá false
            # se linha 3
            if position[1] == 2:
                if (position[0] + i, position[1]) in white_location:
                    there_are += 1
                else:
                    there_are = 0


    if there_are >= 2:
        return True
    if there_are < 2:
        return False


# funcao three in a row
def three_in_a_row(n, position, turn):
    # tres seguidos? mal pela raiz, logo false
    there_are = 0
    maxim = n + 2  # n + 2, pois a casa onde calha o n pode ser a primeira peça de tres, entao tem de ler essa + 2 da frent
    # for i in maxim porque maxim é o num de casas à frente que pode influenciar a jogada com um par
    for i in range(maxim):
        i += 1
        if turn == 'cone':
            # se linha 1
            if position[1] == 0:
                # se passar de linha e tiver um par:
                if (position[0] + i) > 9:
                    linechange = (position[0] + i - 9) - 1  # TODO rever condicao aqui
                    if (9 - linechange, position[1] + 1) in black_location:
                        there_are += 1
                # se estiver na mesma linha e tiver par
                if 0 <= position[0] + i <= 9:
                    if (position[0] + i, position[1]) in black_location:
                        there_are += 1
                # não há par? entao reinicializar na variavel
                else:
                    there_are = 0
            # se linha 2
            if position[1] == 1:
                if (position[0] - i, position[1]) in black_location:
                    there_are += 1
                else:
                    there_are = 0  # se estiverem separados volta ao 0
            # se linha 3
            if position[1] == 2:
                if (position[0] + i, position[1]) in black_location:
                    there_are += 1
                else:
                    there_are = 0

        if turn == 'spool':
            # se linha 1
            if position[1] == 0:
                # se passar de linha e tiver um par:
                if (position[0] + i) > 9:
                    linechange = (position[0] + i - 9) - 1  # TODO rever condicao aqui
                    if (9 - linechange, position[1] + 1) in white_location:
                        there_are += 1
                # se estiver na mesma linha e tiver par
                if 0 <= position[0] + i <= 9:
                    if (position[0] + i, position[1]) in white_location:
                        there_are += 1
                # não há par? entao reinicializar na variavel
                else:
                    there_are = 0
            # se linha 2
            if position[1] == 1:
                if (position[0] - i, position[1]) in white_location:
                    there_are += 1
                else:
                    there_are = 0  # se estiverem separados volta ao 0 e mais importante, se conseguir saltar o par dá false
            # se linha 3
            if position[1] == 2:
                if (position[0] + i, position[1]) in white_location:
                    there_are += 1
                else:
                    there_are = 0

        if there_are >= 3:
            return True

    if there_are < 3:
        return False


# loop do jogo
running = True
while running:
    window.blit(background, (0, 0))

    if menu_state == "main":
        window.blit(title, (678, 123))
        window.blit(bybalente, (905, 330))
        if start_button.draw(window):
            menu_state = "start"
        if load_button.draw(window):
            menu_state = "load"
        if rules_button.draw(window):
            menu_state = "rules"
            comes = "main"
        if quit_start_button.draw(window):
            running = False

    if menu_state == "start":
        window.blit(title, (678, 123))
        if pvp_game_button.draw(window):
            menu_state = "name"
        if bot_game_button.draw(window):
            menu_state = "name"
            game_bot = True
        if back_start_button.draw(window):
            menu_state = "main"

    if menu_state == "load":
        pass

    if menu_state == "rules":
        if back_start_button.draw(window):
            if comes == "main":
                menu_state = "main"
            if comes == "pause":
                menu_state = "pause"


    if menu_state == "name":
        window.blit(title, (678, 123))
        window.blit(input_img, (537, 589))
        if not game_bot:
            if wrt == 1:
                window.blit(player1_img, (537, 544))
                player1_name = arial.render(inputt, True, (0, 0, 0))
                window.blit(player1_name, (580, 613))
                if ok_button.draw(window):
                    if 3 <= len(inputt) <= 7:
                        player1_str = inputt
                        inputt = ""
                        wrt = 2
                    else:
                        menu_state = "start"
                        player1_name = ""
                        player2_name = ""
                        inputt = ""
                        wrt = 1

            if wrt == 2:
                window.blit(player2_img, (537, 544))
                player2_name = arial.render(inputt, True, (0, 0, 0))
                window.blit(player2_name, (580, 613))
                if ok_button.draw(window):
                    if 3 <= len(inputt) <= 7:
                        player2_str = inputt
                        game_start = True
                        menu_state = "game"
                        wrt = 1
                    else:
                        menu_state = "start"
                        player1_name = ""
                        player2_name = ""
                        inputt = ""
                        wrt = 1


        else:
            window.blit(player1_img, (537, 544))
            player1_name = arial.render(inputt, True, (0, 0, 0))
            window.blit(player1_name, (580, 613))
            if ok_button.draw(window):
                if 3 <= len(inputt) <= 7:
                    inputt = "BOT"
                    player2_name = arial.render(inputt, True, (0, 0, 0))
                    game_start = True
                    menu_state = "game"
                else:
                    menu_state = "start"
                    player1_name = ""
                    player2_name = ""
                    inputt = ""

        if back_name_button.draw(window):
            menu_state = "start"
            player1_name = ""
            player2_name = ""
            inputt = ""

    if game_start:
        # verificar se o jogo está pausado
        if game_pause:
            menu_state = "pause"
            # verificar menu
            if menu_state == "pause":
                window.blit(title, (678, 123))
                if resume_button.draw(window):
                    game_pause = False
                    menu_state = "game"
                if save_button.draw(window):
                    pass
                    # TODO: botão de guardar (que vai guardar estado atual do jogo num ficheiro)
                    # TODO: PRIMEIRO LIMPA FICHEIRO, DEPOIS SALVA DEPOIS VERIFICA SE ESTA VAZIO
                    # TODO: SE ESTIVER VAZIO DIZ ERRO SENAO DIZ SAVED
                    # nao esquecer o -- menu_state == "save" para depois fazer menu save com if
                if rules_pause_button.draw(window):
                    menu_state = "rules"
                    comes = "pause"
                if quit_to_menu_button.draw(window):
                    game_pause = False
                    game_start = False
                    menu_state = "start"
                if quit_pause_button.draw(window):
                    running = False

        else:
            display_text("Press esc to menu", arial, white, 0, 0)
            if throw_button.draw(window) and sticks == 0:
                sticks = throw_sticks()
                black_options = check_options(sticks, black_pieces, black_location, 'spool')
                white_options = check_options(sticks, white_pieces, white_location, 'cone')
            if True:
                if sticks == 0:
                    window.blit(sticks_img, (78, 371))
                if sticks == 1:
                    window.blit(um, (78, 371))
                if sticks == 2:
                    window.blit(dois, (78, 371))
                if sticks == 3:
                    window.blit(tres, (78, 371))
                if sticks == 4:
                    window.blit(quatro, (78, 371))
                if sticks == 5:
                    window.blit(cinco, (78, 371))

            # ok esta parte é preciso mesmo comentar:
            # basicamente esta parte do codigo permite alterar o tamanho da janela e manter o tabuleiro centrado
            # os números estranhos são a 'razão' para ficarem sempre centrados em relacao à janela
            x_tabuleiro = 1.2990  # escala x relacao tabuleiro janela
            y_tabuleiro = 1.5104  # escala y relacao tabuleiro janela
            window.blit(tabuleiro_img, (width - width / x_tabuleiro, height - height / y_tabuleiro))
            # TODO: IF TURN.... PRINT PLAYER NAME
            # window.blit(white_img, (485, 380))
            if turn_step <= 1:
                window.blit(player1_name, (938, 792))

            if turn_step >= 2:
                window.blit(player2_name, (938, 792))

            draw_pieces()

            if selection != 100:
                valid_moves = check_valid_moves()
                draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not game_pause:  # se o jogo nao está pausado
                    game_pause = True  # se clicar esc pause
                else:           # se estiver pausado
                    game_pause = False  # esc volta ao jogo
            if menu_state == "name":
                if event.key == pygame.K_BACKSPACE:
                    inputt = inputt[:-1]
                else:
                    inputt += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and sticks != 0:
            x_coord = (event.pos[0] // 98) - 5
            y_coord = (event.pos[1] // 98) - 4
            click_coords = (x_coord, y_coord)
            # TODO bot TURN HERE + HOW HE CHOOSES CLICK COORDS

            # if white turn:
            if turn_step <= 1:
                # NOME
                if click_coords in white_location:
                    selection = white_location.index(click_coords)
                    swap_w_white = click_coords
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_location[selection] = click_coords
                    if click_coords in black_location:
                        black_piece = black_location.index(click_coords)
                        black_location[black_piece] = swap_w_white
                    else:
                        # CASAS ESPECIAIS
                        # CASA DA BELEZA
                        if white_location[selection] == (5, 2) and sticks == 5:
                            white_piece = white_location.index(click_coords)
                            white_pontuation += 1
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                        # CASA DA AGUA
                        if white_location[selection] == (6, 2):
                            # casas possiveis para cair se calhar na casa da água
                            # este for encontra a primeira casa vazia depois da casa da vida caso 5,1 nao esteja livre
                            for i in [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (9, 0), (8, 0), (7, 0), (6, 0), (5, 0)]:
                                if i in black_location or i in white_location:
                                    pass
                                else:
                                    white_location[selection] = i
                                    break
                        # CASA DOS 3 JUIZES
                        if white_location[selection] == (7, 2) and sticks == 3:
                            white_piece = white_location.index(click_coords)
                            white_pontuation += 1
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                        # CASA DOS 2 JUIZES
                        if white_location[selection] == (8, 2) and sticks == 2:
                            white_piece = white_location.index(click_coords)
                            white_pontuation += 1
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)
                        # CASA DE HORUS
                        if white_location[selection] == (9, 2) and sticks == 1:
                            white_piece = white_location.index(click_coords)
                            white_pontuation += 1
                            white_pieces.pop(white_piece)
                            white_location.pop(white_piece)

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
                        white_location[white_piece] = swap_w_black
                    else:
                        # CASAS ESPECIAIS
                        # CASA DA BELEZA
                        if black_location[selection] == (5, 2) and sticks == 5:
                            black_piece = black_location.index(click_coords)
                            black_pontuation += 1
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                        # CASA DA AGUA
                        if black_location[selection] == (6, 2):
                            # casas possiveis para cair se calhar na casa da água
                            # este for encontra a primeira casa vazia depois da casa da vida caso 5,1 nao esteja livre
                            for i in [(5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (9, 0), (8, 0), (7, 0), (6, 0),
                                      (5, 0)]:
                                if i in black_location or i in white_location:
                                    pass
                                else:
                                    black_location[selection] = i
                                    break
                        # CASA DOS 3 JUIZES
                        if black_location[selection] == (7, 2) and sticks == 3:
                            black_piece = black_location.index(click_coords)
                            black_pontuation += 1
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                        # CASA DOS 2 JUIZES
                        if black_location[selection] == (8, 2) and sticks == 2:
                            black_piece = black_location.index(click_coords)
                            black_pontuation += 1
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)
                        # CASA DE HORUS
                        if black_location[selection] == (9, 2) and sticks == 1:
                            black_piece = black_location.index(click_coords)
                            black_pontuation += 1
                            black_pieces.pop(black_piece)
                            black_location.pop(black_piece)

                    black_options = check_options(sticks, black_pieces, black_location, 'spool')
                    white_options = check_options(sticks, white_pieces, white_location, 'cone')
                    turn_step = 0
                    selection = 100
                    sticks = 0
                    valid_moves = []

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