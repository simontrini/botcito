from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
class CompraVenta :
    #cliente = ''
    def __init__(self,cliente, simbolo):
        self.cliente = cliente
        self.simbolo = simbolo
        #print(help(self.cliente))
    def comprarMarket (self,cantidad):
        try:
            market_order = self.cliente.order_market_buy(symbol=self.simbolo, quantity=cantidad)
            #market_order = self.cliente.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
            #self.mostrar(market_order)
        except BinanceAPIException as e:
            # error handling goes here
            print('comprarMarket',e)
        except BinanceOrderException as e:
            # error handling goes here
            print('comprarMarket',e)
        return market_order

    def ventaMarket (self,cantidad):
        try:
            market_order = self.cliente.order_market_sell(symbol=self.simbolo, quantity=cantidad)
            #market_order = self.cliente.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
            #self.mostrar(market_order)
        except BinanceAPIException as e:
            # error handling goes here
            print('ventaMarket',e)
        except BinanceOrderException as e:
            # error handling goes here
            print('ventaMarket',e)
        return market_order

    def comprarStopLimit (self,cantidad,precio):
        try:
            #help(self.cliente)
            limit_order = self.cliente.order_limit_buy(symbol=self.simbolo, quantity=cantidad, price=precio)
            #market_order = self.cliente.order_market_buy(symbol=self.simbolo, quantity=cantidad)
            #market_order = self.cliente.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
            #self.mostrar(market_order)
        except BinanceAPIException as e:
            # error handling goes here
            print('comprarStopLimit',e)
        except BinanceOrderException as e:
            # error handling goes here
            print('comprarStopLimit',e)
        return limit_order

    def venderStopLimit (self,cantidad,precio):
        try:
            #help(self.cliente)
            limit_order = self.cliente.order_limit_sell(symbol=self.simbolo, quantity=cantidad, price=precio)
        except BinanceAPIException as e:
            # error handling goes here
            print('venderStopLimit',e)
        except BinanceOrderException as e:
            # error handling goes here
            print('venderStopLimit',e)
        return limit_order
def main():
    from binance.client import Client
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini') 
    api_key    = config['api']['api_key']
    api_secret = config['api']['api_secret']  
    print('conectando API de testnet',config['api']['test'] )
    client = Client(api_key, api_secret,testnet=config['api']['test'])
    balance = client.get_asset_balance(asset='USDT')
    print(balance)
    compraVeta = CompraVenta(client,'BTCUSDT')
    order = compraVeta.comprarMarket(0.047111)
    print('compra',order)

    #order = compraVeta.ventaMarket(1)
    #print('venta',order)
    ######################

    #order = compraVeta.venderStopLimit(0.00110 , 52000.00)
    #print('compra',order)
if __name__ == '__main__':
    main()
