import pygame
from pygame import mixer
from pygame.locals import *  # para VIDEORESIZE
import button
import os

pygame.init()

# criar janela
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
width, height = info.current_w, info.current_h

window = pygame.display.set_mode((width, height - 60), pygame.RESIZABLE)       # display da janela
pygame.display.set_caption("Senet Game by Balente & Skimmer")   # titulo da janela

# game variables
game_pause = False
menu_state = "main"

# cores
white = (255, 255, 255)

# fontes
arial = pygame.font.SysFont("arialblack", 25)

# imagens
background = pygame.image.load("img/background.png").convert_alpha()
resume_img = pygame.image.load("img/button_resume.png").convert_alpha()
quit_img = pygame.image.load("img/button_quit.png").convert_alpha()
tabuleiro_img = pygame.image.load("img/tabuleiro.png").convert_alpha()
white_img = pygame.image.load("img/cone.png").convert_alpha()
black_img = pygame.image.load("img/spool.png").convert_alpha()

# som
mixer.music.load("audio/background.wav")
mixer.music.play(-1)  # loop infinito

# criar butões
resume_button = button.Button(700, 400, resume_img, 1)
quit_button = button.Button(730, 600, quit_img, 1)

# peças do jogo (TABULEIRO --> 3*10 -> 30 linha 1 começa (0, 0) e acaba (0,10) ver notas.txt
white_pieces = ['cone', 'cone', 'cone', 'cone', 'cone']
white_location = [(0, 0), (2, 0), (4, 0), (6, 0), (8, 0)]
black_pieces = ['spool', 'spool', 'spool', 'spool', 'spool']
black_location = [(1, 0), (3, 0), (5, 0), (7, 0), (9, 0)]
piece_list = ['cone', 'spool']

# quem joga variavel:
# 0 - branca sem select / 1 - branca com select
# 2 - preta sem select / 3 - preta com select
turn_step = 2
selection = 100  # variavel para usar comoo flag de peça selecionada
valid_moves = []  # check ações válidas

# definitions
# funcao mostrar_texto
def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

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
def check_options():
    pass


# loop do jogo
running = True
while running:
    window.blit(background, (0, 0))

    # verificar se o jogo está pausado
    if game_pause:
        # caso queira outra coisa em vez de img: window.fill((250, 200, 100))
        # verificar menu
        if menu_state == "main":
            if resume_button.draw(window):
                game_pause = False
            # TODO: botão de guardar (que vai guardar estado atual do jogo num ficheiro)
            # nao esquecer o -- menu_state == "save" para depois fazer menu save com if
            if quit_button.draw(window):
                running = False

    else:
        display_text("Press esc to menu", arial, white, 0, 0)
        # ok esta parte é preciso mesmo comentar:
        # basicamente esta parte do codigo permite alterar o tamanho da janela e manter o tabuleiro centrado
        # os números estranhos são a 'razão' para ficarem sempre centrados em relacao à janela
        x_tabuleiro = 1.2990  # escala x relacao tabuleiro janela
        y_tabuleiro = 1.5104  # escala y relacao tabuleiro janela
        window.blit(tabuleiro_img, (width - width / x_tabuleiro, height - height / y_tabuleiro))
        # window.blit(white_img, (485, 380))
        draw_pieces()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not game_pause:  # se o jogo nao está pausado
                    game_pause = True  # se clicar esc pausa
                else:           # se estiver pausado
                    game_pause = False  # esc volta ao jogo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = (event.pos[0] // 98)
            y_coord = (event.pos[1] // 98)
            click_coords = (x_coord, y_coord)
            print(click_coords)
            # if white turn:
            if turn_step <= 1:
                if click_coords in white_location:
                    selection = white_location.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_location[selection] = click_coords
                    if click_coords in black_location:
                        black_piece = black_location.index(click_coords)
                        # TODO: trocar uma peça com a outra é aqui
                    black_options = check_options(black_pieces, black_location, 'black')
                    white_options = check_options(white_pieces, white_location, 'black')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                # if black turn
                if turn_step > 1:
                    if click_coords in black_location:
                        selection = black_location.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_location[selection] = click_coords
                        if click_coords in white_location:
                            white_piece = white_location.index(click_coords)
                            # TODO: trocar uma peça com a outra é aqui
                        black_options = check_options(black_pieces, black_location, 'black')
                        white_options = check_options(white_pieces, black_location, 'white')
                        turn_step = 2
                        selection = 100
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