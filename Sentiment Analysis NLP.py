
import pandas as pd
import os
import numpy as np



labels = {'pos': 1, 'neg' : 0}
df= pd.DataFrame()
for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = 'D:/DataScience/PYTHON/aclImdb_v1/aclImdb/'+ s +'/' + l 
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r', encoding = 'UTF-8') as infile:
                txt = infile.readlines()
            df = df.append([[txt, labels[l]]], ignore_index = True)
            
df.columns = ['review', 'sentiment']


np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))

df = pd.read_csv(r'D:\DataScience\PYTHON\aclImdb_v1\aclImdb\Movie_Data.csv')
df.head(3)

from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer()
docs = np.array(['the sun is shining', 
                'the weather is sweet',
                'the sun is shining and the weather is sweet'])
bag = count.fit_transform(docs)

print(count.vocabulary_) 
print(bag.toarray())

from sklearn.feature_extraction.text import TfidfTransformer
tfidf = TfidfTransformer()
np.set_printoptions(precision=2)
print(tfidf.fit_transform(count.fit_transform(docs)).toarray())

import re
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) + ''.join(emoticons).replace('-', '')
    return text


df['review'] = df['review'].apply(preprocessor)


def tokenizer(text):
    return text.split()
tokenizer('hello hi how are you doing')


from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()
def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]

import nltk
nltk.download('stopwords')


from nltk.corpus import stopwords
stop = stopwords.words('english')
print([w for w in tokenizer_porter('a runner likes running and runs as fast as possible') if w not in stop])

x_train = df.loc[:25000, 'review'].values
x_test = df.loc[25000:, 'review'].values
y_train = df.loc[:25000, 'sentiment'].values
y_test = df.loc[25000:, 'sentiment'].values


from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(strip_accents = None, lowercase = False, preprocessor = False)
lr = LogisticRegression(random_state = 0)
param_grid = [{'vect__ngram_range': [(1,1)],
              'vect__stop_words': [stop, None],
              'vect__tokenizer': [tokenizer, tokenizer_porter],
              'clf__penalty' : ['l1', 'l2'],
              'clf__c': [1.0, 10.0, 100.0]},
              
             {'vect__ngram_range': [(1,1)],
              'vect__stop_words': [stop, None],
              'vect__tokenizer': [tokenizer, tokenizer_porter],
              'vect__use_idf' : [False],
              'clf__penalty' : ['l1', 'l2'],
              'clf__c': [1.0, 10.0, 100.0]}
             ]
lr_tfidf = Pipeline([('vect', tfidf), ('clf', lr)])
gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring = 'accuracy', cv = 5, verbose = 1, n_jobs = -1)
gs_lr_tfidf.fit(x_train, y_train)

print("Best parameter set : %s " % gs_lr_tfidf.best_params_)
print('CV Accuracy : %.3f' % gs_lr_tfidf.best_score_)

clf = gs_lr_tfidf.best_estimator_
print('Test Accuracy : %.3f ' % clf.score(x_test, y_test))
