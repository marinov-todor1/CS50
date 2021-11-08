#include <cs50.h>
#include <stdio.h>

int get_starting_size(void);
int get_ending_size(void);

int main(void)
{
    int start_size = get_starting_size();
    int end_size = get_ending_size();
    int years = 0;
    int current_size = start_size;

    while (current_size < end_size)
    {
        current_size = current_size + (current_size / 3) - (current_size / 4);
        years++;
    }
        
    printf("Years: %i\n", years);
}


//Prompt user for starting size
int S;
int get_starting_size(void)
{
    do
    {
        S = get_int("Start size: ");
    }
    while (S < 9);
    return S;

}
//Prompt user for ending size
int E;
int get_ending_size(void)
{
    do
    {
        E = get_int("End size: ");
    }
    while (E < S);
    return E;

}