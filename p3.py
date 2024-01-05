from pulp import *

def maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes):
    # Criação do modelo
    modelo = LpProblem("Maximizar_Lucro", LpMaximize)

    x = [False]
    for i in range(1, t + 1):
        max = max_brinquedos
        if max > brinquedos[i][1]:
            max = brinquedos[i][1]
        xi = LpVariable("brinquedo_" + str(i), 0, max, LpInteger)
        modelo += xi <= max, "Capacidade_Brinquedo_" + str(i)
        x += [xi]
            
    somas = [0] * (t+1)
    
    y = [False]
    for j in range(1, p + 1):
        max = max_brinquedos
        if max > brinquedos[pacotes[j][0]][1]:
            max = brinquedos[pacotes[j][0]][1]
                 
        if max > brinquedos[pacotes[j][1]][1]:
            max = brinquedos[pacotes[j][1]][1]
            
        if max > brinquedos[pacotes[j][2]][1]:
            max = brinquedos[pacotes[j][2]][1]
            
        yj = LpVariable("pacote_" + str(j), 0, max, LpInteger)
        y += [yj]
        somas[pacotes[j][0]] += yj
        somas[pacotes[j][1]] += yj
        somas[pacotes[j][2]] += yj
    
    # Restrição de soma    
    for i in range(1, t + 1):
        modelo += x[i] >= somas[i], "Restricao_Somas_" + str(i)
    
    # Função objetivo
    modelo += lpSum(brinquedos[i][0] * (x[i] - somas[i])  for i in range(1, t + 1)) + \
              lpSum(pacotes[j][3] * y[j] for j in range(1, p + 1)), "Lucro_Total"
        
    # Restrição de capacidade total de produção
    modelo += lpSum(x[i] for i in range(1, t+1)) <= max_brinquedos, "Capacidade_Total"
      
    
    modelo.solve(GLPK(msg=0))

    return int(value(modelo.objective))


################################################################################
# Leitura dos dados de entrada
t, p, max_brinquedos = map(int, input().split())
brinquedos = [False] + [tuple(map(int, input().split())) for _ in range(t)]
pacotes = [False] + [tuple(map(int, input().split())) for _ in range(p)]

# Chamada da função e impressão do resultado
resultado = maximizar_lucro(t, p, max_brinquedos, brinquedos, pacotes)
print(resultado)
################################################################################