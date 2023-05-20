import pygame
import button

pygame.init()

# criar janela
width = 1500
height = 1000

window = pygame.display.set_mode((width, height))       # display da janela
pygame.display.set_caption("Senet Game by Balente & Skimmer")   # titulo da janela

# game variables
game_pause = False
menu_state = "main"

# cores
white = (255, 255, 255)

# fontes
arial = pygame.font.SysFont("arialblack", 40)

# imagens
resume_img = pygame.image.load("img/button_resume.png").convert_alpha()
quit_img = pygame.image.load("img/button_quit.png").convert_alpha()
tabuleiro_img = pygame.image.load("img/tabuleiro.png").convert_alpha()

# criar butões
resume_button = button.Button(700, 400, resume_img, 1)
quit_button = button.Button(730, 600, quit_img, 1)

# peças do jogo (TABULEIRO --> 3*10 -> 30 linha 1 começa (0, 0) e acaba (0,10) ver notas.txt
white_location = [(0, 0)]
black_location =[(0,1)]
# funcao mostrar_texto
def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


# loop do jogo
running = True
while running:

    window.fill((250, 200, 100))

    # verificar se o jogo está pausado
    if game_pause:
        # verificar menu
        if menu_state == "main":
            if resume_button.draw(window):
                game_pause = False
            # TODO: botão de guardar (que vai guardar estado atual do jogo num ficheiro)
            # nao esquecer o -- menu_state == "save" para depois fazer menu save com if
            if quit_button.draw(window):
                running = False
    else:
        display_text("Press esc to menu...", arial, white, 0, 0)
        window.blit(tabuleiro_img, (250, 250))  # está horrível, mas estética fica para depois

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_pause = True
        if event.type == pygame.QUIT:  # dar funcionalidade ao x da janela para sair
            running = False

    # Game logic and updates go here
        # Rendering the screen
    # window.fill((250, 200, 100))  # Fill the window with color
        # Draw your game objects here using pygame.draw and other functions
    pygame.display.update()  # Update the window display


pygame.quit()

# TODO: https://youtube.com/shorts/WWIo6jvC5xA?feature=share ~ detalhe nice