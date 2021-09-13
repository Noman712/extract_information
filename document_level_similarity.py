# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:54:12 2019

@author: Noman
"""



import pandas as pd
import spacy
from spacy.lang.de.stop_words import STOP_WORDS
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
#from translate import Translator
import re
from googletrans import Translator
translator = Translator()
import nltk
from nltk.tokenize import sent_tokenize
import re, math
from collections import Counter



def list_flatten(l):
        result = list()
        for item in l:
            if isinstance(item, (list, tuple)):
                result.extend(item)
            else:
                result.append(item)
        return result



WORD = re.compile(r'\w+')
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)




col = ["sentences"]
df_final = pd.DataFrame(columns=col)


df = pd.read_csv("F:\Codes\\German_Project\\dataset.csv", encoding = "utf-8", sep = ',')
print(df.head())

text_list  = df['info'].tolist()


text = text_list[0]
    #print(text)
    
text = text.replace("&Ouml;"," ")
text = text.replace("&nbsp;"," ");
text = text.replace(",00","")
text = text.replace("Str.","str ")
text = re.sub(r"(-?\d*\.?\d+\.?\d+)",r" \1 ", text)
    
prefix  = "([a-z])[.]"
text = re.sub(prefix,r"\g<1>. ",text)
#text = re.sub(r"(.?\d+)",r"\g<1>", text)
text = re.sub(' +', ' ', text)
text = text.lower()
text = text.strip()
raw_info = text.strip()

vector1 = text_to_vector(text)
for index, text in enumerate(text_list[0:50]):
     text = text.replace("&Ouml;"," ")
     text = text.replace("&nbsp;"," ");
     text = text.replace(",00","")
     text = text.replace("Str.","str ")
     text = re.sub(r"(-?\d*\.?\d+\.?\d+)",r" \1 ", text)
        
     prefix  = "([a-z])[.]"
     text = re.sub(prefix,r"\g<1>. ",text)
     #text = re.sub(r"(.?\d+)",r"\g<1>", text)
     text = re.sub(' +', ' ', text)
     text = text.lower()
     text = text.strip()
     raw_info = text.strip()
     vector2 = text_to_vector(text)
     cosine = get_cosine(vector1, vector2)
     print(cosine)
     if cosine == 0:
         print(index)


