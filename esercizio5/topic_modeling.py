import gensim
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def text_processing(file_location):
    text=[]
    stop = set(stopwords.words('english'))
    return True


def main():

    tokenized_sents = text_processing("esercizio4/texts.txt")

    

if __name__ == '__main__':
   main()