import sys 
sys.path.append('../ProgettoTLN_DiCaro')
import esercizio1.porco as cazzo
from nltk.wsd import lesk


def wordDisambiguation():
    
    phrases = cazzo.main(external=True)
    #print(phrases)

    for concept, phrases_lists in phrases.items():
        for phrase in phrases_lists:
            print(lesk(phrase, concept)) 


def main(external=False):

    wordDisambiguation()

    sent ='A construction used to divide two rooms, temporarily closing the passage between them'
   # print(lesk(sent, 'door'))
    #print(lesk(sent, 'door').definition())






if __name__ == '__main__':
    main()