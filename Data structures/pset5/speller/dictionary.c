// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

#include "dictionary.h"

int size_count;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // iterate and check linked list
    long long index = hash(word);
    node *temp = table[index];

    while (temp != NULL)
    {
        if (strcasecmp(word, temp->word) == 0)
        {
            return true;
        }
        temp = temp->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int len = strlen(word);
    int index = 65599;

    for (int i = 0; i < len; i++)
    {
        index *= toupper(word[i]);
    }

    index = llabs(index % 100000);

    return index;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *inPtr = fopen(dictionary, "r");

    if (inPtr == NULL)
    {
        printf("Couldn't load the file.");
        return 1;
    }

    //buffer where the read words are going to be stored
    char current_word[46];
    size_count = 0;

    while (fscanf(inPtr, "%s", current_word) != EOF)
    {
        //count number of words in the dict
        size_count++;

        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Couldn't allocate memory in load");
            return false;
        }
        //copy the current word into a node
        strcpy(n->word, current_word);
        n->next = NULL;
        
        int len = strlen(current_word);
        for (int i = 0; i < len; i++)
        {
            current_word[i] = toupper(current_word[i]);
        }
        
        //insert the node into a linked list
        long long index = hash(current_word);
        node *tmp = table[index];
        table[index] = n;
        table[index]->next = tmp;
    }
    fclose(inPtr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return size_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    if (true)
    {
        for (int i = 0; i < N - 1; i++)
        {
            node *tmp = table[i];
            node *cursor = table[i];

            while (cursor != NULL)
            {
                cursor = cursor->next;
                free(tmp);
                tmp = cursor;
            }
        }
        return true;
    }
    else
    {
        return false;
    }
}