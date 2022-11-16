import numpy as np
from sys import exit

def troca(B, N, Bpos, Npos, cb, cn, entra, sai):
	for i in range(0,m):
		N[i][entra], B[i][sai] = B[i][sai], N[i][entra]

	cb[sai], cn[entra] = cn[entra], cb[sai]
	Bpos[sai], Npos[entra] = Npos[entra], Bpos[sai]

def passo(B, N, cb, cn):
	##calculo do vetor simplex
	lamb = np.linalg.solve(np.transpose(B), cb)

	##calculo dos custos relativos
	cnr = []

	for i in range(0,len(cn)):
		cnr_input = cn[i] - np.matmul(np.transpose(lamb), np.transpose(N)[i])
		cnr.append(cnr_input)

	##escolha da variavel que entra na base
	cnr_entra = np.amin(cnr)
	entra = cnr.index(cnr_entra)

	return (cnr, entra)

def perturba(xb, y):
	##verifica a variavel que sai
	ep = []

	for i in range(0,m):
		if(y[i] > 0):
			ep.append(xb[i]/y[i])

	ep_entra = np.amin(ep)
	sai = ep.index(ep_entra)

	return sai

##entradas iniciais
n = input("Numero de variaveis = ") ##numero de variaveis de decisao
m = input("Numero de restricoes = ") ##numero de restricoes

c = []
A = []
b = []

##entra com as matrizes c, b e A
print("Entre com o vetor c: ")
for i in range(n):
	c_input = float(input("c%d = " % (i+1)))
	c.append(c_input)

print("Entre com o vetor b: ")
for i in range(0,m):
	b_input = float(input("b%d = " % (i+1)))
	b.append(b_input)

print("Entre com a matriz A")
for i in range(0,m):
	A.append([])
	print("Restricao %d: " % (i+1))
	for j in range(0,n):
		A_input = float(input("a%d,%d = " % (i+1, j+1)))
		A[i].append(A_input)

#Fase 1
##cria a matriz de variaveis artificiais
B = []
N = []

B = np.identity(m)
Bpos = range(n,m+n)

N = A
Npos = range(0,n)

##determina custos basicos e nao basicos
cb = [1.] * m
cn = [0.] * n

while not all(k == 0 for k in cb):
	##resolucao da solucao basica
	xb = np.linalg.solve(B, b)

	##resolve primeiro passo do simplex
	(cnr, entra) = passo(B, N, cb, cn)

	##verifica otimilidade
	if all(i >= 0 for i in cnr):
		print("## Otimo encontrado ##")
		for j in range(0,len(Bpos)):
			print("x%d = %.3f" % (Bpos[j]+1, xb[j]))
		for j in range(0,len(Npos)):
			print("x%d = %.3f" % (Npos[j]+1, 0))
		exit()

	##calcula a direcao
	y = np.linalg.solve(B, np.transpose(N)[entra])

	##verifica se solucao e finita
	if all(i <= 0 for i in y):
		print("## Nao tem solucao finita ##")
		exit()

	##perturba
	sai = perturba(xb, y)

	##troca as variaveis
	troca(B, N, Bpos, Npos, cb, cn, entra, sai)
			
#Fase 2
##remove variaveis artificiais
remove = []

for i in range(0,n):
	if cn[i] != 0:
		remove.append(i)	

Npos = np.delete(Npos, remove)
N = np.delete(N, remove, axis=1)

##atribui os custos reais
cb = []
cn = []

for i in range(0,n-m):
	cn.append(c[Npos[i]])

for i in range(0,m):
	cb.append(c[Bpos[i]])

while(1):
	##resolucao da solucao basica
	xb = np.linalg.solve(B, b)

	##resolve primeiro passo do simplex
	(cnr, entra) = passo(B, N, cb, cn)

	##verifica otimilidade
	if all(i >= 0 for i in cnr):
		print("## Otimo encontrado ##")
		for j in range(0,m):
			print("x%d = %.3f" % (Bpos[j]+1, xb[j]))
		for j in range(0,n-m):
			print("x%d = %.3f" % (Npos[j]+1, 0))
		exit()

	##calcula a direcao
	y = np.linalg.solve(B, np.transpose(N)[entra])

	##verifica se solucao e finita
	if all(i <= 0 for i in y):
		print("## Nao tem solucao finita ##")
		exit()

	##perturba
	sai = perturba(xb, y)

	##troca as variaveis
	troca(B, N, Bpos, Npos, cb, cn, entra, sai)

