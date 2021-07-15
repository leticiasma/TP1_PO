import numpy as np

class Simplex:

    def __init__(self, n, m, c, A, b):

        self.n = n
        self.m = m
        self.c = c
        self.A = A
        self.b = b

    def print_tableau(self, tipo): #melhorar duplicacao

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

    def print_otima(self):
        print("otima")
        print(str(self.val_obj_tb))
        #Faltou printar uma solução que atinge o valor ótimo
        certificado = ""
        for i in range(self.n):
            certificado += str(self.certificado_otimo_tb[i])+" "
        print(certificado)

    def print_inviavel(self):
        print("inviavel")
        certificado = ""
        for i in range(self.n):
            certificado += str(self.certificado_otimo_aux[i])+" "
        print(certificado) #Printa como float... No PDF é int, mas não sei se tem caso float de verdade, acho que sim

    def print_ilimitada(self): #NÃO SEI SE ILIMITADA APARECE NO MEIO DO TABLEAU... ACHO QUE SIM, MAS NÃO ACHEI EXEMPLOS DE TESTE
        print("ilimitada")
        #Falta printar uma Sol Viavel o Certificado de Ilimitabilidade

    def resolve_PL(self):
        viavel = self.testa_viabilidade()

        if(viavel):
            #print("otima ou ilimitada")
            self.monta_tableau_PL()
            self.tableau("original", self.c_tb, self.A_tb, self.b_tb, self.extensao_tb, self.certificado_otimo_tb, self.val_obj_tb)
        else:
            self.print_inviavel()

    def testa_viabilidade(self):

        #Monta PL Auxiliar
        self.monta_tableau_PL_aux()

        #Resolve a PL Auxiliar
        self.tableau("aux", self.c_aux, self.A_aux, self.b_aux, self.extensao_aux, self.certificado_otimo_aux, self.val_obj_aux)

        if(self.val_obj_aux < 0):  
            return False
            
        else:
            return True

    def monta_tableau_PL_aux(self):
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

    def monta_tableau_PL():
        self.m_tb = (self.m)+self.n

        c_ext_canonico = np.zeros(self.n)
        self.c_tb = self.c
        self.c_tb = np.concatenate((self.c_tb, c_ext_canonico))

        for i in range (self.m):
            if(self.c_tb[i] != 0):
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
    
    def tem_ci_negativo(self, c): #ACHO QUE NAO PODIA DAR SO UMA PASSADA POIS PODE SURGIR NEGATIVOS ATRAS. Pensar em um caso que acontece isso
        for j in range ((self.m)+self.n): #j é coluna
            if(c[j] < 0):
                return True, j    
        return False, -1

    def tableau(self, tipo, c, A, b, extensao, certificado_otimo, val_obj): #n e b não mudam para PL original e auxiliar

        #PENSAR NAQUELES CASOS DE DESEMPATE
        tem_negativo, j = self.tem_ci_negativo(c)

        while(tem_negativo):
            #Achar a linha na coluna j com a menor razao b/A
            razao = 2**10
            linha_pivo = 0
            coluna_pivo = 0
            
            ilimitada = 0

            for i in range(self.n): #i é linha
                if(A[i][j] > 0.0 and b[i]/A[i][j] < razao):
                    linha_pivo = i
                    coluna_pivo = j
                    razao = b[i]/A[i][j]
                elif(A[i][j] < 0.0 or A[i][j] == 0.0):
                    ilimitada += 1

            if(ilimitada == self.n):
                self.print_ilimitada()
                self.print_tableau("pl")
                return
            else:    
                #Pivotear: Eliminacao Gaussiana de forma que apenas A[linha_pivo][coluna_pivo] seja 1 e o restante da coluna seja 0
                pivo = A[linha_pivo][coluna_pivo]
                extensao[linha_pivo] /= pivo #talvez nem precise disso pois não faz parte do exercício
                A[linha_pivo] /= pivo
                b[linha_pivo] /= pivo

                #print("\n\nPIVOTEANDO")
                #self.print_tableau()

                valor_op = -1*c[coluna_pivo]
                    
                certificado_otimo += valor_op*extensao[linha_pivo][:]   
                c += valor_op*A[linha_pivo][:]
                val_obj += valor_op*b[linha_pivo]

                #print("\n\nZERANDO PRIMEIRA LINHA")
                #self.print_tableau()

                for i in range(self.n):
                    if(i != linha_pivo):
                        elemento = A[i][coluna_pivo]

                        if(np.sign(elemento) == 1 or np.sign(elemento) == -1):
                            valor_op = -1*elemento
                                
                            extensao[i][:] += valor_op*extensao[linha_pivo][:] 
                            A[i][:] += valor_op*A[linha_pivo][:]
                            b[i] += valor_op*b[linha_pivo]
                        else:
                            continue

                #print("\n\nZERANDO DEMAIS LINHAS")
                #self.print_tableau()

                tem_negativo, j = self.tem_ci_negativo(c)
        
        if(tipo == "original"):
            self.print_otima()
    



