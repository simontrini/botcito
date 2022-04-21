# https://github.com/simontrini/botcito.git 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
import logging
from clienteBinance import clienteBinance
from indices import *
from balance import Balance
from doctor import *
from time import sleep
import configparser
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
#logging.basicConfig(format='%(asctime)s %(message)s')
class BotCito :
    def __init__(self, moneda, par, periodo):
        logging.basicConfig(filename='logMainNet%s.log'% moneda, level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.moneda = moneda
        self.par = par
        self.simbolo = moneda + par
        self.periodo = periodo
        self.clienteBinan = clienteBinance(self.simbolo, periodo)
        self.indices = Indices()
        self.balance = Balance(None,None,moneda)
        self.doctor = Doctor()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
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
        api_key    = self.config['api']['api_key']
        api_secret = self.config['api']['api_secret']    
        testNet = self.config['api']['test']
        if testNet == 'False':
            testnet = False
        else:
            testnet = True
        self.client = self.clienteBinan.conectar(api_key, api_secret,test = testnet )
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
    config = configparser.ConfigParser()
    config.read('config.ini')    
    botcito = BotCito(config['par']['simbolo'], config['par']['estable'], config['par']['periodo'])#
    clienteBinan = botcito.clienteBinan
    cliente = botcito.conectar()
    botcito.balance.setCliente(cliente)
    botcito.balance.setEstable(botcito.getPar())
    #saldo = botcito.balance.getEstable()['free']
    botcito.balance.mostrar()
    if config['doctor']['operar'] == 'False':
        operar = False
    else:
        operar = True    
    monto = float(config['doctor']['monto'])
    ganancia = float(config['doctor']['ganancia'])
    botcito.doctor.setOperar(operar, monto, ganancia)
    while True:
        try:
        #if True:
            #print('TestNet : ',config['api']['test'])
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
            #bandera = botcito.indices.statusRsi()
            botcito.doctor.setConPerdida(True)
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
