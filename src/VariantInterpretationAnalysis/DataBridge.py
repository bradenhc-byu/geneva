################################################################################
# DataBridge -- formulates and sends HTTP requests, saves responses
#
#
#

import httplib2 as http
import json
import os
import re
import urllib2
import xml.etree.ElementTree as ET
try: 
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from Collections import Mutation,Feature
import pyodbc
import mysql.connector


class DataBridge:
    def getGeneIdRequest(genes):
        headers = {
          'Accept': 'application/json',
        }
    
        uri = 'http://rest.genenames.org'
        path = '/search/'
        for gene in genes:
            for gene1 in gene.split(";"):
                path = path +str(gene1)+"+OR+"
        path = path[:-4]
        print path
    
        target = urlparse(uri + path)
        method = 'GET'
        body = ''
        return (target, method,body,headers)

    def getGeneIdCallback(content):
        # assume that content is a json reply
        # parse content with the json module
        data = json.loads(content)
        #print str(data)
        #data2 = data['response']['docs'][0]['hgnc_id']
        data2 = {}
        for i in data['response']['docs']:
            #try:
                data4 = i['symbol']
                data3 = (i['hgnc_id'])[i['hgnc_id'].index(':') + 1:]
                data2[data4] = data3
            #finally:
            #    data2.append("?")
        #data3 = data2[data2.index(':') + 1:]
        #print str(data2)
        return data2

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
            data3 = 0
        #print "GeneFamily: "+data2
        return data3


    requestDispatcher = {
        "GENE_ID": getGeneIdRequest,
        "GENE_FAMILY": getGeneFamilyRequest
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

    def downloadGeneFamily(filename, mutations):
        if not os.path.exists(filename):
            genes = []
            for m in mutations:
                if not m.get_gene() in genes:
                    genes.append(m.get_gene())
            print "GENE LIST LENGTH: "+str(len(genes))
            i=0
            geneIdMap1 = {}
            while i < str(len(genes)):
                genes1 = genes[i:i+100]
                if (len(genes1) > 0):
                    geneIdMap = DataBridge.download("GENE_ID",genes1)
                    for geneName, geneI in geneIdMap.iteritems():
                        if geneName in genes1:
                            geneIdMap1[geneName] = geneI
                    #geneIdMap1.update(geneIdMap)
                    print str(len(geneIdMap1))
                else:
                    break
                i=i+100
            DataBridge.saveToFile(str(geneIdMap1), filename)
            geneIdMap1 = DataBridge.openFromFile(filename)
            map = {}
            #if os.path.exists(filename+"Z"):
            #    map = DataBridge.openFromFile(filename+"Z")
            #for geneId in geneIdMap:
            i=0
            j=0
            print str(len(geneIdMap1))
            for geneName, geneI in geneIdMap1.iteritems(): #use .items() if you have python 3
                i = i+1
                j = j+1

                try:
                    #geneId = DataBridge.download("GENE_ID",geneI)
                    if not geneName in map:
                        geneFamily = DataBridge.download("GENE_FAMILY", geneI)
                        print str(i)+" "+str(j)+" Gene: "+str(geneName)+". GeneID "+str(geneI)+" GeneFamily: " + str(geneFamily)
                        map[geneName] = geneFamily
                        if i > 20:
                            DataBridge.saveToFile(str(map), filename+"Z")
                            i=0
                    else:
                        print str(i)+" "+str(j)+" Gene: "+str(geneName)+". GeneID "+str(geneI)+" GeneFamily: " + str(map[geneName]) + " already saved!"
                finally:
                    i = i
            DataBridge.saveToFile(str(map), filename+"Z")

    def loadSNPData(filename, mutations):
        if os.path.exists(filename): return
        snpMap = {}
        for m in mutations:
            requestUrl = DataBridge.getSNPSummaryRequest(m.get_rs_number())
            print(requestUrl)
            content = urllib2.urlopen(requestUrl).read()
            chr, chrIndex, maf = DataBridge.getSNPSummaryCallback(content)
            m.add_chromosome(chr)
            m.add_chr_index(chrIndex)
            snpMap[m.get_rs_number()] = maf
        DataBridge.saveToFile(str(snpMap), filename)

    loadDispatcher = {
        "GENE_FAMILY": downloadGeneFamily,
        "ALLELE_FREQUENCY": loadSNPData
    }


    @staticmethod
    def loadMap(feature, params):
        filename = feature.get_fileName()
        if not os.path.exists(filename):
            DataBridge.loadDispatcher[feature.get_name()](filename, params)
        myMap = DataBridge.openFromFile(filename)
        #print str(myMap)
        return myMap



    @staticmethod
    def getSNPSummaryCallback(content):
        xmlTree = ET.fromstring(content)
        record = xmlTree.find('DocSum')
        chr = None
        chrIndex = None
        maf = None
        for item in record.findall('Item'):
            if item.attrib['Name'] == 'GLOBAL_MAF':
                maf = item.text
                maf = float(maf.split("=")[1].split("/")[0])
                print(maf)
                continue
            elif item.attrib['Name'] == 'CHRPOS':
                chr, chrIndex = item.text.split(":")
                chrIndex = long(chrIndex)
                print(chr, chrIndex)
                continue
        return chr, chrIndex, maf

    @staticmethod
    def getSNPSummaryRequest(rsNum):
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={}'\
            .format(rsNum)
        return url



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
        self.loadMap(Feature("GENE_FAMILY"), [Mutation("name", "ZNF513", rs_num="1800730", gene="ZNF513")])
        DataBridge.loadMap(Feature("ALLELE_FREQUENCY"), [Mutation("name", "ZNF513", rs_num="1800730")])


def testGerp():
    DataBridge.downloadGerp([Mutation("name", "ZNF513", rs_num="1800730")])

if __name__ == "__main__":
    d=DataBridge()
    d.unit_test()
    # testGerp()
