#!/usr/bin/env python
import json
import time
import string
import random
import logging

LOGGER = logging.getLogger(__name__)

class postData(object):
    def __init__(self):
        pass

    def post_sessions(self, body):
        try:
            with open("users.json") as data_file:    
                usr_data = json.load(data_file)
        except:
            usr_data = {}

        if "UserName" and "Password" in body:
            if body["UserName"] != "admin" or body["Password"] != "password":
                with open("docs/error_unauthorized.json") as data_file:    
                    data = json.load(data_file)
                return (data, {})
        else:
            with open("docs/error_unauthorized.json") as data_file:    
                data = json.load(data_file)
            return (data, {})

        newuser = ''.join(random.choice(string.lowercase + \
                                            string.digits) for _ in range(14))
        session_key = ''.join(random.choice(string.lowercase + \
                                            string.digits) for _ in range(32))

        session = {}
        session["timestamp"] = time.time()
        session["sessionkey"] = session_key
        usr_data[newuser] = session

        with open('users.json', 'w') as outfile:
            json.dump(usr_data, outfile, indent=2)

        with open("docs/error_session.json") as data_file:    
            data = json.load(data_file)

        return (data, {newuser: session})

