#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //check if the user inserted two arguments
    if (argc != 2)
    {
        printf("Usage: ./Substitution KEY\n");
        return 1;
    }
    
    //Get input total lenght, alphabetic characters and duplications
    int count_char = 0;
    int count_alpha = 0;
    int count_duplications = 0;
    
    //Get total length
    for (int i = 0, length = strlen(argv[1]); i < length; i++)
    {
        count_char++;
        //Get alphabetic chars
        if (isalpha(argv[1][i]))
        {
            count_alpha++;
        }
        //Check for duplications
        for (int j = i + 1, length2 = strlen(argv[1]); j < length2; j++)
        {
            if (argv[1][j] == argv[1][i] || argv[1][j] == argv[1][i] - 32 || argv[1][j] == argv[1][i] + 32)
            {
                count_duplications++;
            }
        }
    }
    
    //Validate the key
    if (count_char != 26)
    {
        printf("KEY must contain 26 characters.\n");
        return 1;
    }
    else if (count_alpha != 26)
    {
        printf("KEY must only contain alphabetic characters.\n");
        return 1;
    }
    else if (count_duplications > 0)
    {
        printf("KEY must not contain repeated characters\n");
        return 1;
    }
        
    string plaintext = get_string("plaintext: ");
    string ciphertext = plaintext;
    
    //convert plaintext to ciphertext
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {   
        //convert only alphabetic characters
        if (isalpha(plaintext[i]))
        {
            int p = 0;
            //preserve case
            if (isupper(plaintext[i]))
            {
                p = ciphertext[i] - 65;
                ciphertext[i] = argv[1][p];
                ciphertext[i] = toupper(ciphertext[i]);
            }
            else if (islower(plaintext[i]))
            {
                p = ciphertext[i] - 97;   
                ciphertext[i] = argv[1][p];
                ciphertext[i] = tolower(ciphertext[i]);
            }
        }
    }
    printf("ciphertext: %s\n", ciphertext);
}