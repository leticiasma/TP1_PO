import numpy as np

class Simplex:

    def __init__(self, n, m, c, A, b):

        self.n = n
        self.m = m
        self.c = c
        self.A = A
        self.b = b

    def testa_viabilidade(self):
        #Montar PL Auxiliar
        m_aux = (self.m)+self.n

        c_aux = np.ones(m_aux)#, dtype=int)
        c_aux *= -1

        for i in range(self.m):
            c_aux[i] = 0

        A_aux = self.A
        identidade = np.eye(self.n)#, dtype=int)

        #print("matriz A de restricoes: \n{}".format(A_aux))
        #print("matriz identidade: \n{}".format(identidade))

        A_aux = np.concatenate((A_aux, identidade), axis=1)

        #print("\n\nPL AUXILIAR:\n")
        #print("n restricoes: {}".format(self.n))
        #print("m variaveis: {}".format(m_aux))
        #print("vetor de custo c: {}".format(c_aux))
        #print("matriz A de restricoes: \n{}".format(A_aux))
        #print("vetor b: {}".format(self.b))
        
        self.pl_aux()

        if(self.val_obj_aux < 0):
            self.print_inviavel()
        else:
            print("otima ou ilimitada")
            self.tableau()

        #if(booleano):
        #    print("Eh viavel")
        #else:
        #   print("Eh inviavel")

        #Resulver seu Tableau

    def print_inviavel(self):
        print("inviavel")
        certificado = ""
        for i in range(self.n):
            certificado += str(self.certificado_otimo_aux[i])+" "
        print(certificado) #Printa como float... No PDF é int, mas não sei se tem caso float de verdade, acho que sim

    def print_tableau(self, tipo):

        if(tipo == "pl"):
            print(self.certificado_otimo_tb,"|",self.c_tb,"|",self.val_obj_tb)
            for i in range (self.n):
                print(self.extensao_tb[i],"|",self.A_tb[i],"|",self.b_tb[i])
            print("\n\n")
        elif(tipo == "aux"):
            print(self.certificado_otimo_aux,"|",self.c_aux,"|",self.val_obj_aux)
            for i in range (self.n):
                print(self.extensao_aux[i],"|",self.A_aux[i],"|",self.b_aux[i])
            print("\n\n")

    def pl_aux(self): #n e b não mudam para PL original e auxiliar
        self.m_aux = (self.m)+self.n

        self.certificado_otimo_aux = np.zeros(self.n)

        self.c_aux = np.ones(self.m_aux)
        for i in range(self.m):
            self.c_aux[i] = 0

        self.val_obj_aux = 0

        self.extensao_aux = np.eye(self.n)

        self.A_aux = self.A
        identidade = np.eye(self.n)
        self.A_aux = np.concatenate((self.A_aux, identidade), axis=1)

        self.b_aux = self.b

        #self.print_tableau("aux")

        #FAZER O CASO DE ALGUM B SER NEGATIVO E JÁ REGISTRANDO A OP NO TABLEAU NA EXTENSAO
        for i in range(self.n):
            self.certificado_otimo_aux -= self.extensao_aux[i]
            self.c_aux -= self.A_aux[i][:]
            self.val_obj_aux -= self.b_aux[i]
        
        #self.print_tableau("aux")

        tem_negativo_aux, j = self.tem_ci_negativo_aux()

        while(tem_negativo_aux):
            #Achar a linha na coluna j com a menor razao b/A
            razao = 2**10
            linha_pivo = 0
            coluna_pivo = 0
                
            for i in range(self.n): #i é linha
                if(self.A_aux[i][j] > 0.0 and self.b_aux[i]/self.A_aux[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_aux[i]/self.A_aux[i][j]
                
            #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
            pivo = self.A_aux[linha_pivo][coluna_pivo]
            self.extensao_aux[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
            self.A_aux[linha_pivo] /= pivo
            self.b_aux[linha_pivo] /= pivo

            #print("\n\nPIVOTEANDO")
            #self.print_tableau()

            valor_op = -1*self.c_aux[coluna_pivo]
                
            self.certificado_otimo_aux += valor_op*self.extensao_aux[linha_pivo][:]   
            self.c_aux += valor_op*self.A_aux[linha_pivo][:]
            self.val_obj_aux += valor_op*self.b_aux[linha_pivo]

            #print("\n\nZERANDO PRIMEIRA LINHA")
            #self.print_tableau()

            for i in range(self.n):
                if(i != linha_pivo):
                    elemento = self.A_aux[i][coluna_pivo]

                    if(np.sign(elemento) == 1 or np.sign(elemento) == -1):
                        valor_op = -1*elemento
                            
                        self.extensao_aux[i][:] += valor_op*self.extensao_aux[linha_pivo][:] 
                        self.A_aux[i][:] += valor_op*self.A_aux[linha_pivo][:]
                        self.b_aux[i] += valor_op*self.b_aux[linha_pivo]

                    else:
                        continue

            #print("\n\nZERANDO DEMAIS LINHAS")
            #self.print_tableau()

            tem_negativo_aux, j = self.tem_ci_negativo_aux()
            
        #self.print_tableau("aux")

    def tem_ci_negativo(self): #ACHO QUE NAO PODIA DAR SO UMA PASSADA POIS PODE SURGIR NEGATIVOS ATRAS. Pensar em um caso que acontece isso
        for j in range (self.m_tb): #j é coluna
            if(self.c_tb[j] < 0):
                return True, j    
        return False, -1

    def tem_ci_negativo_aux(self): #ACHO QUE NAO PODIA DAR SO UMA PASSADA POIS PODE SURGIR NEGATIVOS ATRAS. Pensar em um caso que acontece isso
        for j in range (self.m_aux): #j é coluna
            if(self.c_aux[j] < 0):
                return True, j    
        return False, -1

    def tableau(self):

        self.m_tb = (self.m)+self.n

        c_ext_canonico = np.zeros(self.n)
        self.c_tb = self.c
        self.c_tb = np.concatenate((self.c_tb, c_ext_canonico))

        for i in range (self.m):
            self.c_tb[i] *= -1

        self.A_tb = self.A
        identidade = np.eye(self.n)
        self.A_tb = np.concatenate((self.A_tb, identidade), axis=1)

        self.b_tb = self.b

        self.certificado_otimo_tb = np.zeros(self.n)
        self.extensao_tb = np.eye(self.n)
        self.val_obj_tb = 0

        #print("\n\nINICIAL")
        #self.print_tableau()

        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_negativo, j = self.tem_ci_negativo()

        while(tem_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = 2**10
            linha_pivo = 0
            coluna_pivo = 0
                
            for i in range(self.n): #i é linha
                if(self.A_tb[i][j] > 0.0 and self.b_tb[i]/self.A_tb[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = self.b_tb[i]/self.A_tb[i][j]
                
            #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
            pivo = self.A_tb[linha_pivo][coluna_pivo]
            self.extensao_tb[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
            self.A_tb[linha_pivo] /= pivo
            self.b_tb[linha_pivo] /= pivo

            #print("\n\nPIVOTEANDO")
            #self.print_tableau()

            valor_op = -1*self.c_tb[coluna_pivo]
                
            self.certificado_otimo_tb += valor_op*self.extensao_tb[linha_pivo][:]   
            self.c_tb += valor_op*self.A_tb[linha_pivo][:]
            self.val_obj_tb += valor_op*self.b_tb[linha_pivo]

            #print("\n\nZERANDO PRIMEIRA LINHA")
            #self.print_tableau()

            for i in range(self.n):
                if(i != linha_pivo):
                    elemento = self.A_tb[i][coluna_pivo]

                    if(np.sign(elemento) == 1 or np.sign(elemento) == -1):
                        valor_op = -1*elemento
                            
                        self.extensao_tb[i][:] += valor_op*self.extensao_tb[linha_pivo][:] 
                        self.A_tb[i][:] += valor_op*self.A_tb[linha_pivo][:]
                        self.b_tb[i] += valor_op*self.b_tb[linha_pivo]

                    else:
                        continue

            #print("\n\nZERANDO DEMAIS LINHAS")
            #self.print_tableau()

            tem_negativo, j = self.tem_ci_negativo()
            
        self.print_tableau("pl")
    



