#!/usr/bin/env python
import json
import logging

LOGGER = logging.getLogger(__name__)

class deleteData(object):
    def __init__(self):
        pass

    def delete_sessions(self, path):
        user = path.rsplit("/", 2)[-2]

        try:
            with open("users.json") as data_file:    
                usr_data = json.load(data_file)
        except:
            return None

        if usr_data and user in usr_data:
            del usr_data[user]
        else:
            return None

        with open('users.json', 'w') as outfile:
            json.dump(usr_data, outfile, indent=2)

        with open("docs/error_deleted.json") as data_file:    
            data = json.load(data_file)

        return data

