import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import requests


class CryptoCurrency(GridLayout):

    def __init__(self, **kwargs):
        super(CryptoCurrency, self).__init__(**kwargs)
        self.topCoinsList()

    def topCoinsList(self):

        r = requests.get('https://api.coinmarketcap.com/v2/ticker/')

        json_data = r.json()
        keys = json_data['data'].keys()
        allCoins = []
        price = []
        marketCap = []
        changeHr = []

        for i in keys:

            #print("{}:  ${}".format(json_data['data'][i]['name'], json_data['data'][i]['quotes']['USD']['price']))

            price.append("${}".format(json_data['data'][i]['quotes']['USD']['price']))
            marketCap.append("${}".format(json_data['data'][i]['quotes']['USD']['market_cap']))
            changeHr.append("{}%".format(json_data['data'][i]['quotes']['USD']['percent_change_24h']))
            allCoins.append("{}".format(json_data['data'][i]['name']))

        self.ids.coinList.data = [{"value": [w,x,y,z]} for w,x,y,z in zip(allCoins, price, marketCap,changeHr)]

class CryptoCurrencyApp(App):

    # This returns the content we want in the window
    def build(self):
        # Return a label widget with Hello Kivy
        return CryptoCurrency();

if __name__ == "__main__":
    cyrptoApp = CryptoCurrencyApp()
    cyrptoApp.run()
