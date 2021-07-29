import numpy as np
from numpy.core.numeric import isclose
import math

class Simplex:

    def __init__(self, n, m, c, A, b):

        self.n = n
        self.m = m
        self.c = c
        self.A = A
        self.b = b

    def print_tableau(self, tipo): #melhorar duplicacao

        if(tipo == "simples"):
            print(self.certif_otimalidade_PL," | ",self.c_PL," | ",self.val_obj_PL)
            for i in range (self.n):
                print(self.matriz_transform[i],"|",self.A_tableau[i]," | ",self.b_tableau[i])
            print("\n\n")
        elif(tipo == "extendido"):
            print(self.certif_otimalidade_PL," | ",self.c_PL," | ",self.val_obj_PL)
            print(self.certif_otimalidade_AUX," | ",self.c_AUX," | ",self.val_obj_AUX)
            for i in range (self.n):
                print(self.matriz_transform[i]," | ",self.A_tableau[i]," | ",self.b_tableau[i])
            print("\n\n")
            
    def encontra_sol(self): #nao sei se funciona para o caso de multiplas solucaos, mais de uma sol otima
        self.bases_PL = []

        solucao = "" #sera q precisa de dualidade p achar as bases?
        for i in range(self.m): #nao está tratando se é canonico... deveria estar!!!!!!!!!!! urgente
            if (self.c_PL[i] == 0):
                achou_base = False
                for j in range(self.n):
                    if(self.A_tableau[j][i] == 1):
                        achou_base = True
                        self.bases_PL.append(i)

                        if(i != self.m-1):
                            #solucao += str(round(self.b_tableau[j], 7))+" "
                            solucao += "{0:.7f}".format(self.b_tableau[j])+" "
                        else:
                            #solucao += str(round(self.b_tableau[j], 7))
                            solucao += "{0:.7f}".format(self.b_tableau[j])
                
                if(not achou_base):
                    if(i != self.m-1):
                        solucao += "0.0000000 " 
                    else:
                        solucao += "0.0000000"                   
            else:
                if(i != self.m-1):
                    solucao += "0.0000000 " 
                else:
                    solucao += "0.0000000"
        
        print(solucao)

    def print_otima(self):
        print("otima")

        print("{0:.7f}".format(self.val_obj_PL)) #nao precisa ser em float??
        #self.saida.write(str(round(self.val_obj_PL, 7))+"\n") #nao precisa ser em float??

        self.encontra_sol()
        
        certificado = ""
        for i in range(self.n):
            if(i != self.n-1):
                #certificado += str(round(self.certif_otimalidade_PL[i], 7))+" "
                certificado += "{0:.7f}".format(self.certif_otimalidade_PL[i])+" "

            else:
                #certificado += str(round(self.certif_otimalidade_PL[i], 7))
                certificado += "{0:.7f}".format(self.certif_otimalidade_PL[i])
        print(certificado)

    def print_inviavel(self):
        print("inviavel")

        certificado = ""
        for i in range(self.n):
            if(i != self.n-1):
                #certificado += str(round(self.certif_otimalidade_AUX[i], 7))+" "
                certificado += "{0:.7f}".format(self.certif_otimalidade_AUX[i])+" "
                
            else:
                #certificado += str(round(self.certif_otimalidade_AUX[i], 7))
                certificado += "{0:.7f}".format(self.certif_otimalidade_AUX[i])
        print(certificado) #Printa como float... No PDF é int, mas não sei se tem caso float de verdade, acho que sim

    # sempre que todos os coeficientes da coluna correspondente de uma vari´avel candidata forem n˜ao-positivos (ou sejam negativos ou zero
    def print_ilimitada(self): #NÃO SEI SE ILIMITADA APARECE NO MEIO DO TABLEAU... ACHO QUE SIM, MAS NÃO ACHEI EXEMPLOS DE TESTE
        print("ilimitada")
        #Falta printar uma Sol Viavel!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!aaaaaaaaa
        self.encontra_sol()

        certificado = np.zeros(self.m)
        
        for i in range(self.m):
            if (i == self.coluna_ilimitada):
                certificado.append(-1*self.A_tableau[i][])

        #certificado += str(-1*self.c_PL[self.coluna_ilimitada])+" "
        #certificado += "{0:.7f}".format(-1*self.c_PL[self.coluna_ilimitada])+" "
        
        #for i in range(self.n):
        #    if(i != self.n-1):
               #certificado += str(-1*self.A_tableau[i][self.coluna_ilimitada])+" "
        #        certificado += "{0:.7f}".format(-1*self.A_tableau[i][self.coluna_ilimitada])+" "
        #    else:
        #        #certificado += str(-1*self.A_tableau[i][self.coluna_ilimitada])
        #        certificado += "{0:.7f}".format(-1*self.A_tableau[i][self.coluna_ilimitada])
        print(certificado)

    def testa_viabilidade(self):

        #Monta PL Auxiliar
        self.monta_tableau_extendido()

        #Resolve a PL Auxiliar
        #print("RESOLVENDO TB AUX")
        self.tableau()#"aux", self.c_AUX, self.A_tableau, self.b_tableau, self.matriz_transform, self.certif_otimalidade_AUX)#, self.val_obj_AUX)

        if(self.val_obj_AUX < 0 and not np.isclose(self.val_obj_AUX, 0)):  
            return False
            
        else:
            return True

    def resolve_PL(self):
        viavel = self.testa_viabilidade()

        if(viavel): #pensar no caso com mais de uma sol otima, que ficava 0 em cima de algo que não era solucao
            #print("RESOLVENDO TB ORIGINAL REAPROVEITANDO")
            #print("\n")
            self.continua_tableau_PL()
            
            #self.tableau()#"original", self.c_tb, self.A_tb, self.b_tb, self.extensao_tb, self.certificado_otimo_tb)#, self.val_obj_tb)
        else:
            self.print_inviavel()

    def monta_tableau_extendido(self): #tem que adicionar também variáveis artificiais além das de folga
        self.m_AUX = (self.m)+2*self.n
        
        self.A_tableau = self.A
        identidade = np.eye(self.n)
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        self.b_tableau = self.b

        self.c_PL = self.c
        zeros = np.zeros(2*self.n)
        self.c_PL = np.concatenate((self.c_PL, zeros), axis=0)
        for i in range(self.m_AUX):
            if(self.c_PL[i]!=0):
                self.c_PL[i] *= -1

        self.c_AUX = np.ones(self.m_AUX)
        for i in range(self.m+self.n):
            self.c_AUX[i] = 0

        self.val_obj_PL = 0
        self.val_obj_AUX = 0

        self.certif_otimalidade_PL = np.zeros(self.n)
        self.certif_otimalidade_AUX = np.zeros(self.n)

        self.matriz_transform = np.eye(self.n) #transformacao

        #print("TABLEAU INICIAL EXTENDIDO COM VARIAVEIS AUXILIARES")
        #self.print_tableau("extendido")

        for i in range(self.n):
            if(self.b_tableau[i] < 0):
                self.b_tableau[i] *= -1
                self.A_tableau[i] *= -1
                self.matriz_transform[i] *= -1

        #print("TABLEAU INICIAL EXTENDIDO SUMINDO COM b's NEGATIVOS")
        #self.print_tableau("extendido")                 
                    
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        #print("TABLEAU INICIAL EXTENDIDO COM VARIAVEIS ARTIFICIAIS")
        #self.print_tableau("extendido")

        for i in range(self.n):
            self.certif_otimalidade_AUX -= self.matriz_transform[i]
            self.c_AUX -= self.A_tableau[i]
            self.val_obj_AUX -= self.b_tableau[i]

        #print("TORNANDO A PL AUXILIAR CANONICA")
        #self.print_tableau("extendido")
    
    def busca_ci_negativo(self, c): #ACHO QUE NAO PODIA DAR SO UMA PASSADA POIS PODE SURGIR NEGATIVOS ATRAS. Pensar em um caso que acontece isso
        for j in range ((self.m)+self.n): #j é coluna
            if(c[j] < 0 and not np.isclose(c[j], 0)):
                return True, j #mudei isso    
        return False, -1

    def tableau(self):#, tipo, c, A, b, extensao, certificado_otimo): #val_obj): #n e b não mudam para PL original e auxiliar
        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_ci_negativo, j = self.busca_ci_negativo(self.c_AUX)

        while(tem_ci_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = math.inf #2**10
            linha_pivo = 0
            coluna_pivo = 0

            for i in range(self.n): #i é linha
                if(self.A_tableau[i][j] > 0 and self.b_tableau[i]/self.A_tableau[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_tableau[i]/self.A_tableau[i][j] 

                #elif(self.A_tableau[i][j] < 0.0 or self.A_tableau[i][j] == 0.0): #não sei se precisa dessa parte
                    #pass
   
            #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
            pivo = self.A_tableau[linha_pivo][coluna_pivo]

            self.matriz_transform[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
            self.A_tableau[linha_pivo] /= pivo
            self.b_tableau[linha_pivo] /= pivo

            #print("\n\nPIVOTEANDO")
            #self.print_tableau("extendido")

            valor_op_PL = -1*self.c_PL[coluna_pivo]
            valor_op_AUX = -1*self.c_AUX[coluna_pivo]

            self.certif_otimalidade_PL += valor_op_PL*self.matriz_transform[linha_pivo]                      
            self.certif_otimalidade_AUX += valor_op_AUX*self.matriz_transform[linha_pivo]
 
            self.c_PL += valor_op_PL*self.A_tableau[linha_pivo] 
            self.c_AUX += valor_op_AUX*self.A_tableau[linha_pivo]

            self.val_obj_PL += valor_op_PL*self.b_tableau[linha_pivo]
            self.val_obj_AUX += valor_op_AUX*self.b_tableau[linha_pivo]

            #print("\n\nZERANDO PRIMEIRA LINHA")
            #self.print_tableau("extendido")

            for i in range(self.n):
                if(i != linha_pivo):
                    elemento = self.A_tableau[i][coluna_pivo]

                    if(np.sign(elemento) == 1 or np.sign(elemento) == -1):
                        valor_op = -1*elemento
                                
                        self.matriz_transform[i] += valor_op*self.matriz_transform[linha_pivo]
                        self.A_tableau[i] += valor_op*self.A_tableau[linha_pivo]
                        self.b_tableau[i] += valor_op*self.b_tableau[linha_pivo]
                    else:
                        continue

            #print("\n\nZERANDO DEMAIS LINHAS")
            #self.print_tableau("extendido")

            tem_ci_negativo, j = self.busca_ci_negativo(self.c_AUX)
        
        #print("CONFIGURACAO FINAL DO TABLEAU EXTENDIDO")
        #self.print_tableau("extendido")
    
    def continua_tableau_PL(self):
        self.c_PL = np.delete(self.c_PL, np.s_[(len(self.c_PL)-self.n):], 0)
        #print("o tamanho do c aqui eh "+str(len(self.c_PL)))
        self.A_tableau = np.delete(self.A_tableau, np.s_[(len(self.c_PL)):], 1)

        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_ci_negativo, j = self.busca_ci_negativo(self.c_PL)

        while(tem_ci_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = math.inf #2**10
            linha_pivo = 0
            coluna_pivo = 0
            
            ilimitada = 0

            for i in range(self.n): #i é linha
                if(self.A_tableau[i][j] > 0 and self.b_tableau[i]/self.A_tableau[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_tableau[i]/self.A_tableau[i][j]

                elif(self.A_tableau[i][j] < 0 or self.A_tableau[i][j] == 0): #<=
                    ilimitada += 1

            if(ilimitada == self.n):
                self.coluna_ilimitada = j
                self.print_ilimitada()
            
                return
            else:    
                #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
                pivo = self.A_tableau[linha_pivo][coluna_pivo]

                self.matriz_transform[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
                self.A_tableau[linha_pivo] /= pivo
                self.b_tableau[linha_pivo] /= pivo

                #print("\n\nPIVOTEANDO")
                #self.print_tableau("simples")

                valor_op = -1*self.c_PL[coluna_pivo]
                    
                self.certif_otimalidade_PL += valor_op*self.matriz_transform[linha_pivo]  
                self.c_PL += valor_op*self.A_tableau[linha_pivo]
                self.val_obj_PL += valor_op*self.b_tableau[linha_pivo]

                #print("\n\nZERANDO PRIMEIRA LINHA")
                #self.print_tableau("simples")

                for i in range(self.n):
                    if(i != linha_pivo):
                        elemento = self.A_tableau[i][coluna_pivo]

                        if(np.sign(elemento) == 1 or np.sign(elemento) == -1):
                            valor_op = -1*elemento
                                
                            self.matriz_transform[i][:] += valor_op*self.matriz_transform[linha_pivo][:] 
                            self.A_tableau[i][:] += valor_op*self.A_tableau[linha_pivo][:]
                            self.b_tableau[i] += valor_op*self.b_tableau[linha_pivo]

                        else:
                            continue

                #print("\n\nZERANDO DEMAIS LINHAS")
                #self.print_tableau("simples")

                tem_ci_negativo, j = self.busca_ci_negativo(self.c_PL)
        
        #print("CONFIGURACAO FINAL DO TABLEAU SIMPLES")
        #self.print_tableau("simples")
        
        self.print_otima()


