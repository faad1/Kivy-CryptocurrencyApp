import kivy

kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import requests
import math



class CryptoCurrency(GridLayout):
    start = 1
    def __init__(self, **kwargs):
        super(CryptoCurrency, self).__init__(**kwargs)
        self.allCoinsList()

    def allCoinsList(self, page=None):

        grabIds = requests.get('https://api.coinmarketcap.com/v2/listings/')
        idsData = grabIds.json()
        totalRecords = len(idsData['data'])

        allCoins = []
        price = []
        marketCap = []
        changeHr = []

        limit = 100

        if page is not None:
            if page == 'pre' and self.start > 1:
                self.start = self.start - 100
            elif page == 'next' and self.start < 1601:
                self.start = self.start + 100

        r = requests.get("https://api.coinmarketcap.com/v2/ticker/?start={}&limit={}".format(self.start, limit))

        coinData = r.json()
        keys = coinData['data'].keys()

        for i in keys:

            price.append("${}".format(coinData['data'][i]['quotes']['USD']['price']))
            marketCap.append("${}".format(coinData['data'][i]['quotes']['USD']['market_cap']))
            changeHr.append("{}%".format(coinData['data'][i]['quotes']['USD']['percent_change_24h']))
            allCoins.append("{}".format(coinData['data'][i]['name']))

        if self.start == 1:
            self.ids.pre.disabled = True
        elif self.start == totalRecords + 1:
            self.ids.next.disabled = True
        else:
            self.ids.pre.disabled = False
            self.ids.next.disabled = False

        self.ids.coinList.data = [{"value": [w, x, y, z]} for w, x, y, z in zip(allCoins, price, marketCap, changeHr)]

    def searchCoin(self, searchText=None):

        r1 = requests.get('https://api.coinmarketcap.com/v2/listings/')

        json_data = r1.json()
        id_ = None
        total = len(json_data['data'])

        for i in range(total):
            if searchText is not None:
                if searchText.capitalize() == json_data['data'][i]['name'].capitalize():
                    id_ = json_data['data'][i]['id']
                    print(json_data['data'][i]['id'])

        r2 = requests.get('https://api.coinmarketcap.com/v2/ticker/{}'.format(id_))
        data = r2.json()

        self.ids.coinList.data = [{'value':[data['data']['name'],str(data['data']['quotes']['USD']['price']),
                                            str(data['data']['quotes']['USD']['market_cap']),
                                            str(data['data']['quotes']['USD']['percent_change_24h'])]}]
        print(data['data']['name'])
        print(data['data']['quotes']['USD']['price'])
        print(data['data']['quotes']['USD']['market_cap'])
        print(data['data']['quotes']['USD']['percent_change_24h'])

class CryptoCurrencyApp(App):

    # This returns the content we want in the window
    def build(self):
        # Return a label widget with Hello Kivy
        return CryptoCurrency();

if __name__ == "__main__":
    cyrptoApp = CryptoCurrencyApp()
    cyrptoApp.run()
