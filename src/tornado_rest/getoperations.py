#!/usr/bin/env python
import json
import logging
import threading
import collections
from socketIO_client import SocketIO

LOGGER = logging.getLogger(__name__)

TELEMETRY_DATA = []

class web_socket_client(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
 
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def set_telemetry_data(self, *args):
        global TELEMETRY_DATA
        TELEMETRY_DATA = args
    
    def run(self):
        """ Method that runs forever """
        while True:
            socketIO = SocketIO(
                'test-sensors-server.herokuapp.com',
                proxies={'https': 'http://proxy.compaq.com:8080'})
            socketIO.on('telemetry', self.set_telemetry_data)
            socketIO.wait()


class getData(object):
    def __init__(self):
        pass

    def redfish_v1(self):
        with open("docs/index.json") as data_file:    
            data = json.load(data_file)
        return data

    def redfish_v1_session_service(self):
        with open("docs/sessionservice.json") as data_file:    
            data = json.load(data_file)
        return data\
    
    def redfish_v1_resources(self):
        with open("docs/resourcedirectory.json") as data_file:    
            data = json.load(data_file)
        return data

    def redfish_v1_telemetry(self): 
        global TELEMETRY_DATA
        with open("docs/telemetry.json") as data_file:    
            data = json.load(data_file)
 
        tmplist = []
        data["Members@odata.count"] = len(TELEMETRY_DATA[0])
        for idx, _ in enumerate(TELEMETRY_DATA[0]):
            tmplist.append({"@odata.id": "/redfish/v1/Telemetry/" + \
                                                            str(idx + 1) + "/"})
             
        data["Members"] = tmplist
 
        return data
 
    def redfish_v1_telemetry_single(self, path):
        global TELEMETRY_DATA
        try:
            ret_data = collections.OrderedDict()
            ret_data["Name"] = "Telemetry Data"
            ret_data["Description"] = "Telemetry Data View"
            ret_data["@odata.id"] = "/redfish/v1/Telemetry/1/"
            ret_data["@odata.type"] = "#Telemetry.1.0.1.Telemetry"
            
            data = ret_data.copy()
            data.update(TELEMETRY_DATA[0][int(path.split("/")[-2]) - 1])
            return data
        except:
            return None
    
    def redfish_v1_session_service_sessions(self):
        with open("docs/sessionservicesessions.json") as data_file:    
            data = json.load(data_file)

        with open("users.json") as data_file:    
            usr_data= json.load(data_file)

        data["Members@odata.count"] = len(usr_data)
        
        newmemberslist = []
        for user in usr_data:
            newmemberslist.append({"@odata.id": "/redfish/v1/Se" \
                                         "ssionService/Sessions/" + user + "/"})

        data["Members"] = newmemberslist
        return data

    def redfish_v1_session_users(self, path):
        user = path.rsplit("/", 2)[-2]

        with open("users.json") as data_file:    
            usr_data= json.load(data_file)

        if not user in usr_data:
            return None   

        with open("docs/sessionuser.json") as data_file:    
            data = json.load(data_file)

        data["@odata.id"] = path
        data["Id"] = user
        return data

    def not_found(self, path):
        with open("docs/error.json") as data_file:    
            data = json.load(data_file)
        data["error"]["@Message.ExtendedInfo"][0]["MessageArgs"] = [path]
        return data

    def not_authorized(self):
        with open("docs/error_unauthorized.json") as data_file:    
            data = json.load(data_file)
        return data

