import gensim
from pprint import pprint
from gensim import corpora
import nltk
nltk.download('stopwords', quiet=True)
import os
from nltk.corpus import stopwords
import string
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

def text_processing(file_location):
    texts=[]
    stop = set(stopwords.words('english') + list(string.punctuation) + ['--','-','``',"\""])
    for file_name in os.listdir(file_location):
        with open(file_location + file_name, 'r') as f:
            text = f.read().replace("\n",' ')
            tmp = nltk.word_tokenize(text)
            tokens = [doc[0].lower() for doc in nltk.pos_tag(tmp) if doc[0] not in stop and doc[1] in ['NN','NNS','NNP','NNPS']]
            texts.append(tokens)
    return texts

def lda_process(texts,num_topic):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topic)
    
    lda = gensimvis.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(lda,'esercizio5/htmlResults.html')
  
    print(num_topic,' TOPIC')
    pprint(lda_model.print_topics())
   

def main():
    texts = text_processing("esercizio5/data/")
    lda_process(texts,5)

    
if __name__ == '__main__':
   main()