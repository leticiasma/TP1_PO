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

        print("matriz A de restricoes: \n{}".format(A_aux))
        print("matriz identidade: \n{}".format(identidade))

        A_aux = np.concatenate((A_aux, identidade), axis=1)

        print("\n\nPL AUXILIAR:\n")
        print("n restricoes: {}".format(self.n))
        print("m variaveis: {}".format(m_aux))
        print("vetor de custo c: {}".format(c_aux))
        print("matriz A de restricoes: \n{}".format(A_aux))
        print("vetor b: {}".format(self.b))
        
        self.tableau_auxiliar(m_aux, c_aux, A_aux)

        if(self.val_obj < 0):
            print("inviavel")
        else:
            print("viavel")

        #if(booleano):
        #    print("Eh viavel")
        #else:
        #   print("Eh inviavel")

        #Resulver seu Tableau

    def print_tableau(self):
        #print("\n\nTABLEAU\n")
        print(self.certificado_otimo_tb,"|",self.c_tb,"|",self.val_obj_tb)
        for i in range (self.n):
            print(self.extensao_tb[i],"|",self.A_tb[i],"|",self.b_tb[i])
        print("\n\n")

    def tableau_auxiliar(self, m, c, A): #n e b não mudam para PL original e auxiliar
        self.certificado_otimo = np.zeros(self.n)
        self.extensao = np.eye(self.n)

        self.c_tableau = c
        for i in range(m):
            if(self.c_tableau[i] != 0):
                self.c_tableau[i] *= -1

        self.val_obj = 0

        self.print_tableau(A)

        for i in range(self.n):
            self.certificado_otimo -= self.extensao[i]
            self.c_tableau -= A[i]
            self.val_obj -= self.b[i]

        self.print_tableau(A)

        '''for i in range(m):
            if(c[i] < 0):

                print("\nc negativo igual a "+str(c[i])+" na posicao "+str(i))

                linha_pivo = 0
                coluna_pivo = 0
                pivo = A[0][0]

                for j in range(self.n):

                    print("\nAnalisando se A["+str(j)+"]["+str(i)+"] = "+str(A[j][i])+" é diferente de zero\ne se b["+str(j)+"]/A["+str(j)+"]["+str(i)+"]="+str(self.b[j])+"/"+str(A[j][i])+" < A["+str(linha_pivo)+"]["+str(coluna_pivo)+"] = "+str(A[linha_pivo][coluna_pivo])+"\n")

                    if ((A[j][i] != 0.0) and (self.b[j]/A[j][i] < A[linha_pivo][coluna_pivo])):
                        print("Entrou no if!")
                        linha_pivo = j
                        coluna_pivo = i
                        pivo = A[j][i]
                
                print("\nO pivo eh: "+str(pivo)+" da linha "+str(linha_pivo)+" e coluna "+str(coluna_pivo))
                if(np.sign(pivo) == -1):
                    A[linha_pivo] /= -1*pivo
                else:
                    A[linha_pivo] /= pivo 

                self.print_tableau(A)

        #self.print_tableau(A)'''

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

        print("\n\nINICIAL")
        self.print_tableau()

        for j in range (self.m_tb): #j é coluna
            if(self.c_tb[j] < 0):
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

                print("\n\nPIVOTEANDO")
                self.print_tableau()

                valor_op = -1*self.c_tb[coluna_pivo]
                
                self.certificado_otimo_tb += valor_op*self.extensao_tb[linha_pivo][:]   
                self.c_tb += valor_op*self.A_tb[linha_pivo][:]
                self.val_obj_tb += valor_op*self.b_tb[linha_pivo]

                print("\n\nZERANDO PRIMEIRA LINHA")
                self.print_tableau()

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

                print("\n\nZERANDO DEMAIS LINHAS")
                self.print_tableau()

                #for i in range (self.n):

                #if(np.sign(pivo) == -1):
                #    self.A_tb[linha_pivo] /= -1*pivo
                #else:
                     
                #print("O pivo eh "+str(self.A_tb[linha_pivo][coluna_pivo]))
                

        '''for i in range(m):
            if(c[i] < 0):

                print("\nc negativo igual a "+str(c[i])+" na posicao "+str(i))

                linha_pivo = 0
                coluna_pivo = 0
                pivo = A[0][0]

                for j in range(self.n):

                    print("\nAnalisando se A["+str(j)+"]["+str(i)+"] = "+str(A[j][i])+" é diferente de zero\ne se b["+str(j)+"]/A["+str(j)+"]["+str(i)+"]="+str(self.b[j])+"/"+str(A[j][i])+" < A["+str(linha_pivo)+"]["+str(coluna_pivo)+"] = "+str(A[linha_pivo][coluna_pivo])+"\n")

                    if ((A[j][i] != 0.0) and (self.b[j]/A[j][i] < A[linha_pivo][coluna_pivo])):
                        print("Entrou no if!")
                        linha_pivo = j
                        coluna_pivo = i
                        pivo = A[j][i]
                
                print("\nO pivo eh: "+str(pivo)+" da linha "+str(linha_pivo)+" e coluna "+str(coluna_pivo))
                if(np.sign(pivo) == -1):
                    A[linha_pivo] /= -1*pivo
                else:
                    A[linha_pivo] /= pivo 

                self.print_tableau(A)

        #self.print_tableau(A)'''

    



