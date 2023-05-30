n = 4

a = [(0, 0), (0, 0), (4, 0), (6, 0), (8, 0)]

b = [(1, 0), (3, 0), (2, 0), (7, 0), (9, 0)]

location = a + b


# como digo que a seguir a 9,0 é 9,1/8,1....?
#
def olha_fo():
    for i in a:
        # se linha 1
        if i[1] == 0:
            # se mesma linha
            if (i[0] + 1, i[1]) in a:
                return True
            # se seguidos em coluna
            if i[0] + 1 > 9:
                if (i[0], i[1] + 1) in a:
                    return True
        if i[1] == 1:
            # se mesma linha
            if (i[0] - 1, i[1]) in a:
                return True
            # se seguidos em coluna
            if i[0] - 1 < 0:
                if (i[0], i[1] + 1) in a:
                    return True
        if i[1] == 2:
            if i[0] <= 5:
                # se mesma linha
                if (i[0] + 1, i[1]) in a:
                    return True
                # se seguidos em coluna
                if i[0] - 1 < 0:
                    if (i[0], i[1] + 1) in a:
                        return True


def three_in_a_row():
    hmt = 0
    hmt += 1
    print(hmt)
    for i in a:
        hmt += 1
        # se linha 1
        if i[1] == 0:
            if 0 <= i[0] <= 9:
                # se mesma linha
                print(i[0] + 1, i[1])
                print(i[0] + 2, i[1])
                if ((i[0] + 1, i[1]) in a and (i[0] + 2, i[1])) in a:
                    return True
            # se nos cantos
            if (8, 0) in a:
                if (9, 0) and (9, 1) in a:
                    return True
            if (9, 0) in a:
                if (9, 1) and (8, 1) in a:
                    return True
    else:
        return False

i = 1
if i == 1:
    pass
else:
    print("merda")
