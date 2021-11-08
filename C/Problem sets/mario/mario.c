#include <cs50.h>
#include <stdio.h>

int get_valid_input(void);

int main(void)
{
    
    int input = get_valid_input();
    int left_spaces = input - 1;
    int hashes = 1;
    //for gap i < 2 is fixed
    
    //print pyramid
    for (int height = 0; height < input; height++)
    {
        //print left spaces on current row
        for (int row = 0; row < left_spaces; row++)
        {
            printf(" ");
        }
        
        //print left hashes on current row
        for (int row = 0; row < hashes; row++)
        {
            printf("#");
        }
        
        printf("  ");
        
        //print right hashes on current row
        for (int row = 0; row < hashes; row++)
        {
            printf("#");
        }
        
        printf("\n");
    
        //calc new values
        left_spaces--;
        hashes++;
        
    }
}

//Get valid input from the user
int i;
int get_valid_input()
{
    do
    {
        i = get_int("Height: ");
    }
    while (i < 1 || i > 8);
    return i;
}