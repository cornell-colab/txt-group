#Opening packages#
from gensim.models import Word2Vec
import spacy
import csv
import gzip, json
import re
from collections import Counter
nlp = spacy.load('en_core_web_sm')

#Needful things#
word_pattern = re.compile(r"\w[\w\-\']*\w|\w")

#Reading for Vector#
all_lines = []
tokens = []
for line in gzip.open("gutenberg-poetry-v001.ndjson.gz"):
    jrow = json.loads(line.strip())
    jline = jrow['s']
    word_in_line = word_pattern.findall(jline)
    tokens.extend(word_in_line)
    all_lines.append(word_in_line)

total_tokens = len(tokens)
total_counts = Counter(tokens)
vocabulary_size = len(total_counts.keys())

#Reading for New Poems#
'''glor_dat = []
with open ("cssonnets.csv") as worktext:
    reader = csv.reader(worktext)
    count = 0
    for row in reader:
        count += 1
        poem = row[2]
        lined_poem = poem.splitlines()
        lc = 0
        for line in lined_poem:
            lc +=1
            line = line.rstrip()
            tokens = word_pattern.findall(line)
            glor_dat.append([count, lc, tokens, line])'''

#Training Data#
repl_model = model = Word2Vec(all_lines, size = 150,  min_count=5)

#Exploring the Word2Vec Model#
repl_model.wv.most_similar(positive = "string")
#Word Substitution#
Sample = glor_dat[3][2]
Fresh_Sentence =[]
def word_substitute (token):
    candidates = repl_model.wv.most_similar(positive = token)
    Fresh_Sentence.append(candidates[1][0])
   
for item in Sample:
    word_substitute(item)
#What errors does this produce?#
oov_terms = []
check_vector = repl_model.wv

def find_oov_terms(lst):
    for token in lst:
        if token in check_vector.vocab:
            pass
        else:
            oov_terms.append(token)

for item in Sample:
    if item in oov_terms:
        pass
    else:
        word_substitute(item)

print(" ".join(Fresh_Sentence))

#Can NLP produce better poems?#
def swap_by_POS (line):
    pos_line= nlp(line)
    check = []
    new_sent =[]
    for item in pos_line:
        check.append(item.text)
    find_oov_terms(check)
    for word in pos_line:
        if word.text in oov_terms:
            pass
        elif word.pos_ == "NOUN":
            candidates = repl_model.wv.most_similar(positive = str(word))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ =="NOUN":
                    new_sent.append(cand)
                    break
        elif word.pos_ == "VERB":
            candidates = repl_model.wv.most_similar(positive = str(word))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ =="VERB":
                    new_sent.append(cand)
                    break
        else:
            new_sent.append(str(word))
    return(" ".join(new_sent))


flower_gathering =[
"I left you in the morning,", 
"And in the morning glow,",
"You walked a way beside me",
"To make me sad to go.",
"Do you know me in the gloaming,",
"Gaunt and dusty grey with roaming?",
"Are you dumb because you know me not,",
"Or dumb because you know?",

"All for me? And not a question",
"For the faded flowers gay",
"That could take me from beside you",
"For the ages of a day?",
"They are yours, and be the measure", 
"Of their worth for you to treasure,",
"The measure of the little while",
"That I’ve been long away." 
]
#How to retain rhyme#
def longest_common_prefix(seq1, seq2):
    start = 0
    while start < min(len(seq1), len(seq2)):
        if seq1[start] != seq2[start]:
            break
        start += 1
    return seq1[:start]

def longest_common_suffix(seq1, seq2):
    return longest_common_prefix(seq1[::-1], seq2[::-1])[::-1]

def Suffix_keeper(word):
    contenders = repl_model.wv.most_similar(positive = word, topn=200)
    pword = nlp(word)
    pos_word =pword[0].pos_
    names = []
    poss=[]
    swap_word = ""
    for entry in contenders:
        token = entry[0].lower()
        if token != word.lower():
            names.append(token)
            poss.append(longest_common_suffix(word, token))
    longest_commons = str(max(poss, key = len))
    for entry in names:
        if entry.endswith(longest_commons):
            if entry.lower() != OOV_term:
                pcand = nlp(entry)
                pos_cand = pcand[0].pos_
                if pos_cand == pos_word:
                    swap_word = entry
                else:
                    pass
    return(swap_word)

#write code that will use "Suffix_keeper" on last word token of each line#