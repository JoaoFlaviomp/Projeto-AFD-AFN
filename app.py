import streamlit as st
import graphviz
from itertools import product

# Função para coletar as transições do AFD do usuário


def coletar_transicoes_afd(estados, alfabeto):
    if 'transicoes_afd' not in st.session_state:
        st.session_state['transicoes_afd'] = {}

    with st.form("form_transicoes_afd"):
        for estado in estados:
            for simbolo in alfabeto:
                key = f"AFD-{estado}-{simbolo}"
                proximo_estado = st.text_input(f"Transição de {estado} com {simbolo} (deixe vazio para indicar transição inexistente):",
                                               key=key)
                if proximo_estado:  # Apenas adiciona transições definidas
                    st.session_state['transicoes_afd'][(
                        estado, simbolo)] = proximo_estado
        submitted = st.form_submit_button("Salvar Transições AFD")
        if submitted:
            st.success("Transições do AFD salvas com sucesso!")

    return st.session_state['transicoes_afd']

# funçao para gerar imagem do afd


def gerar_imagem_afd(estados, alfabeto, transicoes, estado_inicial, estados_finais):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Normalizar os estados para strings ordenadas e garantir que sejam listados corretamente
    estados = [sorted(map(lambda x: x.strip(), grupo)) if isinstance(
        grupo, (set, list)) else [str(grupo).strip()] for grupo in estados]
    estados_finais = set(map(lambda x: x.strip(), estados_finais))
    estado_inicial = str(estado_inicial).strip()

    # Criar um dicionário para mapear cada estado ao seu grupo correspondente
    estado_para_grupo = {}
    for grupo in estados:
        nome_grupo = ", ".join(grupo)  # Nome do grupo como string concatenada
        for estado in grupo:
            estado_para_grupo[estado] = nome_grupo

    # Criar um conjunto dos nomes dos grupos finais
    grupos_finais = set()
    for grupo in estados:
        nome_grupo = ", ".join(grupo)
        if any(estado in estados_finais for estado in grupo):
            grupos_finais.add(nome_grupo)

    # Adicionar nós para os estados, diferenciando finais e não-finais
    for nome_grupo in estado_para_grupo.values():
        if nome_grupo in grupos_finais:
            dot.node(nome_grupo, shape='doublecircle')  # Estado de aceitação
        else:
            dot.node(nome_grupo, shape='circle')  # Estado normal

    # Adicionar arestas para as transições
    for (estado, simbolo), destino in transicoes.items():
        estado = str(estado).strip()  # Remover espaços extras
        destino = [str(d).strip() for d in destino] if isinstance(
            destino, (list, set)) else [str(destino).strip()]

        # Buscar o grupo correspondente para o estado e o destino
        grupo_estado = estado_para_grupo.get(estado)
        grupo_destino = estado_para_grupo.get(", ".join(sorted(destino)))

        # Verifique se os grupos foram encontrados
        if grupo_estado and grupo_destino:
            dot.edge(grupo_estado, grupo_destino, label=simbolo)
        else:
            print(f"Erro: Estado '{estado}' ou destino '{', '.join(destino)}' não encontrado nos grupos de estados.")

    # Adicionar nó inicial e conectar ao grupo do estado inicial
    grupo_inicial = estado_para_grupo.get(estado_inicial)
    if grupo_inicial:
        dot.node('start', shape='point')
        dot.edge('start', grupo_inicial)
    else:
       print(f"Erro: Estado inicial '{estado_inicial}' não encontrado nos grupos de estados.")
       
    return dot

# Função para simular a aceitação de uma palavra no AFD


def simular_afd_com_palavra(estados, alfabeto, transicoes, estado_inicial, estados_finais, palavra):
    estado_atual = estado_inicial
    for simbolo in palavra:
        if (estado_atual, simbolo) in transicoes:
            estado_atual = transicoes[(estado_atual, simbolo)]
        else:
            return False
    return estado_atual in estados_finais

# Funções para remover estados inalcançáveis


def remover_inalcancaveis(estados, alfabeto, transicoes, estado_inicial):
    alcançáveis = set()

    def dfs(estado):
        if estado not in alcançáveis:
            alcançáveis.add(estado)
            for simbolo in alfabeto:
                if (estado, simbolo) in transicoes:
                    dfs(transicoes[(estado, simbolo)])

    dfs(estado_inicial)
    estados = [estado for estado in estados if estado in alcançáveis]
    return estados

# Função para obter o grupo de um estado na partição


def obter_grupo(estado, particao):
    for grupo in particao:
        if estado in grupo:
            return grupo
    return None

