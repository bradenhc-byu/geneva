################################################################################
# DataBridge -- formulates and sends HTTP requests, saves responses
#
#
#

import json
import httplib as http
from urlparse import urlparse
from Collections import Mutation,Feature


class DataBridge:
    def getGeneFamilyRequest(self, mutations):
        def getGeneId(gene):
            headers = {
                'Accept': 'application/json',
            }

            uri = 'http://rest.genenames.org'
            path = '/search/' + str(gene)  # ZNF513

            target = urlparse(uri + path)
            method = 'GET'
            body = ''

            h = http.Http()

            response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)

            if response['status'] == '200':
                # assume that content is a json reply
                # parse content with the json module
                data = json.loads(content)
                data2 = data['response']['docs'][0]['hgnc_id']
                data3 = data2[data2.index(':') + 1:]
                print str(data3)
                # data3 = data['response']['docs'][0]['gene_family_id']
                # for i in range(len(data2)):
                #  print 'GeneFamily:' + data['response']['docs'][0][ 'gene_family'][i]
                # print 'GeneFamily:' + str(data['response']['docs'][0]['gene_family_id'][i])
                print str(data)

            else:
                print 'Error detected: ' + response['status']
            return str(data3)

        def getGeneFamily(id):
            headers = {
                'Accept': 'application/json',
            }

            uri = 'http://rest.genenames.org'
            path = '/fetch/hgnc_id/' + id  # 1097

            target = urlparse(uri + path)
            method = 'GET'
            body = ''

            h = http.Http()

            response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)

            if response['status'] == '200':
                # assume that content is a json reply
                # parse content with the json module
                data = json.loads(content)
                data2 = data['response']['docs'][0]['gene_family']
                data3 = data['response']['docs'][0]['gene_family_id']
                for i in range(len(data2)):
                    print 'GeneFamily:' + data['response']['docs'][0]['gene_family'][i]
                    print 'GeneFamily:' + str(data['response']['docs'][0]['gene_family_id'][i])
                return (data2, data3)
            else:
                print 'Error detected: ' + response['status']
            return (["ERROR"], ["ERROR"])

        id = getGeneId("ZNF513")
        getGeneFamily(id)


    requestDispatcher = {
        "GENE_FAMILY": getGeneFamilyRequest
    }

    def saveToFile(self, text, fileName):
        f = open(fileName, 'w')
        f.write(text)
        f.close()


    def makeHttpRequest(self, request):
        pass


    @staticmethod
    def download(feature, mutations):
        # TODO: use Log
        requestParams = DataBridge.requestDispatcher[feature.name](mutations)
        h = http.Http()
        response, content = h.request(*requestParams)
        if response['status'] == '200':
            DataBridge.saveToFile(content, feature.__fileName)
        else:
            print 'Error detected: ' + response['status']

    @staticmethod
    def main():
        download(Feature("GENE_FAMILY", "../data/gf.txt"), [Mutation("hello", "ZNF513")])

DataBridge.main()