import spacy
from nltk.wsd import lesk

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
    sentences_dict = []
    lol=[]
    left_list=[]
    right_list=[]
    
    sp = spacy.load('en_core_web_md')
    for sentence in sentences:
        doc = sp(sentence)
        filter_list=[]
        for token in doc:
       
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

                if len(filter_list) ==2: #salva le coppie per ogni frase
                    #disambiguazione
                    z = lesk(sentence,filter_list[0])
                    z1 = lesk(sentence,filter_list[1])

                    if z and z1 is not None:
                        left_list.append(z.lexname())
                        right_list.append(z1.lexname())

                    sentences_dict.append(filter_list)
                    lol.append(sentence)
    
    left_to_right = []
    right_to_left = []
   


    ciao = 1


















def main():
    verb = ["take","took","taken","takes","taking"]
    res= elaborate_sentences(verb)
    cluster(res,verb)
    



if __name__ == '__main__':
    # spacy.cli.download('en_core_web_md')
   main()