# Função para minimizar AFD


def minimizar_afd(estados, alfabeto, transicoes, estado_inicial, estados_finais):
    estados = remover_inalcancaveis(
        estados, alfabeto, transicoes, estado_inicial)
    P = [set(estados_finais), set(
        [estado for estado in estados if estado not in estados_finais])]

    while True:
        nova_particao = []
        for grupo in P:
            subgrupos = {}
            for estado in grupo:
                assinatura = tuple(frozenset(obter_grupo(transicoes.get(
                    (estado, simbolo), None), P) or []) for simbolo in alfabeto)
                if assinatura not in subgrupos:
                    subgrupos[assinatura] = set()
                subgrupos[assinatura].add(estado)
            nova_particao.extend(subgrupos.values())
        if nova_particao == P:
            break
        P = nova_particao

    novos_estados = {min(grupo): grupo for grupo in P}
    novo_estado_inicial = min(obter_grupo(estado_inicial, P))
    novos_estados_finais = {min(grupo)
                            for grupo in P if grupo & set(estados_finais)}

    novas_transicoes = {}
    for novo_estado, grupo in novos_estados.items():
        representante = next(iter(grupo))
        for simbolo in alfabeto:
            if (representante, simbolo) in transicoes:
                destino = transicoes[(representante, simbolo)]
                novo_destino = min(obter_grupo(destino, P))
                novas_transicoes[(novo_estado, simbolo)] = novo_destino

    return P, alfabeto, novas_transicoes, novo_estado_inicial, list(novos_estados_finais)

# Função para coletar as transições do AFND do usuário


def coletar_transicoes_afnd(estados, alfabeto):
    if 'transicoes_afnd' not in st.session_state:
        st.session_state['transicoes_afnd'] = {}

    with st.form("form_transicoes_afnd"):
        for estado in estados:
            for simbolo in alfabeto:
                key = f"AFND-{estado}-{simbolo}"
                proximos_estados = st.text_input(f"Transição de {estado} com {simbolo} (separados por espaço, deixe vazio para transição inexistente):",
                                                 key=key)
                if proximos_estados:  # Apenas adiciona transições definidas
                    st.session_state['transicoes_afnd'][(
                        estado, simbolo)] = proximos_estados.split()
        submitted = st.form_submit_button("Salvar Transições AFND")
        if submitted:
            st.success("Transições do AFND salvas com sucesso!")

    return st.session_state['transicoes_afnd']

# Função para gerar a imagem de AFND usando Graphviz


def gerar_imagem_afnd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Adiciona os estados ao gráfico
    for estado in estados:
        if estado in estados_aceitacao:
            dot.node(estado, shape='doublecircle')  # Estado de aceitação
        else:
            dot.node(estado, shape='circle')  # Estado normal

    # Adiciona o nó inicial e a seta para o estado inicial
    dot.node('start', shape='point')
    dot.edge('start', estado_inicial)

    # Adiciona as transições do AFND
    for (estado, simbolo), proximos_estados in funcoes_transicao.items():
        for proximo_estado in proximos_estados:
            if proximo_estado:
                dot.edge(estado, proximo_estado, label=simbolo)

    # Exibe o gráfico no Streamlit
    st.graphviz_chart(dot.source)
    st.success('Imagem do AFND gerada e exibida com sucesso.')

# Função para simular a aceitação de uma palavra no AFND


def simular_afnd(estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao, palavra):
    estados_atuais = {estado_inicial}
    for simbolo in palavra:
        novos_estados = set()
        for estado in estados_atuais:
            if (estado, simbolo) in funcoes_transicao:
                novos_estados.update(funcoes_transicao[(estado, simbolo)])
        estados_atuais = novos_estados
    return len(estados_atuais.intersection(estados_aceitacao)) > 0

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
        # Verificar se o estado resultante tem algum estado de aceitação do AFND
        if novo_estado.intersection(estados_aceitacao):
            novos_estados_aceitacao.add(novo_estado)

    estados_afd = {", ".join(sorted(estado)) for estado in novos_estados}
    funcoes_transicao_afd = {(str(", ".join(sorted(origem))), simbolo): ", ".join(sorted(destino))
                             for (origem, simbolo), destino in novas_funcoes_transicao.items()}
    estados_aceitacao_afd = {", ".join(sorted(estado))
                             for estado in novos_estados_aceitacao}
    estado_inicial_afd = ", ".join(sorted(novo_estado_inicial))

    return estados_afd, alfabeto, funcoes_transicao_afd, estado_inicial_afd, estados_aceitacao_afd


