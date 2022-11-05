# importing the requests library
import requests
import json
#from config.env.index import configuration


DOMAIN = "https://my.dev.inloc.cloud/api/";

#config = configuration()
#print("domain: "+config.domain())

#DOMAIN = config.domain()

class networkHTTP:
  """ Class to obtain data from cloud"""

  TOKEN = "";
  def __init__ (self):
      print("http class started")

  # updated v0.1.2
  def getToken(self):
     # defining a params dict for the parameters to be sent to the API
     HEADERS = {}

     PARAMS = {}

     URL = "http://localhost:20080/api/token"

     try:
         # sending get request and saving the response as response object
         r = requests.get(url = URL, headers = HEADERS, params = PARAMS)

         if not r:
             print('An error has occurred: ',r.reason)
             print(r.raise_for_status())
             return False

         # extracting data in json format
         response = r.json()

         if response['Error']:
           print("Error on query")
           return False

         self.TOKEN = response['Result']
         return self.TOKEN != None
     except requests.exceptions.Timeout:
       # Maybe set up for a retry, or continue in a retry loop
       print("Couldn't reach api >> timeout >> ",URL)
       return False
     except requests.exceptions.TooManyRedirects:
       # Tell the user their URL was bad and try a different one
       print("Couldn't reach api >> too many redirects >> ",URL)
       return False
     except requests.exceptions.RequestException as e:
       # catastrophic error. bail.
       print("Couldn't reach api >> ",URL)
       print("Maybe is unavailable or the url is wrong")
       return False

  # updated v0.1.1
  def getMap(self,router_mac,ssid):
       # defining a params dict for the parameters to be sent to the API
       HEADERS = {
         'controllertoken':self.TOKEN,
       }

       PARAMS = {
        "router_mac" : router_mac,
        "ssid" : ssid
       }

       URL = DOMAIN + "map/id"

       try:
           # sending get request and saving the response as response object
           r = requests.get(url = URL, headers = HEADERS, params = PARAMS)

           if not r:
               print('An error has occurred: ',r.reason)
               print(r.raise_for_status())
               return

           # extracting data in json format
           response = r.json()

           if response['Error']:
             print("Error on query")
             return;

           return response['Result']
       except requests.exceptions.Timeout:
         # Maybe set up for a retry, or continue in a retry loop
         print("Couldn't reach api >> timeout >> ",URL)
       except requests.exceptions.TooManyRedirects:
         # Tell the user their URL was bad and try a different one
         print("Couldn't reach api >> too many redirects >> ",URL)
       except requests.exceptions.RequestException as e:
         # catastrophic error. bail.
         print("Couldn't reach api >> ",URL)
         print("Maybe is unavailable or the url is wrong")

  # updated v0.1.1
  def updateUserMapInfo(self,floor_id,ip,mac,tag):

      # defining a params dict for the parameters to be sent to the API
      HEADERS = {
        'controllertoken':self.TOKEN,
        "Content-Type": "application/json"
      }
      data = {
        'ip' : ip,
        'mac' : mac,
        'tag': tag
      }

      URL = DOMAIN + "map/"+str(floor_id)+"/data/nodes/info"

      try:
          # update coefs for respective group_id
          r = requests.put(url = URL, headers = HEADERS, data = json.dumps(data))

          if not r:
              print('An error has occurred: ',r.reason)
              print(r.raise_for_status())
              return

          # extracting data in json format
          response = r.json()

          if response['Error']:
            print(response['Message'])
            return;

          row = response['Result']

          groups = []
          #for group in row:
              #groups.append(id:group["id"])

          return row

      except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Couldn't reach api >> timeout >> ",URL)
      except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Couldn't reach api >> too many redirects >> ",URL)
      except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print("Couldn't reach api >> ",URL)
        print("Maybe is unavailable or the url is wrong")
        raise SystemExit(e)
