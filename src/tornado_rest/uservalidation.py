#!/usr/bin/env python
import json
import time
import copy
import logging

LOGGER = logging.getLogger(__name__)

class userValidation(object):
    def __init__(self):
        pass

    def determine_time(self, userdata):
        mins = (time.time() - userdata["timestamp"]) / 60

        if mins > 99999999:
            return True

        return False

    def validate_users(self, header):
        authotized = False

        try:
            with open("users.json") as data_file:    
                usr_data = json.load(data_file)
        except:
            return authotized

        
        tempdict = copy.deepcopy(usr_data)
        for user, userdata in tempdict.iteritems():
            if self.determine_time(userdata):
                del usr_data[user]

        for user in usr_data.itervalues():
            if "X-Auth-Token" in header and \
                                user["sessionkey"] == header["X-Auth-Token"]:
                authotized = True        

        with open('users.json', 'w') as outfile:
            json.dump(usr_data, outfile, indent=2)

        return authotized

