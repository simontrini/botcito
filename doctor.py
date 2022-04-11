import logging
from compraVenta import CompraVenta
from calculos import *
from datetime import datetime
class Doctor :
    def __init__(self):
        self.opera = False
        #monto para operar
        self.monto = 0
        self.operacionAbierta = False
        self.operacion = {}
        self.gananciaAcumulada = 0
        self.numeroOperacione = 0
        self.saldoComprar = 0
        self.saldoVender = 0  
        self.NumeroPerdida = 0
        self.tipoOperando = 'RSI'
        self.conPerdida = False
    def setOperar(self,opera,monto=0,porcentaje=0):
        self.opera = opera
        self.monto = monto
        self.porcentaje = porcentaje
        #self.saldoComprar = monto
        return
    def getOperar(self):
        return self.opera
    def setOperacionAbierta(self,estado):
        self.operacionAbierta = estado
        return
    def getOperacionAbierta(self):
        return self.operacionAbierta    
    def getOperarMonto(self):
        return  self.monto  
    
    def operando(self,client,saldo,compra,vende,simbolo,precioActual,bandera = None):
        if self.tipoOperando == 'RSI':
            self.operandoRsi(client,saldo,compra,vende,simbolo,precioActual)
        if self.tipoOperando == 'RSIKDJ':
            self.operandoRsiKdj(client,saldo,compra,vende,simbolo,precioActual,bandera)
            
    def operandoRsi(self,client,saldo,compra,vende,simbolo,precioActual):
        #print('operando',compra,vende)
        if self.getOperar():
            if self.getOperacionAbierta() :
                #vender
                #print('operandoVenta')
                if vende and self.ganancia(self.operacion['precioCompra'],precioActual) :
                    print('venta venta',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                    self.setOperacionAbierta(False)
                    self.mostrar()
                elif(self.conPerdida):
                    if vende and self.controlPerdida(self.operacion['precioCompra'],precioActual):
                        print('Control de perdida',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                        self.setOperacionAbierta(False)
                        self.mostrar()   
                        #print('perdida')
            else:
                #comprar
                print('operandoCompra')
                if self.saldoOK(saldo, self.monto)and compra:
                    #abre operacion
                    print('compra compra',self.compra(client, precioActual,self.monto,simbolo))
                    self.setOperacionAbierta(True)
                    self.mostrar()
                    #setOperacion()
            
        else:
            logging.info('no operando')
            
    def operandoRsiKdj(self,client,saldo,compra,vende,simbolo,precioActual,bandera):
        if self.getOperar():
            if self.getOperacionAbierta() :
                if vende and self.ganancia(self.operacion['precioCompra'],precioActual) and bandera == 'bajo':
                    print('venta venta',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                    self.setOperacionAbierta(False)
                    self.mostrar()
                elif(self.conPerdida):
                    if vende and self.controlPerdida(self.operacion['precioCompra'],precioActual):
                        print('Control de perdida',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                        self.setOperacionAbierta(False)
                        self.mostrar()  
            else:
                print('operandoCompra')
                if self.saldoOK(saldo, self.monto)and compra:
                    #tiene que comprar en alto pero con prevenidocompra
                #if self.saldoOK(saldo, self.monto)and compra and bandera == 'alto':
                    print('compra compra',self.compra(client, precioActual,self.monto,simbolo))
                    self.setOperacionAbierta(True)
                    self.mostrar()
            
        else:
            logging.info('no operando')
            
    def operandoStopLimit(self,client,saldo,prevenidoCompra,prevenidoVende,compra,vende,simbolo,precioActual):
        #print('operando',compra,vende)
        if self.getOperar():
            if self.getOperacionAbierta() :
                #vender
                #print('operandoVenta')
                if vende and self.ganancia(self.operacion['precioCompra'],precioActual) :
                    #cierra operacion
                    #print('venta venta',self.venta(client,precioActual, self.operacion['CantidadCompra'],simbolo))
                    print('venta venta',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                    self.setOperacionAbierta(False)
                    self.mostrar()
                    #setOperacion()
                else:
                    if vende and self.controlPerdida(self.operacion['precioCompra'],precioActual):
                        print('Control de perdida',self.venta(client,precioActual, round(self.saldoVender,self.lotSize(client,simbolo)),simbolo))
                        self.setOperacionAbierta(False)
                        self.mostrar()                    
            else:
                #comprar
                print('operandoCompra')
                if self.saldoOK(saldo, self.monto)and prevenidoCompra:
                    #abre operacion
                    print('compra compra',self.compraStopLimit(client, precioActual,self.monto,simbolo))
                    #ojo setear operacion abierta al ejecutarse la compraStopLimit
                    self.setOperacionAbierta(True)
                    self.mostrar()
                    #setOperacion()
            
        else:
            logging.info('no operando')    
    def saldoOK(self,saldo,monto):   
        if float(saldo) >= float(monto) :
            print('con saldo')
            return True
        else:
            print('sin saldo')
            return False
        
    def lotSize(self,client,simbolo):   
        info = client.get_symbol_info(simbolo)
        #info = self.client.get_symbol_info('%sUSDT' % coin)
        step_size = [float(_['stepSize']) for _ in info['filters'] if _['filterType'] == 'LOT_SIZE'][0]
        step_size = '%.8f' % step_size
        step_size = step_size.rstrip('0')
        decimals = len(step_size.split('.')[1])   
        return decimals
        
    def ganancia(self,precioCompra,precioActual): 
        calculo = Calculos()
        
        print('ganancia',calculo.porcentaje(precioCompra,precioActual),'por%',precioCompra ,precioActual )
        if calculo.porcentaje(precioCompra,precioActual)>= self.porcentaje :
            return True
        else:
            return False
        
    def compra(self,client, precio, monto,simbolo):
        #self.operacion = {}
        compraVeta = CompraVenta(client,simbolo)
        cantidad = round(float(monto)/float(precio),self.lotSize(client,simbolo))
        order = compraVeta.comprarMarket(cantidad)
        if  order['orderId'] :
            
            self.operacion = {'simbolo': simbolo ,
                         'precioSugerido': precio,
                         'cantidad': cantidad,
                         'precioCompra': order['fills'][0]['price'],
                         'CantidadCompra': order['fills'][0]['qty'],
                         'gananciaAcumulada': self.gananciaAcumulada,
                         'montoCompra': float(order['fills'][0]['price'])*float(order['fills'][0]['qty'])}
            self.numeroOperacione += 1
            self.SaldoComprar(order['fills'][0]['qty'],(float(order['fills'][0]['price'])*float(order['fills'][0]['qty'])))
            print('si se ejecuto la compra')
            #self.mostrar()
            return [True,self.operacion] 
            
        else:
            print('no se ejecuto la compra')
            return [False,None] 
        
    def venta(self,client, precio, cantidad,simbolo):
        calculo = Calculos()       
        compraVeta = CompraVenta(client,simbolo)
        #cantidad = cantidad
        order = compraVeta.comprarMarket(cantidad)
        if  order['orderId'] :
            self.operacion['precioSugeridoVenta'] = precio
            self.operacion['precioVenta'] = order['fills'][0]['price']
            self.operacion['CantidadVenta'] = order['fills'][0]['qty']
            self.gananciaAcumulada += calculo.porcentaje(self.operacion['precioCompra'],self.operacion['precioVenta'])
            self.operacion['gananciaAcumulada'] = self.gananciaAcumulada
            self.operacion['montoVenta'] = float(order['fills'][0]['price'])*float(order['fills'][0]['qty'])
            self.SaldoVender(order['fills'][0]['qty'],(float(order['fills'][0]['price'])*float(order['fills'][0]['qty'])))
            print('si se ejecuto la venta') 
            #self.mostrar()
            return [True,self.operacion] 
            
        else:
            print('no se ejecuto la venta')
            return [False,None]   
        
    def SaldoComprar(self, CantidadCompra,monto):
        self.saldoVender += float(CantidadCompra)
        self.monto -= float(monto)        
        return
    
    def SaldoVender(self, CantidadVenta,monto):
        self.saldoVender -= float(CantidadVenta)
        self.monto += float(monto)
        
        return
    def controlPerdida(self,precioCompra,precioActual):
        calculo = Calculos()
        
        print('gananciaPerdida','por%', calculo.porcentaje(precioCompra,precioActual),precioCompra ,precioActual)
        if calculo.porcentaje(precioCompra,precioActual)+self.porcentaje<= 0 :
            self.NumeroPerdida += 1
            return True
        else:
            return False
        
    def mostrar(self):
        numeroOperacione = self.numeroOperacione
        gananciaAcumulada = "{:.4f}".format(self.gananciaAcumulada)
        operacionAbierta = self.getOperacionAbierta()
        operacion = self.operacion
        NumeroPerdida = self.NumeroPerdida
        salida = f"""
*********************{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}***Indicador:{self.tipoOperando}***Manejo de Perdidas:{self.conPerdida}*******************
** N° Opera|  % Ganancia | OperacionAbierta |  |       Saldo     | SaldoSimbolo        **
**   {numeroOperacione}--{NumeroPerdida}    |    {gananciaAcumulada}  |        { operacionAbierta }        || { self.monto }|        { self.saldoVender }    **
** Operaciones                                                                     **
simbolo{operacion['simbolo']} precioSugerido{operacion['precioSugerido']} cantidad{operacion['cantidad']} precioCompra{operacion['precioCompra']} CantidadCompra{operacion['CantidadCompra']} gananciaAcumulada{operacion['gananciaAcumulada']} montoCompra{operacion['montoCompra']}  
precioSugeridoVenta{operacion['precioSugeridoVenta']} precioVenta{operacion['precioVenta']} CantidadVenta{operacion['CantidadVenta']} montoVenta{operacion['montoVenta']} **
********************************************************************************************
"""     
        logging.info(salida)
        print(salida)          
def main():
    calculo = Calculos()
    print(calculo.porcentaje(100,150))
if __name__ == '__main__':
    main()