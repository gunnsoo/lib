# -*- coding: utf-8 -*-

import json
import requests
import time
import hmac
import hashlib
import urllib
from .exception import AuthException


class API(object):

    def __init__(self, api_key=None, api_secret=None):
        self.api_url = "https://coincheck.com"
        self.api_key = api_key
        self.api_secret = api_secret

    def request(self, endpoint, method="GET", params=None):
        url = self.api_url + endpoint
        body = ""
        auth_header = None

        if method == "POST":
            body = json.dumps(params)
        else:
            if params:
                body = "?" + urllib.parse.urlencode(params)

        if self.api_key and self.api_secret:
            nonce = str(int(time.time() * 1000000000))
            api_secret = str.encode(self.api_secret)
            message = str.encode(nonce + url + body)
            signature = hmac.new(api_secret,
                                   message,
                                   hashlib.sha256).hexdigest()
            auth_header = {
               'ACCESS-KEY'      : self.api_key,
               'ACCESS-NONCE'    : nonce,
               'ACCESS-SIGNATURE': signature
            }

        try:
            with requests.Session() as s:
                if auth_header:
                    s.headers.update(auth_header)

                if method == "GET":
                    response = s.get(url, params=params)
                else:  # method == "POST":
                    response = s.post(url, data=json.dumps(params))
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

    def ticker(self, **params):
        endpoint = "/api/ticker"
        return self.request(endpoint, params=params)

    def trades_history(self, **params):
        endpoint = "/api/trades"
        return self.request(endpoint, params=params)

    def order_books(self, **params):
        endpoint = "/api/order_books"
        return self.request(endpoint, params=params)

    def exchange_rate(self, **params):
        endpoint = "/api/exchange/orders/rate"
        return self.request(endpoint, params=params)

    def shop_rate(self, pair, **params):
        endpoint = "/api/rate" + str(pair)
        return self.request(endpoint, params=params)

    """HTTP Private API"""

    def order(self, **params):
        endpoint = "/api/exchange/orders"
        return self.request(endpoint, method="POST", params=params)

    def open_orders(self, **params):
        endpoint = "/api/exchange/orders/opens"
        return self.request(endpoint, params=params)

    def delete_orders(self, order_id, **params):
        endpoint = "/api/exchange/orders/" + str(order_id)
        return self.request(endpoint, method="DELETE", params=params)

    def order_history(self, **params):
        endpoint = "/api/exchange/orders/transactions"
        return self.request(endpoint, params=params)

    def leverage_positions(self, **params):
        endpoint = "/api/exchange/leverage/positions"
        return self.request(endpoint, params=params)

    def balance(self, **params):
        endpoint = "/api/accounts/balance"
        return self.request(endpoint, params=params)

    def leverage_balance(self, **params):
        endpoint = "/api/accounts/leverage_balance"
        return self.request(endpoint, params=params)

    #TO DO:エラーが出るので直す
    def sending_history(self, **params):
        endpoint = "/api/send_money"
        return self.request(endpoint, params=params)

    #TO DO:エラーが出るので直す
    def deposit_history(self, **params):
        endpoint = "/api/deposit_money"
        return self.request(endpoint, params=params)

    def account(self, **params):
        endpoint = "/api/accounts"
        return self.request(endpoint, params=params)
