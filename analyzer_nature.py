import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import natureProductCodes
from bs4 import BeautifulSoup
import requests

record = {}
articleLinks = []
for year in range(2006,2015):
    record[year] = {}
    for journalName, code in natureProductCodes.natureProductCodes.items():
        if code != "":
            fileName = './previousDownload/' + code + '-' + str(year) + '.json'

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
print df.sort(column='total', ascending=False)

r = requests.get('http://dx.doi.org/10.1038/nnano.2013.286')
soup = BeautifulSoup(r.text)
print soup.find_all('ol', 'affiliations','af-section')
