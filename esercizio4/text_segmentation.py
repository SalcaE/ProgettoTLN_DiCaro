import spacy
import numpy as np

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

    tokens = [[token.lemma_.lower() for token in sent       #tokenizzo le frasi
                        if not token.is_stop and 
                        not token.is_punct and token.text.strip() and 
                        len(token) >= 3] #vedere se tenere
                        for sent in sents]
    tokenized_sents = [x for x in tokens if x] #tolgo liste vuote

    return tokenized_sents, sents

def vocabulary(sentences):
    new_words1 = set()
    new_words2 = set(sentences[0])
    scores=[]

    for i in range(1,len(sentences)-1): #cotrollo parole nuove a sinistra e destra
        left_words = set(sentences[i-1]).difference(new_words1)
        right_words = set(sentences[i+1]).difference(new_words2)
        score = (len(left_words) + len(right_words)) / (len(sentences[i-1])+len(sentences[i+1])) #come nell'articolo
        scores.append(score)
        new_words1 = new_words1.union(sentences[i-1])
        new_words2 = new_words2.union(sentences[i+1])
    last = set(sentences[len(sentences)-1]).difference(new_words1)
    scores.append(len(last)/len(sentences[len(sentences)-1]))
    return scores

def get_boundaries(scores):
    boundaries=[]
    mean = np.mean(scores) -  np.std(scores)
    for i, score in enumerate(scores):
        depth_scores = depth_score(scores, i, "left") + depth_score(scores, i, "right")

        if depth_scores >= mean:
            boundaries.append(i)
    return boundaries

def depth_score(scores, current, side): #cerco gli score migliori su cui mettere un confine
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

def pirnt_results(boundaries, sentences):
    print(boundaries)
    for i, x in enumerate(sentences):
        print(sentences[i])
        if i in boundaries:
            print()

def main():
    #TESTO: ARTICOLO, BARBIE, CORRISPONDENZA CANI
    #tokenized_sents = text_processing("esercizio4/sample.txt")
    tokenized_sents = text_processing("esercizio4/es2.txt")
    scores = vocabulary(tokenized_sents[0])
    boundaries = get_boundaries(scores)
    pirnt_results(boundaries,tokenized_sents[1])
    

if __name__ == '__main__':
   main()