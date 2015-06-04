##########
# Now I need to take in the description of each entry from the json file and feed it into the WordCount class. In order to count the occurance of words in all texts, I need to create a WordCount class. This class should have a function which takes in a certain string, count the occurance of each word in that string, and add the result to the previously stored values in that class. So below is the code to make such a class.

import json
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import natureProductCodes


class WordCount:
    """A simple word count class"""
    def __init__(self):
        self.word_table = {}
        self.msg = ''
        self.ignore_list = {}
        self.ignore_list = ('of', 'the', 'a', 'to', 'and', 'in', 'be', 'as', \
                            'that', 'this', 'can', 'for', 'have', 'is', 'with', \
                            'by', 'are', 'used', 'such', 'on', 'it', 'at', 'from', \
                            'high', 'has', 'an', 'which', '(', ')', ',', 'made', 'its', \
                            'new', '2013', '.', 'two', '-', 'researchers', 'been', 'or', \
                            'using', 'state', '\-', 'not')

    def append(self, string):
        # print 'Analyzing...'
        new_word_array = split_string.split()

        for aword in new_word_array:
            # ignore the normal words
            if aword in self.ignore_list:
                continue
            if aword in self.word_table:
                # if the word exists, add 1
                self.word_table[aword] = self.word_table[aword] + 1
            else:
                # if the word does not exist, init the key with 1
                self.word_table[aword] = 1

        return self.msg

def nature_get_author_address():
    r = requests.get('http://dx.doi.org/10.1038/nnano.2013.286')
    soup = BeautifulSoup(r.text)
    print soup.find_all('ol', 'affiliations','af-section')

def clean_description(desciption_text):
    """ This method cleans the desciption text, remove all unneccesary symbols, make word lower case """
    cleaned_text = desciption_text.replace('<p>', '').replace('</p>', '').replace(',','').replace('.','') \
                    .replace('\'','').replace('(','').replace(')','').replace('-', ' ').lower()
    return cleaned_text

if __name__ == "__main__":
### count the words ###
    json_data=open('./nnano-2010.json')
    data = json.load(json_data)
    word_count = WordCount()

    split_string = ''
    for entry in data:
        if entry[u'dc:description']:
            split_string = clean_description(entry[u'dc:description'])
            word_count.append(split_string)

    pprint(word_count.word_table)

### get the address ###

    nature_get_author_address()

### Get the authors ###
    record = {}
    articleLinks = []
    for year in range(2006,2015):
        record[year] = {}
        for journalName, code in natureProductCodes.natureProductCodes.items():
            if code != "":
                fileName = './' + code + '-' + str(year) + '.json'

                if os.path.isfile(fileName):
                    json_data=open(fileName)
                    data = json.load(json_data)

                    for entry in data:
                        if not entry['dc:creator']:
                            continue
                        if entry["prism:genre"] != 'Research':
                            continue

                        for author in entry['dc:creator']:
                            author = author.replace('  ', ' ')
                            if not author in record[year].keys():
                                record[year][author] = 1
                            else:
                                record[year][author] = record[year][author] + 1

                        articleLinks.append(entry['link'])

    print articleLinks

    df = pd.DataFrame(record)
    df['total'] = df.sum(axis=1)
    # print df.sort(column='total', ascending=False)
