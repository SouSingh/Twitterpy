import pandas as pd
import re

df = pd.read_csv('Twitter.csv',encoding='latin-1')
df.rename(columns={'Mon Apr 06 22:19:45 PDT 2009': 'DOT', '_TheSpecialOne_': 'User', '0':'Review'}, inplace=True)
df.drop(['1467810369'], axis=1, inplace=True)

df['Review']
df['Review'] = df['Review'].replace(4,1)


df.columns = ['Review','DOT','Query','User','Tweets']
df.drop(['Query'],axis=1, inplace=True)

data = df.drop(['DOT','User'], axis='columns')
data_pos = data[data['Review'] == 1]
data_neg = data[data['Review'] == 0]

data_pos = data_pos.iloc[:int(20000)]
data_neg = data_neg.iloc[:int(20000)]

dataset = pd.concat([data_pos, data_neg])
dataset['Tweets']=dataset['Tweets'].str.lower()

stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
             'and','any','are', 'as', 'at', 'be', 'because', 'been', 'before',
             'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do',
             'does', 'doing', 'down', 'during', 'each','few', 'for', 'from',
             'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
             'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
             'into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
             'me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once',
             'only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such',
             't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
             'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
             'through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was',
             'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom',
             'why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre",
             "youve", 'your', 'yours', 'yourself', 'yourselves','@']

import string
english_punctuations = string.punctuation
punctuations_list = english_punctuations
def cleaning_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)
dataset['Tweets']= dataset['Tweets'].apply(lambda x: cleaning_punctuations(x))

def cleaning_repeating_char(text):
    return re.sub(r'(.)1+', r'1', text)
dataset['Tweets'] = dataset['Tweets'].apply(lambda x: cleaning_repeating_char(x))

def cleaning_URLs(data):
    return re.sub('((www.[^s]+)|(https?://[^s]+))',' ',data)
dataset['Tweets'] = dataset['Tweets'].apply(lambda x: cleaning_URLs(x))

def cleaning_numbers(data):
    return re.sub('[0-9]+', '', data)
dataset['Tweets'] = dataset['Tweets'].apply(lambda x: cleaning_numbers(x))

def spiltlist(x):
    return x.split(" ")
dataset['Tweets'] = dataset['Tweets'].apply(lambda x: spiltlist(x) )

dataset['Token'] = dataset['Tweets'].agg(lambda x: ','.join(map(str, x)))

def listToString(s):
    str1 = " "
    return (str1.join(s))
dataset['Tweets'] = dataset['Tweets'].apply(lambda x: listToString(x))

datset = dataset.drop(['Review'], axis='columns')

def result(a,b,c,d):
 search_list = set([a,b,c,d])
 for i in range(0, len(datset['Tweets'])):
   t = datset['Tweets'].apply(lambda x: set.intersection(set(x.split(' ')), search_list))[i]
   if t == search_list:
        return i
        break

def ouuutpu(a,b,c,d):
    t = result(a,b,c,d)
    output = datset['Tweets'][t]
    return output