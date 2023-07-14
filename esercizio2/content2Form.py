import sys 
sys.path.append('../ProgettoTLN_DiCaro')
import esercizio1.similarity as es1
from nltk.wsd import lesk
from collections import Counter
from rich.console import Console
from rich.table import Table
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import wordnet  as wn

def onomasiological_search(phrases):
    definitions = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    syns= {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for concept, phrases_lists in phrases.items():
        flat_list = [item for sublist in phrases_lists for item in sublist]
        sub_list = Counter(flat_list).most_common()[0:5]
        synsets = [wn.synsets(x[0]) for x in sub_list] #estriamo i synsets delle parole piu frequenti

        flat_list2 = [item for sublist in synsets for item in sublist]
        lemma_name= [x.lemmas()[0].name() for x in flat_list2] #estraiamo i nomi sysnet per eliminare room.n1 e room.n2
        sub_list2 = Counter(lemma_name).most_common()[0:10]

        hypos = [wn.synsets(x[0])[0].hyponyms() for x in sub_list2] 
        flat_res = [item for sublist in hypos for item in sublist]
        count_syn = Counter(flat_res).most_common()[0:20] #estraggo i primi 20 iponimi

        syns[concept] = count_syn  
        definitions[concept] = [x[0].definition() for x in count_syn] #degli iponimi
    definitions_lemmas = es1.lemmatizzation(definitions) 
    return definitions_lemmas, syns

def wordDisambiguation_search(phrases):
    res = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for concept, phrases_lists in phrases.items():
        for phrase in phrases_lists:    
            res[concept].append(lesk(phrase, concept)) #applico lesk sul contesto data la parola della definizione
    return res

def vectorizer(definitions_lemmas, phrases):
    cosine_res= {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for key, values in definitions_lemmas.items():
        join_def = definitions_lemmas[key] + phrases[key]
        document=[]
        vectorizer = CountVectorizer()
        for elem in join_def:
            document.append(" ".join(elem)) 
        vectorizer.fit(document)
        vector = vectorizer.transform(document)
        def_wd = vector[0:len(definitions_lemmas[key])] #divido matrice tra frasi definizioni iponimi e non 
        def_og = vector[len(definitions_lemmas[key]):(len(definitions_lemmas[key])+(len(phrases[key])))]
        tuple_list = []
        for elem in def_wd.toarray().tolist():
            i = def_wd.toarray().tolist().index(elem)
            for elem1 in def_og.toarray().tolist():
                j = def_og.toarray().tolist().index(elem1)

                tuple_list.append(((cosine_similarity(def_wd[i].toarray(),def_og[j].toarray())[0][0]), i, j))

        tuple_list.sort(key=lambda x: x[0], reverse=True)

        i = 0
        temp=[]
        for x in tuple_list:  #prendo i primi 5 synset diversi con il valore più alto
            if i < 5:
                if x[1] not in temp:
                    cosine_res[key].append(x)
                    temp.append(x[1])
                    i = i+1
    return cosine_res

def res_score_lesk(res):
    occurrences = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for key, syn in res.items():
        counter = Counter(syn) #conta le occorrenze dei synset nella lista
        leng = len(syn)
        counter.most_common() #ordino decrescente
        occurrences[key] = [(value, occ / leng * 100) for value, occ in counter.most_common()] #calcolo la percentuale di ogni synset
    return occurrences

def res_score(cos,syns):
    occurrences = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    for key, value in cos.items():
        for x in value:
            occurrences[key].append((syns[key][x[1]][0],x[0])) #associo sysnset allo score
    return occurrences 

def print_table(results):
    console = Console()
    table = Table(title="Result")
    table.add_column("Concept", style="bold")
    table.add_column("Synset", style="bold")
    table.add_column("Score", style="bold")
    for key, value in results.items():
        for score in value:
            table.add_row(key, score[0].name(), str(round(score[1],4)))
    console.print(table)
   
def main():
    phrases = es1.main(external=True)

    res = onomasiological_search(phrases)
    cos_res = vectorizer(res[0],phrases)
    score =res_score(cos_res, res[1])
    print_table(score)
    #

    wsd = wordDisambiguation_search(phrases)
    occurrences = res_score_lesk(wsd)
    print_table(occurrences)


if __name__ == '__main__':
    main() 