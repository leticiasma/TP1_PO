import numpy as np
from simplex import Simplex

entrada = open('standard_input.txt', 'r')

n,m = entrada.readline().split() #n restricoes ; m variaveis
n = int(n)
m = int(m)
c = np.array(entrada.readline().split(), dtype='float32')#, dtype='int32') #vetor de custo c, com m inteiros

A =  np.zeros((n, m))#, dtype='int32')
b = np.zeros(n)#, dtype='int32')

for i in range(n):
    linha = np.array(entrada.readline().split())
    A[i] = linha[:-1]
    b[i] = linha[-1]


#print("PL ORIGINAL:\n")
#print("n restricoes: {}".format(n))
#print("m variaveis: {}".format(m))
#print("vetor de custo c: {}".format(c))
#print("matriz A de restricoes: \n{}".format(A))
#print("vetor b: {}".format(b))

simplex = Simplex(n,m,c,A,b)

#simplex.testa_viabilidade()

simplex.tableau()

entrada.close()