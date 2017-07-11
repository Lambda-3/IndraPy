# -*- coding: utf-8 -*-

# Python Indra Client
# --------------------------------------------------------------------
# Copyright (C) 2016 - 2017 Lambda^3
# --------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import requests
import logging

from indra import __version__ as indra_client_version


logger = logging.getLogger(__name__)


class RelatednessRequest(object):

    def __init__(self,
                 model='W2V',
                 language='EN',
                 corpus='wiki-2014',
                 score_function='COSINE'):

        self.model = model
        self.language = language
        self.corpus = corpus
        self.score_function = score_function
        self.pairs = list()

    def add(self, pair):
        self.pairs.append(pair)

    @property
    def payload(self):
        return dict(corpus=self.corpus, model=self.model, language=self.language,
                    scoreFunction=self.score_function, pairs=[dict(t1=t1, t2=t2) for t1, t2 in self.pairs])


class RelatednessResponse(object):

    def __init__(self, response_dict):
        self.__response_dict = response_dict

    def getscore(self, t1=None, t2=None):
        if t1 is not None and t2 is not None:
            res = [p['score'] for p in self.__response_dict['pairs'] if p['t1'] == t1 and p['t2'] == t2]
            return res[0] if res else None
        if t1 is None and t2 is None:
            return self.__response_dict['pairs']
        if t1 is None:
            return {p['t1']: p['score'] for p in self.__response_dict['pairs'] if p['t2'] == t2}
        if t2 is None:
            return {p['t2']: p['score'] for p in self.__response_dict['pairs'] if p['t1'] == t1}


class IndraClient(object):
    public_endpoint = 'http://indra.lambda3.org'
    headers = {'User-Agent': "IndraClient/{}".format(indra_client_version)}

    def __init__(self, base_url=public_endpoint):
        self.__baseurl = base_url
        if base_url == self.public_endpoint:
            logger.warning("Using PUBLIC server @ %s, don't use in production.", base_url)
        else:
            logger.info("Indra Server @ %s", base_url)

    def relatedness(self, request):
        url = "{}/relatedness".format(self.__baseurl)
        res = requests.post(url, json=request.payload)
        res.raise_for_status()
        return RelatednessResponse(res.json())


def main():
    print("Hello World")
