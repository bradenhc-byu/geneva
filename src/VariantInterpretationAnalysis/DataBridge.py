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
import Logger as Log
from Definitions import AVAILABLE_FEATURES

class DataBridge:

    @staticmethod
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
        Log.debug("Gene ID path = " + path)
    
        target = urlparse(uri + path)
        method = 'GET'
        body = ''
        return (target, method,body,headers)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
            data3 = ["?"]
            Log.error("Couldn't find gene family for " + data['response']['docs'][0]['symbol'])
        #print "GeneFamily: "+data2
        return data3




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
            Log.error('Error detected: ' + response['status'])

    @staticmethod
    def downloadGeneFamily(filename, mutations):
        if not os.path.exists(filename):
            genes = []
            for m in mutations:
                if not m.get_gene() in genes:
                    genes.append(m.get_gene())
            Log.info("GENE LIST LENGTH: "+str(len(genes)))
            i = 0
            geneIdMap1 = {}
            while i < str(len(genes)):
                genes1 = genes[i:i+100]
                if (len(genes1) > 0):
                    geneIdMap = DataBridge.download("GENE_ID", genes1)
                    for geneName, geneI in geneIdMap.iteritems():
                        if geneName in genes1:
                            geneIdMap1[geneName] = geneI
                    #geneIdMap1.update(geneIdMap)
                    Log.debug("geneIdMap1 length = " + str(len(geneIdMap1)))
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
            Log.debug("geneIdMap1 length = " + str(len(geneIdMap1)))
            for geneName, geneI in geneIdMap1.iteritems(): #use .items() if you have python 3
                i = i+1
                j = j+1

                try:
                    #geneId = DataBridge.download("GENE_ID",geneI)
                    if not geneName in map:
                        geneFamily = DataBridge.download("GENE_FAMILY", geneI)
                        Log.debug(str(i)+" "+str(j)+" Gene: "+str(geneName)+". GeneID "+str(geneI)+" GeneFamily: " + str(geneFamily))
                        map[geneName] = geneFamily
                        if i > 20:
                            DataBridge.saveToFile(str(map), filename+"Z")
                            i=0
                    else:
                        Log.debug(str(i)+" "+str(j)+" Gene: "+str(geneName)+". GeneID "+str(geneI)+" GeneFamily: " + str(map[geneName]) + " already saved!")
                finally:
                    i = i
            DataBridge.saveToFile(str(map), filename)

    @staticmethod
    def downloadSNPData(filename, mutations):
        filename = AVAILABLE_FEATURES["allele-frequency"][1]
        if os.path.exists(filename) and mutations[0].get_chromosome() != -1: return
        snpMap = {}
        for m in mutations:
            requestUrl = DataBridge.getSNPSummaryRequest(m.get_rs_number())
            content = urllib2.urlopen(requestUrl).read()
            chr, chrIndex, maf = DataBridge.getSNPSummaryCallback(content)
            m.add_chromosome(chr)
            m.add_chr_index(chrIndex)
            snpMap[m.get_rs_number()] = maf
        DataBridge.saveToFile(str(snpMap), filename)
        Log.info("Saved allele frequency map for %s mutations" % len(snpMap))


    @staticmethod
    def getPhastConsRequest(mutation):
        chrString = "chr" + mutation.get_chromosome()
        queryString = "SELECT score WHERE "

    @staticmethod
    def downloadPhastCons(filename, mutations):
        if mutations[0].get_chromosome() == -1:
            # need genomic location (obtained through allele frequency download)
            DataBridge.downloadSNPData(AVAILABLE_FEATURES['allele-frequency'][1], mutations)

        cnx = mysql.connector.connect(user='genome',
                                      host='genome-mysql.soe.ucsc.edu',
                                      database='hg38')
        cursor = cnx.cursor()
        query = """SELECT score FROM phastConsElements20way 
                            WHERE chrom = %s
                            AND chromStart <= %s
                            AND chromEnd >= %s"""

        pcMap = {}
        for m in mutations:
            chrString = "chr" + m.get_chromosome()
            cursor.execute(query, (chrString, m.get_chr_index(), m.get_chr_index()))
            for scores in cursor:
                assert len(scores) == 1
                score = scores[0]
                Log.debug("Mutation rs%s has PhastCon score %d" % (m.get_rs_number(), score))
                pcMap[m.get_rs_number()] = score

        DataBridge.saveToFile(str(pcMap), filename)
        cnx.close()

    @staticmethod
    def loadMap(feature, params):
        filename = feature.get_fileName()
        if not os.path.exists(filename):
            Log.info("Cached file not found. Downloading %s data" % feature.get_name())
            DataBridge.loadDispatcher[feature.get_name()](filename, params)
        myMap = DataBridge.openFromFile(filename)
        #print str(myMap)
        Log.info("Loading map for %s" % feature.get_name())
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
                try:
                    maf = item.text
                    maf = float(maf.split("=")[1].split("/")[0])
                except:
                    maf = "?"
                continue
            elif item.attrib['Name'] == 'CHRPOS':
                chr, chrIndex = item.text.split(":")
                chrIndex = long(chrIndex)
                continue
        return chr, chrIndex, maf

    @staticmethod
    def getSNPSummaryRequest(rsNum):
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={}'\
            .format(rsNum)
        return url


    @staticmethod
    def geneFamTest(mutations):
        feature = Feature(*AVAILABLE_FEATURES['gene-family'])
        feature.__filename += "test"
        try: os.remove(feature.get_fileName())
        except: pass
        gfMap = DataBridge.loadMap(feature, mutations)
        assert gfMap != None
        assert gfMap['TWNK'] == [1167]
        assert gfMap["FBN1"] == ['?']

    @staticmethod
    def mafTest(mutations):
        feature = Feature(*AVAILABLE_FEATURES['allele-frequency'])
        feature.__filename += "test"
        try: os.remove(feature.get_fileName())
        except: pass
        mafMap = DataBridge.loadMap(feature, mutations)
        assert mafMap["374997012"] == "?"
        assert mafMap["2228241"] == 0.0004

    @staticmethod
    def pcTest(mutations):
        feature = Feature(*AVAILABLE_FEATURES['phast-cons'])
        feature.__filename += "test"
        try: os.remove(feature.get_fileName())
        except: pass
        pcMap = DataBridge.loadMap(feature, mutations)
        assert pcMap["374997012"] == 557
        assert pcMap["2228241"] == 367

    @staticmethod
    def genLocationTest(mutations):
        filename = AVAILABLE_FEATURES['allele-frequency'][1] + "test"
        DataBridge.downloadSNPData(filename, mutations)
        assert mutations[0].get_chromosome() == "10"
        assert mutations[0].get_chr_index() == 100989114L
        assert mutations[1].get_chromosome() == "15"
        assert mutations[1].get_chr_index() == 48487353L


    @staticmethod
    def unit_test():
        Log.set_log_level("DEBUG")
        mutations = [Mutation("name", gene="TWNK", rs_num="374997012"),
                     Mutation("blabla", gene="FBN1", rs_num="2228241")]
        assert mutations[0].get_chromosome() == -1

        DataBridge.geneFamTest(mutations)
        DataBridge.pcTest(mutations)
        DataBridge.genLocationTest(mutations)
        DataBridge.mafTest(mutations)

        Log.debug("DATABRIDGE UNIT TESTS PASSED")




DataBridge.requestDispatcher = {
    "GENE_ID": DataBridge.getGeneIdRequest,
    "GENE_FAMILY": DataBridge.getGeneFamilyRequest
}

DataBridge.callbackDispatcher = {
    "GENE_ID": DataBridge.getGeneIdCallback,
    "GENE_FAMILY": DataBridge.getGeneFamilyCallback
}

DataBridge.loadDispatcher = {
    "GENE_FAMILY": DataBridge.downloadGeneFamily,
    "ALLELE_FREQUENCY": DataBridge.downloadSNPData,
    "PHAST_CONS": DataBridge.downloadPhastCons
}


if __name__ == "__main__":
    DataBridge.unit_test()
