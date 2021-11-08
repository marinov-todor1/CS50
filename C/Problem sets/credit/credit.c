#include <math.h>
#include <stdio.h>
#include <cs50.h>

int count_lenght(void);
int add_multiply_digits(void);
int add_digits(void);

int main(void)
{
    //Prompt the user for a credit card number
    long card_number = get_long("Number: ");

    //Take every other digit, starting from one to the last * 2 and put their product numbers together
    long card_number_temp1 = card_number / 10;

    long temp1 = 0;
    long total = 0;
    while (card_number_temp1)
    {
        temp1 += card_number_temp1 % 10 * 2;
        do
        {
            total += temp1 % 10;
            temp1 /= 10;
        }
        while (temp1 != 0);
        temp1 = 0;
        card_number_temp1 /= 100;
    }

    //Take every second digit and add
    long card_number_temp2 = card_number;
    long temp2 = card_number_temp2 % 10;
    while (card_number_temp2)
    {
        card_number_temp2 /= 100;
        temp2 += card_number_temp2 % 10;
    }

    //check check_sum
    bool check_sum = false;
    if ((total + temp2) % 10 == 0)
    {
        check_sum = true;
    }

    //Count input length
    card_number_temp1 = card_number;
    int length_counter = 0;
    while (card_number_temp1)
    {
        card_number_temp1 /= 10;
        length_counter++;
    }

    //Check if AMEX
    bool amex = false;
    long first_digits = 0;
    if (length_counter == 15 && check_sum == true)
    {
        first_digits = card_number / 10000000000000;
        if (first_digits == 34 || first_digits == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (length_counter == 16 && check_sum == true)
    {
        first_digits = card_number / 100000000000000;
        long first_digit = card_number / 1000000000000000;
        if (first_digits == 51 || first_digits == 52 || first_digits == 53 || first_digits == 54 || first_digits == 55)
        {
            printf("MASTERCARD\n");
        }
        else if (first_digit == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (length_counter == 13 && check_sum == true)
    {
        first_digits = card_number / 1000000000000;
        if (first_digits == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    //printf("%ld\n", temp1);
    //printf("%ld\n", temp2);
    //printf("%i\n", check_sum);
    //printf("%i\n", length_counter);
    //printf("%i\n", card_number_temp1);
    //printf("%lo\n", card_number);
}