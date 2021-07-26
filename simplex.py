import numpy as np

class Simplex:

    def __init__(self, n, m, c, A, b):

        self.n = n
        self.m = m
        self.c = c
        self.A = A
        self.b = b

    def print_tableau(self, tipo): #melhorar duplicacao

        if(tipo == "simples"):
            print(self.certif_otimalidade_PL,"|",self.c_PL,"|",self.val_obj_PL)
            for i in range (self.n):
                print(self.matriz_transform[i],"|",self.A_tableau[i],"|",self.b_tableau[i])
            print("\n\n")
        elif(tipo == "extendido"):
            print(self.certif_otimalidade_PL,"|",self.c_original_ext,"|",self.val_obj_PL)
            print(self.certificado_otimo_aux,"|",self.c_aux,"|",self.val_obj_aux)
            for i in range (self.n):
                print(self.matriz_transform[i],"|",self.A_tableau[i],"|",self.b_tableau[i])
            print("\n\n")
    def print_base_sol_otima(self): #nao sei se funciona para o caso de multiplas bases, mais de uma sol otima
        base = ""
        for i in range(self.m):
            if (self.c_PL[i] == 0):
                achou_um = False
                for j in range(self.n):
                    if(self.A_tableau[j][i] == 1):
                        achou_um = True
                        if(i != self.m-1):
                            base += str(self.b_tableau[j])+" "
                        else:
                            base += str(self.b_tableau[j])
                
                if(not achou_um):
                    if(i != self.m-1):
                        base += "0 " 
                    else:
                        base += "0"                   
            else:
                if(i != self.m-1):
                    base += "0 " 
                else:
                    base += "0"
        
        print(base)

    def print_otima(self):
        print("otima")
        print(str(self.val_obj_PL))

        self.print_base_sol_otima()
        #Faltou printar uma solução que atinge o valor ótimo
        certificado = ""
        for i in range(self.n):
            certificado += str(self.certif_otimalidade_PL[i])+" "
        print(certificado)

    def print_inviavel(self):
        print("inviavel")
        certificado = ""
        for i in range(self.n):
            certificado += str(self.certificado_otimo_aux[i])+" "
        print(certificado) #Printa como float... No PDF é int, mas não sei se tem caso float de verdade, acho que sim

    def print_ilimitada(self): #NÃO SEI SE ILIMITADA APARECE NO MEIO DO TABLEAU... ACHO QUE SIM, MAS NÃO ACHEI EXEMPLOS DE TESTE
        print("ilimitada")
        #Falta printar uma Sol Viavel
        certificado = ""
        certificado += str(-1*self.c_PL[self.certificado_ilimitada])+" "

        for i in range(self.n):
            certificado += str(-1*self.A_tableau[i][self.certificado_ilimitada])+" "
        print(certificado)

    def resolve_PL(self):
        viavel = self.testa_viabilidade()

        if(viavel): #pensar no caso com mais de uma sol otima, que ficava 0 em cima de algo que não era base
            #print("otima ou ilimitada")
            print("RESOLVENDO TB ORIGINAL REAPROVEITANDO")
            self.continua_tableau_PL()

            
            #self.tableau()#"original", self.c_tb, self.A_tb, self.b_tb, self.extensao_tb, self.certificado_otimo_tb)#, self.val_obj_tb)
        else:
            self.print_inviavel()

    def testa_viabilidade(self):

        #Monta PL Auxiliar
        self.monta_tableau_PL_aux()

        #Resolve a PL Auxiliar
        print("RESOLVENDO TB AUX")
        self.tableau()#"aux", self.c_aux, self.A_tableau, self.b_tableau, self.matriz_transform, self.certificado_otimo_aux)#, self.val_obj_aux)

        if(self.val_obj_aux < 0):  
            return False
            
        else:
            return True

    def monta_tableau_PL_aux(self): #tem que adicionar também variáveis artificiais além das de folga

        self.m_aux = (self.m)+2*self.n
        
        self.A_tableau = self.A
        self.b_tableau = self.b

        identidade = np.eye(self.n)
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        self.matriz_transform = np.eye(self.n) #transformacao

        for i in range(self.n):
            if(self.b_tableau[i]<0):
                self.b_tableau[i] *= -1
            
                #for j in range(self.m_aux-self.n):
                    #if(self.A_tableau[i] != 0):
                self.A_tableau[i] *= -1
                self.matriz_transform[i] *= -1                 
                    

        identidade = np.eye(self.n)
        self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)
        
        #self.m_aux = (self.m)+2*self.n

        #self.certificado_otimo_aux = np.zeros(self.n)
        self.certificado_otimo_aux = np.zeros(self.n)
        self.certif_otimalidade_PL = np.zeros(self.n)

        #self.c_aux = np.ones(self.m_aux)
        #for i in range(self.m):
        #    self.c_aux[i] = 0

        self.c_aux = np.ones(self.m_aux)
        for i in range(self.m+self.n):
            self.c_aux[i] = 0

        self.c_original_ext = self.c
        zeros = np.zeros(2*self.n)
        
        self.c_original_ext = np.concatenate((self.c_original_ext, zeros), axis=0)

        for i in range(self.m_aux):
            if(self.c_original_ext[i]!=0):
                self.c_original_ext[i] *= -1

        #self.val_obj_aux = 0
        self.val_obj_aux = 0
        self.val_obj_PL = 0

        #self.matriz_transform = np.eye(self.n)

        #self.A_tableau = self.A
        #identidade = np.eye(self.n)
        #self.A_tableau = np.concatenate((self.A_tableau, identidade), axis=1)

        #self.b_tableau = self.b

        #print(str(self.certif_otimalidade_PL)+" | "+str(self.c_original_ext)+" | "+str(self.val_obj_PL))
        self.print_tableau("aux")

        #FAZER O CASO DE ALGUM B SER NEGATIVO E JÁ REGISTRANDO A OP NO TABLEAU NA EXTENSAO
        #for i in range(self.n):
        #    self.certificado_otimo_aux -= self.matriz_transform[i]
        #    self.c_aux -= self.A_tableau[i][:]
        #    self.val_obj_aux -= self.b_tableau[i]

        for i in range(self.n):
            self.certificado_otimo_aux -= self.matriz_transform[i]
            self.c_aux -= self.A_tableau[i][:]
            self.val_obj_aux -= self.b_tableau[i]

        #print(str(self.certif_otimalidade_PL)+" | "+str(self.c_original_ext)+" | "+str(self.val_obj_PL))
        self.print_tableau("aux")

    def continua_tableau_PL(self):

        #elf.m_tb = (self.m)+self.n
        #self.c_tb = self.c
        
        #cuidado se n está deletando de verdade
        #intervalo = 

        self.c_PL = np.delete(self.c_original_ext, np.s_[(len(self.c_original_ext)-self.n):], 0)
        self.A_tableau = np.delete(self.A_tableau, np.s_[(len(self.c_original_ext)-self.n):], 1)

        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_negativo, j = self.tem_ci_negativo(self.c_PL)

        while(tem_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = 2**10
            linha_pivo = 0
            coluna_pivo = 0
            
            ilimitada = 0

            for i in range(self.n): #i é linha
                if(self.A_tableau[i][j] > 0.0 and self.b_tableau[i]/self.A_tableau[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_tableau[i]/self.A_tableau[i][j]
                elif(self.A_tableau[i][j] < 0.0 or self.A_tableau[i][j] == 0.0):
                    ilimitada += 1

            if(ilimitada == self.n):
                self.certificado_ilimitada = j
                #self.print_tableau(tipo)
                self.print_ilimitada()
            
                return
            else:    
                #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
                pivo = self.A_tableau[linha_pivo][coluna_pivo]
                self.matriz_transform[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
                self.A_tableau[linha_pivo] /= pivo
                self.b_tableau[linha_pivo] /= pivo

                print("\n\nPIVOTEANDO")
                self.print_tableau("aux")

                valor_op = -1*self.c_PL[coluna_pivo]
                    
                self.certif_otimalidade_PL += valor_op*self.matriz_transform[linha_pivo][:]   
                self.c_PL += valor_op*self.A_tableau[linha_pivo][:]
                #if(tipo == "aux"):
                self.val_obj_PL += valor_op*self.b_tableau[linha_pivo]
                #else:
                    #print("a somar :",valor_op*b[linha_pivo])
                    #print("val obj :",self.val_obj_tb)
                #aaaaaaaaaaaaaaaaaaaaaaaaaaa self.val_obj_tb += valor_op*b[linha_pivo]

                print("\n\nZERANDO PRIMEIRA LINHA")
                self.print_tableau("original")

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

                print("\n\nZERANDO DEMAIS LINHAS")
                self.print_tableau("original")

                tem_negativo, j = self.tem_ci_negativo(self.c_PL)
        
        print("CONFIGURACAO FINAL")
        self.print_tableau("original")
        
        #if(tipo == "original"):
        self.print_otima()


        #self.c_PL = self.c_original_ext

        #print(self.c_PL)
    
    def tem_ci_negativo(self, c): #ACHO QUE NAO PODIA DAR SO UMA PASSADA POIS PODE SURGIR NEGATIVOS ATRAS. Pensar em um caso que acontece isso
        for j in range ((self.m)+self.n): #j é coluna
            if(c[j] < 0):
                return True, j    
        return False, -1

    def tableau(self):#, tipo, c, A, b, extensao, certificado_otimo): #val_obj): #n e b não mudam para PL original e auxiliar

        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_negativo, j = self.tem_ci_negativo(self.c_aux)

        while(tem_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = 2**10
            linha_pivo = 0
            coluna_pivo = 0
            
            #ilimitada = 0

            for i in range(self.n): #i é linha
                if(self.A_tableau[i][j] > 0.0 and self.b_tableau[i]/self.A_tableau[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_tableau[i]/self.A_tableau[i][j]
                elif(self.A_tableau[i][j] < 0.0 or self.A_tableau[i][j] == 0.0):
                    #ilimitada += 1
                    pass

            #if(ilimitada == self.n):
            if(False):
                pass
                #self.certificado_ilimitada = j
                #self.print_tableau(tipo)
                #self.print_ilimitada()
            
                #return
            else:    
                #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
                pivo = self.A_tableau[linha_pivo][coluna_pivo]
                self.matriz_transform[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
                self.A_tableau[linha_pivo] /= pivo
                self.b_tableau[linha_pivo] /= pivo

                print("\n\nPIVOTEANDO")
                self.print_tableau("aux")

                valor_op = -1*self.c_aux[coluna_pivo]
                valor_op_ext = -1*self.c_original_ext[coluna_pivo]
                    
                self.certificado_otimo_aux += valor_op*self.matriz_transform[linha_pivo][:]
                self.certif_otimalidade_PL += valor_op_ext*self.matriz_transform[linha_pivo][:]   
                self.c_aux += valor_op*self.A_tableau[linha_pivo][:]
                self.c_original_ext += valor_op_ext*self.A_tableau[linha_pivo][:]
                #if(tipo == "aux"):
                self.val_obj_aux += valor_op*self.b_tableau[linha_pivo]
                self.val_obj_PL += valor_op_ext*self.b_tableau[linha_pivo]
                #else:
                    #print("a somar :",valor_op*b[linha_pivo])
                    #print("val obj :",self.val_obj_tb)
                #aaaaaaaaaaaaaaaaaaaaaaaaaaa self.val_obj_tb += valor_op*b[linha_pivo]

                print("\n\nZERANDO PRIMEIRA LINHA")
                self.print_tableau("aux")

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

                print("\n\nZERANDO DEMAIS LINHAS")
                self.print_tableau("aux")

                tem_negativo, j = self.tem_ci_negativo(self.c_aux)
        
        print("CONFIGURACAO FINAL")
        self.print_tableau("aux")
        
        #if(tipo == "original"):
            #self.print_otima()
    



