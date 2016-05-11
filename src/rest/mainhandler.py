#!/usr/bin/env python
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self, filename):
        self.render("index.html")

