import random

def tabuleiro():
    list(range(30))


def jogada():
    paus = rodar_os_paus()
    if paus==2:
        


def rodar_os_paus():

    sticks = [random.randint(0, 1) for i in range(4)]    # 0 corresponde a preto e o 1 corresponde a branco
    total = sum(sticks)

    if total == 0:  # If all sticks show the unmarked side
        total = 5  # Set the total to 1 instead of 0

    return total


class Pecas:
    def __init__(self, cor, posicao=0):         #define as peças do senet
        self.cor = cor
        self.posicao = posicao

    def mover(self, num_casas):
        self.posicao += num_casas


preta1 = Pecas('preto')
preta2 = Pecas('preto')
preta3 = Pecas('preto')
preta4 = Pecas('preto')
preta5 = Pecas('preto')

branca1 = Pecas('branco')
branca2 = Pecas('branco')
branca3 = Pecas('branco')
branca4 = Pecas('branco')
branca5 = Pecas('branco')


def main():
    print("-----Menu-----")
    print('Novo jogo')
    print('carregar jogo')
    print('saida')
