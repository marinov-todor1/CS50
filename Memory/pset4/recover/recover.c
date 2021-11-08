#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage ./recover image\n");
        return 1;
    }

    char *inFile = argv[1];
    BYTE buffer[512];
    int file_counter = 0;
    char filename[8];

    FILE *inPtr = fopen(inFile, "r");
    FILE *outPtr = NULL;


    do
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (file_counter == 0)
            {
                sprintf(filename, "%03i.jpg", file_counter);
                outPtr = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, outPtr);
                file_counter++;
            }
            else
            {
                fclose(outPtr);
                sprintf(filename, "%03i.jpg", file_counter);
                outPtr = fopen(filename, "w");
                fwrite(&buffer, sizeof(BYTE), 512, outPtr);
                file_counter++;
            }
        }
        else if (file_counter != 0 && outPtr != NULL)
        {
            fwrite(&buffer, sizeof(BYTE), 512, outPtr);
        }
    }
    while (fread(&buffer, sizeof(BYTE), 512, inPtr) >= 512);
}