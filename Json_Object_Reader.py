# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 22:22:12 2019

@author: Noman
"""




import json
from collections import namedtuple

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



class All_Data:  
    def __init__(self, raw_text, city,document_type,dates, hrg, zip_code,
                 register_type,role, money, company_name_,company_type,
                 locations, persons,company_subject, events):  
        self.raw_text = raw_text  
        self.city = city 
        self.document_type = document_type
        self.dates = dates
        self.hrg = hrg 
        self.zip_code = zip_code
        self.register_type = register_type
        
        
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




def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr
    


def list_flatten(l):
    result = list()
    for item in l:
        if isinstance(item, (list, tuple)):
            result.extend(item)
        else:
            result.append(item)
    return result




def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)

import json
with open('F:\Codes\\German_Project\\test_results.json', 'r') as file:
    all_data = json.load(file)
    print(len(all_data))
  
counting = 0
for data in all_data[0:100]:
    raw_text = ''.join(extract_element_from_json(data, ["raw_text"]))
    #print(raw_text)
    city = ''.join(extract_element_from_json(data, ["city"]))
    document_type = ''.join(extract_element_from_json(data, ["document_type"]))
    hrg = ''.join(extract_element_from_json(data, ["hrg"]))
    zip_code = ''.join(extract_element_from_json(data, ["zip_code"]))
    register_type = ''.join(extract_element_from_json(data, ["register_type"]))
    role = ''.join(extract_element_from_json(data, ["role"]))
    company_name_ = ''.join(extract_element_from_json(data, ["company_name_"]))
    company_type = ''.join(extract_element_from_json(data, ["company_type"]))
    company_subject = ''.join(extract_element_from_json(data, ["company_subject"]))
    money = extract_element_from_json(data, ["money"])

    
    
    
    #print(extract_element_from_json(data, ["locations", "street"]))
    dates = list_flatten(list_flatten(extract_element_from_json(data, ["dates"])))
    locations = list_flatten(list_flatten(extract_element_from_json(data, ["locations"])))
    persons = list_flatten(list_flatten(extract_element_from_json(data, ["persons"])))
    events = list_flatten(list_flatten(extract_element_from_json(data, ["events"])))
    #print(dates)


    Address_Data_list = []
    business_address = ""
    unknown_sentences = []
    text = raw_text
    sentencess = []
    sentences_nltk = sent_tokenize(text)
    for sen in sentences_nltk:
        if len(sen) > 25:
            sentencess.append(sen)
            if sen.find("geschäftsanschrift") != -1:
                business_address = sen
                #print("here")
            
            
    if text.find(document_type) != -1:
        si = text.find(document_type)
        #print(si)
        li = text.rfind(".")#find_nth(text, "." ,2)
       # print(li)
        address_ = text[si:li]
        business_address = address_
        #print("here1")
        
    #print(business_address) 
    
    """
    if business_address.find(company_name_) != -1:
        si = business_address.find(company_name_)
        li = find_nth(business_address, "." ,2)
        address_ = business_address[si:li]
        business_address = address_
            
    print(business_address)    
    """
    

    
    
    
    loc_found = True
    for loc in locations:
        if not loc["city"]:
            loc_found = False
            break
    


    if not loc_found:
        addresses_ = re.findall(r"\((.*?)\)",text)
        #print (addresses_)
        address = ''.join(list(filter(None, addresses_)))
        
        if business_address.find(hrg) != -1 or business_address.find(zip_code) != -1 or business_address.find(str(company_name_)) != -1:
            raw = business_address
            #print (business_address)
            raw = raw.replace("geschäftsanschrift"," ")
            data = raw.split(" ")
            role = "location"
            street = raw
            street = street.replace(zip_code, "")
            if len(data) > 0:
                street = street.replace(data[len(data)-1], "")
            
            address_obj = Address_Data(data[len(data)-1], zip_code, street, role, raw)
            Address_Data_list.append(address_obj.__dict__)
            
        elif address.find(zip_code) != -1:
            raw = address
            #print (address)
            raw = raw.replace("geschäftsanschrift"," ")
            data = raw.split(" ")
            role = "location"
            street = raw
            street = street.replace(zip_code, "")
            if len(data) > 0:
                street = street.replace(data[len(data)-1], "")
            
            address_obj = Address_Data(data[len(data)-1], zip_code, street, role, raw)
            Address_Data_list.append(address_obj.__dict__)
        else:
            print("nothing")


    #print(Address_Data_list)
     
    if len(Address_Data_list) == 0:
        for l in locations:
            address_obj = Address_Data(l["city"], l["zipcode"], l["street"], l["role"], l["raw"])
            Address_Data_list.append(address_obj.__dict__)
    
    """
            if len(address_) < 40:
                li = find_nth(address_, "." ,1)
            else:
                li = find_nth(address_, "." ,2)
            """
    """
    if len(Address_Data_list) == 0:
        print(city) 
        print(hrg)        
        print(zip_code)
        print(company_name_) 
        print(len(business_address))
        
        if len(business_address) == 0:
            print("zero")
            if raw_text.find(str(company_name_)) != -1 or raw_text.find(hrg) != -1  or raw_text.find(document_type) != -1:
                si = -1
                if raw_text.find(company_name_) != -1:
                    si = raw_text.find(company_name_)
                elif raw_text.find(hrg) != -1:
                    si = raw_text.find(hrg)
                else:
                    si = raw_text.find(document_type)
                    
                
                #li = raw_text.rfind(".")
                if raw_text.find(str("die")) != -1:
                    li = raw_text.find("die")
                else:
                    li = raw_text.rfind(".")
                    
                #print(si)
                #print(li)
                address_ = raw_text[si:li]
                print(address_)
                print(len(address_))
                if zip_code in address_ or str(company_name_) in address_:
                    si = address_.find(',')
                    li = li = find_nth(address_, "." ,2)
                    print(si)
                    print(li)
    
                address_final = address_[si:li]
                print(address_final)
                #print(address_final)
                business_address = address_final
            business_address = business_address.replace(",", "")
            business_address = business_address.replace(":", "")
            print(business_address)
        else:
            if business_address.find(str(company_name_)) != -1 or business_address.find(hrg) != -1 or  business_address.find(document_type) != -1:
                dates = list_flatten(list_flatten(extract_element_from_json(data, ["dates"])))
                date = ""
                for l in dates:
                    date = l["date"]
                business_address = business_address.replace(str(date)," ")
                raw_text = business_address
                print("\n")
                print(raw_text)
                print("\n")
                si = -1
                if raw_text.find(company_name_) != -1:
                    si = raw_text.find(company_name_)
                elif raw_text.find(hrg) != -1:
                    si = raw_text.find(hrg)
                else:
                    si = raw_text.find(document_type)
                    
                print(si)
                #li = business_address.rfind(".")
                li = find_nth(raw_text, "." ,2)
                print(li)
                address_ = business_address[si:li]
                #print(address_)
                business_address = address_
                business_address = business_address.replace(company_name_," ")
    
                
                
                raw = business_address
                #print (business_address)
                raw = raw.replace("geschäftsanschrift"," ")
    
                
                
                data = raw.split(" ")
                role = "location"
                street = raw
                street = street.replace(zip_code, "")
                if len(data) > 0:
                    street = street.replace(data[len(data)-1], "")
                
                address_obj = Address_Data(data[len(data)-1], zip_code, street, role, raw)
                Address_Data_list.append(address_obj.__dict__)
                print(Address_Data_list)
        """
    
    
    
    

    
    
    print ("Record extracted:" + str(counting))
    counting = counting + 1
    data_obj = All_Data(str(raw_text), str(city), str(document_type), dates  , str(hrg) , str(zip_code), str(register_type), str(role), str(money), str(company_name_), str(company_type),  Address_Data_list , persons ,company_subject,events)

    #data_obj = All_Data("a", "b", "",  dates_list , "g", "h", "i", "j", "k", "l" , "m", Address_Data_list , Persons_Data_list ,"p",events_changes)
    All_Data_list.append(data_obj)





import json
with open('F:\Codes\\German_Project\\test_results_layer2.json', 'w') as file:
  json.dump([ob.__dict__ for ob in All_Data_list], file,ensure_ascii=False)
print("done")
        
        













