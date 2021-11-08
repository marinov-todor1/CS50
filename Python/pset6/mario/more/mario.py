import cs50

while True:
    height = cs50.get_int("Height: ")
    if height > 0 and height < 9:
        break

left_spaces = height - 1
hashes = 1

for i in range(height):

    for b in range(left_spaces):
        print(" ", end="")

    for c in range(hashes):
        print("#", end="")

    print("  ", end="")

    for d in range(hashes):
        print("#", end="")

    print("")

    left_spaces -= 1
    hashes += 1