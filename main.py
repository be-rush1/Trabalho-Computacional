
import pyomo.environ as pyEnv
path = '/Applications/CPLEX_Studio_Community2211/cplex/bin/x86-64_osx/cplex'

cost_matrix = [[99999999999]*20 for i in range(20)]
##-------------------------LEITURA DA INSTÂNCIA--------------------##
file = open('cidades2')
lines = file.readlines()
file.close()
for j in range(len(lines)):
    aux = lines[j][:-1].split('\t')
    cost_matrix[int(aux[0])][int(aux[1])] = float(aux[-1])
    cost_matrix[int(aux[1])][int(aux[0])] = float(aux[-1])
                #aux = [int(i) for i in aux if i != '']
    #cost_matrix.append(aux)
print(cost_matrix)
n = len(cost_matrix)

##-------------------------DECLARACAO DO MODELO E SEUS PARAMETROS--------------------##

# Modelo
modelo = pyEnv.ConcreteModel()
# Indices para as cidades
modelo.M = pyEnv.RangeSet(n)
modelo.N = pyEnv.RangeSet(n)
# Indice auxiliar para a variavel u
modelo.U = pyEnv.RangeSet(2, n)

# Variavel de decisao xij
modelo.x = pyEnv.Var(modelo.N, modelo.M, within=pyEnv.Binary)
# Variavel de decisao auxiliar u
modelo.u = pyEnv.Var(modelo.N, within=pyEnv.NonNegativeIntegers, bounds=(0, n - 1))

# Matriz de custo cij
modelo.c = pyEnv.Param(modelo.N, modelo.M, initialize=lambda modelo, i, j: cost_matrix[i - 1][j - 1])


##-------------------------DECLARACAO DA FUNCAO OBJETIVO E RESTRICOES--------------------##

def func_objetivo(modelo):
    return sum(modelo.x[i, j] * modelo.c[i, j] for i in modelo.N for j in modelo.M)


modelo.objetivo = pyEnv.Objective(rule=func_objetivo, sense=pyEnv.minimize)


##------------------------------------------------------##
# So sai 1 caminho de cada cidade

def rule_rest1(modelo, M):
    return sum(modelo.x[i, M] for i in modelo.N if i != M) == 1


modelo.rest1 = pyEnv.Constraint(modelo.M, rule=rule_rest1)


##------------------------------------------------------##
# So entra 1 caminho em cada cidade

def rule_rest2(modelo, N):
    return sum(modelo.x[N, j] for j in modelo.M if j != N) == 1


modelo.rest2 = pyEnv.Constraint(modelo.N, rule=rule_rest2)


##------------------------------------------------------##
# Restricao de quebra de ciclos

def rule_rest3(modelo, i, j):
    if i != j:
        return modelo.u[i] - modelo.u[j] + modelo.x[i, j] * n <= n - 1
    else:
        # Sim, essa restricao desse else nao diz nada
        return modelo.u[i] - modelo.u[i] == 0


modelo.rest3 = pyEnv.Constraint(modelo.U, modelo.N, rule=rule_rest3)

##-------------------------RESOLUCAO DO MODELO--------------------##
solver = pyEnv.SolverFactory('cplex', executable=path)
resultado = solver.solve(modelo, tee=True)
print('\n-------------------------\n')
# modelo.pprint()
# modelo.objetivo()
print(resultado)

##-------------------------PRINT DAS VARIAVEIS DE DECISAO ESCOLHIDAS--------------------##

lista = list(modelo.x.keys())
res = []
for i in lista:
    if modelo.x[i]() != 0:
        res.append(i)
        print(i, '--', modelo.x[i]())
print(res)
