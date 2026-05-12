pessoas_total = int(input())

pessoas = [] * pessoas_total

for i in range(pessoas_total):
    pessoas.append(int(input()))

total_time = 0
last_time = 0

for pessoa in pessoas:
    if pessoa - last_time > 10:
        total_time += 10
    else:
        total_time += pessoas - last_time

    last_time = pessoa

print(total_time)