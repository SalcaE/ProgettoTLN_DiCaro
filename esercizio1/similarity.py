import nltk
import pandas as panda
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import wordnet
from rich.console import Console
from rich.table import Table
import string
import numpy as np
 

def read_tsv(location):
    data = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }

    fileText= panda.read_csv(location, sep='\t', header=None)
    for row in fileText.columns[1:]:
        x= fileText[row].tolist()
        key=  x.pop(0)
        data[key] = x
    return data


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:         
        return None


def lemmatizzation(data):
    lemmas_set = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }

    lemmatizer = WordNetLemmatizer()
    stop = set(stopwords.words('english') + list(string.punctuation) + ["'s", "'", "n't","\"", "``", "'d", "'re", "''","''"])#rimozioni di parole e punteggiature 

    for key, values in data.items():
        tokens = [word_tokenize(i.lower()) for i in values]
        for x in tokens:
            lemmas = []
            index = tokens.index(x)
            tmp = [word for word in x if not word in stop]
            tmp_line = list(map(lambda x: (x[0], pos_tagger(x[1])), nltk.pos_tag(tmp)))
            for word, tag in tmp_line:
                if tag is None:
                    lemmas.append(word)
                else:
                    lemmas.append(lemmatizer.lemmatize(word, tag))
            tokens[index] = lemmas #sovrascrivi nella stessa posizione la nuova frase lemmatizata
        lemmas_set[key] = tokens
    return lemmas_set
    

def similarity(lemmas):
    similarity = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for key, values in lemmas.items():
        sum = 0
        document=[]
        vectorizer = CountVectorizer()
        for elem in values:
            document.append(" ".join(elem)) #per ogni array convertilo in stringa e mettilo in document
        vector = vectorizer.fit_transform(document)
        
        cont = 0
        for x in vector.toarray().tolist():
            i = vector.toarray().tolist().index(x)
            
            for y in vector.toarray().tolist():
                j = vector.toarray().tolist().index(y)
                
                if i != j :

                    #sum = sum + dist_euclidea(vector[0],vector[1])
                    sum = sum + cosine_similarity(vector[i].toarray(),vector[j].toarray())[0][0]
                    cont = cont + 1
                       
        similarity[key] = (sum/cont)
    return similarity

def dist_euclidea(v0,v1):
    a= np.array(v0.toarray())
    b= np.array(v1.toarray())
    return np.linalg.norm(a-b)
    

def print_table(results):
    console = Console()
    table = Table(title="Result")
    table.add_column("")
    table.add_column("Astratto")
    table.add_column("Concreto")
    table.add_row("Generico", str(round(results['pain'], 6)), str(round(results['door'], 6)))
    table.add_row("Specifico", str(round(results['blurriness'], 6)), str(round(results['ladybug'], 6)))
    console.print(table)


def main(external=False):
    data=read_tsv('esercizio1\TLN-definitions-23.tsv')
    lemmas = lemmatizzation(data)
    results = similarity(lemmas)

    if not external:
        print_table(results)
    
    return lemmas

if __name__ == '__main__':

    main()
