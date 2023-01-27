import random

l1 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
l2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

len_a = len(l1)
len_b = len(l2)

amount1 = random.randint(0, len_a)
split_1_at = random.randint(0, amount1)
split_2_b = random.randint(0, len_b)
cross_len = len_a - amount1

crossed = l1[:split_1_at]
crossed += l2[max(0, min(split_2_b, len_b - cross_len))
                  :min(len_b, split_2_b + cross_len)]
crossed += l1[split_1_at + cross_len:]

for s in list(((("\033[32m" if i < 10 else "\033[33m") + str(i)) for i in crossed)):
    print(s)
print("\033[0m")
print(amount1, split_1_at, split_2_b, cross_len, len(crossed))
