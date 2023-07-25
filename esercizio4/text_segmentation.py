import spacy
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from nltk.tokenize import sent_tokenize



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

    return texts

#tupla {(lf,rf,score),...}

def main():
    sentences = text_processing("esercizio4/sample.txt")
    

if __name__ == '__main__':
   main()