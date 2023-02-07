import random

g = [1, 2, 3, 4, 5, 6, 7, 8, 9]

l1 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
l2 = [100, 200, 300, 400, 500, 600, 700, 800, 900]

l3 = []

for a, b in zip(l1, l2):
    r = random.random()
    
    if r < 0.45:
        l3.append(a)
    elif r < 0.90:
        l3.append(b)
    else:
        l3.append(random.choice(g))

for s in list(((("\033[32m" if i < 10 else "\033[33m" if i < 100 else "\033[34m") + str(i)) for i in l3)):
    print(s)
print("\033[0m")
