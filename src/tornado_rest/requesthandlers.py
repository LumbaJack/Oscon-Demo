from tornado.web import RequestHandler
from jsonschema import ValidationError
from tornado_rest.exceptions import APIError
import json
import os

class BaseHandler(RequestHandler):
    """BaseHandler for all other RequestHandlers"""

    __url_names__ = ["__self__"]
    __urls__ = []


class APIHandler(BaseHandler):
    """RequestHandler for API calls

    - Sets header as ``application/json``
    - Provides custom write_error that writes error back as JSON \
    rather than as the standard HTML template
    """

    def _strc2dic(self, data):
        """ Get a structure and return a dictionary

        """
        ret ={}
        for f,t in data._fields_:
           if f != "header":
               if hasattr(t, '_length_'):
                   ret[f] = []
                   for c in getattr(data, f):
                       ret[f].append(hex(c))
               else:
                   ret[f] = hex(getattr(data, f))
        return ret

    def _ba2str(self, data):
        """ Get a byte array and return a string

        """
        ret = ""
        for v in data:
            if v != 0:
                ret += chr(v)
        return ret

    def _ba2ascii(self, data):
        """ Get a byte array and return a string

        """
        ret = ""
        for v in data:
            if v in range(32,126):
                ret += chr(v)
        return ret

    def _is_ipmi(self):
        """Determine if ipmi is supported."""
        return os.path.isfile('/sys/class/ipmi/ipmi0') or os.path.islink('/sys/class/ipmi/ipmi0')


    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
                self.json_body = json.loads(self.request.body)
                self.request.arguments.update(self.json_body)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request

        # Set up response dictionary.
        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.add_header('Access-Control-Allow-Origin', '*')
        self.add_header('Access-Control-Allow-Headers', '*')
        self.add_header('Access-Control-Allow-Methods', '*')
        

    def write_error(self, status_code, **kwargs):
        """Override of RequestHandler.write_error

        Calls ``error()`` or ``fail()`` from JSendMixin depending on which
        exception was raised with provided reason and status code.

        :type  status_code: int
        :param status_code: HTTP status code
        """
        def get_exc_message(exception):
            return exception.log_message if \
                hasattr(exception, "log_message") else str(exception)

        self.clear()
        self.set_status(status_code)

        try:
            exception = kwargs["exc_info"][1]
        except:
            exception = ""
        if any(isinstance(exception, c) for c in [APIError, ValidationError]):
            # ValidationError is always due to a malformed request
            if isinstance(exception, ValidationError):
                self.set_status(400)
            self.write({'status': 'fail', 'data': get_exc_message(exception)})
            self.finish()
        else:
            self.write({
                "status": "fail",
                "message": self._reason,
                "data": get_exc_message(exception),
                "code": status_code})
            self.finish()

    def write_ok(self, data):
        data = {"status": "ok",
                "data": data}
        self.write(data)

    def get_argument(self, name, default = None):
        try:
            return self.request.arguments[name]
        except:
            return default

    def help(self):
        if not self._desc:
            self._desc = "Generic help description."
        if not self._param:
            self._param = {"Generic param."}

        help = {"Description": self._desc,
                "Params": self._param
               }
        return help

    def get(self):
       self.write_ok(self.help())



