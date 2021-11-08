from cs50 import get_int

def main():

    #Prompt the user for a credit card number
    card_number = get_int("Number: ")

    #Take every other digit, starting from one to the last * 2 and put their product numbers together
    card_number_temp1 = int(card_number / 10)
    temp1 = 0
    total = 0

    while (card_number_temp1):
        temp1 += card_number_temp1 % 10 * 2

        while True:
            total += temp1 % 10
            temp1 /= 10

            if temp1 == 0:
                break

    #Take every second digit and add
    card_number_temp2 = card_number;
    temp2 = card_number_temp2 % 10

    while (card_number_temp2):
        int(card_number_temp2 /= 100)
        temp2 += card_number_temp2 % 10

    check_sum = False
    if (total + temp2) % 10 == 0:
        check_sum = True



def count_length():

def add_multiply_digits():

def add_digits():