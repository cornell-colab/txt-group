#adapted from Mimno/week2/sentiment.py#
import re, sys
from collections import Counter
import matplotlib.pyplot as plt 

syuzhet = "syuzhet.csv"
text = "sample_text.txt"

#Getting Weights from Classifer#
mapWordWeights = {}
with open(syuzhet) as guide:
    for line in guide:
        weight, word = line.split(",")
        word = word.rstrip()
        mapWordWeights[word] = float(weight)

#Scoring words#
def score_counts(counter):
    score = 0
    total_tokens = sum(counter.values())
    if total_tokens == 0:
        return 0
    for word in counter.keys():
        if word in mapWordWeights:
            score += mapWordWeights[word]* counter[word]
    score = score /total_tokens
    return(score)


#Making txt file readable#
word_pattern = re.compile(r"\w[\w\-\']*\w|\w")
structuredParas = []
with open(text) as passage:
    line_number = 0
    for line in passage:
        line = line.rstrip()
        tokens = word_pattern.findall(line)
        Para_counts = Counter(tokens)
        structuredParas.append({ 'text': line, 'counts': Para_counts, 'score': score_counts(Para_counts), 'line': line_number })
        line_number += 1

structuredParas.sort(key = lambda x: x['line'])

for Para in structuredParas:
    print("{}\t{}\t{}".format(Para['line'],Para['score'], Para['text']))

#Plotting it out#
x_axis = []
y_axis = []
for item in range(len(structuredParas)):
    line_score=structuredParas[item]['score']
    line_number=structuredParas[item]['line']
    x_axis.append(line_number)
    y_axis.append(line_score)
    
plt.plot(x_axis, y_axis)
plt.xlabel('duration')
plt.ylabel('valence')
plt.title('sentiment')
plt.show()
