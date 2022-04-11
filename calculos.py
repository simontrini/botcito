import logging
class Calculos :
    #def __init__(self):
        
    def diferencia(self, base, final):
        retorno = float(final) - float(base)
        return retorno
    
    def porcentaje(self, base, final):
        
        retorno = 100 * (self.diferencia(base, final) / float(base))
        return retorno  
    
def main():
    calculo = Calculos()
    print(calculo.porcentaje(20,21.492957800000017))
if __name__ == '__main__':
    main()