import heapq
from collections import deque

# 1 Busca Sega
# 1.1 Algoritmo de Busca em Extensão (BE)
def busca_em_largura(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada.\n")
        return None

    fila = deque([(inicio, [inicio])])
    visitados = set()

    while fila:
        cidade_atual, caminho = fila.popleft()

        if cidade_atual == objetivo:
            print(f"Caminho encontrado (BE): {' -> '.join(caminho)}\n")
            return caminho

        if cidade_atual not in visitados:
            visitados.add(cidade_atual)
            for vizinho, _ in grafo.get(cidade_atual, []):
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [vizinho]))

    print("Nenhum caminho encontrado com BE.")
    return None

#1.2 Algoritmo de Busca de Custo Uniforme (BCU)
def busca_custo_uniforme(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada.")
        return None, None

    fila = []
    heapq.heappush(fila, (0, inicio, [inicio]))
    visitados = set()

    while fila:
        custo_atual, cidade_atual, caminho = heapq.heappop(fila)

        if cidade_atual == objetivo:
            print(f"Caminho encontrado (BCU): {' -> '.join(caminho)}")
            print(f"Custo total: {custo_atual} km\n")
            return caminho, custo_atual

        if cidade_atual in visitados:
            continue
        visitados.add(cidade_atual)

        for vizinho, custo in grafo.get(cidade_atual, []):
            if vizinho not in visitados:
                heapq.heappush(fila, (custo_atual + custo, vizinho, caminho + [vizinho]))

    print("Nenhum caminho encontrado com BCU.")
    return None, None

# 1.3 Algoritmo de Busca em Profundidade (BP)
def busca_em_profundidade(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada")
        return None
    
    pilha = [(0, inicio, [inicio])]
    visitados = set()
    
    while pilha:
        custo_atual, cidade_atual, caminho =pilha.pop()
        
        if cidade_atual == objetivo:
            print(f"Caminho encontrado (BP): {' -> '.join(caminho)}")
            print(f" Custo total: {custo_atual} km\n")
            return caminho, custo_atual
        
        if cidade_atual not in visitados:
            visitados.add(cidade_atual)
            
            for vizinho, custo in reversed(grafo.get(cidade_atual, [])):
                if vizinho not in visitados:
                    pilha.append((custo_atual + custo, vizinho, caminho + [vizinho]))   # Retira o último elemento da pilha
                    
    print("Nenhum caminho encontrado com BP")
    return None

# 1.4 Algoritmo de Busca em Profundidade Limitada(BPL)
def busca_em_profundidade_limitada(grafo, inicio, objetivo, limite):
    def dls_recursivo(cidade, caminho, profundidade, custo_total):
        if profundidade > limite:
            return None, None  # Excedeu o limite

        if cidade == objetivo:
            return caminho, custo_total

        for vizinho, custo in grafo.get(cidade, []):
            if vizinho not in caminho:
                resultado, custo_final = dls_recursivo(vizinho, caminho + [vizinho], profundidade + 1, custo_total + custo)
                if resultado:
                    return resultado,  custo_final

        return None, None

    resultado, custo_total = dls_recursivo(inicio, [inicio], 0, 0)
    
    if resultado:
        print(f"\nCaminho encontrado (BPL): {' -> '.join(resultado)}")
        print(f"Custo total: {custo_total} km\n")
        return resultado, custo_total
    else:
        print(f"Nenhum caminho encontrado dentro do limite {limite}.")
        return None

#1.5 Algoritmo de Busca Aprofundamento Iterativo (BAIP)
def busca_aprofundamento_iterativo(grafo, inicio, objetivo, limite_max=20):
    print(f"Iniciando busca de aprofundamento iterativo de {inicio} para {objetivo}...")
    for limite in range(limite_max + 1):
        print(f"Tentando limite de profundidade: {limite}")
        resultado = busca_em_profundidade_limitada(grafo, inicio, objetivo, limite)
        
        # Verifica se o retorno não é None antes de desempacotar
        if resultado is not None:
            caminho, custo_total = resultado  # Desempacotando corretamente o retorno
            print(f"Caminho encontrado com IDS: {' -> '.join(caminho)}")
            print(f"Custo total: {custo_total} km\n")
            return caminho, custo_total
        else:
            print(f"Nenhum caminho encontrado com limite {limite}.")
    
    print("Nenhum caminho encontrado com IDS.")
    return None, None

#1.6 Algoritmo de Busca Bidirecional (BB)
from collections import deque

def busca_bidirecional(grafo, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada.")
        return None, None

    frente_inicio = deque([(inicio, [inicio], 0)])  # Fila a partir da origem
    frente_objetivo = deque([(objetivo, [objetivo], 0)])  # Fila a partir do destino
    visitados_inicio = {inicio: (0,[inicio])}
    visitados_objetivo = {objetivo: (0,[objetivo])}

    while frente_inicio and frente_objetivo:
        # Expande do início
        caminho_inicio, custo_inicio = expandir_fronteira(fronteira=frente_inicio, visitados_atual=visitados_inicio, visitados_oposto=visitados_objetivo, grafo=grafo)
        if caminho_inicio:
            print(f"Caminho encontrado (BB): {' -> '.join(caminho_inicio)}")
            print(f"custo total: {custo_inicio} km\n")
            return caminho_inicio, custo_inicio

        # Expande do destino
        caminho_objetivo, custo_objetivo = expandir_fronteira(fronteira=frente_objetivo, visitados_atual=visitados_objetivo, visitados_oposto=visitados_inicio, grafo=grafo)
        if caminho_objetivo:
            print(f"Caminho encontrado (BB): {' -> '.join(caminho_objetivo)}")
            print(f"custo total: {custo_objetivo}km\n")
            return caminho_objetivo, custo_objetivo

    print("Nenhum caminho encontrado com busca bidirecional.")
    return None, None

def expandir_fronteira(fronteira, visitados_atual, visitados_oposto, grafo):
    cidade_atual, caminho, custo_atual = fronteira.popleft()
    
    for vizinho, custo in grafo.get(cidade_atual, []):
        if vizinho not in visitados_atual:
            novo_caminho = caminho + [vizinho]
            novo_custo = custo_atual + custo
            visitados_atual[vizinho] = (novo_caminho, novo_custo)
            fronteira.append((vizinho, novo_caminho, novo_custo))

            if vizinho in visitados_oposto:
                caminho_oposto, custo_oposto = visitados_oposto[vizinho]
                caminho_final = novo_caminho[:-1] + list(reversed(caminho_oposto))
                custo_final= novo_custo + custo_oposto
                return caminho_final, custo_final  # Junta os caminhos encontrados

    return None, None

# 2 Com Informação
# 2.1 Busca gulosa 
def busca_gulosa(grafo, heuristica, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada.")
        return None, None
    
    if objetivo != "Bucharest":
        print("Aviso: A busca gulosa foi projetada para o destino 'Bucharest'. Os resultados podem não ser ideais.")
    
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (heuristica[inicio], inicio, [inicio]))
    visitados = set()
    
    while fila_prioridade:
        _, cidade_atual, caminho = heapq.heappop(fila_prioridade)
        
        if cidade_atual == objetivo:
            print(f"\nCaminho encontrado (Busca Gulosa): {' -> '.join(caminho)}\n")
            return caminho, heuristica[cidade_atual]
        
        if cidade_atual not in visitados:
            visitados.add(cidade_atual)
            
            for vizinho, _ in grafo.get(cidade_atual, []):
                if vizinho not in visitados:
                    heapq.heappush(fila_prioridade, (heuristica[vizinho], vizinho, caminho + [vizinho]))
                    
    print("Nenhum caminho encontrado com Busca Gulosa.")
    return None, None

# Busca A Estrela
def busca_a_estrela(grafo, heuristica, inicio, objetivo):
    if inicio not in grafo or objetivo not in grafo:
        print("Cidade de origem ou destino não encontrada.")
        return None, None

    fila_prioridade = []
    heapq.heappush(fila_prioridade, (heuristica[inicio], 0, inicio, [inicio]))  # (f, g, cidade, caminho)
    visitados = {}

    while fila_prioridade:
        _, custo_g, cidade_atual, caminho = heapq.heappop(fila_prioridade)

        if cidade_atual == objetivo:
            print(f"\nCaminho encontrado (A*): {' -> '.join(caminho)}")
            print(f"Custo total: {custo_g} km\n")
            return caminho, custo_g

        if cidade_atual in visitados and visitados[cidade_atual] <= custo_g:
            continue  # Já encontramos um caminho melhor para essa cidade

        visitados[cidade_atual] = custo_g  # Marca como visitado com o menor custo encontrado

        for vizinho, custo in grafo.get(cidade_atual, []):
            novo_custo_g = custo_g + custo  # Atualiza g(n)
            f_n = novo_custo_g + heuristica.get(vizinho, float('inf'))  # Calcula f(n)
            heapq.heappush(fila_prioridade, (f_n, novo_custo_g, vizinho, caminho + [vizinho]))

    print("Nenhum caminho encontrado com A*.")
    return None, None

grafo = {
    'Oradea': [('Zerind',71), ('Sibiu',151)],
    'Zerind': [('Arad',75), ('Oradea',71)],
    'Sibiu': [('Rimnicu Vilcea', 80),('Fagaras',99), ('Arad', 140), ('Oradea',151)],
    'Arad': [('Timisoara', 118),('Sibiu', 140), ('Zerind', 75)],
    'Fagaras': [('Bucharest',211), ('Sibiu',99)],
    'Rimnicu Vilcea':[('Pitesti',97), ('Craiova',146),('Sibiu',80)],
    'Timisoara': [('Lugoj', 111),('Arad',118) ],
    'Craiova': [('Drobeta', 120), ('Pitesti', 101), ('Rimnicu Vilcea', 146)],
    'Pitesti': [('Craiova',138),('Bucharest', 101), ('Rimnicu Vilcea', 97)],
    'Lugoj': [('Mehadia',70), ('Timisoara',111)],
    'Mehadia': [('Drobeta',75), ('Lugoj', 70)],
    'Drobeta': [('Craiova', 120), ('Mehadia',75)],
    'Bucharest': [('Pitesti',101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest',90)],
    'Urziceni': [('Bucharest',85), ('Hirsova',98), ('Vaslui',142)],
    'Hirsova': [('Urziceni',98), ('Eforie',86)],
    'Eforie': [('Hirsova',86)],
    'Vaslui':[('Urziceni',142), ('Iasi',92)],
    'Iasi': [('Vaslui',92), ('Neamt',87)],
    'Neamt':[('Iasi',87)]
}

heuristica = {
    "Arad": 366, "Zerind": 374, "Oradea": 380, "Sibiu": 253, "Fagaras": 176,
    "Rimnicu Vilcea": 193, "Pitesti": 100, "Bucharest": 0, "Timisoara": 329,
    "Lugoj": 244, "Mehadia": 241, "Drobeta": 242, "Craiova": 160,
    "Giurgiu": 77, "Urziceni": 80, "Vaslui": 199, "Iasi": 226, "Neamt": 234,
    "Hirsova": 151, "Eforie": 161
}
print("cidades disponíveis:",','.join(grafo.keys()))
origem = input("Escolha a origem: ").strip().title()
destino = input("Escolha o destino: ").strip().title()
limite = int(input("Digite o limite de profundidade para a BP: "))
    
if origem in grafo and destino in grafo:
    busca_em_largura(grafo, origem, destino)
    busca_custo_uniforme(grafo, origem, destino)
    busca_em_profundidade(grafo, origem, destino)
    busca_em_profundidade_limitada(grafo, origem, destino, limite=10)
    busca_aprofundamento_iterativo(grafo, origem, destino)
    busca_bidirecional(grafo, origem, destino)
    busca_gulosa(grafo, heuristica, origem, destino)
    busca_a_estrela(grafo, heuristica, origem, destino)

else:
    print("Cidade de origem ou destino não encontrada no grafo.")
