import graphviz
from collections import defaultdict

# Função para gerar a imagem do AFD


def gerar_imagem_afd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, nome_arquivo='afd'):
    dot = graphviz.Digraph()

    # Define Layout Horizontal
    dot.attr(rankdir='LR')

    # Adiciona os estados ao grafo
    for estado in estados:
        if estado in estados_aceitacao:
            # Estados de aceitação com círculo duplo
            dot.node(estado, shape='doublecircle')
        else:
            dot.node(estado, shape='circle')

    # Adiciona o estado inicial com uma seta extra
    dot.node('start', shape='point')  # Nó invisível para o estado inicial
    dot.edge('start', estado_inicial)

    # Adiciona as transições
    for (estado, simbolo), proximo_estado in funcoes_transicao.items():
        if proximo_estado is not None:
            dot.edge(estado, proximo_estado, label=simbolo)

    # Renderiza o arquivo .dot e a imagem
    dot.render(nome_arquivo, format='png', cleanup=True)
    print(f'Imagem do AFD gerada: {nome_arquivo}.png')

# Função para gerar a imagem do AFND


def gerar_imagem_afnd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, nome_arquivo='afnd'):
    dot = graphviz.Digraph()

    # Define Layout Horizontal
    dot.attr(rankdir='LR')

    # Adiciona os estados ao grafo
    for estado in estados:
        if estado in estados_aceitacao:
            # Estados de aceitação com círculo duplo
            dot.node(estado, shape='doublecircle')
        else:
            dot.node(estado, shape='circle')

    # Adiciona o estado inicial com uma seta extra
    dot.node('start', shape='point')  # Nó invisível para o estado inicial
    dot.edge('start', estado_inicial)

    # Adiciona as transições
    for (estado, simbolo), proximos_estados in funcoes_transicao.items():
        for proximo_estado in proximos_estados:
            if proximo_estado is not None:
                dot.edge(estado, proximo_estado, label=simbolo)

    # Renderiza o arquivo .dot e a imagem
    dot.render(nome_arquivo, format='png', cleanup=True)
    print(f'Imagem do AFND gerada: {nome_arquivo}.png')

# Função para simular o AFND


def simular_afnd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, entrada):
    estados_atuais = {estado_inicial}

    for simbolo in entrada:
        novos_estados = set()
        for estado in estados_atuais:
            if (estado, simbolo) in funcoes_transicao:
                novos_estados.update(funcoes_transicao[(estado, simbolo)])
        estados_atuais = novos_estados

    return len(estados_atuais.intersection(estados_aceitacao)) > 0

# Função para simular o AFD


def simular_afd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, entrada):
    estado_atual = estado_inicial
    for simbolo in entrada:
        estado_atual = funcoes_transicao.get((estado_atual, simbolo))
        if estado_atual is None:
            return False
    return estado_atual in estados_aceitacao

# Função para converter AFND para AFD


def converter_afnd_para_afd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao):
    novo_estado_inicial = frozenset([estado_inicial])
    novos_estados = set([novo_estado_inicial])
    novos_estados_aceitacao = set()
    novas_funcoes_transicao = {}

    fila = [novo_estado_inicial]
    while fila:
        estado_atual = fila.pop(0)
        for simbolo in alfabeto:
            novos_estados_resultantes = set()
            for estado in estado_atual:
                if (estado, simbolo) in funcoes_transicao:
                    novos_estados_resultantes.update(
                        funcoes_transicao[(estado, simbolo)])
            novo_estado = frozenset(novos_estados_resultantes)
            if novo_estado:
                novas_funcoes_transicao[(estado_atual, simbolo)] = novo_estado
                if novo_estado not in novos_estados:
                    novos_estados.add(novo_estado)
                    fila.append(novo_estado)

    for novo_estado in novos_estados:
        if novo_estado.intersection(estados_aceitacao):
            novos_estados_aceitacao.add(novo_estado)

    # Converte os estados para strings para a visualização
    estados_afd = {str(estado) for estado in novos_estados}
    funcoes_transicao_afd = {(str(origem), simbolo): str(destino)
                             for (origem, simbolo), destino in novas_funcoes_transicao.items()}
    estados_aceitacao_afd = {str(estado) for estado in novos_estados_aceitacao}
    estado_inicial_afd = str(novo_estado_inicial)

    return estados_afd, alfabeto, funcoes_transicao_afd, estado_inicial_afd, estados_aceitacao_afd

# Função para minimizar AFD


