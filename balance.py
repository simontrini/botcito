import logging
from datetime import datetime
class Balance :
    #Balance clase para agrupar los saldos del cliente
    #estable moneda estable para el intercambion 
    def __init__(self, client = None,estable='BUSD',moneda='BTC'):
        self.client = client
        self.estable = estable
        self.moneda = moneda        
        #self.saldo = self.client.get_asset_balance(asset= estable)
        #self.saldo = self.setEstable(self.estable)
    def getEstable(self):
        return self.getSaldo(self.estable)
    def setEstable(self,nuevaEstable):
        self.estable = nuevaEstable
        #self.saldo = self.getSaldo(self.estable)
        return     
    def getMoneda(self):
        return self.getSaldo(self.moneda)
    def setMoneda(self,nuevaEstable):
        self.estable = nuevaEstable
        return    
    def getSaldo(self, moneda):        
        return self.client.get_asset_balance(asset= moneda)    
    def setCliente(self,client):
        self.client = client
        return    
    def mostrar(self):
        saldo = self.getEstable()
        libre = "{:.6f}".format(float(saldo['free']))
        bloqueado = "{:.6f}".format(float(saldo['locked']))
        
        #k = "{:.2f}".format(float(self.kdjObj.k))
        #d = "{:.2f}".format(float(self.kdjObj.d))
        #j = "{:.2f}".format(float(self.kdjObj.j))
        #arriba = '      '
        #abajo = 'abajo '          
        #if self.kdjObj.Nivel == 'arriba':
            #arriba = 'arriba'
            #abajo = '      '
        #if self.kdjObj.Nivel == 'NiNi':
            #arriba = '      '
            #abajo = '      '        
        #saldoooo {'asset': 'BUSD', 'free': '10000.00000000', 'locked': '0.00000000'}
        salida = f"""
***********************{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}********************************************
** Moneda   |  Libre: |   Bloqueado:  |                                               **
**   {saldo['asset']}   | {libre}   |  { bloqueado }      |                                               **
********************************************************************************************
"""
        logging.info(salida)
        print(salida)   
    #def escribirLog(self):
        #logging.info('%s:%s | RSI:%s | K:%s | D:%s | J:%s | Nivel:%s | Compra:%s | Venta:%s',
                     #'BTC',
                     #"{:.4f}".format(float(self.getPrecioActual())),
                     #"{:.2f}".format(float(self.rsi)),
                     #"{:.2f}".format(float(self.kdjObj.k)),
                     #"{:.2f}".format(float(self.kdjObj.d)),
                     #"{:.2f}".format(float(self.kdjObj.j)),
                     #self.kdjObj.Nivel,
                     #1,
                     #1)
    
def main():
    from binance.client import Client
    api_key    = 'RAGCg4uGonc8ox0nKOZxnK7Ejx8tUXL5VlQ16l9PF46FvzuJeH46n408ekEsE9iw'
    api_secret = 'ZzSYviWTS5BtrA27MQmZ5Ez702DDKOv0il91Sbp4UM1G3V8QuOWR9kMsgShWoNyY'    
    print('conectando API de testnet')
    client = Client(api_key, api_secret,testnet=True) 
    #****
    #api_key    = 'a9lsESnZ2WD2fMj7OlHYf8IkxvEfNB0HXK01zkYyeY74oOEHUgLfbI3uypmKfAS5'
    #api_secret = 'PCQr84bWjXhRivvee5gG5OkI6WjalinuVyDqmHs7YF3yhokW1DipWUFk1ohwTUfj'     
    #print('conectando API de mainnet') 
    #client = Client(api_key, api_secret,testnet=False) 
    #****
    #balance = Balance(estable='BTC')
    #***************************************************
    balance = Balance(estable='BUSD')
    balance.setCliente(client)
    saldo = balance.getEstable()['free']
    balance.mostrar() 
    balance = Balance(estable='BTC')
    balance.setCliente(client)
    saldo = balance.getEstable()['free']
    balance.mostrar()  
    #***************************************************
    #info = client.get_symbol_info('BNBUSDT')
    ##info = self.client.get_symbol_info('%sUSDT' % coin)
    #step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
    #step_size = '%.8f' % step_size
    #step_size = step_size.rstrip('0')
    #decimals = len(step_size.split('.')[1])   
    #print(decimals)
    #info = client.get_all_orders(symbol='BTCBUSD', limit=100)
    #info = client.get_order(symbol='BTCBUSD',orderId='6826954')  
    #info = client.get_open_orders(symbol='BTCBUSD')
    #info = client.get_all_orders(symbol='BTCBUSD', limit=20)
    #print(info)
    #info = client.get_exchange_info()['symbols']
    #for i in range(len(info)):
        #print(info[i]['symbol'],info[i]['type'],info[i]['status'])    
if __name__ == '__main__':
    main()