import re
import pandas as pd
from collections import Counter
from random import sample

import zlib
import numpy as np
import gensim
from gensim import corpora
import math
from collections import Counter

punctuations = ['.', '…', ',', ';', ':', '!', '?', '\n', '–', '-', '_', '(', ')', "'"]

def preprocessing(text):
    for p in punctuations:
        text = text.replace(p, '')      #remove punctuation marks and new lines
    text = text.lower()                 #lower registered all letters
    text = re.sub(r'[“”"]', '', text)   #remove quotation mark in english encoding 
    text = re.sub(r'[«»"]', '', text)   #remove quotation mark in russian encoding
    text = text.replace(' ', '_')       #replace space with underline mark
    text = text.replace('__', '_')
    text = text + "E"                   #add end token to the text (all letter is lower case so E won't be misrepresented)
    return text

def ngram_letter_count(n, text):
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    total = len(ngrams)
    counter = Counter(ngrams)
    # Convert counts to frequency
    frequencies = {ng: count / total for ng, count in counter.items()}
    return frequencies, total

def to_df(frequencies, total):
    rows = []
    for gram, freq in frequencies.items():
        rows.append({'n_gram': gram, 'frequency': freq, 'total_ngrams': total * freq})
        df = pd.DataFrame(rows)
    return df

def to_file(frequencies, total, filename='ngram_freq.xlsx'):
    df = to_df(frequencies, total)
    df.to_excel(filename, index=False)
    print(f"Saved to {filename}")

def create_BOW(frequencies, total):
    bow = []
    for f in frequencies.items():
        for _ in range(0, int(f[1] * total)):
            bow.append(f[0])
    return bow

def preprocessing_wlist(text):
    for p in punctuations:
        text = text.replace(p, '')      #remove punctuation marks and new lines
    text = text.lower()                 #lower registered all letters
    text = re.sub(r'[“”"]', '', text)   #remove quotation mark in english encoding 
    text = re.sub(r'[«»"]', '', text)   #remove quotation mark in russian encoding
    text = text.replace('__', ' ')
    wlist = text.split(' ')
    wlist = list(filter(None, wlist))   #remove empty string
    return wlist

def compute_tf(corpus, dict):
    tf = {}
    for doc in corpus:
        doc_len = sum(count for _, count in doc)
        for word_id, count in doc:
            tf[dict[word_id]] = count/doc_len
        tf_df = pd.DataFrame(list(tf.items()), columns=['word', 'TF'])
    return tf_df

def compute_idf(corpus, dict):
    idf = {}
    num_docs = len(corpus)
    for doc in corpus:
        for word_id, _ in doc:
            if word_id not in idf:
                idf[word_id] = 0
            idf[word_id] += 1
    idf = {dict[word_id]: np.log(num_docs / count) for word_id, count in idf.items()}
    idf_df = pd.DataFrame(list(idf.items()), columns=['word', 'IDF'])
    return idf_df

def compute_tfidf(corpus, dict):
    tfidf = {}
    tfidf_model = gensim.models.TfidfModel(corpus, id2word=dict)
    for bow in corpus:
        for word_id, value in tfidf_model[bow]:
            tfidf[dict[word_id]] = value
    tfidf_df = pd.DataFrame(list(tfidf.items()), columns=['word', 'TFIDF'])
    return tfidf_df

def process_tfidf(tfidf, texts, threshold):
    # Get words with low tfidf score
    low_score_words = []
    for key, value in tfidf.items():
        if value < threshold:
            low_score_words.append(key)
    # Filter out words in low score list
    filtered_texts = []
    for text in texts:  
        filtered_text = text.copy()
        for word in low_score_words:
            if word in text:
                filtered_text.remove(word)
        filtered_texts.append(filtered_text)
    return filtered_texts

#compute normalized compressed distance between 2 texts. This value represent kolmogorov complexity of a text in relation to the other
def NCD(str1, str2):
    s1 = zlib.compress(str1.encode())
    s2 = zlib.compress(str2.encode())
    s3 = zlib.compress((str1 + str2).encode())
    res = (s3.__sizeof__() - min(s1.__sizeof__(), s2.__sizeof__()))/max(s1.__sizeof__(), s2.__sizeof__())
    return res

#compute entropy of each text
def compute_entropy(tf):
    entropy = 0
    values = list(tf.values())
    for value in values:
        entropy += -value*math.log2(value)
    return entropy

def compute_bow_entropy(text, size):
    bows = []
    for i in range(0, len(text), size):
            bows.append([text[i:i+size]])
    res = []
    for bow in bows:
        dic = corpora.Dictionary(bow)
        corpus = [dic.doc2bow(bow) for bow in bow]
        tf = compute_tf(corpus, dic)
        scoresTF = dict(zip(tf['word'], tf['TF']))
        res.append(compute_entropy(scoresTF))
    return res

#compute volume of recived information from 1 source by reading from the other source
#for the sake of simplicity, use positional pairing relation, every texts therefor has the same length
def compute_transinfo(text1, text2):
    total = len(text1)
    joint_pairs = list(zip(text1, text2))
    joint_counts = Counter(joint_pairs)
    count1 = Counter(text1)
    count2 = Counter(text2)
    res = 0
    for (x, y), joint_count in joint_counts.items():
        p_xy = joint_count / total
        p_x = count1[x] / total
        p_y = count2[y] / total
        res += p_xy * math.log2(p_xy / (p_x * p_y))
    return res