import random
import display
import pygame


white_pieces = ['cone0', 'cone2', 'cone4', 'cone6', 'cone8']
white_location = [(0, 0), (9, 2), (0, 4), (0, 6), (0, 8)]
black_pieces = ['spool1', 'spool3', 'spool5', 'spool7', 'spool9']
black_location = [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9)]


class Pecas:
    def __init__(self, cor, posicao=0):         # define as peças do senet
        self.cor = cor
        self.posicao = posicao


def move_piece(piece_name, num_moves):                  # verçao melhorada da funçao mover_peao
    if piece_name in white_pieces:                      #esta altera a coluna em que esta e a linha
        index = white_pieces.index(piece_name)
        current_location = white_location[index]
        current_row, current_col = current_location
        new_col = current_col + num_moves
        if new_col > 10:
            new_row = current_row + (new_col // 10)
            new_col = new_col % 10
        else:
            new_row = current_row
        white_location[index] = (new_row, new_col)
    elif piece_name in black_pieces:
        index = black_pieces.index(piece_name)
        current_location = black_location[index]
        current_row, current_col = current_location
        new_col = current_col + num_moves
        if new_col > 10:
            new_row = current_row + (new_col // 10)
            new_col = new_col % 10
        else:
            new_row = current_row
        black_location[index] = (new_row, new_col)
    else:
        print("Invalid piece name.")


#def mover_peao(nomepeao,novalocalizacao):           #esta funçao pega nos peoes como os meteste no display
 #   if nomepeao in white_pieces:                    #e troca a localizaçao por exemplo mover_peao('cone2', (0, 3))
  #      index = white_pieces.index(nomepeao)
   #     white_location[index] = novalocalizacao
    #elif nomepeao in black_pieces:
     #   index = black_pieces.index(nome_peao)
     #   black_location[index] = novalocalizacao
   # else:
   #     print("Invalid piece name.")


def jogada():
    paus = rodar_os_paus()
    if paus==1:
        peao= escolher_peao()
        mover_peao(peao,localizacao)
        jogada()
    elif paus==2:
        peao = escolher_peao()
        mover_peao(peao,localizacao)
    elif paus==3:
        peao = escolher_peao()
        mover_peao(peao,localizacao)
    elif paus==4:
        peao = escolher_peao()
        mover_peao(peao,localizacao)
        jogada()
    elif paus==5:
        peao = escolher_peao()
        mover_peao(peao,localizacao)
        jogada()

def rodar_os_paus():
    sticks = [random.randint(0, 1) for i in range(4)]    # 0 corresponde a preto e o 1 corresponde a branco
    total = sum(sticks)

    if total == 0:  # If all sticks show the unmarked side
        total = 5  # Set the total to 1 instead of 0
    else:
         return 0
    return total


def main():
    print("-----Menu-----")
    print('Novo jogo')
    print('carregar jogo')
    print('saida')
