import json, urllib, urllib2, codecs

arcgisServerRootURL = "http://sampleserver6.arcgisonline.com/arcgis/"

restURL = arcgisServerRootURL + "rest/services"

#REST or SOAP
protocol = "REST"

#If you wish to use a token, set getToken to true and specify following parameters
getToken = False
tokenURL = arcgisServerRootURL + "tokens/generateToken"
username = "username1"
password = "pwd1"

#Get Token and Service List from Server
if getToken == True:
    token = getToken(tokenURL, username, password)['token']
    serviceList = restCrawl(restURL, token, protocol)
else:
    serviceList = restCrawl(restURL, "", protocol)

log = codecs.open("services.txt",encoding='utf-8', mode="w+")
for service in serviceList:
    print service
    log.write(service + "\n")
log.close()




def restCrawl(restURL, token, protocol):
    if token != "":
        tokenstring = "&token="+token
    else:
        tokenstring = ""
    crawl_URL = restURL + "?f=json" + tokenstring
    crawl_request = urllib2.Request(url=crawl_URL)
    crawl_response = urllib2.urlopen(crawl_request)
    crawl_string = crawl_response.read()
    crawl_obj = json.loads(crawl_string)
    folders = []
    services = []
    serviceURLs = []
    for serviceDir in crawl_obj['folders']:
        folders.append(serviceDir)
    for service in crawl_obj['services']:
        services.append(service)
    for service in services:
        serviceURLs.append(restURL + "/" + service['name'] + "/" + service['type'])
        getInfoFromService(restURL + "/" + service['name'] + "/" + service['type'])

    for folder in folders:
        services = []
        folder_URL = restURL + "/" + folder + "?f=json" +tokenstring
        folder_request = urllib2.Request(url=folder_URL)
        folder_response = urllib2.urlopen(folder_request)
        folder_string = folder_response.read()
        folder_obj = json.loads(folder_string)
        for service in folder_obj['services']:
            services.append(service)
        for service in services:
            serviceURLs.append(restURL + "/" + service['name'] + "/" + service['type'])
            getInfoFromService(restURL + "/" + service['name'] + "/" + service['type'])
    if protocol == "REST":
        return serviceURLs
    elif protocol == "SOAP":
        soapURLs=[]
        for item in serviceURLs:
             soapURL = item.replace("rest/","")
             soapURLs.append(soapURL)
        return soapURLs
    else:
        print "Invalid protocol specified"
        return serviceURLs

def getInfoFromService(AGSserviceURL):
    print "Getting service level info"
    print AGSserviceURL
    crawlServiceURL = AGSserviceURL + "?f=json" + tokenstring
    crawlServiceURLReq = urllib2.Request(url=crawlServiceURL)
    crawlServiceResp = urllib2.urlopen(crawlServiceURLReq)
    crawlserviceObj = json.loads(crawlServiceResp.read())

    for serviceLayer in crawlserviceObj['layers']:
        print serviceLayer

#    for service in crawl_obj['services']:
#        services.append(service)
#    for service in services:
#        serviceURLs.append(restURL + "/" + service['name'] + "/" + service['type'])







####################################################

#### getToken Documentation ####
#getToken gets a token for ArcGIS Server and returns the entire response from
#the server. The token itself can then be parsed out using ['token'].
#
#tokenURL = The ArcGIS Server Token URL.
#username = The username used to get a token.
#password = The password associated with the username.
#referer = The URL or IP address to be used as the referer
#
#eg. getToken("server/tokens/generateToken", "user1","pswd","mymachine.com")['token']
#

def getToken(tokenURL, username, password):
    token_POSTdata = {'username':username,'password':password,'f':"json"}
    token_request = urllib2.Request(url=tokenURL,data = urllib.urlencode(token_POSTdata))
    token_response = urllib2.urlopen(token_request)
    token_string = token_response.read()
    token_obj = json.loads(token_string)
    return token_obj



