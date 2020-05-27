import numpy as np
import baseoption
from scipy.stats import norm

class EuropeanOption:
    def __init__(self, S, K, T, sig, r, call_or_put='C'):
        self.S = S
        self.K = K
        self.T = T
        self.sig = sig
        self.r = r
        self.call_or_put = call_or_put # 'C' or 'Put'
    
    def get_option_price(self):
        if self.call_or_put == 'C':
            self.price = self.calculate_call_price()
            self.delta = self.calculate_call_delta()
        else:
            self.price = self.calculate_put_price()
            self.delta = self.calculate_put_delta()

    def calculate_iv(self, option_price):
        # TODO: calculate option implied vol using bisection method
        # while loop is good enough for a single option
        low = 0 
        high = 10
        while mid - low > 1e-5:
            pass
        iv = 0
        # TODO: use for instead of while for vectorzation
        # 2^10 = 1024; 14
        # 10. / 1000 = 0.001
        return iv

    def calculate_call_price(self):
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        d2 = d1 - tmp
        price = self.S * self.N(d1) - self.K * np.exp(-self.r * self.T) * self.N(d2)
        return price

    def calculate_put_price(self):
        # TODO
        price = 0
        return price

    @staticmethod
    def N(x):
        return norm.cdf(x)

    @staticmethod
    def n(x):
        return np.exp(-x**2) / np.sqrt(2 * np.pi)

    def calculate_call_delta(self):
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        delta = np.exp(-self.r * self.T) * self.N(d1) 
        return delta

    def calculate_put_delta(self):
        # TODO
        delta = 0
        return delta
    
    def calculate_gamma_test(self, h):
        option1 = EuropeanOption(self.S+h, self.K, self.T, self.sig, self.r, call_or_put=self.call_or_put)
        option2 = EuropeanOption(self.S-h, self.K, self.T, self.sig, self.r, call_or_put=self.call_or_put)
        gamma = (option1.get_option_price() - 2 * self.price + option2.get_option_price()) / h**2
        return gamma

    def calculate_gamma(self):
        """ Analytical solution """
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        gamma = self.n(d1) * np.exp(-self.r * self.T) / (self.S * self.sig * np.sqrt(self.T))
        return gamma

    def calculate_vega(self):
        # TODO
        vega = 0
        return vega

    def calculate_theta(self):
        # TODO
        theta = 0
        return theta

if __name__ == '__main__':
    """ Test case:
    calculate greeks and implid vol of ATM call and put 20180102, at 10:00:00
    1. minute data
    2. find ATM, 510050.SH minute price, expired in Jan 2018
    3. Calculate greeks
    """
    pass