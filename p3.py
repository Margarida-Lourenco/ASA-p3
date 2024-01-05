from pulp import *

def maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes):
    # Criação do modelo
    modelo = LpProblem("Maximizar_Lucro", LpMaximize)

    # Variáveis de decisão
    x = LpVariable.dicts("brinquedo", range(1, t + 1), 0, None, LpInteger)
    y = LpVariable.dicts("pacote", range(1, p + 1), 0, None, LpInteger)
    # z indica se o brinquedo i está no pacote j, 1 se sim, 0 se não
    z = LpVariable.dicts("no_pacote", ((i,j) for i in range(1, t + 1) for j in range(1, p + 1)), cat=LpBinary)
    
    # Preenchendo a variável z com base nos dados
    for i in range(1, t + 1):
        for j in range(1, p + 1):
            z[i, j].value = 0  # Inicialmente, nenhum brinquedo está no pacote
            if i in pacotes[j - 1][:-1]:
                z[i, j].value = 1  # Se o brinquedo i está no pacote j, atribui 1

    # Função objetivo
    modelo += lpSum(brinquedos[i-1][0] * x[i] for i in range(1, t + 1)) + \
              lpSum(pacotes[j-1][3] * y[j] for j in range(1, p + 1)), "Lucro_Total"

    # Restrições de capacidade de produção de cada brinquedo
    for i in range(1, t + 1):
        modelo += x[i] <= brinquedos[i-1][1], f"Capacidade_Producao_Brinquedo_{i}"
        
    # Restrição de capacidade total de produção
    modelo += lpSum(x[i] for i in x) + \
            + lpSum(3 * y[j] for j in range(1, p + 1)) <= max_brinquedos, "Capacidade_Total"

    # Para construir um pacote, é necessário produzir pelo menos 1 de cada brinquedo que o compõe
    for j in range(1, p + 1):
        for i in range(1, t + 1):
            if z[i,j] == 1:       # Se o brinquedo i está no pacote j
                modelo += x[i] >= y[j], f"Brinquedo_{i}_no_Pacote_{j}"
            
        # Restrição do lucro do pacote
    for j in range(1, p + 1):
        modelo += lpSum(z[i,j] * brinquedos[i-1][0] for i in x) <= pacotes[j-1][3], f"Lucro_Pacote_{j}"
        
    modelo.solve(GLPK(msg=0))

    for i in x:
        for j in y:
            print(f"Brinquedo {i} no pacote {j}: {z[i,j].varValue}")
            
    for i in x:
        print(f"Brinquedo {i}: {x[i].varValue}")  # Imprime a quantidade de brinquedos i produzidos
        
    for j in y:
        print(f"Pacote {j}: {y[j].varValue}")   # Imprime a quantidade de pacotes j produzidos

    return int(value(modelo.objective))


################################################################################
# Leitura dos dados de entrada
entrada = input().split()
t, p, max_brinquedos = map(int, entrada[:3])
brinquedos = [tuple(map(int, input().split())) for _ in range(t)]
pacotes = [tuple(map(int, input().split())) for _ in range(p)]

# Chamada da função e impressão do resultado
resultado = maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes)
print(resultado)
################################################################################