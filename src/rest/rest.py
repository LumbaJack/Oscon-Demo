#!/usr/bin/env python
import logging

from tornado_rest.exceptions import APIError
from tornado_rest.getoperations import getData
from tornado_rest.requesthandlers import APIHandler

LOGGER = logging.getLogger(__name__)

REDFISH = "/redfish/"
INDEX = REDFISH + "v1/"
TELEMETRY = INDEX + "telemetry/"

class iLORedfish(APIHandler):
    def __init__(self, *args, **kwargs):
        super(iLORedfish, self).__init__(*args, **kwargs)
        self.gethandler = getData()

    def get(self, path):            
        try:
            path = REDFISH + path

            if path.lower() == TELEMETRY:
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_telemetry()
            elif path.lower().startswith(TELEMETRY):
                self.set_header('Allow', 'GET')
                data = self.gethandler.redfish_v1_telemetry_single(path)
            else:
                self.set_status(400)
                data = self.gethandler.not_found(path)
        except Exception, excp:
            LOGGER.exception("GET: %s", excp)
            raise APIError(409, log_message=excp)

        self.write(data)

