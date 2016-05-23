#    drowse
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

'''
Drowse is a slim REST client for python
'''

import logging
import urllib
import requests

__all__ = ['API', 'Resource']
__version__ = '0.2.0'
__author__ = 'Lorenzo Gaggini'
__contributors__ = []


USER_AGENT = 'python-drowse/%s' % __version__

logging.basicConfig(level=logging.INFO)


class Resource(object):

    # TODO: some attrs could be on a inner meta class
    # so Resource can have a minimalist namespace  population
    # and minimize collitions with resource attributes
    def __init__(self, uri, api, id):
        self.api = api
        self.uri = uri
        self.url = api.base_url + uri
        self.id = id
        self.attrs = {}

    def __getattr__(self, name):
        '''
        Resource attributes (eg: user.name) have priority
        over inner rerouces (eg: users(id=123).applications)
        '''
        logging.debug('getattr.name: %s' % name)
        # Reource attrs like: user.name
        if name in self.attrs:
            return self.attrs.get(name)
        logging.debug('self.url: %s' % self.url)
        # Inner resoruces for stuff like: GET /users/{id}/applications
        key = self.uri + '/' + name
        logging.info('Accessing inner resource with uri: %s' % key)
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api,
                                           id=None)
        return self.api.resources[key]

    def __call__(self, id=None):
        logging.debug('call.id: %s' % id)
        logging.debug('call.self.url: %s' % self.url)
        if id is None:
            return self
        key = self.uri + '/' + str(id)
        self.api.resources[key] = Resource(uri=key,
                                           api=self.api,
                                           id=id)
        logging.debug(self.api.resources)
        return self.api.resources[key]

    # GET /resource
    # GET /resource/id?arg1=value1&...
    def get(self, **kwargs):
        url = self.url
        if len(kwargs) > 0:
            url = '%s?%s' % (url, urllib.urlencode(kwargs))
        logging.info('GET %s ' % url)
        response = requests.get(url, auth=self.api.auth,
                                headers=self.api.customHeaders,
                                verify=self.api.verify)
        response.raise_for_status()
        return response.json()

    # POST /resource
    def post(self, json):
        logging.info('POST %s ' % self.url)
        response = requests.post(self.url, auth=self.api.auth,
                                 headers=self.api.customHeaders,
                                 json=json, verify=self.api.verify)
        response.raise_for_status()
        return response.json()

    # PUT /resource/id
    def put(self, json):
        if self.id is None:
            logging.error('id is mandatory for put')
            return
        logging.info('PUT %s ' % self.url)
        response = requests.put(self.url, auth=self.api.auth,
                                headers=self.api.customHeaders,
                                json=json, verify=self.api.verify)
        response.raise_for_status()
        return response.json()

    # DELETE /resource/id
    def delete(self, json=None):
        if self.id is None:
            logging.error('id is mandatory for delete')
            return
        logging.info('DELETE %s ' % self.url)
        response = requests.delete(self.url, auth=self.api.auth,
                                   headers=self.api.customHeaders,
                                   json=json, verify=self.api.verify)
        response.raise_for_status()


class API(object):
    def __init__(self, base_url, authUser=None, authKeyHeader=None,
                 authSecret=None, authSecretHash=True, verify=True):
        self.base_url = base_url + \
                        '/' if not base_url.endswith('/') else base_url
        self.resources = {}
        self.auth = None
        self.customHeaders = {'User-Agent': USER_AGENT}
        self.verify = verify

        self._auth(authUser, authKeyHeader, authSecret, authSecretHash)
        logging.debug('http auth %s' % self.auth)
        logging.debug('requests customHeaders' % self.customHeaders)

    def __getattr__(self, name):
        logging.debug('API.getattr.name: %s' % name)

        key = name
        if key not in self.resources:
            logging.info('Accessing resource with uri: %s' % key)
            self.resources[key] = Resource(uri=key,
                                           api=self,
                                           id=None)
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
            self.customHeaders[authKeyHeader] = authSecret
