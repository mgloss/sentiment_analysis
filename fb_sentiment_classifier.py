# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:27:20 2017

@author: pmaldonado
"""

import pandas as pd 
import numpy as np

corpus = pd.read_excel("./labels/FBData.xlsx", sheetname = "Data")

corpus = corpus[corpus['web'].isin(['TmobileCz','o2cz','vodafoneCZ'])]
corpus = corpus[corpus['GOLD'].isin(['p','n',0])]

## Split randomly in training and testing
train = corpus.sample(frac=0.8)
test = corpus.loc[~corpus.index.isin(train.index)]


##########################################
## Feature extraction 
##########################################

from sklearn.feature_extraction.text import CountVectorizer

# Import custom stop words in Czech

cz_sw = pd.read_csv('cz_stop_words.txt')
my_stop_words = list(cz_sw['word']) + ["bych"]

count_vect = CountVectorizer(analyzer="word"
                             , stop_words=my_stop_words)

#count_vect = CountVectorizer(analyzer="word")



#  Different methods of counting word frequency
X_train_counts = count_vect.fit_transform(train['Text'])


## Label encoder
from sklearn.preprocessing import LabelEncoder

le  = LabelEncoder()
y_train = le.fit_transform(train['GOLD'].astype(str))


##########################################
## Training the model
##########################################


from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train_counts, y_train)

# Convert to matrix form the test data
X_test = count_vect.transform(test['Text'])
y_test = le.transform(test['GOLD'].astype(str))


y_preds = clf.predict(X_test)


from sklearn.metrics import classification_report
print(classification_report(y_test, y_preds))


##########################################
## Interpreting model results
##########################################

def print_topn(vect, clf, class_labels, n=10):
    feature_names = vect.get_feature_names()
    for i, class_label in enumerate(class_labels):
        topn= np.argsort(clf.coef_[i])[-n:]
        print("%s: %s "% (class_label,
              " ".join(feature_names[j] for j in topn)))


# Show important words
print_topn(count_vect, clf, le.classes_, n=20)        


##########################################################################
## YOUR TURN:
## 0. Filter out some words that make no sense (for instance "bych" above)    
## 1. Read your table 
## 2. Apply count_vect.transform to the column that has the comments
## 3. Score the model. You can use clf.predict on the vectorized data frame
## 4. Save the dataframe and load it back into Keboola. 
##      The resulting dataframe should have columns 
##      operator|message|sentiment.
##    To transform back the labels of the model into our labels, 
##    you can use le.inverse_transform    
##########################################################################