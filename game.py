# bibliotecas e defines
import random

# MENU


# OPCAO A
# pedir nome
player1 = input("What's your name? ")
print("Hey " + player1 + " let's play senet!\n")

# rand para saber quem começa
who_starts = random.randint(0, 1)
if who_starts == 0:
    p1_starts = True
    print(player1 + " starts!")
else:
    p1_starts = False
    print("BOT starts!")

# DISPLAY
display = "display here"
# brancas começam sempre
if p1_starts:
    # chamar aqui a funcao do jogo em si que recebe um 1 ou algo do genero se p1 for verdadeiro para saber quem é
    # as brancas e as pretas
    pass
else:
    pass
