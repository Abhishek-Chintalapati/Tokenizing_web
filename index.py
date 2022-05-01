from fileinput import filename
from pdb import Pdb
from bs4 import BeautifulSoup
from matplotlib.font_manager import json_dump
from nltk import word_tokenize
import sys
import os
import json
import time
import matplotlib.pyplot as plt
from collections import defaultdict

STOP_WORDS_LIST = []
LINKED_LIST = {} #defaultdict(lambda: defaultdict(dict))
TEMP = {}
WORDS_COUNT = {}
WORDS_ONCE = {}
N_GRAM_LIST = {}
N_GRAM_COUNT = {}
TDM = {}
DICT_FILE = {}
COUNT = 0 

def read_each_file(file_directory_path, dest_dir):
    """
    Function takes input as html files from directory path and destination directoy where HTML files have to  parsed. It reads each file from the directory path

    """
    count = 0
    for filename in os.listdir(file_directory_path):
        start_time = time.time()
        with open(os.path.join(file_directory_path, filename), errors="ignore") as content:
            data = content.read()
            count +=  1
            write_each_file(data, count, dest_dir, filename, start_time)
            #write_n_gram(data, dest_dir,filename, count)
    END_TIME = time.time()
    temp_dict = {}
    for index, filename in enumerate(os.listdir(file_directory_path)):
        temp_dictn = final_hash_table(dest_dir, filename, index+1, END_TIME, temp_dict)

    #for index,filename in enumerate(os.listdir(file_directory_path)):
    temp_dict = {}
    posting_file(filename)
    temp_dictn = dict_file(temp_dict)
    # for index, filename in enumerate(os.listdir(file_directory_path)):
    #     final_n_gram_table(dest_dir, filename, index+1)

    # bm25('international', k = 1.2, b = 0.75)

    #aggregate_json_files(hash_tab, dest_dir)
    #computations_plot(temp_dictn)



def write_each_file(data, count, dest_dir, filename, start_time):
    """
    Function takes data of each file as argument, count is for number of files which is used for plot. This would write by creating a new file and writing the structured tokens. It would return the tokens list and a dictonary containin keys as file numbers and values as time taken to generate files

    """
    tokens_list = []
    temp_dict = {}
    soap_text = BeautifulSoup(data, 'html.parser').get_text()
    tokens = word_tokenize(soap_text)                                                                                                                                           
    for token in tokens:
        if token not in STOP_WORDS_LIST :
            token_x = token.strip("|").lower()
            final_token = ''.join(filter(str.isalpha, token_x))
            if final_token and len(final_token) > 1:
                tokens_list.append(final_token)
                end_time = time.time()
    WORDS_COUNT[count] = len(tokens_list)
    hash_table_insert(tokens_list, count)  



                                                                   
def hash_table_insert(tokens_list, count):    
    """ 
    creation of hash table for all the tokens with values as frequency 

    """
    for token in tokens_list:
        if token not in LINKED_LIST:
            LINKED_LIST.setdefault(token, {})
        
        if token in LINKED_LIST and count not in LINKED_LIST[token]:
            LINKED_LIST[token][count]  = tokens_list.count(token)


def final_hash_table(dest_dir, filename, file_number, END_TIME, temp_dict):
#with open(os.path.join(dest_dir, filename.replace("html", "wts")),'w') as new_file:
    temp =  {}
    start_time = time.time()
    for token in LINKED_LIST.keys() :
        #values_sum = sum(d.get(file_number, 0) for d in LINKED_LIST.values() if d)
        if file_number in LINKED_LIST[token]:
            tf = LINKED_LIST[token][file_number] / WORDS_COUNT[file_number]
            token_count = len(LINKED_LIST[token])
            idf = 1/ token_count
            ans = tf * idf 
            temp [token] = ans
            if token not in TDM:
                TDM.setdefault(token, {})
            if token in TDM and file_number not in TDM[token]:
                TDM[token][file_number]  = ans
        
    end_time = time.time()
    final_time = end_time - start_time
    if file_number == 1 :
        temp_dict[file_number] = end_time
    temp_dict [file_number] = final_time
    #json.dump(temp, new_file, indent=4)
    #return temp_dict


def posting_file(filename):
    with open(os.path.join(dest_dir, "postings_file.txt"), 'w') as new_file:
        for token in TDM.keys():
            for numbers in TDM[token].keys():
                if TDM[token][numbers]!= None :
                   new_file.write(str(numbers) + "," + str(TDM[token][numbers]))
                   new_file.write('\n')


