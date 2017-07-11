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


import unittest
import json

from indra.client import RelatednessRequest, RelatednessResponse, IndraClient


class RelatednessTest(unittest.TestCase):

    def setUp(self):
        self.client = IndraClient()

    def test_simple_call(self):
        request = RelatednessRequest()
        request.pairs.extend([("love", "hate"), ("love", "peace"), ("love", "sex")])
        response = self.client.relatedness(request)
        print(response)


class ResponseAPITest(unittest.TestCase):

    def setUp(self):
        self.response = RelatednessResponse(json.loads("""{
            "corpus": "wiki-2014",
            "model": "W2V",
            "scoreFunction": "COSINE",
            "language": "EN",
    
            "pairs": [{
                "t1": "love",
                "t2": "hate",
                "score": 0.58
            }, {
                "t1": "love",
                "t2": "sex",
                "score": 0.31
            }, {
                "t1": "love",
                "t2": "peace",
                "score": 0.098
            }]
        }
        """))

    def test_relatedness_response0(self):
        self.assertEqual(self.response.getscore(),
                         [{'t2': 'hate', 't1': 'love', 'score': 0.58},
                          {'t2': 'sex', 't1': 'love', 'score': 0.31},
                          {'t2': 'peace', 't1': 'love', 'score': 0.098}])

    def test_relatedness_response1(self):
        self.assertEqual(self.response.getscore(t1='love'), {'sex': 0.31, 'hate': 0.58, 'peace': 0.098})

    def test_relatedness_response2(self):
        self.assertEqual(self.response.getscore('unknown'), {})

    def test_relatedness_response3(self):
        self.assertEqual(self.response.getscore(t2='love'), {})

    def test_relatedness_response4(self):
        self.assertEqual(self.response.getscore(t2='peace'), {'love': 0.098})
