import random

def shuffle(list):
    output = list.copy()
    for i in range(len(list) - 1, 0, -1):
        r = random.randrange(0, i)
        a = output[i]
        b = output[r]
        output[i] = b
        output[r] = a
    return output