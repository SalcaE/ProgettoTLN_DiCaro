import spacy
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from nltk.tokenize import sent_tokenize

from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn import preprocessing


def text_processing(filename):
    texts =[]
    spa = spacy.load('en_core_web_md')

    with open(filename, 'r', encoding="utf8") as f:
        texts = f.read().splitlines()
    sents = []
    for text in texts:
        doc = spa(text)
        for sent in doc.sents:
            sents.append(sent)

    tokenized_sents = [[token.lemma_.lower() for token in sent 
                        if not token.is_stop and 
                        not token.is_punct and token.text.strip() and 
                        len(token) >= 3] #vedere se tenere
                        for sent in sents]
    senteces = [x for x in tokenized_sents if x]

    return senteces

def vocabulary(sentences):
    new_words1 = set()
    new_words2 = set(sentences[0])
    scores=[]

    for i in range(1,len(sentences)-1):
        left_words = set(sentences[i-1]).difference(new_words1)
        right_words = set(sentences[i+1]).difference(new_words2)
        score = (len(left_words) + len(right_words)) / (len(sentences[i-1])+len(sentences[i+1]))
        scores.append(score)
        new_words1 = new_words1.union(sentences[i-1])
        new_words2 = new_words2.union(sentences[i+1])
    last = set(sentences[len(sentences)-1]).difference(new_words1)
    scores.append(len(last)/len(sentences[len(sentences)-1]))
    return scores

def boundaries(scores, sentences): #+1 ordine score tokens 
    boundaries=[]
    mean = np.mean(scores) -  np.std(scores)
    for i, score in enumerate(scores):
        depth_scores = depth_score(scores, i, "left") + depth_score(scores, i, "right")

        if depth_scores >= mean:
            boundaries.append(i)
    x = []
    for i in boundaries:
        x.append(sentences[i+1])
    
    return boundaries

def depth_score(scores, current, side):
    depth_score = 0
    i = current
    while scores[i] - scores[current] >= depth_score:
        depth_score = scores[i] - scores[current]

        if side == 'left':
            i = i - 1
            if (i < 0): break
        else:
            i = i + 1
            if (i == len(scores)): break
    return depth_score


def main():
    #sentences = text_processing("esercizio4/sample.txt")
    sentences = text_processing("esercizio4/es2.txt")
    scores=vocabulary(sentences)
    boundaries2 = boundaries(scores, sentences)
    

if __name__ == '__main__':
   main()