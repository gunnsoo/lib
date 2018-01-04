# -*- coding: utf-8 -*-

import json
import requests
import time
import hmac
import hashlib
import urllib
from datetime import datetime
from decimal import Decimal
from .exception import AuthException


class API(object):

    def __init__(self, api_key=None, api_secret=None):
        self.api_url = "https://api.zaif.jp"
        self.api_key = api_key
        self.api_secret = api_secret

    def get_nonce(self):
        now = datetime.now()
        nonce = str(int(time.mktime(now.timetuple())))
        microseconds = '{0:06d}'.format(now.microsecond)
        return Decimal(nonce + '.' + microseconds)

    def request(self, endpoint, method="GET", func_name=None, params=None):
        url = self.api_url + endpoint
        auth_header = None

        if self.api_key and self.api_secret:
            params["nonce"] = self.get_nonce()
            params["method"] = func_name
            params = urllib.parse.urlencode(params)

            signature = hmac.new(bytearray(self.api_secret.encode('utf-8')),
                         digestmod=hashlib.sha512)
            signature.update(params.encode('utf-8'))

            auth_header = {
                "key": self.api_key,
                "sign": signature.hexdigest()
            }

        try:
            with requests.Session() as s:
                if auth_header:
                    s.headers.update(auth_header)

                if method == "GET":
                    response = requests.get(url, params=params)
                else:  # method == "POST":
                    response = s.post(url, data=params)
        except requests.RequestException as e:
            print(e)
            raise e

        if response.status_code != 200:
            response.raise_for_status()

        content = ""
        if len(response.content) > 0:
            content = json.loads(response.content.decode("utf-8"))

        return content

    """HTTP Public API"""

    def currencies(self, params):
        endpoint = "/api/1/currencies/" + params
        return self.request(endpoint)

    def currency_pairs(self, params):
        endpoint = "/api/1/currency_pairs/" + params
        return self.request(endpoint)

    def last_price(self, params):
        endpoint = "/api/1/last_price/" + params
        return self.request(endpoint)

    def ticker(self, params):
        endpoint = "/api/1/ticker/" + params
        return self.request(endpoint)

    def trades(self, params):
        endpoint = "/api/1/trades/" + params
        return self.request(endpoint)

    def depth(self, params):
        endpoint = "/api/1/depth/" + params
        return self.request(endpoint)

    """HTTP Private API"""

    def get_info(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="get_info", params=params)

    def get_info2(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="get_info2", params=params)

    def get_personal_info(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="get_personal_info", params=params)

    def get_id_info(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="get_id_info", params=params)

    def trade_history(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="trade_history", params=params)

    def active_orders(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="active_orders", params=params)

    def trade(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="trade", params=params)

    def cancel_order(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="cancel_order", params=params)

    def withdraw(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="withdraw", params=params)

    def deposit_history(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="deposit_history", params=params)

    def withdraw_history(self, **params):
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/tapi"
        return self.request(endpoint, method="POST", func_name="withdraw_history", params=params)
