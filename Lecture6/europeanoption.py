import numpy as np
from scipy.stats import norm


class EuropeanOption:
    def __init__(self, S, K, T, sig, r, call_or_put='C'):
        """
        :param S:交易所金融资产现价
        :param K:期权交割价格
        :param T:期权有效期
        :param sig: 年度化标准差
        :param r:连续复利计无风险利率Ｈ
        :param call_or_put:call_or_put
        """
        self.S = S
        self.K = K
        self.T = T
        self.sig = sig
        self.r = r
        self.call_or_put = call_or_put  # 'C' or 'Put'
        self.tmp = self.sig * np.sqrt(self.T)
        self.d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / self.tmp
        self.d2 = self.d1 - self.tmp

    def get_option_price(self, sig=None, iv=None):
        if iv:
            if self.call_or_put == 'C':
                return self.calculate_call_price(sig)
            else:
                return self.calculate_put_price(sig)

        if self.call_or_put == 'C':
            self.price = self.calculate_call_price(sig)
            self.delta = self.calculate_call_delta()
        else:
            self.price = self.calculate_put_price(sig)
            self.delta = self.calculate_put_delta()


    def calculate_iv(self, option_price):
        # TODO: calculate option implied vol using bisection method
        # while loop is good enough for a single option
        f = lambda sig: (self.get_option_price(sig, iv=True) - option_price)

        low = 0
        high = 10
        for _ in range(100):
            sig = (low + high) / 2
            if f(sig) == 0 or (high - low) / 2 < 1e-5:
                return sig
            if np.sign(f(sig)) == np.sign((f(low))):
                low = sig
            else:
                high = sig
        return (low + high) / 2

        # iv = 0
        # # TODO: use for instead of while for vectorzation
        # # 2^10 = 1024; 14
        # # 10. / 1000 = 0.001
        # return iv

    def calculate_call_price(self, sig=None):
        sig = sig if sig is not None else self.sig
        tmp = sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * sig ** 2) * self.T) / tmp
        d2 = d1 - tmp
        price = self.S * self.N(d1) - self.K * np.exp(-self.r * self.T) * self.N(d2)
        return price

    def calculate_put_price(self, sig=None):
        sig = sig if sig is not None else self.sig
        tmp = sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * sig ** 2) * self.T) / tmp
        d2 = d1 - tmp
        price = self.K * np.exp(-self.r * self.T) * (1 - self.N(d2)) - self.S * (1 - self.N(d1))
        return price

    @staticmethod
    def N(x):
        return norm.cdf(x)

    @staticmethod
    def n(x):
        return np.exp(-x ** 2) / np.sqrt(2 * np.pi)

    def calculate_call_delta(self):
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        delta = np.exp(-self.r * self.T) * self.N(d1)
        return delta

    def calculate_put_delta(self):
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        n = -1
        delta = n * norm.cdf(n * d1)
        return delta

    def calculate_gamma_test(self, h):
        option1 = EuropeanOption(self.S + h, self.K, self.T, self.sig, self.r, call_or_put=self.call_or_put)
        option2 = EuropeanOption(self.S - h, self.K, self.T, self.sig, self.r, call_or_put=self.call_or_put)
        gamma = (option1.get_option_price() - 2 * self.price + option2.get_option_price()) / h ** 2
        return gamma

    def calculate_gamma(self):
        """ Analytical solution """
        tmp = self.sig * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sig ** 2) * self.T) / tmp
        gamma = self.n(d1) * np.exp(-self.r * self.T) / (self.S * self.sig * np.sqrt(self.T))
        return gamma

    def calculate_vega(self):
        d1 = self.d1
        vega = (self.S * norm.pdf(d1) * np.sqrt(self.T)) / 100
        return vega

    def calculate_theta(self, is_call):
        if is_call is True:
            n = 1
        elif is_call is False:
            n = -1
        else:
            raise ValueError

        theta = (-1 * (self.S * norm.pdf(self.d1) * self.sig) / (2 * np.sqrt(self.T)) - n * self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(n * self.d2)) / 365
        return theta


if __name__ == '__main__':
    """ Test case:
    calculate greeks and implid vol of ATM call and put 20180102, at 10:00:00
    1. minute data
    2. find ATM, 510050.SH minute price, expired in Jan 2018
    3. Calculate greeks
    """
    pass
