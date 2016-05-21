#    Python Nap
#
#    Copyright (c) 2016 Lorenzo Gaggini
#    Based on a work by (c) 2008 Rafael Xavier de Souza    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Nap is a slim REST client for python
"""

#__all__ = ["API", "Resource"]
__version__ = "0.0.1"
__author__ = "Lorenzo Gaggini"
__contributors__ = []

import logging
import urllib
import requests

USER_AGENT = "python-nap/%s" % __version__

logging.basicConfig(level=0)


class Resource(object):

    # TODO: some attrs could be on a inner meta class
    # so Resource can have a minimalist namespace  population
    # and minimize collitions with resource attributes
    def __init__(self, uri, api):
        #logging.info("init.uri: %s" % uri)
        self.api = api
        self.uri = uri
        self.url = api.base_url + uri
        self.id = None
        self.attrs = {}

    def __getattr__(self, name):
        """
        Resource attributes (eg: user.name) have priority
        over inner rerouces (eg: users(id=123).applications)
        """
        #logging.info("getattr.name: %s" % name)
        # Reource attrs like: user.name
        if name in self.attrs:
            return self.attrs.get(name)
        #logging.info("self.url: %s" % self.url)
        # Inner resoruces for stuff like: GET /users/{id}/applications
        key = self.uri + '/' + name
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api)
        return self.api.resources[key]

    def __call__(self, id=None):
        #logging.info("call.id: %s" % id)
        #logging.info("call.self.url: %s" % self.url)
        if id == None:
            return self
        self.id = str(id)
        key = self.uri + '/' + self.id
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api)
        return self.api.resources[key]

    # GET /resource
    # GET /resource/id?arg1=value1&...
    def get(self, **kwargs):
        if self.id == None:
            url = self.url
        else:
            url = self.url + '/' + str(self.id)
        if len(kwargs) > 0:
            url = "%s?%s" % (url, urllib.urlencode(kwargs))
        return requests.get(url, auth=self.api.auth, headers=self.api.customHeaders, verify=self.api.verify).json()

    # POST /resource
    def post(self, json):
        return requests.post(self.url, auth=self.api.auth, headers=self.api.customHeaders, json=json, verify=self.api.verify).json()

    # PUT /resource/id
    def put(self, json):
        if not self.id:
            return
        url = self.url + '/' + str(self.id)
        return requests.put(url, auth=self.api.auth, headers=self.api.customHeaders, json=json, verify=self.api.verify).json()

    # DELETE /resource/id
    def delete(self, id, json):
        url = self.url + '/' + str(id)
        return request.delete(url, headers=headers, json=json, verify=self.api.verify).json();


class API(object):
    def __init__(self, base_url, authUser=None, authKeyHeader=None, authSecret=None, authSecretHash=True, verify=True):
        self.base_url = base_url + '/' if not base_url.endswith('/') else base_url
        self.resources = {}
        self.auth = None;
        self.customHeaders = None;
        self.verify = verify

        self._auth(authUser, authKeyHeader, authSecret, authSecretHash)

    def __getattr__(self, name):
        #logging.info("API.getattr.name: %s" % name)
        
        key = name
        if not key in self.resources:
            #logging.info("Creating resource with uri: %s" % key)
            self.resources[key] = Resource(uri=key,
                                           api=self)
        return self.resources[key]

    def _auth(self, authUser, authKeyHeader, authSecret, authSecretHash):
        # basic http auth
        if authUser and not authSecretHash:
            self.auth = requests.auth.HTTPBasicAuth(authUser, authSecret)
            return
        # digest http auth
        elif authUser and authSecretHash:
            self.auth = requests.auth.HTTPDigestAuth(authUser, authSecret)
            return
        # custom key auth
        elif authKeyHeader:
            self.customHeaders = {authKeyHeader: authSecret}
