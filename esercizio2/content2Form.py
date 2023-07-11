import sys 
sys.path.append('../ProgettoTLN_DiCaro')
import esercizio1.similarity as es1
from nltk.wsd import lesk
from collections import Counter
from rich.console import Console
from rich.table import Table

def wordDisambiguation():
    phrases = es1.main(external=True)
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

def res_score(res):
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

def print_table(results):
    console = Console()
    table = Table(title="Result")
    table.add_column("Concept", style="bold")
    table.add_column("Disambiguated Concept", style="bold")
    table.add_column("Score", style="bold")
    for key, value in results.items():
        for score in value:
            table.add_row(key, score[0].name(), str(round(score[1],4)))
    console.print(table)
   
def main():
    wsd = wordDisambiguation()
    occurrences = res_score(wsd)
    print_table(occurrences)

if __name__ == '__main__':
    main() #ciaone