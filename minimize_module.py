from graphviz import Digraph

class DFA:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

class DFAOptimizer:
    def __init__(self, dfa):
        self.dfa = dfa

    def minimizar_dfa(self):
        print("Minimizando DFA")

        # Particionamento inicial: aceitação vs não aceitação
        particao = [self.dfa.estados_finais, self.dfa.estados - self.dfa.estados_finais]

        while True:
            nova_particao = []
            for grupo in particao:
                novos_grupos = {}
                for estado in grupo:
                    chave = tuple(self.dfa.transicoes.get((estado, simbolo), None) for simbolo in self.dfa.alfabeto)
                    if chave not in novos_grupos:
                        novos_grupos[chave] = set()
                    novos_grupos[chave].add(estado)

                nova_particao.extend(novos_grupos.values())
            if set(map(frozenset, nova_particao)) == set(map(frozenset, particao)):
                break
            particao = nova_particao

        return particao

    def print_minimized_dfa(self, particao):
        print("DFA Minimizado:")
        for grupo in particao:
            print(grupo)

        # Gerar o gráfico do DFA minimizado
        automato = Digraph()
        automato.attr(rankdir='LR')  # LR significa da esquerda para a direita
        automato.attr('node', shape='circle')

        estado_map = {}
        novo_estado_inicial = ''
        novos_estados_finais = []

        # Criar um mapeamento de estados
        for i, grupo in enumerate(particao):
            novo_estado = f'q{i}'
            for estado in grupo:
                estado_map[estado] = novo_estado
                if estado == self.dfa.estado_inicial:
                    novo_estado_inicial = novo_estado
                if estado in self.dfa.estados_finais:
                    novos_estados_finais.append(novo_estado)

        # Adicionar os nós e transições
        for grupo in particao:
            estado_repr = next(iter(grupo))
            if estado_repr in novos_estados_finais:
                automato.node(estado_map[estado_repr], shape='doublecircle', fontsize='19', fontcolor='green')
            else:
                automato.node(estado_map[estado_repr])

        for (estado, simbolo), destino in self.dfa.transicoes.items():
            novo_estado = estado_map.get(estado, estado)
            novo_destino = estado_map.get(destino, destino)
            automato.edge(novo_estado, novo_destino, label=simbolo)

        automato.render('AutomatoMinimizado', format='png', cleanup=True)

def minimiza_afd():
    # Suponha que você tenha um DFA definido aqui
    # Isso deve ser substituído com a lógica real de obtenção do DFA
    # Exemplo de dados do DFA:
    estados = {'q0', 'q1', 'q2'}
    alfabeto = {'0', '1'}
    transicoes = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q2',
        ('q1', '1'): 'q0',
        ('q2', '0'): 'q1',
        ('q2', '1'): 'q2'
    }
    estado_inicial = 'q0'
    estados_finais = {'q2'}

    dfa = DFA(estados, alfabeto, transicoes, estado_inicial, estados_finais)
    optimizer = DFAOptimizer(dfa)
    minimized_partition = optimizer.minimizar_dfa()
    optimizer.print_minimized_dfa(minimized_partition)
