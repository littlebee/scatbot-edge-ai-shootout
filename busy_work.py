#!/usr/bin/env python3

# Anything really would do here, just needs to be something that runs continuously
# and consumes 100% of one CPU core (25% overall on 4 core Pi 4)
#
# The benchmarks.sh script kicks off one, then two, then three to produce 4 sets of
# FPS results for 100%, 75%, 50%, and 25%
#
# I wanted to limit the interactions with the file system to the one initial read
# because most of scatbot's subsystems just read and write data from i2c and
# update central state (central_hub) over a socket.
#
import os

file_content = None

print('opening test file')
with open('testdata/tale_of_two_cities.txt', 'r') as f:
    file_content = f.read()  # Read whole file in the file_content string

while True:
    print("\nComputing word frequency for Tale of Two Cities\n")
    word_dict = {}
    current_word = ""
    for char in file_content:
        if char in ["\n", "\r", " ", ".", ";", ",", "?", "(", ")", "!", "\"", "'"]:
            if len(current_word) > 0:
                word = current_word.lower()
                current_count = word_dict.get(word)
                if current_count == None:
                    word_dict[word] = 1
                else:
                    word_dict[word] = current_count + 1
                current_word = ""
        else:
            current_word += char

    print("finished!")
    print(word_dict)
