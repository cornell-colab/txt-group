## SNIPPET 1
## Use the code below to identify the sentiment of an entire message

# first, we import the relevant modules from the NLTK library
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# next, we initialize VADER so we can use it within our Python script
sid = SentimentIntensityAnalyzer()

# the variable 'message_text' now contains the text we will analyze.
message_text = '''Like you, I am getting very frustrated with this process. I am genuinely trying to be as reasonable as possible. I am not trying to "hold up" the deal at the last minute. I'm afraid that I am being asked to take a fairly large leap of faith after this company (I don't mean the two of you -- I mean Enron) has screwed me and the people who work for me.'''

print(message_text)

# Calling the polarity_scores method on sid and passing in the message_text outputs a dictionary with negative, neutral, positive, and compound scores for the input text
scores = sid.polarity_scores(message_text)

# Here we loop through the keys contained in scores (pos, neu, neg, and compound scores) and print the key-value pairs on the screen

for key in sorted(scores):
        print('{0}: {1}, '.format(key, scores[key]), end='')

## SNIPPET 2
## Add in sentence-by-sentence analysis

from nltk import sent_tokenize, word_tokenize

message_sentences_list = sent_tokenize(message_text)

for sentence in message_sentences_list:
    scores = sid.polarity_scores(sentence)
    for key in sorted(scores):
        print('{0}: {1}, '.format(key, scores[key]), end='')


## SNIPPET 3
## Reading data in from a .csv file into a dictionary structure

import csv

file_name = "input.csv"
with open(file_name) as file_handle:
    song_data = csv.DictReader(file_handle)
    for row in song_data:
        print(song_data)


# to separate lines by newline character ('\n')
line_list = lyrics.split('\n')

# to append all songs to a big ol list to work with in Python

all_songs = []
file_name = "input.csv"
with open(file_name) as file_handle:
    song_data = csv.DictReader(file_handle)
    for row in song_data:
        all_songs.append(row)

