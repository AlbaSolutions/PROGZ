#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 12:54:24 2020

@author: AlbaSol
"""

import requests
class webber(requests.Session):
    auth = None
    __attrs__ = requests.Session.__attrs__ + ['base_url']

    def __init__(self,myurl):
        """Handle HTTP session related work."""
        super(webber, self).__init__()
        self.headers.update({
            # Only accept JSON responses
            'Accept': 'application/vnd.api+json',
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always send JSON
            'Content-Type': "application/json",
            # Custom User-Agent string
            'User-Agent': 'josfclient v0.0.1',
            })
        self.base_url = myurl


    def basic_auth(self, username, password):
        self.auth = (username, password)
        if 'Authorization' in self.headers:
            self.headers.pop('Authorization')

    def tok_auth(self, tok):
        self.token = tok
        if 'Authorization' in self.headers:
            self.headers.pop("Authorization: Bearer <"+self.token+">")

    def build_url(self, *args):
        parts = [self.base_url]
        parts.extend(args)
        # canonical OSF URLs end with a slash
        return '/'.join(parts) + '/'

    def put(self, url, *args, **kwargs):
        response = super(webber, self).put(url, *args, **kwargs)
        if response.status_code == 401:
            raise Exception
        return response

    def get(self, url, *args, **kwargs):
        response = super(webber, self).get(url, *args, **kwargs)
        if response.status_code == 401:
            raise Exception
        return response

    def DLfile(self,filereq,dest):
        with open(dest, "wb") as localfile:
            localfile.write(self.get(filereq).content)

    def ULnewfile(self,upfile,prjid,data):
        #pth ="http://files.osf.io/v1/resources/<node_id>/providers/<provider_id>/<id_or_path>"
        pth ="https://files.osf.io/v1/resources/"
        pth+=prjid
        pth+="/providers/osfstorage/?kind=file&name="
        pth+=upfile
        self.put(pth,data)
