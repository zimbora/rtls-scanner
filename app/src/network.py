


# importing the requests library
import requests
import json
from config.index import configuration

config = configuration()

DOMAIN = config.domain
TOKEN = config.token
print("localhost: "+config.localhost)
print("domain: "+DOMAIN)

class networkHTTP:
  """ Class to obtain data from cloud"""

  def __init__ (self):
      print("http class started")
      self.controllertoken = ""

  # updated v0.1.1
  def getToken(self):
      # defining a params dict for the parameters to be sent to the API
      HEADERS = {
      }

      PARAMS = {}

      URL = "http://" + config.localhost + ":" + str(config.web_port) + "/api/token"

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

          self.controllertoken = response['Result']
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
        raise SystemExit(e)

  # updated v0.1.1
  def getFloors(self):

    PARAMS = {}
    return self.api_get(PARAMS,'/maps')

  # !! not working
  def getMap(self,router_mac,ssid):

    PARAMS = {
      "ssid" : ssid,
      "router_mac" : router_mac
    }

    return self.api_get(PARAMS ,'/map/id')

  # updated v0.1.1
  def getWifiCrendentials(self,map_id):

    return self.api_get({},'/map/'+str(map_id)+"/wifi/credentials")

  # develop..
  def getDimensions(self,map_id):

      PARAMS = {}
      row = self.api_get(PARAMS,'/map/' + str(map_id) + '/svg_info')
      if len(row) > 0:
          return row[0]['svg_info']
      else:
        return row

  # updated v0.1.1
  def getSniffersGroups(self,map_id):

      PARAMS = {}
      return self.api_get(PARAMS,'/map/' + str(map_id) + '/data/sniffers/groups')

  # updated v0.1.1
  def updateCoefs(self,group_id,coefs,mean,std,samples,devices,floor_id):

      # defining a params dict for the parameters to be sent to the API
      HEADERS = {
        'token':TOKEN,
        "Content-Type": "application/json"
      }
      data = {
        'group_id' : group_id,
        #'coefs' : json.dumps(list(coefs)),
        'coefs' : list(coefs),
        'mean' : mean,
        'std' : std,
        'n_samples' : samples,
        'n_devices' : devices
      }

      URL = DOMAIN + "/map/"+floor_id+"/data/sniffers/groups/coefs"
      print(data)
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

  # updated v0.0.2
  # send
  def updatePatternMessages(self,node,group_id,keys,values):
      '''
      print("node: ",node)
      print("group_id: ",group_id)
      print("keys: ",keys)
      print("values: ",values)
      '''
      # defining a params dict for the parameters to be sent to the API
      HEADERS = {
        'token':TOKEN,
      }
      data = {
        'Sniffers_groups_id' : group_id,
        'Nodes_id' : node,
        'key' : keys,
        'value' : values,
      }

      URL = DOMAIN + "/data/messages/new/pattern"

      try:
          r = requests.post(url = URL, headers = HEADERS, data = data)

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

  # updated v0.1.1
  def updateUserMapInfo(self,floor_id,ip,mac,tag):

    if self.controllertoken == "":
      return

    # defining a params dict for the parameters to be sent to the API
    HEADERS = {
      'controllertoken':self.controllertoken,
      "Content-Type": "application/json"
    }
    data = {
      'ip' : ip,
      'mac' : mac,
      'tag': tag
    }

    URL = DOMAIN + "/map/"+str(floor_id)+"/data/nodes/info"

    try:
        # update coefs for respective group_id
        r = requests.put(url = URL, headers = HEADERS, data = json.dumps(data))

        if not r:
            print('An error has occurred: ',r.reason)
            print(r.raise_for_status())
            return

        try:
          response = r.json()

          if response['Error']:
            print(response['Message'])
            return False
          else:
            return True

        except ValueError:
          print("Invalid JSON response")
          # Handle the case when the response is not valid JSON
          return False

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

  # updated v0.1.1
  def getSniffers(self,map_id):

      PARAMS = {}
      return self.api_get(PARAMS,'/map/' + str(map_id) + '/sniffers')

  # updated v0.0.2
  def getNrOfAvailableMessages(self,group_id,floor_id):

     PARAMS = {
       'group_id' : group_id,
       'floor_id' : floor_id,
     }

     row = self.api_get(PARAMS,'/data/sniffers/groups/n_msgs')
     if len(row) > 0:
         return row[0]["COUNT(*)"]
     else:
         return row

  # updated v0.1.1
  def getNrOfAvailablePatternMessages(self,group_id,floor_id):

     PARAMS = {
       'group_id' : group_id
     }

     row = self.api_get(PARAMS,'/map/'+str(floor_id)+'/data/messages/count/pattern')
     if len(row) > 0:
         return row[0]["COUNT(*)"]
     else:
         return row

  # updated v0.0.2
  def getMessages(self,group_id,limit,mac):

     PARAMS = {
       'group_id' : group_id,
       'limit' : limit,
       'macAddress' : mac
     }

     return self.api_get(PARAMS,'/data/sniffers/groups/msgs')

  # updated v0.1.1
  def getPatternMessages(self,group_id,limit,floor_id):

    PARAMS = {
      'group_id' : group_id,
      'limit'    : limit,
    }

    return self.api_get(PARAMS,'/map/'+str(floor_id)+'/data/messages/pattern')

  # getting messages from DB which have a position sent by the client
  # updated v0.1.2
  def getFeedbackHistory(self,group_id,map_id):

      # defining a params dict for the parameters to be sent to the API
      PARAMS = {
        'group_id':group_id,
      }

      return self.api_get(PARAMS,'/map/'+str(map_id)+'/data/nodes/feedback')

  # updated v0.1.2
  def getWeights(self,group_id,map_id):

   # defining a params dict for the parameters to be sent to the API
   PARAMS = {
     'group_id':group_id,
   }

   return self.api_get(PARAMS,'/map/'+str(map_id)+'/data/sniffers/groups/nn')

  # updated v0.1.2
  def updateWeights(self,data,floor_id):
     print("updating weights")
     print(json.dumps(data))
     # defining a params dict for the parameters to be sent to the API
     HEADERS = {
       'token':TOKEN,
       "Content-Type": "application/json"
     }

     URL = DOMAIN + "/map/"+str(floor_id)+"/data/sniffers/groups/nn"
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

  def api_get(self,PARAMS,path):

    HEADERS = {};
    if TOKEN != "":
        HEADERS['token'] = TOKEN
    else:
        HEADERS['controllertoken'] = self.controllertoken

    URL = DOMAIN + path

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
      raise SystemExit(e)
