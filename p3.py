from pulp import *

def maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes):
    # Criação do modelo
    modelo = LpProblem("Maximizar_Lucro", LpMaximize)

    # Variáveis de decisão
    x = LpVariable.dicts("brinquedo", range(t), 0, max_brinquedos, LpInteger)
    y = LpVariable.dicts("pacote", range(p), 0, None, LpInteger)

    # Função objetivo
    modelo += lpSum(brinquedos[i][0] * x[i] for i in range(t)) + \
                lpSum(pacotes[j][3] * y[j] for j in range(p)), "Lucro_Total"

    # Restrições de capacidade de produção
    for i in range(t):
        modelo += x[i] <= brinquedos[i][1], f"Capacidade_Producao_Brinquedo_{i}"

    # Restrições de capacidade total
    modelo += lpSum(x[i] for i in range(t)) <= max_brinquedos, "Capacidade_Total"

    # Restrições de pacotes
    for j in range(p):
        # Verifica se a chave existe no dicionário antes de acessar
        if pacotes[j][:3] and all(i < t for i in pacotes[j][:3]):
            modelo += lpSum(x[i] for i in pacotes[j][:3]) >= y[j], f"Brinquedos_Pacote_{j}"

    # Resolve o modelo
    modelo.solve()

    # Retorna o valor da função objetivo (lucro máximo)
    return value(modelo.objective)


###############################################################################
# Leitura dos dados de entrada
entrada = input().split()
t, p, max_brinquedos = map(int, entrada[:3])
brinquedos = [tuple(map(int, input().split())) for _ in range(t)]
pacotes = [tuple(map(int, input().split())) for _ in range(p)]

# Chamada da função e impressão do resultado
resultado = maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes)
print(resultado)
###############################################################################