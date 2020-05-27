#!/usr/bin/python3

""" Option basic info
"""
class BaseOption:
    def __init__(self, security_code, K, expire_date, call_or_put, contract_unit=10000):
        self.security_code = security_code
        self.K = K
        self.expire_date = expire_date
        self.call_or_put = call_or_put
        self.contract_unit = contract_unit