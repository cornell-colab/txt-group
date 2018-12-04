#Opening packages#
from gensim.models import Word2Vec
import spacy
import csv
import gzip, json
import re
from collections import Counter
import pronouncing
import nltk
nlp = spacy.load('en_core_web_sm')
try:
    arpabet = nltk.corpus.cmudict.dict()
except LookupError:
    nltk.download('cmudict')
    arpabet = nltk.corpus.cmudict.dict()
from itertools import product as iterprod

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
            if entry != word:
                pcand = nlp(entry)
                pos_cand = pcand[0].pos_
                if pos_cand == pos_word:
                    swap_word = entry
                elif pos_word in ["PRON", "ADV", "ADP"]:
                    swap_word = pword.text
    return(swap_word)

def rhymer(line):
    words = word_pattern.findall(line)
    target_word = words[-1]
    return(Suffix_keeper(target_word))

def swap_by_POS (line):
    pos_line= nlp(line)
    length = word_pattern.findall(line)
    check = []
    new_sent =[]
    for item in pos_line:
        check.append(item.text)
    find_oov_terms(check) 
    for position in range(len(length) - 1):
        if str(pos_line[position]) in oov_terms:
            new_sent.append(str(pos_line[position]))
        elif pos_line[position].pos_ == "NOUN":
            candidates = repl_model.wv.most_similar(positive = str(pos_line[position]))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ =="NOUN":
                    new_sent.append(cand)
                    break
        elif pos_line[position].pos_ == "VERB":
            candidates = repl_model.wv.most_similar(positive = str(pos_line[position]))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ == "VERB":
                    new_sent.append(cand)
                    break
        else:
            new_sent.append(str(pos_line[position]))
    new_sent.append(rhymer(line))
    
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

for line in flower_gathering:
    swap_by_POS(line)

#Sweating the scansion#

def wordbreak(s):
    s = s.lower()
    if s in arpabet:
        return arpabet[s]
    middle = len(s)/2
    partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
    for i in partition:
        pre, suf = (s[:i], s[i:])
        if pre in arpabet and wordbreak(suf) is not None:
            return [x+y for x,y in iterprod(arpabet[pre], wordbreak(suf))]
    return None


def estimate_stress(word):
    if len(pronouncing.phones_for_word(word)) > 0:
            apra_word = pronouncing.phones_for_word(word)
            stress = pronouncing.stresses(apra_word[0])
            return(stress)
    else:
        oov_terms.append(word)
        wb_word = wordbreak(word)
        if wb_word is None:
            pass
        else:
            apra_word = " ".join(wb_word[0])
            stress = pronouncing.stresses(apra_word)    
            return(stress)

def new_Suffix_keeper(word):
    contenders = repl_model.wv.most_similar(positive = word, topn=200)
    pword = nlp(word)
    wstress = estimate_stress(word)
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
            if entry != word:
                pcand = nlp(entry)
                pos_cand = pcand[0].pos_
                if pos_cand == pos_word:
                    if wstress == estimate_stress(str(pcand)):
                        swap_word = entry
                elif pos_word in ["PRON", "ADV"]:
                    swap_word = pword.text
    return(swap_word)


def new_rhymer(line):
    words = word_pattern.findall(line)
    target_word = words[-1]
    return(new_Suffix_keeper(target_word))


def new_swap_by_POS (line):
    pos_line= nlp(line)
    length = word_pattern.findall(line)
    check = []
    new_sent =[]
    for item in pos_line:
        check.append(item.text)
    find_oov_terms(check) 
    for position in range(len(length) - 1):
        if str(pos_line[position]) in oov_terms:
            new_sent.append(str(pos_line[position]))
        elif pos_line[position].pos_ == "NOUN":
            candidates = repl_model.wv.most_similar(positive = str(pos_line[position]))
            wstress = estimate_stress(str(pos_line[position]))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ =="NOUN":
                    if estimate_stress(str(cand)) == wstress:
                        new_sent.append(cand)
                        break
        elif pos_line[position].pos_ == "VERB":
            candidates = repl_model.wv.most_similar(positive = str(pos_line[position]))
            wstress = estimate_stress(str(pos_line[position]))
            for candidate in range(len(candidates)):
                cand = candidates[candidate][0]
                pos_cand = nlp(cand)
                if pos_cand[0].pos_ == "VERB":
                    if estimate_stress(str(cand)) == wstress:
                        new_sent.append(cand)
                        break
        else:
            new_sent.append(str(pos_line[position]))
    new_sent.append(new_rhymer(line))
    
    return(" ".join(new_sent))