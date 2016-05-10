#!/usr/bin/env python
import os
import tornado.web
import tornado.ioloop
import logging.config
import tornado.autoreload
import tornado.httpserver
from rest.rest import iLORest
import tornado_rest.getoperations

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
    routes = [(r'/redfish/(.*)', iLORest)]
    settings = {"debug": True, "cookie_secret":"+lyFdq7yVzOdpb1SIspHdfQ1SnZzB" \
                "CJ0Xg9Sf8LsAxFQ1dzsOMGPC4SI18Ve/cUrjStcfYNLcWVjhHa8F0a77pohs" \
                "N2DPV2sW+Y5zqnxeXAbX+9kbhiDNIkGbMdEJUfQHEBuuixxRpV3BcwmF065E" \
                "1RTCo6halg07rwsS3iTtlI"}
    application = Application(routes=routes, settings=settings)
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": os.path.join("ca.crt"),
        "keyfile": os.path.join("ca.key"),
    })

    http_server.listen(4443)
    ioloop = tornado.ioloop.IOLoop.instance()
    if debug:
        tornado.autoreload.start(ioloop)
    ioloop.start()


if __name__ == '__main__':
    logging.config.fileConfig('./conf.ini', disable_existing_loggers=False)
    LOGGER = logging.getLogger(__name__)
    debug = True
    main()

