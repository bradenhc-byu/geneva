################################################################################
# DataBridge -- formulates and sends HTTP requests, saves responses
#
#
#

import httplib2 as http
import json
import os
import re
try: 
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from Collections import Mutation,Feature
import pyodbc
import mysql.connector


class DataBridge:
    def getGeneIdRequest(gene):
        headers = {
          'Accept': 'application/json',
        }
    
        uri = 'http://rest.genenames.org'
        path = '/search/' + str(gene)  # ZNF513
    
        target = urlparse(uri + path)
        method = 'GET'
        body = ''
        return (target, method,body,headers)

    def getGeneIdCallback(content):
        # assume that content is a json reply
        # parse content with the json module
        data = json.loads(content)
        data2 = data['response']['docs'][0]['hgnc_id']
        data3 = data2[data2.index(':') + 1:]
        #print str(data3)
        #print str(data)
        return [data3]

    def getGeneFamilyRequest(id):
        headers = {
          'Accept': 'application/json',
        }
    
        uri = 'http://rest.genenames.org'
        path = '/fetch/hgnc_id/' + id  # 1097
        
        target = urlparse(uri + path)
        method = 'GET'
        body = ''
        return (target, method,body,headers)

    def getGeneFamilyCallback(content):
        # assume that content is a json reply
        # parse content with the json module
        data = json.loads(content)
        #print str(data['response']['docs'][0])
        try:
            data2 = data['response']['docs'][0]['gene_family']
            data3 = data['response']['docs'][0]['gene_family_id']
            #for i in range(len(data2)):
            #    print 'GeneFamily:' + data['response']['docs'][0]['gene_family'][i]
            #    print 'GeneFamilyId:' + str(data['response']['docs'][0]['gene_family_id'][i])
            #data2 = data2[0]
        except:
            data2 = ["?"]
        #print "GeneFamily: "+data2
        return data2

    @staticmethod
    def getSearchRequest(rsNum):
        headers = {}
        uri = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term=' + rsNum

        target = urlparse(uri)
        method = 'GET'
        body = ''
        return (target, method, body, headers)

    @staticmethod
    def getSearchCallback(content):
        # $web = $1 if ($output = ~ / < WebEnv > (\S +) < \ / WebEnv > / );
        # $key = $1 if ($output = ~ / < QueryKey > (\d +) < \ / QueryKey > / );
        webEnv = re.search(r"<WebEnv>(\S+)</WebEnv>").group(1)
        queryKey = re.search(r"<QueryKey>(\d+)</QueryKey>").group(1)
        return webEnv, queryKey


    requestDispatcher = {
        "GENE_ID": getGeneIdRequest,
        "GENE_FAMILY": getGeneFamilyRequest,
        "GENOMIC_LOCATION": getGenomicLocationRequest
    }

    callbackDispatcher = {
        "GENE_ID": getGeneIdCallback,
        "GENE_FAMILY": getGeneFamilyCallback
    }

    @staticmethod
    def saveToFile(text, fileName):
        f = open(fileName, 'w')
        f.write(text)
        f.close()

    @staticmethod
    def openFromFile(filename):
        return eval(open(filename, 'r').read())

    @staticmethod
    def download(feature, mutations):
        (target, method, body, headers) = DataBridge.requestDispatcher[feature](mutations)
        h = http.Http()
        response, content = h.request(target.geturl(),method,body,headers)
        if response['status'] == '200':
            return DataBridge.callbackDispatcher[feature](content)
        else:
            print 'Error detected: ' + response['status']

    def downloadGeneFamily(filename, params):
        genes = []
        for f in params:
            if not f.get_gene() in genes:
                genes.append(f.get_gene())
        print "GENE LIST LENGTH: "+str(len(genes))
        i=0
        j=0
        map = {}
        for gene in genes:
            i = i+1
            j = j+1

            try:
                geneId = DataBridge.download("GENE_ID", gene)
                geneFamily = DataBridge.download("GENE_FAMILY", geneId[0])
                print str(j)+" "+str(j)+" Gene: "+str(gene)+". GeneID "+str(geneId[0])+" GeneFamily: " + str(geneFamily)
                map[gene] = geneFamily
                if i > 20:
                    DataBridge.saveToFile(str(map), filename)
                    i=0
            finally:
                i = i
        DataBridge.saveToFile(str(map), filename)

    loadDispatcher = {
        "GENE_FAMILY": downloadGeneFamily,
    }

    @staticmethod
    def loadMap(feature, filename, params):
        if not os.path.exists(filename):
            DataBridge.loadDispatcher[feature](filename,params)
        myMap = DataBridge.openFromFile(filename)
        print str(myMap)
        return myMap


    @staticmethod
    def loadGenomicLocation(mutations):
        for m in mutations:
            if m.__chr == -1: continue
            (target, method, body, headers) = DataBridge.getSearchRequest(m)
            h = http.Http()
            response, content = h.request(target.geturl(), method, body, headers)
            if response['status'] == '200':
                queryKey, webEnv = DataBridge.getSearchCallback(content)
            else:
                print 'Error detected: ' + response['status']




    @staticmethod
    def downloadGerp(mutations, fileName):
        # cnxn = pyodbc.connect('DRIVER={MySQL};SERVER=genome-mysql.soe.ucsc.edu;UID=genome;')
        # cnxn = pyodbc.connect("Login Prompt=False;User ID=genome;Data Source=genome-mysql.soe.ucsc.edu;CHARSET=UTF8")
        # cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        # cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        # cnxn.setencoding(encoding='utf-8')
        # cursor = cnxn.cursor()


        cnx = mysql.connector.connect(user='genome',
                                      host='genome-mysql.soe.ucsc.edu',
                                      database='hg19')
        cursor = cnx.cursor("SELECT ")

        cnx.close()



    def unit_test(self):
        self.loadMap("GENE_FAMILY", "GENEFAMILY.txt", ["ZNF513"])


def testGerp():
    DataBridge.downloadGerp([Mutation("name", "ZNF513")])


# d=DataBridge()
# d.unit_test()
testGerp()