def minimizar_afd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao):
    P = [set(estados_aceitacao), set(estados) - set(estados_aceitacao)]
    W = [set(estados_aceitacao), set(estados) - set(estados_aceitacao)]

    while W:
        A = W.pop()
        for simbolo in alfabeto:
            X = {estado for estado in estados if (
                estado, simbolo) in funcoes_transicao and funcoes_transicao[(estado, simbolo)] in A}
            for Y in P[:]:
                intersecao = X & Y
                diferenca = Y - X
                if intersecao and diferenca:
                    P.append(intersecao)
                    P.append(diferenca)
                    P.remove(Y)
                    if Y in W:
                        W.remove(Y)
                        W.append(intersecao)
                        W.append(diferenca)
                    else:
                        if len(intersecao) <= len(diferenca):
                            W.append(intersecao)
                        else:
                            W.append(diferenca)

    novo_estados = {'_'.join(sorted(particao)) for particao in P}
    novo_estado_inicial = next(('_'.join(sorted(particao))
                               for particao in P if estado_inicial in particao), None)
    novos_estados_aceitacao = {'_'.join(
        sorted(particao)) for particao in P if particao & set(estados_aceitacao)}
    novas_funcoes_transicao = {}
    for particao in P:
        novo_estado = '_'.join(sorted(particao))
        for simbolo in alfabeto:
            destinos = {funcoes_transicao[(estado, simbolo)] for estado in particao if (
                estado, simbolo) in funcoes_transicao}
            if destinos:  # Apenas considere destinos não vazios
                destino = next(iter(destinos))  # Obtém um elemento do conjunto
                destino_particao = next(('_'.join(sorted(p))
                                        for p in P if destino in p), None)
                if destino_particao:
                    novas_funcoes_transicao[(
                        novo_estado, simbolo)] = destino_particao

    return novo_estados, alfabeto, novas_funcoes_transicao, novo_estado_inicial, novos_estados_aceitacao


while True:
    # Menu principal para seleção do tipo de autômato
    print("Escolha o tipo de autômato (1 para AFD, 2 para AFND, 3 para Converter AFND para AFD, 4 para Minimizar AFD, 5 para Sair): ", end="")
    tipo_automato = int(input())

    if tipo_automato == 5:
        print("Saindo do programa...")
        break

    estados = []  # Lista para os estados
    alfabeto = []  # Lista para o alfabeto
    funcoes_transicao = {}  # Dicionário para as funções de transição
    estado_inicial = ""  # String para o estado inicial
    estados_aceitacao = []  # Lista para os estados de aceitação

    print("Informe o conjunto de estados: ", end="")
    estados = input().split()

    print("Informe o alfabeto: ", end="")
    alfabeto = input().split()

    print("Informe o estado inicial: ", end="")
    estado_inicial = input()

    print("Informe o conjunto de estados de aceitação: ", end="")
    estados_aceitacao = input().split()

    print("Defina as funções de transição:")
    for estado in estados:
        for simbolo in alfabeto:
            #print(f"\tPara o estado {estado} com o símbolo '{
                  #simbolo}', informe os estados de destino separados por espaço (ou deixe vazio para nenhuma transição):")
            print(f"\t {simbolo}")
            print(f"{estado}\t----->\t", end="")
            transicoes = input().split()
            if tipo_automato == 1:
                funcoes_transicao[(estado, simbolo)
                                  ] = transicoes[0] if transicoes else None
            else:
                funcoes_transicao[(estado, simbolo)] = frozenset(transicoes)

    # Gerar imagem do autômato
    if tipo_automato == 1:
        gerar_imagem_afd(estados, alfabeto, funcoes_transicao,
                         estado_inicial, estados_aceitacao)
    elif tipo_automato == 2:
        gerar_imagem_afnd(estados, alfabeto, funcoes_transicao,
                          estado_inicial, estados_aceitacao)
    elif tipo_automato == 3:
        estados_afd, alfabeto_afd, funcoes_transicao_afd, estado_inicial_afd, estados_aceitacao_afd = converter_afnd_para_afd(
            estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao)
        gerar_imagem_afd(estados_afd, alfabeto_afd, funcoes_transicao_afd,
                         estado_inicial_afd, estados_aceitacao_afd)
    elif tipo_automato == 4:
        estados_min, alfabeto_min, funcoes_transicao_min, estado_inicial_min, estados_aceitacao_min = minimizar_afd(
            estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao)
        if estado_inicial_min is not None:
            gerar_imagem_afd(estados_min, alfabeto_min, funcoes_transicao_min,
                             estado_inicial_min, estados_aceitacao_min)
        else:
            print("Erro ao minimizar: estado inicial não encontrado.")

    # Loop de reconhecimento
    while tipo_automato in [1, 2]:
        print("\nEscolha uma opção:")
        print("1. Reconhecer uma linguagem")
        print("2. Voltar ao menu principal")
        opcao = int(input("Opção: "))

        if opcao == 2:
            break
        elif opcao == 1:
            entrada = input("Informe a linguagem a ser reconhecida: ")
            if tipo_automato == 1:
                if simular_afd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, entrada):
                    print("Reconheceu")
                else:
                    print("NÃO reconheceu")
            else:
                if simular_afnd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, entrada):
                    print("Reconheceu")
                else:
                    print("NÃO reconheceu")
        else:
            print("Opção inválida! Tente novamente.")