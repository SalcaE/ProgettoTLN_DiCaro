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

    return tokenized_sents

def vocabulary(sentences):
    tupla=()
    meh=[]
    mehmeh=[]
    riempiScore=[]
    for i in range(0,len(sentences)):
        if i+1 < len(sentences):#scorro fino all'ultimo
            
            x=list(set(sentences[i])-set(sentences[i+1]))
            x1=list(set(sentences[i+1])-set(sentences[i]))

            ciao = set(sentences[i+1])
            prova= [f for f in sentences[i] if f not in ciao ]

            for word in sentences[i]:
                if word not in sentences[i+1]:
                    meh.append(word)

            for word in sentences[i+1]:
                if word not in sentences[i]:
                    meh.append(word)

            score = len(meh)/(len(sentences[i])+len(sentences[i+1]))
                #if word in sentences[i+1]:
                    #sentences[i].remove(word)
                    #sentences[i+1].remove(word)
                    #lollino = 1

                    #z= sentences[i].index(word)
                    #z1 = sentences[i+1].index(word)
                    #sentences[i].pop(z)
                    #sentences[i+1].pop(z)
            #tupla= (i,i+1)
            tupla= (i,i+1,score)
            mehmeh.append(tupla)
            riempiScore.append([score])
           # meh.append(tupla)
  


    #fare uno score [0,1],[1,2]

    #normalizzo
    print("cazzo-NP")
    #x_norm = (riempiScore-np.min(riempiScore))/(np.max(riempiScore)-np.min(riempiScore))
 
    t=[]
    for a in mehmeh:
        x_norm = (a[2]-np.min(riempiScore))/(np.max(riempiScore)-np.min(riempiScore))
        i= mehmeh.index(a)
        tt=(a[0],a[1],x_norm)
        mehmeh[i] = tt
        t.append(x_norm)
      
        

    print(mehmeh)


    #prendo il minimo 3 volte(non credo vada...)
    print("valori minimi")
    print(sorted(t)[1])
    print(sorted(t)[2])
    print(sorted(t)[3])

    pene = 20
    



#tupla {(lf,rf,score),...}

def main():
    sentences = text_processing("esercizio4/sample.txt")
    vocabulary(sentences)
    

if __name__ == '__main__':
   main()