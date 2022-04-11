from binance.client import Client
from time import sleep
from binance import ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
#from binance.exceptions import BinanceAPIException, BinanceOrderException
import pandas as pd
#import btalib
from os import system
from datetime import datetime
#import numpy as np
import logging
#from botCito import BotCito
#logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
#logging.basicConfig(format='%(asctime)s %(message)s')
class clienteBinance:
    simbolo = ''
    btc_price = 0
    periodo = ''
    L = 20
    M = 10
    R = 5
    mediaL = 0
    mediaM = 0
    mediaR = 0
    df = pd.DataFrame( columns=['date', 'k', 'd'])
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms') 
    #tabla = [[0,0,0],[0,0,0],[0,0,0]]
    #tabla1 = []
    inicio = 0
    k_ = 0	
    d_ = 0 
    rsi = 0
    rsiBajo = 20
    rsiAlto = 80
    prevenidoCompra = False
    Compra = False
    prevenidoVenta = False
    Venta = False
    Nivel = ''
    def __init__(self, simbolo, periodo):
        self.simbolo = simbolo
        self.periodo = periodo 
    def conectar(self, api_key, api_secret, test = False ):
        logging.info('conectando API de testnet')
        print('conectando API de testnet')
        try:
            client = Client(api_key, api_secret,testnet=test) 
            return client
        except :
            logging.debug('Oops!  Hay problemas para conectar.  Try again...')
            print("Oops!  Hay problemas para conectar.  Try again...") 
            sleep(5)
            self.conectar(api_key, api_secret)
        
    def precioActual(self, client):    
        try:
            self.btc_price = client.get_symbol_ticker(symbol= self.simbolo)
            return self.btc_price["price"]
        except Exception as e:
            print("Oops!  Hay problemas en el precioActual.  Try again...",e) 
            sleep(5)     
            self.precioActual( client)
    
    def precioActual1(self, client):
        try:
            self.btc_price = client.get_symbol_ticker(symbol= self.simbolo)   
            return
        except Exception as e:
            print("Oops!  Hay problemas en el precioActual1.  Try again...",e) 
            sleep(5)           
    
    def consulta(self, client):
        try:
            timestamp = client._get_earliest_valid_timestamp(self.simbolo, '1m')
            bars = client.get_historical_klines(self.simbolo, client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")
            for line in bars:
                del line[5:]
            self.btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
            self.btc_df.set_index('date', inplace=True)
            self.btc_df.index = pd.to_datetime(self.btc_df.index, unit='ms')  
        except Exception as e:
            print("Oops!  Hay problemas en la consulta.  Try again...",e) 
            sleep(5)                
    
    #def mostrar(self):
        #precio = "{:.4}".format(float(self.btc_price["price"]))
        #rsi = "{:.2f}".format(float(self.rsi))
        #k = "{:.2f}".format(float(self.mediaL))
        #d = "{:.2f}".format(float(self.mediaM))
        #j = "{:.2f}".format(float(self.mediaR))
        #arriba = '      '
        #abajo = 'abajo '          
        #if self.Nivel == 'arriba':
            #arriba = 'arriba'
            #abajo = '      '
        #if self.Nivel == 'NiNi':
            #arriba = '      '
            #abajo = '      '        
        
        #print(f"""
#********************************************************************************************
#** Ultimo Precio    |  RSI: |   K:  |   D:  |   j:  |  {arriba}   **
#**   {precio}   | {rsi} | { k } | { d } | { j } |  {abajo }   **
#********************************************************************************************
#""")    
    
    def bandera(self, client):
        #self.mostrar()
        #print('Ultimo Precio:',self.btc_price["price"])
        #print('rsi',self.rsi,' k:',self.mediaL,'d:',self.mediaM,'j:',self.mediaR,)
        abajo = False
        arriba =False
        self.Nivel = 'abajo'
        x = 'x'
        if ((self.mediaM < self.mediaL) or (self.mediaM < self.mediaL)):
            x= 'xx'
            self.Nivel = 'NiNi'
        if ((self.mediaM > self.mediaL) and (self.mediaM > self.mediaR)):
            abajo = True
            arriba = False
            self.Nivel = 'abajo'
            x= 'x'
        
        if ((self.mediaM < self.mediaL) and (self.mediaM < self.mediaR)):
            arriba = True
            abajo = False
            self.Nivel = 'arriba'
            x='xxxx'
        #print('onToy',nivel ,'..--',x)
        if self.rsi < self.rsiBajo:
            print('prevenido true', self.rsi)
            self.prevenidoCompra = True
            self.Compra = False
            self.Venta = False 
        if self.rsi > self.rsiBajo and self.prevenidoCompra :
            print('prevenido false ', self.rsi)
            self.Compra = True
            self.prevenidoCompra = False
        if self.rsi > self.rsiAlto:
            self.prevenidoVenta = True
            self.Venta = False 
            self.Compra = False
        if self.rsi < self.rsiAlto and self.prevenidoVenta :
            self.Venta = True 
            self.prevenidoVenta = False
        logging.info('%s:%s | RSI:%s | K:%s | D:%s | J:%s | Nivel:%s | Compra:%s | Venta:%s',
                     self.simbolo,
                     "{:.4f}".format(float(self.btc_price['price'])),
                     "{:.2f}".format(float(self.rsi)),
                     "{:.2f}".format(float(self.mediaL)),
                     "{:.2f}".format(float(self.mediaM)),
                     "{:.2f}".format(float(self.mediaR)),
                     self.Nivel,
                     self.Compra,
                     self.Venta)
        return self.Nivel
    
    def getBalance(self,client, simbolo):
        balance = client.get_asset_balance(asset=simbolo)
        return balance
   