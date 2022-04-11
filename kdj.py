class Kdj:
    #simbolo = ''
    #btc_price = 0
    #periodo = ''
    #L = 20
    #M = 10
    #R = 5
    k = 0
    d = 0
    j = 0
    #df = pd.DataFrame( columns=['date', 'k', 'd'])
    #df.set_index('date', inplace=True)
    #df.index = pd.to_datetime(df.index, unit='ms') 
    #tabla = [[0,0,0],[0,0,0],[0,0,0]]
    #tabla1 = []
    #inicio = 0
    k_ = 0	
    d_ = 0 
    #rsi = 0
    #rsiBajo = 20
    #rsiAlto = 80
    #prevenidoCompra = False
    #Compra = False
    #prevenidoVenta = False
    #Venta = False
    Nivel = ''    
    def cal_KDJ(self, close, low, high, N=9, M1=3, M2=3):	
        datalen=len(close)	
        kdj_list=[]
        k_ = self.k_	
        d_ = self.d_        
        for i in range(datalen):	
            if i-N<0:	
                kdj_list.append(None)	
            else:	
                # Calcular RSV	
                c = float(close[i])	
                l = float(min(low[i-N:i]))	
                h = float(max(high[i-N:i]))	
                rsv = ((c - l) / (h - l))*100	
                if i - N == 0 and k_ == 0 and d_ == 0 :	
                    k_ = 50	
                    d_ = 50	
                k = (2/M1)*k_ + (1/M1)*rsv	
                d = (2/M2)*d_ + (1/M2)*k	
                j = 3*k - 2*d
                self.k = float(k)
                self.d = float(d)
                self.j = float(j)         
                kdj_list.append((k,d,j))	
                k_ = k	
                d_ = d
        self.k_ = k	
        self.d_ = d
        return
        #return kdj_list
    
    def statusKdj(self):
        abajo = False
        arriba =False
        self.Nivel = 'abajo'
        x = 'x'
        if ((self.d < self.k) or (self.d < self.k)):
            x= 'xx'
            self.Nivel = 'NiNi'
        if ((self.d > self.k) and (self.d > self.j)):
            abajo = True
            arriba = False
            self.Nivel = 'abajo'
            x= 'x'
        
        if ((self.d < self.k) and (self.d < self.j)):
            arriba = True
            abajo = False
            self.Nivel = 'arriba'
            x='xxxx' 
        #return
        return self.Nivel
    	
    
