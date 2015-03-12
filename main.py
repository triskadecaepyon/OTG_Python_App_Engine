#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import logging
import webapp2

# This specific section allows for python
# packages in folders to be accessible from
# The view and worker scope.  This allows for
# code isolation and reduced coupling
import sys
sys.path.insert(0, 'support_packages')
sys.path.insert(0, 'backend_python_files')

from google.appengine.api import users
from google.appengine.ext.webapp import template

# This imports the worker.py into the scope of the
# view handlers
import worker

# --------------------------------------------------------------------------
# Page Rendering system
# Based on multiple sources, books, and the Django template engine.
# --------------------------------------------------------------------------


def render_page(handler, tname='front_page.htm', values={}):
    temp = os.path.join(
        os.path.dirname(__file__), 'templates/' + tname)
    if not os.path.isfile(temp):
        logging.info("render error for : " + str(tname))
        return False

    newval = dict(values)
    newval['path'] = handler.request.path
    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)

    return True


# --------------------------------------------------------------------------
# Views and classes
#
# The main views should encapsulate the abstract items required to
# render them.  Functionality and logic behind them should be placed in the
# worker role, as shown by worker.register_user(user).  This allows for less
# semantics when changing out back end code.
# --------------------------------------------------------------------------


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout = users.create_logout_url('/')
            name = users.User.email(user)
            # Register user; will return if already registered
            worker.register_user(user)
            render_page(self, 'front_page.htm', {'logout': logout, 'name': name})
        else:
            login = users.create_login_url(self.request.uri)
            render_page(self, 'front_page.htm', {'login': login})

    def post(self):
        # Use this to handle POST calls within Main Handler
        print "Post on MainHandler (Fill this method in or delete if needed)"

# Adding additional classes: For each additional "View", add classes and matching
# url routers below in the webapp2.WSGIApplication list.

# --------------------------------------------------------------------------
# URL class handler
# Contains the classes and url regex matches to url handlers
# --------------------------------------------------------------------------

app = webapp2.WSGIApplication([
                                  ('/', MainHandler)
                              ], debug=True)

