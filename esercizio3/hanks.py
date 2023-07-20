import spacy
from nltk.wsd import lesk
from collections import defaultdict
from rich.console import Console
from rich.table import Table

def elaborate_sentences(verb):
    sentences = set()
    with open('esercizio3/sentences.txt', 'r', encoding="utf8") as values:
        
        for sentence in values:
            if any(item in sentence for item in verb):
                sentences.add(sentence)
         
    personal_name = set()
    with open('esercizio3/nomi_persone.txt', 'r', encoding="utf8") as x:
        personal_name = x.read().split('\n')
    
    list_sentences = list(sentences)
    for count,sentence in enumerate(list_sentences):  # metto person al posto dei nomi
        for word in sentence.split() :
            if word in personal_name:
                    list_sentences[count] = sentence.replace(word, 'person')
                    
    return list_sentences

def cluster(sentences,verb):
    left_list=[]
    right_list=[]
    
    sp = spacy.load('en_core_web_md')
    for sentence in sentences:
        tokens = sp(sentence)
        filter_list=[]
        for token in tokens:
       
            if any(item in token.lemma_ for item in verb):
               
                for child in token.children:
                    match child.pos_:
                        case "NOUN":
                           filter_list.append(child.text)
                        case "PRON":
                            if child.text == 'it' or child.text == 'It':
                                filter_list.append('thing')                                 
                            elif child.text == 'they' or child.text == 'They':
                                continue
                            else:
                                filter_list.append('person')

                if len(filter_list) == 2: #salva le coppie per ogni frase
                    x = lesk(sentence,filter_list[0])
                    y = lesk(sentence,filter_list[1])

                    if x and y is not None:
                        left_list.append(x.lexname())
                        right_list.append(y.lexname())
    
    left_to_right = defaultdict(set)
    right_to_left = defaultdict(set)
    for count, item in enumerate(left_list):
        left_to_right[item].add(right_list[count])
    for count, item in enumerate(right_list):
        right_to_left[item].add(left_list[count])

    print_tables(left_list,right_list,left_to_right,right_to_left)
    
def print_tables(left_list,right_list,left_to_right,right_to_left):
    console = Console()
    table_l = Table(show_header=True, title="TAKE left to right", show_lines=True)
    table_l.add_column("Frequenza")
    table_l.add_column("Sinistra")
    table_l.add_column("Destra")

    for item in left_to_right:
        fre = left_list.count(item)
        table_l.add_row(str(fre)+'/'+str(len(left_list)),item, str(left_to_right[item]))
    console.print(table_l)

    table_r = Table(show_header=True, title="TAKE right to left", show_lines=True)
    table_r.add_column("Frequenza")
    table_r.add_column("Sinistra")
    table_r.add_column("Destra")
    for item in right_to_left:
        fre = right_list.count(item)
        table_r.add_row(str(fre)+'/'+str(len(right_list)),item, str(right_to_left[item]))
    console.print(table_r)

def main():
    verb = ["take","took","taken","takes","taking"]
    #verb = ["do","does","doing","did","done"]
    res= elaborate_sentences(verb)
    cluster(res,verb)
    

if __name__ == '__main__':
   main()