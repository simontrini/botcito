# https://github.com/simontrini/botcito.git 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
import logging
from clienteBinance import clienteBinance
from indices import *
from balance import Balance 
from doctor import *
from time import sleep
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
#logging.basicConfig(format='%(asctime)s %(message)s')
class BotCito :
    def __init__(self, moneda, par, periodo):
        logging.basicConfig(filename='logKDJ%s.log'% moneda, encoding='utf-8', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')        
        self.moneda = moneda
        self.par = par
        self.simbolo = moneda + par 
        self.periodo = periodo 
        self.clienteBinan = clienteBinance(self.simbolo, periodo)
        self.indices = Indices()
        self.balance = Balance(None,None,moneda)
        self.doctor = Doctor()
    #.......   moneda    
    def setMoneda(self, moneda):
        self.moneda = moneda
        return
    
    def getMoneda(self):
        return self.moneda  
    #.......   moneda 
    #.......   par    
    def setPar(self, par):
        self.par = par
        return
    
    def getPar(self):
        return self.par  
    #.......   par  
    #.......   simbolo    
    def getSimbolo(self):
        self.simbolo = self.moneda + self.par 
        return self.simbolo  
    #.......   simbolo
    #.......   periodo    
    def setPeriodo(self, periodo):
        self.periodo = periodo
        return
    
    def getPeriodo(self):
        return self.periodo  
    #.......   periodo   
    #.......   clienteBinan    
    def conectar(self):
        api_key    = 'RAGCg4uGonc8ox0nKOZxnK7Ejx8tUXL5VlQ16l9PF46FvzuJeH46n408ekEsE9iw'
        api_secret = 'ZzSYviWTS5BtrA27MQmZ5Ez702DDKOv0il91Sbp4UM1G3V8QuOWR9kMsgShWoNyY'  
        #
        
        #
        #api_key    = 'a9lsESnZ2WD2fMj7OlHYf8IkxvEfNB0HXK01zkYyeY74oOEHUgLfbI3uypmKfAS5'
        #api_secret = 'PCQr84bWjXhRivvee5gG5OkI6WjalinuVyDqmHs7YF3yhokW1DipWUFk1ohwTUfj'         
        self.client = self.clienteBinan.conectar(api_key, api_secret,True)
        return self.client 
    #def setConexcion(self):        
        #self.client = self.clienteBinan.conectar()
        #return
    def getConexcion(self):        
        self.client 
        return self.client     
    #.......   clienteBinan    
    #.......   RSI    
    #def setConexcion(self):        
        #self.client = self.clienteBinan.conectar()
        #return
    #def getRsiUltimo(self,t):        
        #rsiUltimo = rsi.RSI(t)[-1]
        #return rsiUltimo     
    #.......   RSI      
def main():
    botcito = BotCito('BTC', 'USDT', '1m')#
    clienteBinan = botcito.clienteBinan
    cliente = botcito.conectar()
    botcito.balance.setCliente(cliente)
    botcito.balance.setEstable(botcito.getPar())
    saldo = botcito.balance.getEstable()['free']
    botcito.balance.mostrar()
    botcito.doctor.setOperar(True,50,0.2)
    while True:
        try:
        #if True:
            saldo = botcito.balance.getEstable()['free']
            #print(clienteBinan.simbolo,':',clienteBinan.precioActual1( cliente)) btc_price["price"]
            precioActual = clienteBinan.precioActual( cliente)
            botcito.indices.setPrecioActual(precioActual)
            clienteBinan.consulta(cliente)
            #print(clienteBinan.btc_df['close'][:-1])
            botcito.indices.calcularRsi(clienteBinan.btc_df['close'])
            botcito.indices.calcularKdj(clienteBinan.btc_df['close'],clienteBinan.btc_df['low'],clienteBinan.btc_df['high'])
            botcito.indices.mostrar()
            #botcito.indices.escribirLog()
            bandera = botcito.indices.statusKdj()
            botcito.doctor.operando(cliente,
                                    saldo,
                                    botcito.indices.getStatusCompra(),
                                    botcito.indices.getStatusVenta(),
                                    clienteBinan.simbolo,
                                    precioActual,
                                    bandera
                                    )
            sleep(1)
        except Exception as e :
            print("Oops!  Hay problemas en el main.  Try again...",e) 
            sleep(5)  
        
if __name__ == '__main__':
    main()