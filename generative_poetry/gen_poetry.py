import nltk, re, collections, sys
import matplotlib.pyplot as plt
import csv
import random
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

        line = row[int(sys.argv[2])]
        sentence = sent_tokenize(line)
        for part in range(0, len(sentence)):
            tokens = word_pattern.findall(sentence[part])
            tagged_words = nltk.pos_tag(tokens)
            tidy_tagged_tokens.append([count, part, tagged_words])
        count += 1
ttt = tidy_tagged_tokens

def generate_words_by_pos(tidy_tagged_tokens):
    # create a new dictionary to store lists of words, arranged by POS
    words_by_post = {}
    for entry in tidy_tagged_tokens:
        # print(entry)
        tokens = entry[2]
        if len(tokens) > 0:
            for token in tokens:
                word = token[0]
                pos = token[1]
                
                # if this is the first time we're seeing a specific POS, create new list with one item, our current word
                if pos not in words_by_post:
                    words_by_post[pos] = [word]
                else:
                    # otherwise, add the current word to our growing list for that POS
                    words_by_post[pos].append(word)

    return words_by_post

def output_words_given_pos(tidy_tagged_tokens, pos):
    words_by_pos = generate_words_by_pos(tidy_tagged_tokens)
    matching_words = words_by_pos[pos]
    if matching_words:
        print(matching_words)
    else:
        print('No words found for that POS')

def output_pos_cheat_sheet():
    print('''
    CC coordinating conjunction
    CD cardinal digit
    DT determiner
    EX existential there (like: “there is” … think of it like “there exists”)
    FW foreign word
    IN preposition/subordinating conjunction
    JJ adjective ‘big’
    JJR adjective, comparative ‘bigger’
    JJS adjective, superlative ‘biggest’
    LS list marker 1)
    MD modal could, will
    NN noun, singular ‘desk’
    NNS noun plural ‘desks’
    NNP proper noun, singular ‘Harrison’
    NNPS proper noun, plural ‘Americans’
    PDT predeterminer ‘all the kids’
    POS possessive ending parent’s
    PRP personal pronoun I, he, she
    PRP$ possessive pronoun my, his, hers
    RB adverb very, silently,
    RBR adverb, comparative better
    RBS adverb, superlative best
    RP particle give up
    TO, to go ‘to’ the store.
    UH interjection, errrrrrrrm
    VB verb, base form take
    VBD verb, past tense took
    VBG verb, gerund/present participle taking
    VBN verb, past participle taken
    VBP verb, sing. present, non-3d take
    VBZ verb, 3rd person sing. present takes
    WDT wh-determiner which
    WP wh-pronoun who, what
    WP$ possessive wh-pronoun whose
    WRB wh-abverb where, when
    ''')
    # source: https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b

def generate_poem_lib_style(tidy_tagged_tokens, user_recipe=None):
    words_by_pos = generate_words_by_pos(tidy_tagged_tokens)
    possible_recipes = [
        ['Hello', 'my', 't_JJ', 't_NNP', '\nI', 'wish', 'for', 'you', 'to', 't_VB', 't_NN'],
        [],
        [],
        []
    ]
    
    if user_recipe:
        recipe = user_recipe
    else:
        # replace with randomness measure
        recipe = possible_recipes[0]
    
    # now let's print out our poem
    working_poem = []
    for item in recipe:

        if 't_' in item:
            pos = item[2:]
            try:
                matching_words = words_by_pos[pos]
            except:
                matching_words = ['.']
            random_num = random.randint(0, len(matching_words) - 1)
            output_word = matching_words[random_num]
        else:
            output_word = item
        
        working_poem.append(output_word)
    print('\n')
    print(' '.join(working_poem))
    print('\n')


        

