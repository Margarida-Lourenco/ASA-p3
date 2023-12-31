from pulp import *

def maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes):
    # Criação do modelo
    modelo = LpProblem("Maximizar_Lucro", LpMaximize)

    # Variáveis de decisão
    x = LpVariable.dicts("brinquedo", range(1, t + 1), 0, None, LpInteger)
    y = LpVariable.dicts("pacote", range(1, p + 1), 0, None, LpInteger)

    # Função objetivo
    modelo += lpSum(brinquedos[i-1][0] * x[i] for i in range(1, t + 1)) + \
              lpSum(pacotes[j-1][3] * y[j] for j in range(1, p + 1)), "Lucro_Total"

    # Restrições de capacidade de produção de cada brinquedo
    for i in range(1, t + 1):
        modelo += x[i] <= brinquedos[i-1][1], f"Capacidade_Producao_Brinquedo_{i}"

    # Restrição de capacidade total de produção
    modelo += lpSum(x[i] for i in range(1, t + 1)) \
            + lpSum(pacotes[j-1][3] * y[j] for j in range(1, p + 1)) <= max_brinquedos, "Capacidade_Total"

    modelo.solve(GLPK(msg=0))

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