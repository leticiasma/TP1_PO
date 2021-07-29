import numpy as np
from simplex import Simplex
#from simplexteste import Simplex

#precisao
#correcao do output automatica ou manual
#usar todos os round e isclose
#guardar quais colunas fazem parte da base acho melhor na hora de achar a solucao na funcao q eu fiz

#tratar arredondamentos, já que estou printando string, mas, provavelmente, tem que ser em numero

n,m = input().split() #n restricoes ; m variaveis
n = int(n)
m = int(m)
c = np.array(input().split(), dtype='float32') #vetor de custo c, com m inteiros

A =  np.zeros((n, m))
b = np.zeros(n)

for i in range(n):
    linha = np.array(input().split())
    A[i] = linha[:-1]
    b[i] = linha[-1]

simplex = Simplex(n,m,c,A,b)

simplex.resolve_PL()