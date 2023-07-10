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
    data = []
    fileText= panda.read_csv(location, sep='\t', header=None)
    for row in fileText.columns[1:]:
        x= fileText[row].tolist()
        key=  x.pop(0)
        data.append({key: x})
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
    lemmas_set = {  #dizionario di array
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }

    lemmatizer = WordNetLemmatizer() #classe contentente tutti i lemmi(parole base)
    stop = set(stopwords.words('english') + list(string.punctuation) + ["'s", "'", "n't","\"", "``", "'d", "'re", "''","''"])#rimozioni di parole e punteggiature 
    for a in data: #a è elemento array {key:[frasi]}
        for key, values in a.items(): #values contiene tutte le frasi già divise su key
            tokens = [word_tokenize(i.lower()) for i in values]#trasformo ogni paraola delle frasi in token e le metto lower
            for x in tokens:
                lemmas = []
                index = tokens.index(x) #prendo indice nell'array di token/frasi
                tmp = [word for word in x if not word in stop] #in tmp ho la frase pulita con le stop
                tmp_line = list(map(lambda x: (x[0], pos_tagger(x[1])), nltk.pos_tag(tmp))) #fai tagging VEDI
                for word, tag in tmp_line:
                    if tag is None:
                        lemmas.append(word) #copia diretto
                    else: #se il tag è conosciuto:      
                        lemmas.append(lemmatizer.lemmatize(word, tag)) #metti parole base/lemmatizzata
                tokens[index] = lemmas #sovrascrivi nella stessa posizione la nuova frase lemmatizata <3
            lemmas_set[key] = tokens #metti all'interno della giusta key del dizionario l'insieme di parole lemmatizzate (edu chan <3)
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
        vectorizer = CountVectorizer()#per creare la matrice di parole uniche
        for elem in values:#per ogni array token
            document.append(" ".join(elem)) #per ogni array convertilo in stringa e mettilo in document
        vectorizer.fit(document)#magia
        vector = vectorizer.transform(document) #codifica il documuento

        #print("Vocabulary: ", vectorizer.vocabulary_)
        
        cont = 0 #reset per ogni key nuova
        for x in vector.toarray().tolist():
            i = vector.toarray().tolist().index(x)#prendo la posizione dell'array dentro vector (all'inizio il primo..)
            
            for y in vector.toarray().tolist():#prendo element
                j = vector.toarray().tolist().index(y) #prendo posizione di y
                
                if i != j : #entra tranne quando è se stesso l'array 

                    #sum = sum + dist_euclidea(vector[0],vector[1])

                    sum = sum + cosine_similarity(vector[0].toarray(),vector[1].toarray())[0][0]
                    
                    cont = cont + 1 #cont= Totrighe * TotRighe-1
                       
        similarity[key] = (sum/cont) #metto la media tra totale valore/volte che è stato calcolato
    return similarity

def dist_euclidea(v0,v1):
    a= np.array(v0.toarray())
    b= np.array(v1.toarray())
    return np.linalg.norm(a-b)
    



def print_table(results):
    console = Console()
    table = Table(title="Result")
    table.add_column("")#prima colonna vuota
    table.add_column("Astratto")
    table.add_column("Concreto")
    table.add_row("Generico", str(round(results['pain'], 6)), str(round(results['door'], 6)))#round arrotonda le cifre decimali a 6
    table.add_row("Specifico", str(round(results['blurriness'], 6)), str(round(results['ladybug'], 6)))
    console.print(table)


def main(external=False):
    data=read_tsv('Esercizio1\TLN-definitions-23.tsv')#data = array {'key':[frase1,frase2]} {key..}
    lemmas = lemmatizzation(data) #lemmas: dizionario sulle key con tutte frasi lemmatizzate 
    results = similarity(lemmas)
   # print_table(results)
    

    if not external:
        print_table(results)
    
    return lemmas


if __name__ == '__main__':
    # print(squash_function([1,2,1]))
    main()
