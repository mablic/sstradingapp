from lib2to3.pgen2.literals import simple_escapes
from math import log, sqrt, pi, exp
from scipy.stats import norm
from .riskFreeInterest import RiskFreeRate

class PriceModel:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price = 0
        self.riskFreeRate = RiskFreeRate.get_risk_free_rate()

    def get_price(self):
        return self.price

class OptionModel(PriceModel):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.d1 = 0
        self.d2 = 0
        self.price = []
    
    def __d1(self, S, K, T, sigma):
        return (log(S/K) + (self.riskFreeRate+sigma**2/2.0)*T)/(sigma*sqrt(T))
    
    def __d2(self, d1, T, sigma):
        return d1 - sigma * sqrt(T)

    def set_base(self, S, K, T, sigma):
        self.d1 = self.__d1(S, K, T, sigma)
        self.d2 = self.__d2(self.d1, T, sigma)

    def black_scholes_call(self, S, K, T, sigma):
        self.price = norm.cdf(self.d1)*S-norm.cdf(self.d2)*K*exp(-self.riskFreeRate*T)
        return self.price
    
    def black_scholes_put(self, S, K, T, sigma):
        self.price = K*exp(-self.riskFreeRate*T)-S+self.black_scholes_call(S, K, T, sigma)
    
    def get_price(self):
        return self.price

if __name__ == '__main__':
    print(norm.cdf(5))