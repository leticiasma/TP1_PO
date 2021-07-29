import numpy as np
from numpy.core.numeric import isclose
#import functools
import math

class Simplex:

    def __init__(self, n, m, c, A, b):

        self.n = n
        self.m = m
        self.c = c
        self.A = A
        self.b = b

    def print_tableau(self, tipo):

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
            
    def encontra_sol(self):
        self.bases_PL = []

        solucao = ""
        canonicos = np.eye(self.n)

        for i in range(self.m):
            if (np.isclose(self.c_PL[i], 0)):
                vetor_aux = []

                achou_base = False

                for linha in range(self.n):
                    vetor_aux.append(self.A_tableau[linha][i])
                    
                for j in range(self.n):
                    #if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,canonicos[:][j],vetor_aux), True):                     
                    #if ((canonicos[:][j] == vetor_aux).all()):
                    if (canonicos[:][j] == vetor_aux).all():

                        achou_base = True
                        
                        base = i
                        indice_do_1 = j
                        
                        par = (i, indice_do_1)
                        self.bases_PL.append(par)

                        if(i != self.m-1):
                            solucao += "{0:.7f}".format(self.b_tableau[indice_do_1])+" "
                        else:
                            solucao += "{0:.7f}".format(self.b_tableau[indice_do_1])

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

        print("{0:.7f}".format(self.val_obj_PL))

        self.encontra_sol()
        
        certificado = ""
        for i in range(self.n):
            if(i != self.n-1):
                certificado += "{0:.7f}".format(self.certif_otimalidade_PL[i])+" "

            else:
                certificado += "{0:.7f}".format(self.certif_otimalidade_PL[i])
        print(certificado)

    def print_inviavel(self):
        print("inviavel")

        certificado = ""
        for i in range(self.n):
            if(i != self.n-1):
                certificado += "{0:.7f}".format(self.certif_otimalidade_AUX[i])+" "
                
            else:
                certificado += "{0:.7f}".format(self.certif_otimalidade_AUX[i])
        print(certificado)

    def print_ilimitada(self):
        print("ilimitada")

        self.encontra_sol()

        certificado = np.zeros(self.m)
        certificado_str = ""
        
        for base in self.bases_PL:
            if(self.coluna_ilimitada < self.m):
                certificado[self.coluna_ilimitada] = 1
            if(not np.isclose(self.A_tableau[base[1]][self.coluna_ilimitada],0)):
                certificado[base[0]] = -1*self.A_tableau[base[1]][self.coluna_ilimitada]
            else:
                certificado[base[0]] = self.A_tableau[base[1]][self.coluna_ilimitada]

        for i in range(self.m):
            if(i != self.m-1):
                certificado_str += "{0:.7f}".format(certificado[i])+" "
            else:
                certificado_str += "{0:.7f}".format(certificado[i])

        print(certificado_str)

    def testa_viabilidade(self):

        #Monta PL Auxiliar
        self.monta_tableau_extendido()

        #Resolve a PL Auxiliar
        self.tableau()

        if(self.val_obj_AUX < 0 and not np.isclose(self.val_obj_AUX, 0)):  
            return False
            
        else:
            return True

    def resolve_PL(self):
        viavel = self.testa_viabilidade()

        if(viavel):
            self.continua_tableau_PL()
            
        else:
            self.print_inviavel()

    def monta_tableau_extendido(self):
        self.m_AUX = (self.m)+2*self.n
        
        self.A_tableau = self.A
        identidade = np.eye(self.n)
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        self.b_tableau = self.b

        self.c_PL = self.c
        zeros = np.zeros(2*self.n)
        self.c_PL = np.concatenate((self.c_PL, zeros), axis=0)
        for i in range(self.m_AUX):
            if(not np.isclose(self.c_PL[i],0)):
                self.c_PL[i] *= -1

        self.c_AUX = np.ones(self.m_AUX)
        for i in range(self.m+self.n):
            self.c_AUX[i] = 0

        self.val_obj_PL = 0
        self.val_obj_AUX = 0

        self.certif_otimalidade_PL = np.zeros(self.n)
        self.certif_otimalidade_AUX = np.zeros(self.n)

        self.matriz_transform = np.eye(self.n)

        for i in range(self.n):
            if(self.b_tableau[i] < 0):
                self.b_tableau[i] *= -1
                self.A_tableau[i] *= -1
                self.matriz_transform[i] *= -1              
                    
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        for i in range(self.n):
            self.certif_otimalidade_AUX -= self.matriz_transform[i]
            self.c_AUX -= self.A_tableau[i]
            self.val_obj_AUX -= self.b_tableau[i]
    
    def busca_ci_negativo(self, c):
        for j in range ((self.m)+self.n): #j é coluna
            if(c[j] < 0 and not np.isclose(c[j], 0)):
                return True, j   
        return False, -1

    def tableau(self):
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
   
            #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
            pivo = self.A_tableau[linha_pivo][coluna_pivo]

            self.matriz_transform[linha_pivo] /= pivo
            self.A_tableau[linha_pivo] /= pivo
            self.b_tableau[linha_pivo] /= pivo

            valor_op_PL = -1*self.c_PL[coluna_pivo]
            valor_op_AUX = -1*self.c_AUX[coluna_pivo]

            self.certif_otimalidade_PL += valor_op_PL*self.matriz_transform[linha_pivo]                      
            self.certif_otimalidade_AUX += valor_op_AUX*self.matriz_transform[linha_pivo]
 
            self.c_PL += valor_op_PL*self.A_tableau[linha_pivo] 
            self.c_AUX += valor_op_AUX*self.A_tableau[linha_pivo]

            self.val_obj_PL += valor_op_PL*self.b_tableau[linha_pivo]
            self.val_obj_AUX += valor_op_AUX*self.b_tableau[linha_pivo]

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

            tem_ci_negativo, j = self.busca_ci_negativo(self.c_AUX)
    
    def continua_tableau_PL(self):
        self.c_PL = np.delete(self.c_PL, np.s_[(len(self.c_PL)-self.n):], 0)
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

                elif(self.A_tableau[i][j] < 0 or np.isclose(self.A_tableau[i][j],0)):
                    ilimitada += 1

            if(ilimitada == self.n):
                self.coluna_ilimitada = j
                self.print_ilimitada()
            
                return
            else:    
                #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
                pivo = self.A_tableau[linha_pivo][coluna_pivo]

                self.matriz_transform[linha_pivo] /= pivo
                self.A_tableau[linha_pivo] /= pivo
                self.b_tableau[linha_pivo] /= pivo

                valor_op = -1*self.c_PL[coluna_pivo]
                    
                self.certif_otimalidade_PL += valor_op*self.matriz_transform[linha_pivo]  
                self.c_PL += valor_op*self.A_tableau[linha_pivo]
                self.val_obj_PL += valor_op*self.b_tableau[linha_pivo]

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

                tem_ci_negativo, j = self.busca_ci_negativo(self.c_PL)
        
        self.print_otima()


