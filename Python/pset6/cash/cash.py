from cs50 import get_float

while True:
    change = get_float("Change: ")

    if change > 0:
        break

change = int(change * 100)

coins_used = 0

while change != 0:
    if change - 25 >= 0:
        change -= 25
        coins_used += 1

    elif change - 10 >= 0:
        change -= 10
        coins_used += 1

    elif change - 5 >= 0:
        change -= 5
        coins_used += 1

    elif change - 1 >= 0:
        change -= 1
        coins_used += 1

print(f"{coins_used}")