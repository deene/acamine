import json
import urllib2, urllib
import time
import os.path

class AgentNature:
    """
    Common base class for all journal downloads
    ## One class to download json from Nature

    The following class downloads takes in the journal name and year as argument and uses the [Nature API](http://www.nature.com/developers/documentation/api-references/opensearch-api/) to download all the articles of that year and journal. The result is then stored in a json object array file, named by the journal name and year, i.e. nnano-2011.json.
    """

    def __init__(self, name):
        self.name = name

    def query(self, year, productCode):
        content = None # to store the response of the query
        jsonObjArray = [] # to store all the entries extracted from the response

        # loop months
        for month in range(1,13):
            if month < 10:
                thisMonth =  '0' + str(month)
            else:
                thisMonth = str(month)

            # loop days
            for day in range(1,32):

                # make all day number two digits
                if day<10:
                    thisDay = '0' + str(day)
                else:
                    thisDay = str(day)

                # construct the targetDate string
                targetDate = str(year) + '-' + thisMonth + '-' + thisDay
                print(targetDate)

                # construct the queryWord to be sent
                queryWord = 'prism.productCode=' + productCode + '+AND+prism.publicationDate=' + targetDate
                url = 'http://api.nature.com/content/opensearch/request?&recordPacking=unpacked&queryType=cql&maximumRecords=100&httpAccept=application/json&query=' + queryWord

                # start the query by calling urllib2
                try:
                    content = urllib2.urlopen(url).read()
                    data = json.loads(content)
                except:
                    print("URL error\n")
                    continue

                # if the response is not empty, then extract the entries
                if data['feed']['opensearch:totalResults'] != 0:
                    print("found match")
                    for entry in data['feed']["entry"]:
                        jsonObjArray.append(entry)

                # put a delay so that we don't overload the nature servers
                time.sleep(1)

        return jsonObjArray


    def download(self, productCode, year, fileName):
        logfile = open('log.txt', 'a')
        datafile = open(fileName, 'w+')
        logfile.write("Start Download" + ' ' + productCode + ' ' + str(year) + ' into file: ' + fileName + '\n')

        query_result = self.query(year, productCode)

        # store the entries to the output file
        json.dump(query_result, datafile, indent=4)
        datafile.close()
        logfile.write(fileName + ' done.\n')
        logfile.close()
        return True

    def load_file(self, fname):
        """ This method load the nature meta data json file and return a list of json objects """
        json_file = open(fname)
        entry_json_list = json.load(json_file)
        return entry_json_list

## crawl IEEE Xplore
#keyword = urllib.quote_plus("graphene")
#url = "http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?&hc=1&querytext=" + keyword
#content = urllib2.urlopen(url).read()
#tree = ET.fromstring(content)
#for child in tree.iter('title'):
#	print child.text
#
## crawl Springer
#url = 'http://api.springer.com/metadata/json?p=100&q=title:graphene&api_key=3a3sxqg25fmwnzrsy2qmgjds'
#content = urllib2.urlopen(url).read()
#data = json.loads(content)
#for record in data['records']:
#	print record['title'].encode('utf-8')
#	#print record['doi'].encode('utf-8')
#
#myfile = open('Nature-record.json', 'w')
#myfile.write(content)
#myfile.close()