def dict_file(temp_dict):
    count = 0 
    start_time = time.time()
    with open(os.path.join(dest_dir, "dict_file.txt"), 'w') as new_file:
        i = 0
        for token in TDM.keys():
            if token not in DICT_FILE:
                DICT_FILE.setdefault(token,[])
            if token in DICT_FILE :
                i = i+1
                DICT_FILE [token].append(len(TDM[token].keys()))
                if i == 1:
                    c = list(TDM[token].keys())[0]
                    DICT_FILE[token].append(c)
                    count = count + len(TDM[token].keys()) 
                else:
                    DICT_FILE[token].append(count +1)
                    count = count + len(TDM[token].keys())   
                    end_time = time.time()  
                    final_time = end_time - start_time
                    if i == 1 :
                        temp_dict[1] = end_time
                    if i == 10000 or 50000 or 100000 or 200000 or 300000:
                        temp_dict [i] = final_time
                    #json.dump(temp, new_file, indent=4)
        json.dump(DICT_FILE, new_file, indent=4)
    return temp_dict



            





 def bm25(word, k=1.2, b=0.75):
     # term frequency...
     avgdl = sum((WORDS_COUNT[i]) for i in WORDS_COUNT) / 503
     N = 503
     temp = {}
     with open(os.path.join(dest_dir, "bm25.json" ), 'w') as file_name:
         for i, d in enumerate(WORDS_COUNT):
             if i+1 in LINKED_LIST[word]:
                 freq = LINKED_LIST[word][i+1]  # or f(q,D) - freq of query in Doc
                 tf = (freq * (k + 1)) / (freq + k * (1 - b + b * WORDS_COUNT[i+1] / avgdl))
                 # inverse document frequency...
                 N_q = len(LINKED_LIST[word])  # number of docs that contain the word
                 idf = ((N - N_q + 0.5) / (N_q + 0.5)) + 1
                 temp[i+1] = round(tf*idf, 4)
             else :
                 continue
         json.dump(temp,file_name, indent=4) 

 def final_n_gram_table(dest_dir, filename, file_number):
     with open(os.path.join(dest_dir, filename.replace("html", "ngram")),'w') as new_file:
         temp =  {}
         for token in N_GRAM_LIST.keys() :
             #values_sum = sum(d.get(file_number, 0) for d in LINKED_LIST.values() if d)
             if file_number in N_GRAM_LIST[token]:
                 tf = N_GRAM_LIST[token][file_number] / N_GRAM_COUNT[file_number]
                 token_count = len(N_GRAM_LIST[token])
                 idf = 1/ token_count
                 ans = tf * idf 
                 temp [token] = ans
         json.dump(temp, new_file, indent=4)



 def aggregate_json_files(hash_tab, dest_dir):
     """
     sorting these hash tables based on keys and values

     """
     with open(os.path.join(dest_dir, "hash_tab_value_sorted.json"), 'w') as hash_tab_file:
         hashed_dict = dict(sorted(hash_tab.items(), key=lambda item: item[1], reverse=True))
         json.dump(hashed_dict, hash_tab_file, ensure_ascii=False, indent=4)
     with open(os.path.join(dest_dir, "hash_tab_key_sorted.json"), 'w') as hash_tab_file:
         hashed_dict = dict(sorted(hash_tab.items(), key=lambda item: item[0]))
         json.dump(hashed_dict, hash_tab_file, ensure_ascii=False, indent=4)



 def write_n_gram(data, dest_dir, filename, count):
     tokens_list = []
     temp_dict = {}
     soap_text = BeautifulSoup(data, 'html.parser').get_text()
     tokens = word_tokenize(soap_text)                                                                                                                                                   
     tokens_list = []
     s = []
     for token in tokens:
         s = [tokens_list.append(token[i:i+3]) for i in range(len(token)-3+1)]
     N_GRAM_COUNT[count] = len(tokens_list)
     n_gram_hash(tokens_list, count)


 def n_gram_hash(tokens_list, count) :
     for token in tokens_list:
         if token not in N_GRAM_LIST:
             N_GRAM_LIST.setdefault(token, {})
       
         if token in N_GRAM_LIST and count not in N_GRAM_LIST[token]:
             N_GRAM_LIST[token][count]  = tokens_list.count(token)



 def computations_plot(temp_dict):
     """
   
     plots for analysis of time taken for compuations and aggregations of those files

     """


     fig,ax = plt.subplots(figsize=(6,6))
     files = list(temp_dict.keys())
     times = list(temp_dict.values())
     files = [100, 200, 300, 400, 500]
     ax.plot(files,times)
     ax.xaxis.set_major_locator(plt.MaxNLocator(10))
     plt.xticks(rotation=30)
     ax.set_xlabel("Each File Number")
     ax.set_ylabel("Size in KB for total files")
     ax.set_title("Size for creation of postings + Dict files")
     plt.show()
   
     agg_time = []
     curr_time = 0
     for time in times:
         curr_time = curr_time + time
         agg_time.append(curr_time)
     fig,ax2 = plt.subplots(figsize=(6,6))
     ax2.plot(files,agg_time)
     ax2.xaxis.set_major_locator(plt.MaxNLocator(15))
     plt.xticks(rotation=30)
     ax2.set_xlabel("Files")
     ax2.set_ylabel("Time for files")
     ax2.set_title("Aggregation time")
     plt.show()

 plt.title("Probability of tokens VS Rank ")
 plt.ylabel("Probability of token")
 plt.xlabel("Rank of words")
 rank_list = []
 value_list = []
 sum_values =  sum(WORDS_COUNT.values())
 for rank, value in enumerate(WORDS_ONCE) : 
     rank_list.append(rank + 1)
     value_list.append(WORDS_ONCE[value] / sum_values )
 plt.loglog(
     rank_list,
     value_list        
 )
 plt.show()



if __name__ == "__main__":
    path = os.getcwd()
    file_directory_path = path + "\\Stop_words.txt"
    f = open(file_directory_path, "r")
    STOP_WORDS_LIST = f.read().splitlines()
    f.close()
    # file_path = path + "\\hash_tab_value_sorted.txt"
    # f = open(file_path, "r")
    # WORDS_ONCE = json.loads(f.read())
    # f.close()
    file_directory_path = sys.argv[1]
    dest_dir = sys.argv[2]
    read_each_file(file_directory_path, dest_dir)
    print(TDM)


  
