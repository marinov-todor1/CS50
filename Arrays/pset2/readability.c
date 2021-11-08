#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

//Calculate how many words are in the text
int calc_words(string text);

//Calculate how many sentences are in the text
int calc_sentences(string text);

//Calculate how many english letters are in the text
int calc_letters(string text);

int main(void)
{
    string input = get_string("Text: ");
    int total_letters = calc_letters(input);
    int total_words = calc_words(input);
    int total_sentences = calc_sentences(input);
    
    float avg_letters = total_letters / (total_words / 100.0);
    float avg_sentences = total_sentences / (total_words / 100.0);
    
    //Compute grade level according to Coleman-Liau formula
    int grade = round(0.0588 * avg_letters - 0.296 * avg_sentences - 15.8);
    
    //Print text grade level
    if (grade < 1)
    {
        printf("Before Grade 1\n");    
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

//Compute the total number of sentences
int calc_sentences(string text)
{
    int sentences = 0;
    
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences += 1;
        }
    }
    return sentences;
}

//Compute the total number of words
int calc_words(string text)
{
    int words = 1;
    
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
    }
    return words;
}

//Compute the total number of letters
int calc_letters(string text)
{
    int letters = 0;
    
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
    }
    return letters;
}