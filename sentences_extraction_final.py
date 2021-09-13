# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:58:10 2019

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




#df_results = pd.read_csv("F:\Codes\\German_Project\\test_results.csv", encoding = "cp1252", sep = ',')
df_results = pd.read_csv("F:\Codes\\German_Project\\test_results.csv", encoding = "ISO-8859-1", sep = ',')

print(df_results.shape)
print(df_results.index)


text_list  = df_results['raw_text'].tolist()
event_info = pd.Series(df_results['event'].values.tolist())

print(len(str(event_info[1])))
if len(str(event_info[1])) == 3:
    print("empty!")
else:
    print("fill")    

money_info = pd.Series(df_results['money'].values.tolist())
print(len(text_list))
#print(text_list[0])
print(df_results.iloc[0])



#for i in range(0, len(text_list)):
for i in range(0, 20):
     
    text = text_list[i]
    print(text)
    
    
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
    #print(text)
    
    sentencess = []
    sentences_nltk = sent_tokenize(text)
    for sen in sentences_nltk:
        if len(sen) > 75:
            sentencess.append(sen)
    
    unknown_sentences = []
    
    
            #print(df_results.iloc[i])
    df = df_results.iloc[i]
    

    
       
        
    for sen in sentencess:
        if str(df.city) in sen:
            print("Found!")
        elif str(df.document_type) in sen:
            print("Found!")
        elif str(df.document_date) in sen:
            print("Found!")
        elif str(df.published) in sen:
            print("Found!")
        elif str(df.hrg) in sen:
            print("Found!")
        elif str(df.register_court) in sen:
            print("Found!")
        elif str(df.role) in sen:
            print("Found!")
        elif str(df.money) in sen:
            print("Found!")
        elif str(df.company) in sen:
            print("Found!")
        elif str(df.company_type) in sen:
            print("Found!")
        elif str(df.address) in sen:
            print("Found!")
        #elif str(directors_info) in sen:
        #    print("Found!")
        elif str(df.company_subject) in sen:
            print("Found!")
        else:
            val_event = False
            val_money = False
            if len(str(event_info[i])) == 3:
                print("")
            else:
                events_list = event_info[i].split(",")
                print(events_list)
                for val in events_list:
                    if val in sen:
                        print(val)
                        print("Found event!")
                        val_event = True
                        #print(sen)
                        break
                
            if val_event:
                print("Nothing Event!")
                
            if len(str(money_info[i])) == 3:
                print("")
            else:

                if money_info[i]:
                    money_list = money_info[i].split(",")
                    for val in money_list:
                        if val in sen:
                            print("Found Money!")
                            val_money = True
                            #print(val)
                            #print(sen)
                            break
                if val_money or val_event:
                    print("Nothing Money!")


            if val_money == False and val_event == False:
                print("Sentence Added unknown!")
                unknown_sentences.append(sen)
                

    print("Unknown sentences:\n")
    print(unknown_sentences) 
        
  
    unknown_data = '|'.join(unknown_sentences)
    #df_results[i]['unknown_sentences'] = unknown_sentences
    #df_results.loc[df.index[i],'unknown_sentences'] = unknown_sentences
    df_results.ix[i,'unknown_sentences']= unknown_data
    #df_results.set_value('unknown_sentences', i, unknown_sentences)
    #df_results.loc[df_results['unknown_sentences']] = unknown_sentences




import csv
export_csv = df_results.to_csv (r'F:\Codes\\German_Project\\test_results_final.csv', encoding='ISO-8859-1', sep = ',', header=True) #Don't forget to add '.csv' at the end of the path


import csv
import json

with open('F:\Codes\\German_Project\\test_results_final.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open('F:\Codes\\German_Project\\test_results_final.json', 'w') as f:
    json.dump(rows, f,ensure_ascii=False)



