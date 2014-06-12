#!/usr/bin/env python

import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.escape import json_encode 
import logging

#Mongo
from mongoengine import *
import models
import bson
from bson import json_util
import csv
import json
import re
import bcrypt
from datetime import datetime
from utils import *
from handlers.handlers import *
from handlers.admin_handlers import *

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

#Connect to mongo
connect('db', host=os.environ.get('MONGOLAB_URI'))

# application settings and handle mapping info
class Application(tornado.web.Application):
    def __init__(self):
        self.stats = StatsGenerator()
        self.files = FileGenerator()
        handlers = [
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
            (r"/(?:([A-Za-z]{2})/)?", MainHandler),
            (r"/2/?", MainHandler2),
            # (r"/sankeyChart/?", SankeyChartHandler),
            (r"/submitCompany/?", SubmitCompanyHandler),
            (r"/validate/?", ValidateHandler),
            (r"/edit/([a-zA-Z0-9]{24})/?", EditCompanyHandler),
            (r"/addData/([a-zA-Z0-9]{24})/?", SubmitDataHandler),
            # (r"/media/?", MediaHandler),
            (r"/delete/([a-zA-Z0-9]{24})/?", DeleteCompanyHandler),
            (r"/admin/companies/?", CompanyAdminHandler),
            (r"/admin/agencies/?", AgencyAdminHandler),
            (r"/admin/company-edit/([a-zA-Z0-9]{24})/?", AdminEditCompanyHandler),
            (r"/admin/agency-edit/([a-zA-Z0-9]{24})/?", AdminEditAgencyHandler),
            (r"/admin/agency-delete/([a-zA-Z0-9]{24})/?", DeleteAgencyHandler),
            (r'/(?:([A-Za-z]{2})/)?about/?', AboutHandler),
            (r"/resources/?", ResourcesHandler),
            (r"/(?:([A-Za-z]{2})/)?stats/?", FindingsHandler),
            (r"/chart/?", ChartHandler),
            (r"/download/?", DownloadHandler),
            (r'/download/(.*)/?',tornado.web.StaticFileHandler, {'path':os.path.join(os.path.dirname(__file__), 'static')}),
            (r"/candidates/?", CandidateHandler),
            (r"/list/?", ListHandler),
            (r'/thanks/?', ThanksHandler),
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
            (r'/register/?', RegisterHandler),
            (r"/([^/]+)/?", CompanyHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                "datetime": datetime},
            debug=True,
            cookie_secret=os.environ.get('COOKIE_SECRET'),
            xsrf_cookies=True,
            login_url="/login"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()









































