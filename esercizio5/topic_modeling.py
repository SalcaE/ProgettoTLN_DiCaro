import gensim
import spacy
from gensim import corpora
import nltk
nltk.download('stopwords')
import os
from nltk.corpus import stopwords
import string
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

def text_processing(file_location):
    #pyLDAvis.enable_notebook()
    texts=[]
    stop = set(stopwords.words('english')+list(string.punctuation)+['--','-','``',"\""])
    for file_name in os.listdir(file_location):
        with open(file_location + file_name, 'r') as f:
            text = f.read().replace("\n",' ')
            tmp = nltk.word_tokenize(text)
            tokens = [doc[0].lower() for doc in nltk.pos_tag(tmp) if doc[0] not in stop and doc[1] in ['NN','NNS','NNP','NNPS']]
            texts.append(tokens)
            print("ale")

    num_topics = 15
    dictionary = corpora.Dictionary(texts)
    corpussss = [dictionary.doc2bow(text) for text in texts]
    lda_model = gensim.models.LdaMulticore(corpus=corpussss, id2word=dictionary, num_topics=num_topics)
    print(lda_model.print_topics())
    lda = gensimvis.prepare(lda_model, corpussss, dictionary)
    pyLDAvis.display(lda)
    print('NAPOHAZEW')
    return texts


def main():

    tokenized_sents = text_processing("esercizio5/data/")

    

if __name__ == '__main__':
   main()