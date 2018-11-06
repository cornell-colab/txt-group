import nltk, re, collections, sys
import matplotlib.pyplot as plt
import csv
from collections import OrderedDict
from nltk.tokenize import sent_tokenize
from nltk import ngrams

word_pattern = re.compile(r"\w[\w\-\']*\w|\w")
##This step creates a list that tokenizes and tags each sentence in CSV file. Count is equal to the row of the csv and part is equal to the sentence in that row##
tidy_tagged_tokens = []
with open(sys.argv[1]) as worktext:
    reader = csv.reader(worktext)
    count = 0
    for row in reader:
        count += 1
        line = row[int(sys.argv[2])]
        sentence = sent_tokenize(line)
        for part in range(len(sentence)):
            tokens = word_pattern.findall(sentence[part])
            tagged_words = nltk.pos_tag(tokens)
            tidy_tagged_tokens.append([count, part, tagged_words])
ttt = tidy_tagged_tokens

def graph_Word_Placement(tidy_tagged_tokens, word):
    material_to_plot =[]
    for entry in tidy_tagged_tokens:
        for section in entry[2]:
            if word in section[0]:
                mark = entry[0]
                material_to_plot.append(mark)
    lim = max(material_to_plot)
    graphmat = collections.Counter(material_to_plot)
    for i in range(lim):
        if i in graphmat.keys():
            pass
        else:
            graphmat[i] = 0
    graphmat = OrderedDict(sorted(graphmat.items(), key=lambda t: t[0]))
    x_axis = []
    for item in graphmat.keys():
        x_axis.append(item)
    y_axis = []
    for item in graphmat.values():
        y_axis.append(item)
    plt.plot(x_axis, y_axis)
    plt.xlabel('entry')
    plt.ylabel('appearance')
    plt.title(word)
    plt.show()

def find_common_adjnoun(tidy_tagged_tokens):
    biadjnoun = []
    for entry in tidy_tagged_tokens:
            for section in range(len(entry[2])):
                if 'JJ' in  entry[2][section]:
                    if len(entry[2]) - section > 2:
                        if 'NN' in entry[2][section + 1]:
                            biadjnoun.append(" ".join([entry[2][section][0], entry[2][section + 1][0]]))
    fdist = nltk.FreqDist(biadjnoun)
    return(fdist.most_common(10))

def generate_word_contexts(tidy_tagged_tokens, word):
    context = []
    for entry in tidy_tagged_tokens:
        for section in range(len(entry[2])):
            if word in entry[2][section]:
                if len(entry[2]) - section > 2:
                    context.append(" ".join([entry[2][section -1][0], entry[2][section][0], entry[2][section + 1][0]]))
    context_dist = nltk.FreqDist(context)
    return(context_dist)

def generate_cool_contexts(tidy_tagged_tokens):
    cool_context = []
    for entry in tidy_tagged_tokens:
        for section in entry[2]:
            if section[1].startswith('N') or section[1].startswith('V') :
                if len(section[0]) > 1:
                    cool_context.append(section[0])
    n = 3
    trigrams = ngrams(cool_context, n)
    tridist = nltk.FreqDist(trigrams)
    return(tridist)