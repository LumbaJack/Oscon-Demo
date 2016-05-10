#!/usr/bin/env python
import socket
import logging
import urlparse

from tornado_rest.exceptions import APIError
from tornado_rest.getoperations import getData
from tornado_rest.postoperations import postData
from tornado_rest.deleteoperations import deleteData
from tornado_rest.requesthandlers import APIHandler
from tornado_rest.uservalidation import userValidation

LOGGER = logging.getLogger(__name__)

REDFISH = "/redfish/"
INDEX = REDFISH + "v1/"
RESOURCES = INDEX + "resourcedirectory/"
TELEMETRY = INDEX + "telemetry/"
SESSIONSERVICE = INDEX + "sessionservice/"
SESSIONS = SESSIONSERVICE + "sessions/"

class iLORest(APIHandler):
    def __init__(self, *args, **kwargs):
        super(iLORest, self).__init__(*args, **kwargs)
        self.gethandler = getData()
        self.posthandler = postData()
        self.deletehandler = deleteData()
        self.uservalidation = userValidation()

    def get(self, path):            
        try:
            path = REDFISH + path

            if not path.endswith("/"):
                self.redirect(path + "/")
            elif path.lower() == INDEX:
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1()
            elif not self.uservalidation.validate_users(\
                                                    self.request.headers._dict):
                self.set_status(401)
                data = self.gethandler.not_authorized()
            elif path.lower() == RESOURCES:
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_resources()
            elif path.lower() == TELEMETRY:
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_telemetry()
            elif path.lower().startswith(TELEMETRY):
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_telemetry_single(path)
            elif path.lower() == SESSIONSERVICE:
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_session_service()
            elif path.lower() == SESSIONS:
                self.set_header('Allow', 'GET POST')
                data = self.gethandler.redfish_v1_session_service_sessions()
            elif path.lower().startswith(SESSIONS):
                self.set_header('Allow', 'GET DELETE')
                data = self.gethandler.redfish_v1_session_users(path)
                if not data:
                    self.set_status(400)
                    data = self.gethandler.not_found(path)
            else:
                self.set_status(400)
                data = self.gethandler.not_found(path)
        except Exception, excp:
            LOGGER.exception("GET: %s", excp)
            raise APIError(409, log_message=excp)

        self.write(data)

    def post(self, path):
        try:
            path = REDFISH + path

            if path.lower() == SESSIONS:
                hostname = urlparse.urlparse("%s://%s"
                        % (self.request.protocol, self.request.host)).hostname
                ip_address = socket.gethostbyname(hostname)
                self.set_status(201)

                (data, body) = self.posthandler.post_sessions(self.json_body)
                for item in body: 
                    self.set_header('X-Auth-Token', body[item]["sessionkey"])
                    location = "https://%s:443/redfish/v1/SessionService/Ses" \
                                                "sions/%s/" % (ip_address, item)
                    self.set_header('Location', location)
                else:
                    if not body:
                        self.set_status(401)
            else:
                self.set_status(400)
                data = self.gethandler.not_found(path)
        except Exception, excp:
            LOGGER.exception("POST: %s", excp)
            raise APIError(409, log_message=excp)

        self.write(data)

    def delete(self, path):
        try:
            path = REDFISH + path

            if not self.uservalidation.validate_users(\
                                                    self.request.headers._dict):
                self.set_status(401)
                data = self.gethandler.not_authorized(path)
            elif path.lower().startswith(SESSIONS):
                data = self.deletehandler.delete_sessions(path)
                if not data:
                    self.set_status(400)
                    data = self.gethandler.not_found(path)
            else:
                self.set_status(400)
                data = self.gethandler.not_found(path)
        except Exception, excp:
            LOGGER.exception("DELETE: %s", excp)
            raise APIError(409, log_message=excp)

        self.write(data)

