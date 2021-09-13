# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 17:09:44 2019

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




#nlp = spacy.load("de_core_news_md")



text = "ffentliche bekanntmachung regisstar amtsgericht stuttgart aktenzeichen: hrb 213459 bekannt gemacht am: 04.06.2007 07 : 50 uhr \ndie in () gesetzten angaben der geschäftsanschrift und des unternehmensgegenstandes erfolgen ohne gewähr. \nlöschungen\n 31.05.2007 pro optik augenoptik-fachgeschäft gmbh, plochingen (zehntgasse 1, 73207 plochingen). die gesellschaft (übertragender rechtsträger) hat ihr vermögen unter auflösung ohne abwicklung nach maßgabe des spaltungsplans vom 22.12.2006 und des versammlungsbeschlusses vom 22.12.2006 aufgespaltet und hiervon deren fachgeschäft in plochingen mit allen aktiva und passiva auf die neu gegründete gesellschaft mit beschränkter haftung &quot;pro optik augenoptik fachgeschäft gmbh&quot;, plochingen (amtsgericht stuttgart hrb 722997 ) und gleichzeitig den teilbetrieb in ravensburg mit allen aktiva und passiva auf die neu gegründete gesellschaft mit beschränkter haftung &quot;pro optik augenoptik fachgeschäft gmbh&quot;, ravensburg (amtsgericht ulm hrb 720924 ) übertragen. auf die bei gericht eingereichten urkunden wird bezug genommen. das registerblatt ist geschlossen. als nicht eingetragen wird bekanntgemacht: den gläubigern der an der aufspaltung beteiligten rechtsträger ist, wenn sie binnen sechs monaten nach dem tag, an dem die eintragung der aufspaltung in das register des sitzes desjenigen rechtsträgers, dessen gläubiger sie sind, nach § 19 abs. 3 umwg als bekanntgemacht gilt, ihren anspruch nach grund und höhe schriftlich anmelden, sicherheit zu leisten, soweit sie nicht befriedigung verlangen können. dieses recht steht den gläubigern jedoch nur zu, wenn sie glaubhaft machen, dass durch die aufspaltung die erfüllung ihrer forderung gefährdet wird."
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

c = nlp(raw_info)
print(data_persons)
        
    
    
person_pattern = [{'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_PUNCT': True},
           {'LIKE_NUM': True}]


person2_pattern = [
        {'IS_ASCII': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'IS_ASCII': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'IS_ASCII': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'IS_ASCII': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'LIKE_NUM': True}]



person1_pattern = [
        {'IS_ALPHA': True, 'OP': '?'},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True, 'OP': '*'},
           {'IS_PUNCT': True},
           {'LIKE_NUM': True}]


    
matcher = Matcher(nlp.vocab)
    
#matcher.add("person_pattern", None, person_pattern)
matcher.add("person1_pattern", None, person1_pattern)
    #print("Persons patterns")
    
persons_list = []
for m_id,start,end in matcher(data_persons):
    #print(data_persons[start:end])
    _person = str(data_persons[start:end])
    person_info = _person.split(",")
    person_info = list(filter(None, person_info)) # fastest
    print(len(person_info))
    if len(person_info) == 4:
        birthday = str(person_info[3])
        birthday = birthday.replace("*","")
        birthday = birthday.replace(" ","")
        birthdigits = birthday.replace(".","")
        print(birthdigits)
        
        if birthdigits.isdigit():
            print("yes")
        
        persons_list.append(data_persons[start:end])
    
        
print(persons_list)    


    
Persons_Data_list = []
person_info_final = []
for person in persons_list:
    _person = str(person)
    
    person_info = _person.split(",")
    print(len(person_info))
        #print(person_info)
    if len(person_info) >= 4:
        if len(person_info) >= 4:
            birthday = str(person_info[3])
            birthday = birthday.replace("*","")
            birthday = birthday.strip()
        else:
            birthday = ""
            #print(birthday)
            
            city = str(person_info[2])
            
            name = str(person_info[1])
            
            surname = str(person_info[0])
            
            raw = str(person)
            if director_found:
                role = "director"
            else:
                role = ""
                               
                                
            per_list = [birthday,city,name,surname,role,raw] 
            Persons_Data_list.append(per_list)
            
print(Persons_Data_list)
            
            
            
            
            
            
            
            
            
 """           
 pattern = [{'ORTH': '('},
           {'IS_ASCII': True, 'OP': '*'},
           {'ORTH': ')'}]           
"""            
        