from bs4 import BeautifulSoup
import requests

# this is the module to read the risk free interest data from the web

class RiskFreeRate:
    
    @classmethod
    def get_risk_free_rate(cls):
        yahooFinance = "https://finance.yahoo.com/quote/%5ETNX/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAABZWJngYFyrgd-F7IrctueRrs82R7rpUN3hLDt0sNSjGVV5rh_AUDxTTnDqj1G7sez5akPy9cKwFGAZ8rwD3myVlmANyy70yRKkfEL3l_vNbfAj7VU692fFj3FAmf7gwtfvVR264EOag9IUEorNjc-14WTiLeXG28f4ajYuTzmyU"
        r = requests.get(yahooFinance).text
        soup = BeautifulSoup(r)
        s = soup.find('table').find_all('a', {'external text'})
        riskFreeRate = soup.find('fin-streamer',{'data-symbol':'^TNX'})['value']
        return float(riskFreeRate)/100