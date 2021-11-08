#include <cs50.h>
#include <stdio.h>
#include "helpers.h"
#include "math.h"
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //take the pixel and avg. the values of RGB to gray scale
            int avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            if (round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue) > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            }

            if (round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue) > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            }

            if (round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue) > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0, m = 1; j < width / 2; j++, m++)
        {
            //take pixel 0
            //put it into temp
            //copy pixel 400 into pixel 0
            //copy temp into pixel 400

            RGBTRIPLE tempLeft = image[i][j];

            //take the right side and put it on the left
            image[i][j] = image[i][width - m];

            //take the left side and put it on the right
            image[i][width - m] = tempLeft;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //take pixel 0
    //take pixel 0 - 1 row - 1 column
    //take pixel 0 - 1 row
    //take pixel 0 - 1 row + 1 column
    //take pixel 0 - 1 column
    //take pixel 0 + 1 column
    //take pixel 0 + 1 row - 1 column
    //take pixel 0 + 1 row
    //take pixel 0 + 1 row + 1 column
    //if pixel is beyond hight or width {return -1}
    //calculate the avg. of each color and update a temp image
    RGBTRIPLE imageTemp[height][width];

    //crawl over each pixel
    for (int picture_row = 0; picture_row < height; picture_row++)
    {
        for (int picture_column = 0; picture_column < width; picture_column++)
        {
            int GridEndRow = -2;
            int GridEndCol = -2;
            int imageTempBlue = 0;
            int imageTempRed = 0;
            int imageTempGreen = 0;
            float pixel_count = 0;

            //crawl over the 9grid of each pixel
            for (int GridStartRow = 1; GridStartRow > GridEndRow; GridStartRow--)
            {
                if (picture_row == 0)
                {
                    GridEndRow = -1;
                }

                if (picture_row == height - 1 && GridStartRow != -1)
                {
                    GridStartRow = 0;
                }

                for (int GridStartCol = 1; GridStartCol > GridEndCol; GridStartCol--)
                {
                    if (picture_column == 0)
                    {
                        GridEndCol = -1;
                    }

                    if (picture_column == width - 1 && GridStartCol != -1)
                    {
                        GridStartCol = 0;
                    }

                    imageTempBlue += image[picture_row + GridStartRow][picture_column + GridStartCol].rgbtBlue;
                    imageTempRed += image[picture_row + GridStartRow][picture_column + GridStartCol].rgbtRed;
                    imageTempGreen += image[picture_row + GridStartRow][picture_column + GridStartCol].rgbtGreen;

                    pixel_count++;

                }
            }

            float avgBlue = imageTempBlue / pixel_count;
            float avgRed = imageTempRed / pixel_count;
            float avgGreen = imageTempGreen / pixel_count;


            //change the pixel in the temp image
            imageTemp[picture_row][picture_column].rgbtBlue = round(avgBlue);
            imageTemp[picture_row][picture_column].rgbtRed = round(avgRed);
            imageTemp[picture_row][picture_column].rgbtGreen = round(avgGreen);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = imageTemp[i][j];
        }
    }
    return;
}
