import numpy as np
from simplex import Simplex

entrada = open('standard_input.txt', 'r')

n,m = entrada.readline().split() #n restricoes ; m variaveis
n = int(n)
m = int(m)
c = np.array(entrada.readline().split(), dtype='float32') #vetor de custo c, com m inteiros

A =  np.zeros((n, m))
b = np.zeros(n)

for i in range(n):
    linha = np.array(entrada.readline().split())
    A[i] = linha[:-1]
    b[i] = linha[-1]

simplex = Simplex(n,m,c,A,b)

simplex.resolve_PL()

entrada.close()