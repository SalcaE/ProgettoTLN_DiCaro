import gensim
from gensim import corpora
import nltk
nltk.download('stopwords')
import os
from nltk.corpus import stopwords
import string
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

def text_processing(file_location):
    texts=[]
    stop = set(stopwords.words('english')+list(string.punctuation)+['--','-','``',"\""])
    for file_name in os.listdir(file_location):
        with open(file_location + file_name, 'r') as f:
            text = f.read().replace("\n",' ')
            sapo = [doc.lower() for doc in nltk.word_tokenize(text) if doc not in stop]
            texts.append(sapo)

    num_topics = 15
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    pyLDAvis.enable_notebook()
    gensimvis.prepare(lda_model, corpus, dictionary, mds='mmds')
    return texts


def main():

    tokenized_sents = text_processing("esercizio5/data/")

    

if __name__ == '__main__':
   main()