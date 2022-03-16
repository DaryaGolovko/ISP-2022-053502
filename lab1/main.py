import os
from count import Tasks


with open(r'/Users/golovko/isp/text.txt') as file:
    if os.path.getsize('/Users/golovko/isp/text.txt') == 0:
        raise EOFError("File is empty")
    print("Welcome to the club")
    print("Enter N")
    n: int = int(input())
    print("Enter K")
    k: int = int(input())
    if k == 0 or n == 0:
        print("Error, you're a looser")
    text: str = file.read()
    task: Tasks = Tasks()
    print(f"Number of words in the text: {task.count_iteration(text)}")
    print(f"The number of average words in the sentence: {task.average_word_num(text)}")
    print(f"Median: {task.count_median(text)}")
    print("Top 3 n-grams:")
    task.top_ngrammas(text, k, n)
