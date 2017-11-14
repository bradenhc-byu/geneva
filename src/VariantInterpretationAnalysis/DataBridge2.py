################################################################################
# DataBridge -- formulates and sends HTTP requests, saves responses
#
#
#

class DataBridge:
    def __init__(self:
        pass



    def getGeneFamilyRequest(self, mutations):
        pass


    requestDispatcher = {
        "GENE_FAMILY": getGeneFamilyRequest
    }


    def getData(self, feature, mutations):
        request = DataBridge.requestDispatcher[feature.name](mutations)
        response = makeHttpRequest(request)
        saveToFile(response, feature.fileName)