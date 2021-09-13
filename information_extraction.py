# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 09:11:28 2019

@author: Noman
"""

import pandas as pd
import spacy
from spacy.lang.de.stop_words import STOP_WORDS
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
#from translate import Translator
import re
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')




nlp = spacy.load("de_core_news_sm", parser=False)









col = ['raw_text','city', 'document_type',"document_date","published","hrg", "zip_code" ,"register_court", "information" ,"role","money"
       ,"company","company_type","address","persons_info","company_subject","event","unknown_sentences"]
df_final = pd.DataFrame(columns=col)





match_df = pd.read_csv("noman/match_data.csv", encoding = "ISO-8859-1", sep = ',')
print(match_df.head())


class All_Data:  
    def __init__(self, raw_text, city,document_type,dates, hrg, zip_code,
                 register_type, information ,role, money, company_name_,company_type,
                 locations, persons,company_subject, events):  
        self.raw_text = raw_text  
        self.city = city 
        self.document_type = document_type
        self.dates = dates
        self.hrg = hrg 
        self.zip_code = zip_code
        self.register_type = register_type
        self.information = information
        
        
        self.role = role  
        self.money = money 
        self.company_name_ = company_name_
        
        
        self.company_type = company_type  
        self.locations = locations 
        self.persons = persons
        self.company_subject = company_subject
        self.events = events
        



class Dates_Data:  
    def __init__(self, date, role):  
        self.date = date  
        self.role = role 
        
        

class Persons_Data:  
    def __init__(self, birthday, city, name, surname, role ,raw):  
        self.birthday = birthday  
        self.city = city 
        self.name = name
        self.surname = surname
        self.role = role
        self.raw = raw



class Address_Data:  
    def __init__(self, city, zipcode, street, role, raw):  
        self.city = city  
        self.zipcode = zipcode 
        self.street = street
        self.role = role
        self.raw = raw      



class Events_Data:  
    def __init__(self, event_type, new_value, raw):  
        self.event_type = event_type  
        self.new_value = new_value 
        self.raw = raw    


class Directors_Data:  
    def __init__(self, per, org, loc,birth):  
        self.per = per  
        self.org = org 
        self.loc = loc
        self.birth = birth


All_Data_list  = []

df = pd.read_csv("noman/test_file.csv", encoding = "utf-8", sep = ',')




text_list  = df['info'].tolist()




counting = 1
#for i in range(0, 100):
for i in range(0, len(text_list)):
     
    text = text_list[i]
    
    #print(text)
    #addresses 
    addresses_ = re.findall(r"\((.*?)\)",text)
    
    
    #print("Address:")
    #print(addresses_)
    #print("\n")
    
    #comp_name =  
    comp_name_ = []
    comp_name_ = re.findall(r"\. (.*?)\,",text)
    #print("company:")
    if len(comp_name_) == 0:
        #print("The company list is empty")
        print("")
    else:
        comp_name_.append("")
        #print(comp_name_[0])
    #print("\n")
    
    
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
    #print(raw_info)
    
    
    sentences_nltk = sent_tokenize(text)
    #print(sentences_nltk)
    doc =  nlp(text)
    #print(doc)
    
        
    events_changes = []
    
    doc_sent = []
    for sen in doc.sents:
        doc_sent.append(sen)
    #print(doc_sent) 
    
    #geschäftsführer == director
    #Geschäftsanschrift == business address
    #Gegenstand == subject
    
    directors_list = []
    business_address= ""
    company_subject = ""
    
    #it works perfectly...get directors data in a list then apply loop to extract directors information
    #business address is perfectly fine.
    #subject is also good.
    director_found = False
    for sen in sentences_nltk:
        sentence  = str(sen)
       # print(sentence)
        if 'geschäftsführer' in sentence:
            director_found = True
            directors_list.append(sentence)
            #print("DIRECTOR:" + sentence + "\n")
            
        if sentence.find("geschäftsanschrift") != -1:
            business_address = sentence
            #print("BUS_ADDRESS:" + sentence + "\n")
        if 'gegenstand' in sentence:
            subject = sentence
            sub = str(sentence)
            si = sentence.find('gegenstand')
            li = sentence.rfind(".")
            company_subject = sentence[si:li]
            #print("gegenstand......." + sentence[si:li])
            #print("SUBJECT:" + sentence + "\n")
            
        if 'gesetzte' in sentence:
            sub = str(sentence)
            si = sentence.find('gesetzte')
            li = sentence.rfind(".")
            company_subject = sentence[si:li]
            #print("gesetzte......." + sentence[si:li])
        if 'gesetzten' in sentence:
            sub = str(sentence)
            si = sentence.find('gesetzten')
            li = sentence.rfind(".")
            company_subject = sentence[si:li]
            #print("gesetzten......." + sentence[si:li])

                
        dir_list = []  
        for director in directors_list:
            director_data = nlp(director)   
            for word in director_data.ents:
                loc = ""
                per = ""
                org = ""
                birth = ""
                if word.label_ == "LOC":
                    #print(word.text, word.label_)
                    loc = word.text
                if word.label_ == "ORG":
                    #print(word.text, word.label_)
                    org = word.text
                if word.label_ == "PER":
                    #print(word.text, word.label_)
                    per = word.text
                    if per == "":
                        per  = loc
                par_matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
                par_matcher.add("DATE", None, nlp("01.01.1900"))
                for m_id,start,end in par_matcher(director_data):
                    #print(director_data[start:end])
                    birth = director_data[start:end]
                if per != "" and str(birth) != "":
                    dir_ = Directors_Data(per, org,loc,birth)
                    dir_list.append(dir_)
    

    if business_address.find("geschäftsanschrift") != -1:
        if business_address.find("hrb") == -1 &  business_address.find("hr") == -1:
        #print(business_address)
            si = business_address.find(':')
            li = business_address.rfind(".")
            address_ = business_address[si:li]
            business_address = address_
    else:      
        for ad in addresses_:
            add = str(ad)
            add = add.lower()
            if add != "" and 'hr' not in add:
                business_address = add
        
        
    #print(business_address)

            
    dir_info = ""            
    for obj in dir_list[:1]: 
        #print( obj.per, obj.loc, obj.org, obj.birth, sep =' ' ) 
        #dir_info = str(obj.per) + "," + str(obj.birth)
        print("")

    
    
    """
    doc_words = []
    for word in doc.sents:
        doc_words.append(word.text)
        sentence  = str(word.text)
        if 'geschäftsführer' in sentence:
            director = sentence
            print("DIRECTOR:" + sentence + "\n")
        elif 'geschäftsanschrift' in sentence:
            business_address = sentence
            print("BUS_ADDRESS:" + sentence + "\n")
        elif 'gegenstand' in sentence:
            subject = sentence
            print("SUBJECT:" + sentence + "\n")
        #   print(sentence)
    """ 
    
        
    #print(doc_words)
    
    
    data_without_stopwords = [word for word in doc if word.is_stop == False]
    #print(data_without_stopwords)
    
    #print("\n")
    data_without_punct = [word for word in doc if word.is_punct == False]
    #print(data_without_punct)
    
    #print("\n")
    data_filter = list(filter(None, data_without_punct)) # fastest
    data_filter = map(str, data_filter)
    #print(data_filter)
    
    text = ' '.join(map(str, data_filter))
    
    
    text = re.sub(r"(-?\d*\.?\d+\.?\d+)",r" \1 ", text)
    
    prefix  = "([a-z])[.]"
    text = re.sub(prefix,r"\g<1>. ",text)
    #text = re.sub(r"(.?\d+)",r"\g<1>", text)
    
    text = re.sub(' +', ' ', text)
    #print(text)
    
    #translator = Translator(from_lang='de', to_lang='en')
    #translation_text = translator.translate(text)
    #print(translation_text)
    
    #translation_text = translator.translate(text)
    #print(translation_text.text)
    
    #print("\n")
    #print("Address:")
    #print(addresses_)
    #print("\n")
    
    
    #en_nlp = spacy.load("en_core_web_lg")
    #data_english = en_nlp(text)
    
    
    #for token in data_english:
    #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #            token.shape_, token.is_alpha, token.is_stop)
    
    """
    persons_eng = []
    org_eng = []
    for word in data_english.ents:
        if word.label_ == "ORG":
            print(word.text, word.label_)
            org_eng.append(word.text)
        if word.label_ == "PERSON":
            print(word.text, word.label_)
            persons_eng.append(word.text)
    
    print("\n")
    print("ORGANIZATION:")
    print(org_eng)
    print("\n")
    
    
    print("\n")
    print("PERSONS:")
    print(persons_eng)
    print("\n")
    """
    
    data_persons = nlp(raw_info)
    #print(data_persons)
        
    
    
    person_pattern = [{'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_ALPHA': True},
           {'IS_PUNCT': True},
           {'IS_PUNCT': True},
           {'LIKE_NUM': True}]
    matcher = Matcher(nlp.vocab)
    
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
    
    
    #matcher.add("person_pattern", None, person_pattern)
    matcher.add("person1_pattern", None, person1_pattern)
    #print("Persons patterns")
    persons_list = []
    for m_id,start,end in matcher(data_persons):
        #print(data_persons[start:end])
        _person = str(data_persons[start:end])
        person_info = _person.split(",")
        person_info = list(filter(None, person_info)) # fastest
        #print(len(person_info))
        if len(person_info) == 4:
            birthday = str(person_info[3])
                   
            birthday = birthday.replace("*","")
            birthday = birthday.replace(" ","")
            birthdigits = birthday.replace(".","")
            
            if birthdigits.isdigit():
                persons_list.append(data_persons[start:end])
        
    print(len(persons_list))    
    
    
    Persons_Data_list = []
    person_info_final = []
    for person in persons_list:
        _person = str(person)
        person_info = _person.split(",")
        person_info = list(filter(None, person_info))
        #print(person_info)
        if len(person_info) == 4:
            if len(person_info) == 4:
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
            p_obj = Persons_Data(birthday,city,name,surname,role,raw)
            Persons_Data_list.append(p_obj.__dict__)
            person_info_final.append(per_list)
        
        
    #print(Persons_Data_list)
    
    
    zipcode_pattern = [{'IS_PUNCT': True},
           {'LIKE_NUM': True}]
    matcher = Matcher(nlp.vocab)
    
    matcher.add("person_pattern", None, zipcode_pattern)
    #print("Persons patterns")
    zipcode = ""
    for m_id,start,end in matcher(data_persons):
        #print(data_persons[start:end])
        zipcode_ = str(data_persons[start:end])
        zipcode_ = zipcode_.replace(",","")
        zipcode_ = zipcode_.strip()
        if len(zipcode_) == 5 and zipcode_.isdigit():
            zipcode = zipcode_
        
    #print(zipcode)    
    
 
    
    #for token in data_filter:
    #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #            token.shape_, token.is_alpha, token.is_stop)
    
    
    #pos tag...it help us to find dates, names etc...
    #for word in data_filter:
    #    print(word.text, word.pos_)
        
        
        
    #ner recognition
    #for word in data_filter.ents:
    #    print(word.text, word.label_)
    
    data_filter = nlp(text)
    persons_ = []
    person = ""
    organization = ""
    location = ""
    for word in data_filter.ents:
        if word.label_ == "LOC":
            #print(word.text, word.label_)
            location = word.text
        if word.label_ == "ORG":
            #print(word.text, word.label_)
            organization = word.text
        if word.label_ == "PER":
            persons_.append(word.text)
            person = word.text
            #print(word.text, word.label_)
    
    dir_info = "" 
           
    for obj in dir_list:
        if obj.per == "":
            obj.per = person
        if obj.org == "":
            obj.org = organization
        if obj.loc == "":
            obj.loc = location
        #print( obj.per, obj.loc, obj.org, obj.birth, sep =' ' )

        if str(obj.per).find("") != -1 and str(obj.birth).find("") != -1:
            #dir_info += str(obj.per) + "," + str(obj.birth)
            print("")
        #print("\n")
        
    #print(len(dir_list))
    for obj in dir_list:
        #print(str(obj.per))
        print("")
        #print(str(obj.birth))
        
        
    remove_index = []
    if len(dir_list) > 1:
        for index,obj in enumerate(dir_list):
            for i in range(1, len(dir_list)):
                obj1 = dir_list[i]
                if str(obj.birth) == str(obj1.birth):
                    remove_index.append(i)
                    
    remove_index = list(set(remove_index)) 
    #print(remove_index)               
    for index,obj in enumerate(dir_list):
        del dir_list[index]
    
    #print(len(dir_list))     
    dir_info_list = []
    for obj in dir_list:
        if str(obj.per) and str(obj.birth):
            dir_info_list.append(str(obj.per) + "," + str(obj.birth))
            #dir_info += str(obj.per) + "," + str(obj.birth) + ";"
            #events_changes.append("director:"  + str(obj.per) + "," + str(obj.birth))
            #events_changes.append(str(obj.per))
            #events_changes.append(str(obj.birth))
    #print("\n")
    #print(events_changes)

    #print("\nGerman Person:")       
    #print(persons_)
    
    
    
    
    
    #print("\n")
    #print("hra/hrb:")
    
    #patterns
    pr_pattern = [{'ORTH': 'pr'}, {'LIKE_NUM': True}]
    gnr_pattern = [{'ORTH': 'gnr'}, {'LIKE_NUM': True}]
    hra_pattern = [{'ORTH': 'hra'}, {'LIKE_NUM': True}]
    hrb_pattern = [{'ORTH': 'hrb'}, {'LIKE_NUM': True}]
    vr_pattern = [{'ORTH': 'vr'}, {'LIKE_NUM': True}]
    #date_pat = [{'LIKE_NUM': True}]
    
    matcher = Matcher(nlp.vocab)
    matcher.add("hra_pat", None, hra_pattern)
    matcher.add("hrb_pat", None, hrb_pattern)
    matcher.add("vr_pat", None, vr_pattern)
    matcher.add("gnr_pat", None, gnr_pattern)
    matcher.add("pr_pat", None, pr_pattern)
    hrab = []
    for m_id,start,end in matcher(data_filter):
        #print(data_filter[start:end])
        hrab.append(data_filter[start:end])
    
    
    if len(hrab) == 0:
        #print("The hrab list is empty")
        hrab.append("")    
    else:
        business_address.replace(str(hrab[0]), " ")
    
    if len(hrab) > 1:
       #print("The hrab list is empty")
        #events_changes.append("location cahnges, value:"  + str(hrab[1]) + ";")
        eo = Events_Data("location_changed:", str(hrab[1]),"")
        #events_changes.append("location_changed:" + str(hrab[1]))
        events_changes.append(eo.__dict__)
    #print("\n")
    
    
    #organization
    #pattern = [{'IS_ASCII': True},{'ORTH': 'GmbH'}]
    #pattern = [{'OP': '*'},{'ORTH': 'oHG'}]
    #pattern = [{'OP': '*'},{'ORTH': 'GmbH'}]
    
    

           
    
    
    #Neueintragungen 16.10.2006 AM design OHG, Murrhardt 
    #cut characters (Neueintragungen 16.10.2006) based on their length...
    #then pick data until comma, or colon or bracket 
    #this is your company name
    
    #print("\n")
    #print("Company Type:")
    company_type = []
    ohg_pattern = [{'OP': '?'},{'ORTH': 'ohg'}]
    gmbh_pattern = [{'OP': '?'},{'ORTH': 'gmbh'}]
    matcher = Matcher(nlp.vocab)
    
    matcher.add("oHG_pat", None, ohg_pattern)
    matcher.add("GmbH_pat", None, gmbh_pattern)
    
    for m_id,start,end in matcher(data_filter):
        #print(data_filter[start:end])
        company_type.append(data_filter[start:end])
    
    if len(company_type) == 0:
        #print("The company_type list is empty")
        company_type.append(organization)
    
    #print("\n")
    
    
    #company type
    
    #print("\n")
    #print("Register Court:")
    
    data_filter_new = nlp(text[0:150])
    
    register_type = ""
    reg_star_pattern = [{'ORTH': 'regisstaramtsgericht'},{'IS_ALPHA': True}]    
    reg_star2_pattern = [{'ORTH': 'amtsgericht'},{'IS_ALPHA': True}]
    reg_star3_pattern = [{'ORTH': 'amtsgericht'},{'OP': '?'}]
    matcher = Matcher(nlp.vocab)
    
    matcher.add("REGSTAR_pat", None, reg_star_pattern)
    #matcher.add("REGSTAR1_pat", None, reg_star1_pattern)
    matcher.add("REGSTAR2_pat", None, reg_star2_pattern)
    matcher.add("REGSTAR3_pat", None, reg_star3_pattern)
    
    for m_id,start,end in matcher(data_filter_new):
        #print(data_filter[start:end])
        register_type = str(data_filter_new[start:end])
        
    
    register_type = register_type.replace("amtsgericht","")
    #print(register_type)
    #print("\n")
    
    
    
    
    
    #money
    #print("\n")
    #print("Money:")
    money_ = []
    moneyeur_pattern = [{'LIKE_NUM': True}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': 'eur'}]
    moneyeur1_pattern = [ {'LIKE_NUM': True}, {'ORTH': 'eur'}]
    money_gbp_pattern = [{'LIKE_NUM': True}, {'IS_PUNCT': True}, {'LIKE_NUM': True}, {'ORTH': 'gbp'}]
    
    matcher = Matcher(nlp.vocab)
    matcher.add("EUR_pat", None, moneyeur_pattern)
    matcher.add("EUR1_pat", None, moneyeur1_pattern)
    matcher.add("GBP_pat", None, money_gbp_pattern)
    
    for m_id,start,end in matcher(data_filter):
        #print(data_filter[start:end])
        money_.append(str(data_filter[start:end]))
        
    if len(money_) == 0:
        #print("The money_ list is empty")
        money_.append("") 
    #print("\n")
    
    #role and role type
    #pattern = [{'OP': '?'},{'ORTH': 'director'},{'OP': '?'}]
    #print("\n")
    #print("Role:")
    roles = []
    role_pattern = [{'OP': '?'},{'ORTH': 'geschäftsführer'},{'OP': '?'}]
    matcher = Matcher(nlp.vocab)
    matcher.add("Role_pat_dir", None, role_pattern)
    
    for m_id,start,end in matcher(data_filter):
        #print(data_filter[start:end])
        roles.append(data_filter[start:end])
        
    if len(roles) == 0:
        #print("The roles list is empty")
        roles.append("")
    #print("\n")
    
    
    
    
    #dates found
    dates_ = []
    par_matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
    par_matcher.add("DATE", None, nlp("01.01.1900"))
    for m_id,start,end in par_matcher(data_filter):
        dates_.append(data_filter[start:end])
        #print(data_filter[start:end])
    
    #print("Dates:")
    #print(dates_)   
    
    if len(dates_) == 0:
        #print("The dates_ list is empty")
        dates_.append("00.00.0000")
    
   # print("\n")    
    
    
    #zipcode found
    codes_ = []  
    par_matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
    par_matcher.add("POSTCODE", None, nlp("00000"))
    for m_id,start,end in par_matcher(data_filter):
        codes_.append(data_filter[start:end])
        #print(data_filter[start:end])
    
    codes_ = map(str, codes_)
    post_code = "" 
    for c in codes_:
        if len(c) == 5:
            post_code = c
             
    #print("zip code:"+ post_code)
    #print("\n")
    
    
    #events found
    eventsdf = match_df[pd.notnull(match_df['events'])]    
    terms = eventsdf.events.tolist()
    terms = list(map(str, terms))
    terms = [x.lower() for x in terms]
    #print(terms)
    # Only run nlp.make_doc to speed things up
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("Events_List", None, *patterns)
    
    doc = nlp(text)
    
    
    events_ = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        events_.append(span)
        #print(span.text)

    if len(events_) == 0:
        #print("The events_ list is empty")
        events_.append("")  
        
    #print("Events:")      
    #print(events_[0])
    #print("\n")
    
    
    
    
    #print(business_address) 
    ba_length = business_address.split(' ')
    #print(len(ba_length))
    if business_address == "" or len(ba_length) < 4 or business_address.find("ffentliche") != -1 :
        for sen in sentences_nltk:
            sentence  = str(sen)
            #print(sentence)
            if sentence.find(str(events_[0])) != -1:
                #print(sentence)
                si = sentence.find(',')
                li = sentence.rfind(".")
                address_ = sentence[si:li]
                business_address = address_
    business_address = business_address.replace(",", "")
    business_address = business_address.replace(":", "")
    #print(business_address)
 
    
    
    
    
        
    #information found        
    informationdf = match_df[pd.notnull(match_df['information'])]    
    terms = informationdf.information.tolist()
    terms = list(map(str, terms))
    #terms = [x.lower() for x in terms]
    information_names = []
    for x in terms:
        x = x.lower()
        x = x.split()
        information_names.append(x[0])
    #print(cities_names[0:5])
    
    #print(terms)
    # Only run nlp.make_doc to speed things up
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in information_names]
    matcher.add("Information_Names", None, *patterns)
    
    doc = nlp(text)
    
    #print("Cities:")
    informations_ = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        len_of_city = len(str(span))
        if len_of_city > 2:
            informations_.append(doc[start:end])
        #print(span.text)
    informations_ = list(map(str, informations_))
    informations_unique = list(set(informations_))
    #print(cities_unique)
    
    if len(informations_unique) == 0:
        #print("The cities_unique list is empty")
        informations_unique.append("")
    
    #print("\n")
    
    
    
    
    
    
    #city found        
    citiesdf = match_df[pd.notnull(match_df['cities'])]    
    terms = citiesdf.cities.tolist()
    terms = list(map(str, terms))
    #terms = [x.lower() for x in terms]
    cities_names = []
    for x in terms:
        x = x.lower()
        x = x.split()
        cities_names.append(x[0])
    #print(cities_names[0:5])
    
    #print(terms)
    # Only run nlp.make_doc to speed things up
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in cities_names]
    matcher.add("Cities_List", None, *patterns)
    
    doc = nlp(text)
    
    #print("Cities:")
    cities_ = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        len_of_city = len(str(span))
        if len_of_city > 2:
            cities_.append(doc[start:end])
        #print(span.text)
    cities_ = list(map(str, cities_))
    cities_unique = list(set(cities_))
    #print(cities_unique)
    
    if len(cities_unique) == 0:
        #print("The cities_unique list is empty")
        cities_unique.append(location)
    
    #print("\n")
    
    
    #companies found        
    companiesdf = match_df[pd.notnull(match_df['company_name'])]    
    terms = companiesdf.company_name.tolist()
    terms = list(map(str, terms))
    terms = [x.lower() for x in terms]
    
    # Only run nlp.make_doc to speed things up
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(text) for text in terms]
    #print(patterns)
    matcher.add("Companies_List", None, *patterns)
    
    #print("Companies:")
    companies_ = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        companies_.append(span)
        #print(span.text)
    #print("\n")
    
    
    
    similar_word = nlp(text)
    for word in similar_word.sents:
        if(word and word.vector_norm):
          for token in patterns:
            if(token and token.vector_norm):
                if  token.similarity(word) >= 0.9:
                    #print(str(word.text))
                    if len(company_type) == 0:
                        company_type.append(word.text)  
                        if len(company_type) == 0:
                            company_type.append("")  
                    break
                    #print(str(word.text) + ":" + str(token.text) + ":" + str(token.similarity(word)))
    
    
    company_name_ = ""
    
    for sen in sentences_nltk:
        sentence  = str(sen)
       # print(sentence)
        if str(dates_[1]) in sentence and str(events_[0]) in sentence:
            sub = str(sentence)
            #print(sub)
            si = sub.find(str(events_[0]))
            li = sub.find(",")
            subject = sub[si:li]
            
            subject = subject.replace(str(dates_[1]),"")
            subject = subject.replace(str(events_[0]),"")
            #print(subject)
            if str(hrab[0]) in subject:
                subject = subject.replace(str(hrab[0]),"")
            
            subject= subject.strip()
            company_name_= subject
            
    company_type = ""
    companiesdf = match_df[pd.notnull(match_df['company_name'])]    
    terms = companiesdf.company_name.tolist()
    terms = list(map(str, terms))
    terms = [x.lower() for x in terms]
    
    for term in terms:
        if term in company_name_:
            company_type = term
    
    
    
    if len(money_) > 1:
        for money in money_[1:]:
            md = str(money)
            event_type = "new kapital"
            
            raw = "price"
            
            money_data = [event_type,md,raw] 
            eo = Events_Data(event_type,md,raw)
            events_changes.append(eo.__dict__)
            #events_changes.append(money_data)
     
        
    loc_found = True
    Address_Data_list = []
    location_info = []
    if zipcode in business_address and cities_unique[0] in business_address:
        raw = business_address
        raw = raw.replace("geschäftsanschrift"," ")
        data = raw.split(" ")
        role = "location"
        street = raw
        street = street.replace(zipcode, "")
        if len(data) > 0:
            street = street.replace(data[len(data)-1], "")
        
        #location_ = [cities_unique[0], zipcode, street, role, raw]
        location_ = [data[len(data)-1], zipcode, street, role, raw]
        address_obj = Address_Data(data[len(data)-1], zipcode, street, role, raw)
        Address_Data_list.append(address_obj.__dict__)
        location_info.append(location_)
        
    elif zipcode in business_address or str(events_[0]) in business_address or str(hrab[0]) in business_address:
        raw = business_address
        role = "location"
        raw = raw.replace("geschäftsanschrift"," ")
        data = raw.split(" ")
        street = raw
        street = street.replace(zipcode, "")
        if len(data) > 0:
            street = street.replace(data[len(data)-1], "")
        street = street.replace(register_type, "")
        street = street.replace("geschäftsanschrift", "")
        
        
        location_ = [data[len(data)-1], zipcode, street, role, raw]
        address_obj = Address_Data(data[len(data)-1], zipcode, street, role, raw)
        Address_Data_list.append(address_obj.__dict__)
        location_info.append(location_)
    else:
        #business_address = ""
        loc_found = False
        location_info.append("")
        address_obj = Address_Data("", "", "", "", "")
        Address_Data_list.append(address_obj.__dict__)
        #location_info.append(business_address)
    
    
    #print(Address_Data_list)
    
    
    
    
    
    if not loc_found:
        addresses_ = re.findall(r"\((.*?)\)",text)
        #print (addresses_)
        address = ''.join(list(filter(None, addresses_)))
        
        if business_address.find(str(hrab[0])) != -1 or business_address.find(zipcode) != -1 or business_address.find(str(events_[0])) != -1:
            raw = business_address
            #print (business_address)
            raw = raw.replace("geschäftsanschrift"," ")
            data = raw.split(" ")
            role = "location"
            street = raw
            street = street.replace(zipcode, "")
            if len(data) > 0:
                street = street.replace(data[len(data)-1], "")
            
            address_obj = Address_Data(data[len(data)-1], zipcode, street, role, raw)
            Address_Data_list.append(address_obj.__dict__)
            
        elif address.find(zipcode) != -1:
            raw = address
            #print (address)
            raw = raw.replace("geschäftsanschrift"," ")
            data = raw.split(" ")
            role = "location"
            street = raw
            street = street.replace(zipcode, "")
            if len(data) > 0:
                street = street.replace(data[len(data)-1], "")
            
            address_obj = Address_Data(data[len(data)-1], zipcode, street, role, raw)
            Address_Data_list.append(address_obj.__dict__)
        else:
            print("")
            #print("nothing")


    #print(Address_Data_list)
        
    
    
    
    
    
    if len(person_info_final) > 1:
        for person in persons_list[1:]:
            _person = str(person)
            person_info = _person.split(",")
            person_info = list(filter(None, person_info))
            #print(person_info)
            if len(person_info) == 4:
                birthday = str(person_info[3])
                birthday = birthday.replace("*","")
                birthday = birthday.strip()
                #print(birthday)
            
                city = str(person_info[2])
                
                name = str(person_info[1])
                
                surname = str(person_info[0])
                
                event_type = "director"
                
                raw = "director"
                person_data = str([event_type,name,surname,birthday,raw])
                eo = Events_Data(event_type, person_data, raw)              
                #events_changes.append(person_data)
                events_changes.append(eo.__dict__)
    
    
    #print(events_changes)    

            
    #events_str = ','.join(events_changes)
    #print(events_str)
    money_str = ','.join(money_)
    
    dc = str(dates_[1])
    dp = str(dates_[0])
    
    dates_list = []
    do = Dates_Data(dc,"document created")
    do1 = Dates_Data(dp,"document published")
    dates_list.append(do.__dict__)
    dates_list.append(do1.__dict__)


    
    print ("Record extracted:" + str(counting))
    counting = counting + 1
    #df_final = df_final.append({'raw_text':raw_info,'city':cities_unique[0] , 'document_type': events_[0]
    #                            ,'document_date': dates_[1],'published': dates_[0],'hrg': hrab[0], 'zip_code': zipcode, 'register_court': register_type,'role': roles[0]
    #                            ,'money': money_str,'company': organization,'company_type': company_type[0],'address': business_address
    #                            , 'persons_info': dir_info_list,'company_subject': subject,'event': events_str,'unknown_sentences': ""}, ignore_index=True)

    data_obj = All_Data(str(raw_info), str(register_type), str(events_[0]), dates_list  , str(hrab[0]) , str(zipcode), str(register_type), str(informations_unique) ,str(roles[0]), str(money_str), str(company_name_), str(company_type),  Address_Data_list , Persons_Data_list ,company_subject,events_changes)

    #data_obj = All_Data("a", "b", "",  dates_list , "g", "h", "i", "j", "k", "l" , "m", Address_Data_list , Persons_Data_list ,"p",events_changes)
    All_Data_list.append(data_obj)





import json
with open('noman/test_results.json', 'w') as file:
  json.dump([ob.__dict__ for ob in All_Data_list], file,ensure_ascii=False)
print("done")

"""    
    df_final = df_final.append({'raw_text':raw_info,'city':cities_unique[0] , 'document_type': events_[0]
                                ,'document_date': dates_[1],'published': dates_[0],'hrg': hrab[0], 'zip_code': zipcode, 'register_court': register_type,'role': roles[0]
                                ,'money': money_str,'company': company_name_,'company_type': company_type,'address': location_info
                                , 'persons_info': person_info_final,'company_subject': company_subject,'event': events_changes,'unknown_sentences': ""}, ignore_index=True)
    
    
pd.set_option('display.max_rows', 10)  
pd.set_option('display.max_columns', 12)          
print(df_final.sample())

import csv
export_csv = df_final.to_csv (r'F:\Codes\\German_Project\\test_results.csv', encoding='cp1252', header=True) #Don't forget to add '.csv' at the end of the path
#export_csv = df_final.to_csv (r'F:\Codes\\German_Project\\test_results.csv', encoding='utf-8', header=True) #Don't forget to add '.csv' at the end of the path
#export_csv = df_final.to_csv (r'F:\Codes\\German_Project\\test_results.csv', encoding='ISO-8859-1', sep = ',', header=True) #Don't forget to add '.csv' at the end of the path


import csv
import json

with open('F:\Codes\\German_Project\\test_results.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open('F:\Codes\\German_Project\\test_results.json', 'w') as f:
    json.dump(rows, f,ensure_ascii=False)

"""

