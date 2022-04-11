from rsi import *
from kdj import *
from calculos import *
import logging
class Indices :
    def __init__(self):
        self.rsiBajo = 20
        self.rsiAlto = 80  
        self.rsi = 0
        self.rsiObj = Rsi()
        self.kdjObj = Kdj()
        self.prevenidoCompra = False
        self.prevenidoVenta = False
        self.Compra = False
        self.Venta = False   
        self.precioActual = 0 
        self.nivelKdj = None
    def statusRsi(self):
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
        #if self.rsi < (self.rsiAlto -10) and  (self.rsi > self.rsiBajo + 10):
            #self.Venta = False 
            #self.Compra = False        
    def statusKdj(self):
        return self.nivelKdj 
    def getStatusCompra(self):
        return self.Compra
    def getStatusVenta(self):
        #if Calculos.porcentaje(sel)
        return self.Venta    
    
    def setDf(self, df):
        self.df = df
        return
    
    def getDf(self):
        return self.df 
    
    def setPrecioActual(self, precioActual):
        self.precioActual = precioActual
        return
    
    def getPrecioActual(self):
        return self.precioActual
    
    def calcularRsi(self, t):
        self.rsi = self.rsiObj.RSI(t)[-1]
        self.statusRsi()
        #self.mostrar()
        return 
    
    def calcularKdj(self, close, low, high):
        self.kdjObj.cal_KDJ(close, low, high)
        self.nivelKdj = self.kdjObj.statusKdj()
        #self.mostrar()
        return     

    def mostrar(self):
        precio = "{:.6}".format(float(self.getPrecioActual()))
        rsi = "{:.2f}".format(float(self.rsi))
        k = "{:.2f}".format(float(self.kdjObj.k))
        d = "{:.2f}".format(float(self.kdjObj.d))
        j = "{:.2f}".format(float(self.kdjObj.j))
        arriba = '      '
        abajo = 'abajo ' 
        if self.kdjObj.Nivel == 'arriba':
            arriba = 'arriba'
            abajo = '      '
        if self.kdjObj.Nivel == 'NiNi':
            arriba = '      '
            abajo = '      '        
        
        print(f"""
********************************************************************************************
** Ultimo Precio:|  RSI: |   K:  |   D:  |   j:  |  {arriba}   **
**   {precio}      | {rsi} | { k } | { d } | { j } |  {abajo }   **
********************************************************************************************
""")    
    def escribirLog(self):
        logging.info('%s:%s | RSI:%s | K:%s | D:%s | J:%s | Nivel:%s | Compra:%s | Venta:%s',
                     'BTC',
                     "{:.4f}".format(float(self.getPrecioActual())),
                     "{:.2f}".format(float(self.rsi)),
                     "{:.2f}".format(float(self.kdjObj.k)),
                     "{:.2f}".format(float(self.kdjObj.d)),
                     "{:.2f}".format(float(self.kdjObj.j)),
                     self.kdjObj.Nivel,
                     1,
                     1)
