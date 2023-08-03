import os
import json as js
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
import pandas as pd

def synset_processing(file_location):
    elements= {}
    index = 0
    for file_name in os.listdir(file_location):

        f=open(file_location + file_name, 'r')
        data_worker = js.load(f)

        for i, syn in enumerate(data_worker['dataset']):
            values=[0,0,0,0,0] #hard T-F, Basic, Adv, time

            if data_worker['isHard'][i] == True:
                values[0] = values[0] + 1
            else:
                values[1] = values[1] + 1

            if data_worker['answers'][i] == "basic":
                values[2] = values[2] + 1
            else:
                values[3] = values[3] + 1

            values[4] = data_worker['timeDiffs'][i]

            if syn.split('\'')[1] in elements: 
                    
                    x = elements[syn.split('\'')[1]]
                    values = [x[i] + values[i] for i in range(len(x))]
                    if index == len(os.listdir(file_location))-1:
                        p = values[4]/10
                        values[4] = p

            elements[syn.split('\'')[1]] = values
        index = index + 1

    data = {
        'syn': [],
        'difficulty': [],
        'len':[],
        'category': [],
        'time': []
    }

    for key, elem in elements.items():

        data['syn'].append(key)
        data['len'].append(len(key))
        data['time'].append(elem[4])

        if elem[0] > elem[1]:
            data['difficulty'].append('hard')
        else:
            data['difficulty'].append('easy')

        if elem[2] > elem[3]:
            data['category'].append('basic')
        else:
            data['category'].append('advanced')
    df = pd.DataFrame(data)
    print(df)

    le = LabelEncoder()
    label = le.fit_transform(df['category']) #basic 1 | advanced 0
    label1 = le.fit_transform(df['difficulty'])
    label2 = le.fit_transform(df['syn'])

    df.drop("category", axis=1, inplace=True)
    df.drop("difficulty", axis=1, inplace=True)
    df.drop("syn", axis=1, inplace=True)

    df["syn"] = label2
    df["difficulty"] = label1
    df["category"] = label

    return df

def classifier(data):
    train_data = data.iloc[:,0:4]
    target = data.iloc[:,4]
    X_train, X_test, y_train, y_test = train_test_split(train_data,target,test_size=0.2)

    lr = LogisticRegression(solver='liblinear',multi_class='ovr')
    lr.fit(X_train, y_train)
    print('LOGIC REGRESSION score: ', lr.score(X_test, y_test))


    model=DecisionTreeClassifier()
    leave_val=LeaveOneOut()
    mod_score2=cross_val_score(model,X_train,y_train,cv=leave_val)
    print('LEAVE ONE OUT score: ',np.mean(mod_score2))


    model=DecisionTreeClassifier()
    kfold_validation=KFold(100)
    mod_score3=cross_val_score(model,X_train,y_train,cv=kfold_validation)
    print('KFOLD score: ',np.mean(mod_score3))


    sk_fold=StratifiedKFold(n_splits=100)
    model=DecisionTreeClassifier()
    mod_score4=cross_val_score(model,X_train,y_train,cv=sk_fold)
    print('STRATIFIED KFOLD score: ',np.mean(mod_score4))


def main():
    data = synset_processing("esercizio6/dataset_basic_advanced_TLN2023/")
    classifier(data)

    
if __name__ == '__main__':
   main()