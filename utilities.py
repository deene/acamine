##########
# Now I need to take in the description of each entry from the json file and feed it into the WordCount class. In order to count the occurance of words in all texts, I need to create a WordCount class. This class should have a function which takes in a certain string, count the occurance of each word in that string, and add the result to the previously stored values in that class. So below is the code to make such a class.

import json
from pprint import pprint

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

json_data=open('./download/nnano-2012.json')
data = json.load(json_data)
word_count = WordCount()

split_string = ''
for entry in data:
    if entry[u'dc:description']:
        split_string = entry[u'dc:description'].replace('<p>', '').replace('</p>', '').replace(',','').replace('.','') \
                        .replace('\'','').replace('(','').replace(')','').replace('-', ' ').lower()
        word_count.append(split_string)

pprint(word_count.word_table)
