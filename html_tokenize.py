from bs4 import BeautifulSoup
from nltk import word_tokenize
import sys
import os
import json
import time
import matplotlib.pyplot as plt


def read_each_file(file_directory_path, dest_dir):
    """
    Function takes input as html files from directory path and destination directoy where HTML files have to  parsed. It reads each file from the directory path

    """
    count = 1
    for filename in os.listdir(file_directory_path):
        start_time = time.time()
        with open(os.path.join(file_directory_path, filename), errors="ignore") as content:
            data = content.read()
            temp_dict, tokens_list  = write_each_file(data, count, dest_dir, filename, start_time)
            hash_tab = hash_table_insert(tokens_list)
    aggregate_json_files(hash_tab, dest_dir)
    computations_plot(temp_dict)


def write_each_file(data, count, dest_dir, filename, start_time):
    """
    Function takes data of each file as argument, count is for number of files which is used for plot. This would write by creating a new file and writing the structured tokens. It would return the tokens list and a dictonary containin keys as file numbers and values as time taken to generate files

    """
    tokens_list = []
    temp_dict = {}
    with open(os.path.join(dest_dir, filename.replace("html", "txt")),'w') as new_file:
        soap_text = BeautifulSoup(data, 'html.parser').get_text()
        tokens = word_tokenize(soap_text)
        for token in tokens:
            token_x = token.strip("|").lower()
            final_token = ''.join(filter(str.isalpha, token_x))
            if final_token:
                tokens_list.append(final_token)
                new_file.write(final_token)
                new_file.write("\n")
                end_time = time.time()
                if count == 1 or 50 or 100 or 150 or 200 :
                    temp_dict[count] = end_time - start_time
                    count += 1
    return temp_dict, tokens_list


def hash_table_insert(tokens_list):    
    """ 
    creation of hash table for all the tokens with values as frequency 

    """
    hash_tab = {}
    for token in tokens_list:
        if token in hash_tab:
            hash_tab[token] += 1
        elif (token == "") :
            continue
        else :
            hash_tab[token] = 1
    return hash_tab


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
    
def computations_plot(temp_dict):
    """
    plots for analysis of time taken for compuations and aggregations of those files

    """
    fig,ax = plt.subplots(figsize=(6,6))
    files = list(temp_dict.keys())
    times = list(temp_dict.values())
    ax.plot(files,times)
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.xticks(rotation=30)
    ax.set_xlabel("Each File Number")
    ax.set_ylabel("Time for each file")
    ax.set_title("Time for parsing HTML files")
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



if __name__ == "__main__":
    file_directory_path = sys.argv[1]
    dest_dir = sys.argv[2]
    read_each_file(file_directory_path, dest_dir)


  