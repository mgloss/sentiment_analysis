
# coding: utf-8

# In[ ]:

import pandas as pd 
import numpy as np

corpus = pd.read_excel("FBData.xlsx", sheetname = "Data")


# In[255]:

# corpus = corpus[corpus['web'].isin(['TmobileCz','o2cz','vodafoneCZ'])]
corpus = corpus[corpus['GOLD'].isin(['p','n',0])]


# In[256]:

## Split randomly in training and testing
train = corpus.sample(frac=0.8)
test = corpus.loc[~corpus.index.isin(train.index)]


# In[257]:

##########################################
## Feature extraction 
##########################################

from sklearn.feature_extraction.text import CountVectorizer

# Import custom stop words in Czech

cz_sw = pd.read_csv('cz_stop_words.txt', names = ['word'])

my_stop_words = list(cz_sw['word']) + (["bych", "taky", "jo", "no", "den", "tam", "sem", "něco"])

count_vect = CountVectorizer(analyzer='word', stop_words=my_stop_words)


# In[258]:

# cz_sw = pd.read_csv('cz_stop_words.txt')
cz_sw.head(10)


# In[259]:

#  Different methods of counting word frequency
X_train_counts = count_vect.fit_transform(train['Text'])


# In[260]:

## Label encoder
from sklearn.preprocessing import LabelEncoder


# In[261]:

le  = LabelEncoder()
y_train = le.fit_transform(train['GOLD'].astype(str))


# In[262]:


##########################################
## Training the model
##########################################


from sklearn.naive_bayes import MultinomialNB


# In[263]:

clf = MultinomialNB().fit(X_train_counts, y_train)


# In[264]:

# Convert to matrix form the test data
X_test = count_vect.transform(test['Text'])
y_test = le.transform(test['GOLD'].astype(str))


# In[265]:

y_preds = clf.predict(X_test)


# In[266]:

from sklearn.metrics import classification_report
print(classification_report(y_test, y_preds))


# In[267]:

##########################################
## Interpreting model results
##########################################

def print_topn(vect, clf, class_labels, n=10):
    feature_names = vect.get_feature_names()
    for i, class_label in enumerate(class_labels):
        topn= np.argsort(clf.coef_[i])[-n:]
        print("%s: %s "% (class_label,
              " ".join(feature_names[j] for j in topn)))


# In[268]:

# Show important words
print_topn(count_vect, clf, le.classes_, n=20)


# In[271]:

o2 = pd.read_csv("Czechitas/commentsO2_clean.csv", encoding = "UTF-8", sep=';')
o2['message'] = o2['message'].fillna('a')
X_o2 = count_vect.transform(o2['message'])
o2_preds = clf.predict(X_o2)
o2['prediction'] = le.inverse_transform(o2_preds)
o2_final = pd.DataFrame(o2, columns =['operator', 'created_time', 'message', 'likes_count', 'comments_count','prediction'])
o2_final['operator'] = 'o2'


# In[272]:

tm = pd.read_csv("Czechitas/commentsTM_clean.csv", encoding = "UTF-8", sep=';')
tm['message'] = tm['message'].fillna('a')
X_tm = count_vect.transform(tm['message'])
tm_preds = clf.predict(X_tm)
tm['prediction'] = le.inverse_transform(tm_preds)
tm_final = pd.DataFrame(tm, columns =['operator', 'created_time', 'message', 'likes_count', 'comments_count','prediction'])
tm_final['operator'] = 'tm'


# In[273]:

vf = pd.read_csv("Czechitas/commentsVF_clean.csv", encoding = "UTF-8", sep=';')
vf['message'] = vf['message'].fillna('a')
X_vf = count_vect.transform(vf['message'])
vf_preds = clf.predict(X_vf)
vf['prediction'] = le.inverse_transform(vf_preds)
vf_final = pd.DataFrame(vf, columns =['operator', 'created_time', 'message', 'likes_count', 'comments_count','prediction'])
vf_final['operator'] = 'vf'


# In[280]:

sentiment = pd.concat([o2_final, tm_final, vf_final], ignore_index=True)
sentiment.head()


# In[281]:

sentiment['id'] = range(1, len(sentiment))
sentiment.to_csv('sentiment.csv', encoding='utf-8', sep=";")