def gerar_palavras_teste(alfabeto, n_max=4):
    palavras = []
    for n in range(1, n_max + 1):
        # Corrigido para usar o comprimento n
        for palavra in product(alfabeto, repeat=n):
            palavras.append("".join(palavra))
    return palavras

# Função para demonstrar equivalência entre AFND e AFD


def demonstrar_equivalencia_afnd_afd(estados_afnd, alfabeto, funcoes_transicao_afnd, estado_inicial_afnd, estados_aceitacao_afnd, estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd):
    palavras_teste = gerar_palavras_teste(alfabeto)
    for palavra in palavras_teste:
        aceita_afnd = simular_afnd(estados_afnd, alfabeto, funcoes_transicao_afnd,
                                   estado_inicial_afnd, estados_aceitacao_afnd, palavra)
        aceita_afd = simular_afd_com_palavra(
            estados_afd, alfabeto, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd, palavra)
        if aceita_afnd != aceita_afd:
            st.error(f"Diferença encontrada para a palavra '{palavra}':")
            st.write(f"AFND aceita: {aceita_afnd}, AFD aceita: {aceita_afd}")
            return False
    st.success(
        "AFND e AFD convertido são equivalentes para todas as palavras geradas!")
    return True

# Classe da Máquina de Turing


class MaquinaDeTuring:
    def __init__(self, estados, alfabeto_entrada, alfabeto_fita, simbolo_vazio, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_fita = alfabeto_fita
        self.simbolo_vazio = simbolo_vazio
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.fita = []
        self.head = 0
        self.estado_atual = self.estado_inicial

    def carregar_palavra(self, palavra):
        self.fita = list(palavra) + [self.simbolo_vazio]
        self.head = 0
        self.estado_atual = self.estado_inicial

    def passo(self):
        if self.estado_atual in self.estados_finais:
            return True

        simbolo_atual = self.fita[self.head]
        if simbolo_atual not in self.transicoes[self.estado_atual]:
            return False

        estado_destino, simbolo_novo, direcao = self.transicoes[self.estado_atual][simbolo_atual]
        self.fita[self.head] = simbolo_novo
        self.estado_atual = estado_destino

        if direcao == 'R':
            self.head += 1
        elif direcao == 'L':
            self.head -= 1

        if self.head < 0:
            self.fita.insert(0, self.simbolo_vazio)
            self.head = 0
        elif self.head >= len(self.fita):
            self.fita.append(self.simbolo_vazio)

        return None

    def executar(self):
        while True:
            resultado = self.passo()
            if resultado is not None:
                return resultado

    def obter_resultado(self):
        return ''.join(self.fita).strip(self.simbolo_vazio)

# Função para criar a máquina de Turing de incremento binário


def maquina_incremento_binario():
    estados = {"q0", "q1", "q2", "qa"}
    alfabeto_entrada = {"0", "1"}
    alfabeto_fita = {"0", "1", "_"}
    simbolo_vazio = "_"
    estado_inicial = "q0"
    estados_finais = {"qa"}

    transicoes = {
        "q0": {
            "0": ["q0", "0", "R"],
            "1": ["q0", "1", "R"],
            "_": ["q1", "_", "L"]
        },
        "q1": {
            "0": ["qa", "1", "S"],
            "1": ["q1", "0", "L"],
            "_": ["q2", "_", "R"]
        },
        "q2": {
            "_": ["qa", "1", "S"],
            "0": ["qa", "1", "S"]
        }
    }

    return MaquinaDeTuring(estados, alfabeto_entrada, alfabeto_fita, simbolo_vazio, transicoes, estado_inicial, estados_finais)

# Função para criar a máquina de Turing de verificação de palíndromo


def maquina_verificacao_palindromo():
    estados = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q_aceita', 'q_rejeita'}
    alfabeto_entrada = {'0', '1'}
    alfabeto_fita = {'0', '1', 'X', '_'}
    simbolo_vazio = '_'
    estado_inicial = 'q0'
    estados_finais = {'q_aceita'}

    transicoes = {
        'q0': {
            '0': ('q1', 'X', 'R'),
            '1': ('q2', 'X', 'R'),
            '_': ('q_aceita', '_', 'N'),  # Se vazio, é palíndromo
            # Se apenas marcadores, também é palíndromo
            'X': ('q_aceita', 'X', 'N'),
        },
        'q1': {  # Encontrou '0', busca o '0' correspondente no final
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            'X': ('q1', 'X', 'R'),
            '_': ('q3', '_', 'L')  # Ao encontrar vazio, volta para verificar
        },
        'q2': {  # Encontrou '1', busca o '1' correspondente no final
            '0': ('q2', '0', 'R'),
            '1': ('q2', '1', 'R'),
            'X': ('q2', 'X', 'R'),
            '_': ('q4', '_', 'L')  # Ao encontrar vazio, volta para verificar
        },
        'q3': {  # Comparando último '0' com o primeiro '0'
            '0': ('q5', 'X', 'L'),
            'X': ('q3', 'X', 'L'),
        },
        'q4': {  # Comparando último '1' com o primeiro '1'
            '1': ('q5', 'X', 'L'),
            'X': ('q4', 'X', 'L'),
        },
        'q5': {  # Retorna para o início da palavra para continuar
            '0': ('q5', '0', 'L'),
            '1': ('q5', '1', 'L'),
            'X': ('q5', 'X', 'L'),
            '_': ('q0', '_', 'R'),  # Volta ao início da palavra
        },
    }

    return MaquinaDeTuring(estados, alfabeto_entrada, alfabeto_fita, simbolo_vazio, transicoes, estado_inicial, estados_finais)

# Função principal para executar no Streamlit


def main():
    st.title("Simulador de Autômatos e Máquinas de Turing")

    opcao = st.sidebar.selectbox("Escolha o tipo de operação",
                                 ["AFD", "AFND", "Máquina de Turing: Incremento Binário", "Máquina de Turing: Verificação de Palíndromo", "Demonstrar Equivalência AFND e AFD"])

    if opcao == "AFD":
        st.header("Autômato Finito Determinístico (AFD)")
        estados = st.text_input("Estados (separados por espaço):").split()
        alfabeto = st.text_input("Alfabeto (separado por espaço):").split()
        estado_inicial = st.text_input("Estado inicial:")
        estados_finais = st.text_input(
            "Estados finais (separados por espaço):").split()

        transicoes = coletar_transicoes_afd(estados, alfabeto)

        if st.button("Mostrar AFD"):
            if transicoes:
                dot = gerar_imagem_afd(
                    estados, alfabeto, transicoes, estado_inicial, estados_finais)
                st.graphviz_chart(dot.source)
            else:
                st.write("Por favor, defina as transições do AFD.")

        if st.button("Minimizar AFD"):
            if transicoes:
                estados_agrupados, alfabeto, novas_transicoes, novo_estado_inicial, novos_estados_finais = minimizar_afd(
                    estados, alfabeto, transicoes, estado_inicial, estados_finais)
                st.write("Estados agrupados:", estados_agrupados)
                st.write("Novas transições:", novas_transicoes)
                st.write("Novo estado inicial:", novo_estado_inicial)
                st.write("Novos estados finais:", novos_estados_finais)

                # Renderiza o grafo minimizado
                dot = gerar_imagem_afd(
                    estados_agrupados, alfabeto, novas_transicoes, novo_estado_inicial, novos_estados_finais)
                st.graphviz_chart(dot.source)
            else:
                st.write(
                    "Por favor, defina as transições do AFD antes de minimizar.")

        palavra_teste = st.text_input("Digite uma palavra para testar no AFD:")
        if st.button("Testar palavra no AFD"):
            if transicoes and palavra_teste:
                aceita = simular_afd_com_palavra(
                    estados, alfabeto, transicoes, estado_inicial, estados_finais, palavra_teste)
                if aceita:
                    st.write(f"A palavra '{palavra_teste}' foi **aceita** pelo AFD.")
                else:
                    st.write(f"A palavra '{palavra_teste}' foi **rejeitada** pelo AFD.")
            else:
                st.write(
                    "Por favor, defina as transições do AFD e insira uma palavra para testar.")

    elif opcao == "AFND":
        st.header("Autômato Finito Não Determinístico (AFND)")
        estados = st.text_input("Estados (separados por espaço):").split()
        alfabeto = st.text_input("Alfabeto (separado por espaço):").split()
        estado_inicial = st.text_input("Estado inicial:")
        estados_aceitacao = st.text_input(
            "Estados de aceitação (separados por espaço):").split()

        funcoes_transicao = coletar_transicoes_afnd(estados, alfabeto)

        if st.button("Mostrar AFND"):
            if funcoes_transicao:
                dot = gerar_imagem_afnd(
                    estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao)
                st.graphviz_chart(dot.source)
            else:
                st.write("Por favor, defina as transições do AFND.")

        if st.button("Converter AFND para AFD"):
            if funcoes_transicao:
                estados_afd, alfabeto_afd, funcoes_transicao_afd, estado_inicial_afd, estados_aceitacao_afd = converter_afnd_para_afd(
                    estados, alfabeto, funcoes_transicao, estado_inicial, estados_aceitacao)

                st.write("Estados do AFD:", estados_afd)
                st.write("Transições do AFD:", funcoes_transicao_afd)
                st.write("Estado inicial do AFD:", estado_inicial_afd)
                st.write("Estados de aceitação do AFD:", estados_aceitacao_afd)

                # Renderiza o grafo do AFD convertido
                dot = gerar_imagem_afd(
                    estados_afd, alfabeto_afd, funcoes_transicao_afd, estado_inicial_afd, estados_aceitacao_afd)
                st.graphviz_chart(dot.source)
            else:
                st.write(
                    "Por favor, defina as transições do AFND antes de converter.")

        palavra_teste_afnd = st.text_input(
            "Digite uma palavra para testar no AFND:")
        if st.button("Testar palavra no AFND"):
            if funcoes_transicao and palavra_teste_afnd:
                aceita = simular_afnd(estados, alfabeto, funcoes_transicao,
                                      estado_inicial, estados_aceitacao, palavra_teste_afnd)
                if aceita:
                    st.write(f"A palavra '{palavra_teste}' foi **aceita** pelo AFND.")
                else:
                    st.write(f"A palavra '{palavra_teste}' foi **rejeitada** pelo AFND.")
            else:
                st.write(
                    "Por favor, defina as transições do AFND e insira uma palavra para testar.")

    elif opcao == "Máquina de Turing: Incremento Binário":
        st.header("Máquina de Turing: Incremento de Número Binário")
        palavra = st.text_input("Digite o número binário para incremento:")
        if st.button("Executar"):
            mt_incremento = maquina_incremento_binario()
            mt_incremento.carregar_palavra(palavra)
            resultado = mt_incremento.executar()
            if resultado:
                st.write(f"Resultado do incremento: {mt_incremento.obter_resultado()}")
            else:
                st.write(
                    f"Erro ao executar a Máquina de Turing para a palavra '{palavra}'.")

    elif opcao == "Máquina de Turing: Verificação de Palíndromo":
        st.header("Máquina de Turing: Verificação de Palíndromo")
        palavra = st.text_input(
            "Digite a palavra para verificação de palíndromo:")
        if st.button("Executar"):
            mt_palindromo = maquina_verificacao_palindromo()
            mt_palindromo.carregar_palavra(palavra)
            resultado = mt_palindromo.executar()
            if resultado:
                st.write(f"A palavra '{palavra}' é um palíndromo: Sim")
            else:
                st.write(f"A palavra '{palavra}' é um palíndromo: Não")

    elif opcao == "Demonstrar Equivalência AFND e AFD":
        st.header("Demonstrar Equivalência entre AFND e AFD com Palavras de Teste")

        # Obtenha os parâmetros do AFND do usuário
        estados_afnd = st.text_input(
            "Estados do AFND (separados por espaço):").split()
        alfabeto = st.text_input("Alfabeto (separado por espaço):").split()
        estado_inicial_afnd = st.text_input("Estado inicial do AFND:")
        estados_aceitacao_afnd = st.text_input(
            "Estados de aceitação do AFND (separados por espaço):").split()

        funcoes_transicao_afnd = coletar_transicoes_afnd(
            estados_afnd, alfabeto)

        # Obtenha os parâmetros do AFD do usuário
        estados_afd = st.text_input(
            "Estados do AFD (separados por espaço):").split()
        estado_inicial_afd = st.text_input("Estado inicial do AFD:")
        estados_aceitacao_afd = st.text_input(
            "Estados de aceitação do AFD (separados por espaço):").split()

        transicoes_afd = coletar_transicoes_afd(estados_afd, alfabeto)

        if st.button("Demonstrar Equivalência"):
            if funcoes_transicao_afnd and transicoes_afd:
                equivalente = demonstrar_equivalencia_afnd_afd(
                    estados_afnd, alfabeto, funcoes_transicao_afnd, estado_inicial_afnd, estados_aceitacao_afnd,
                    estados_afd, transicoes_afd, estado_inicial_afd, estados_aceitacao_afd
                )

                if equivalente:
                    st.write(
                        "O AFND e o AFD convertido são equivalentes para todas as palavras geradas.")
                else:
                    st.write(
                        "O AFND e o AFD convertido **não** são equivalentes.")
            else:
                st.write("Por favor, defina as transições de ambos os autômatos.")


if __name__ == "__main__":
    main()
