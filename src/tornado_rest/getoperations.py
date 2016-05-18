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
                'rover-sensors-data-provider.52.35.15.130.nip.io',
                proxies={'https': 'http://proxy.compaq.com:8080'})
            socketIO.on('telemetry', self.set_telemetry_data)
            socketIO.wait()


class getData(object):
    def __init__(self):
        pass

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
            ret_data["@odata.id"] = path
            ret_data["@odata.type"] = "#Telemetry.1.0.1.Telemetry"
            
            data = ret_data.copy()
            data.update(TELEMETRY_DATA[0][int(path.split("/")[-2]) - 1])
            return data
        except:
            return None

    def not_found(self, path):
        with open("docs/error.json") as data_file:    
            data = json.load(data_file)
        data["error"]["@Message.ExtendedInfo"][0]["MessageArgs"] = [path]
        return data

