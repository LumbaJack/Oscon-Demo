#!/usr/bin/env python
import os
import tornado.web
import tornado.ioloop
import logging.config
import tornado.autoreload
import tornado_rest.getoperations

from rest.rest import iLORedfish
from rest.mainhandler import MainHandler 

dirname = os.path.dirname(__file__)

STATIC_PATH = os.path.join(dirname, 'static')
TEMPLATE_PATH = os.path.join(dirname, 'templates')

class Application(tornado.web.Application):
    """Entry-point for the app

    - Generate API documentation using provided routes
    - Initialize the application

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes for the app
    :type  settings: dict
    :param settings: Settings for the app
    """

    def __init__(self, routes, settings):
        # Unless compress_response was specifically set to False in
        # settings, enable it
        compress_response = "compress_response"
        if compress_response not in settings:
            settings[compress_response] = True

        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )

def main():
    tornado_rest.getoperations.web_socket_client()
    routes = [(r'/redfish/(.*)', iLORedfish), (r'/', MainHandler), \
          (r'/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH})]
    settings = {"template_path": TEMPLATE_PATH, "static_path": STATIC_PATH, 
                "debug": True, "cookie_secret":"+lyFdq7yVzOdpb1SIspHdfQ1SnZzB" \
                "CJ0Xg9Sf8LsAxFQ1dzsOMGPC4SI18Ve/cUrjStcfYNLcWVjhHa8F0a77pohs" \
                "N2DPV2sW+Y5zqnxeXAbX+9kbhiDNIkGbMdEJUfQHEBuuixxRpV3BcwmF065E" \
                "1RTCo6halg07rwsS3iTtlI"}
    application = Application(routes=routes, settings=settings)
    application.listen(5000)
    ioloop = tornado.ioloop.IOLoop.instance()
    if debug:
        tornado.autoreload.start(ioloop)
    ioloop.start()


if __name__ == '__main__':
    logging.config.fileConfig('./conf.ini', disable_existing_loggers=False)
    LOGGER = logging.getLogger(__name__)
    debug = True
    main()

