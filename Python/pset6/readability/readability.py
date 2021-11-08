from cs50 import get_string

text = get_string("Text: ")

words = len(text.split())

scentences = 0

letters = 0

for c in text:
    if c.isalpha():
        letters += 1
        
    if c == "?" or c == "!" or c == ".":
        scentences += 1
        
avg_letters = letters / (words / 100)
avg_scentences = scentences / (words / 100)

grade = round(0.0588 * avg_letters - 0.296 * avg_scentences - 15.8)

if grade >= 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {grade}")