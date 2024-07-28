import os
import base_module


class AutomatonCreator:
    def __init__(self, caracteres_especiais):
        self.caracteres_especiais = caracteres_especiais
        self.estados = []
        self.alfabeto = []
        self.transicoes = {}
        self.estado_inicial = ""
        self.estados_finais = []
        self.pasta_dfa = "DFAs/"
        self.pasta_nfa = "NFAs/"

    def criar_automato(self):
        while True:
            print("Menu de Opções")
            print("1. Criar um AFD")
            print("2. Criar um AFN")
            print("3. Testar linguagem no AFD ou AFN")
            print("4. Voltar para o Menu ")
            opcao = int(input("Digite a opção desejada: "))
            if opcao == 1:
                self.criar_dfa()
            elif opcao == 2:
                self.criar_nfa()
            elif opcao == 3:
                self.testar_linguagem()
            elif opcao == 4:
                print("Retornando ao menu principal.")
                break

    def criar_dfa(self):
        print("Criando um AFD")

        if not os.path.exists(self.pasta_dfa):
            os.mkdir(self.pasta_dfa)

        self.estados = self.obter_entrada("Digite o conjunto de estados: ")
        if not self.e_entrada_valida(self.estados):
            return

        self.alfabeto = self.obter_entrada("Digite o alfabeto do autômato: ")
        if not self.e_entrada_valida(self.alfabeto):
            return

        self.estado_inicial = input("Digite o estado inicial: ")
        if not self.e_entrada_valida([self.estado_inicial]):
            return

        self.estados_finais = self.obter_entrada(
            "Digite o(s) estado(s) final(is): ")
        if not self.e_entrada_valida(self.estados_finais):
            return

        self.definir_transicoes()

        arquivo_dfa = base_module.GerenciadorArquivos.armazenar_arquivo(
            self.pasta_dfa, self.transicoes)
        arquivo_dfa.close()

        arquivo_info_dfa = base_module.GerenciadorArquivos.armazenar_info(
            self.pasta_dfa, self.estado_inicial, self.estados_finais, self.alfabeto
        )
        arquivo_info_dfa.close()

        lista_transicoes = base_module.GerenciadorArquivos.converter_dict_para_lista(
            self.transicoes)

        automato_dfa = base_module.Automato(
            self.estado_inicial, self.estados_finais, lista_transicoes
        )
        automato_dfa.desenhar_automato().render(
            self.pasta_dfa + "dfa_automaton", format="png", cleanup=True
        )

    def criar_nfa(self):
        print("Criando um AFN")

        if not os.path.exists(self.pasta_nfa):
            os.mkdir(self.pasta_nfa)

        self.estados = self.obter_entrada("Digite o conjunto de estados: ")
        if not self.e_entrada_valida(self.estados):
            return

        self.alfabeto = self.obter_entrada("Digite o alfabeto do autômato: ")
        if not self.e_entrada_valida(self.alfabeto):
            return

        self.estado_inicial = input("Digite o estado inicial: ")
        if not self.e_entrada_valida([self.estado_inicial]):
            return

        self.estados_finais = self.obter_entrada(
            "Digite o(s) estado(s) final(is): ")
        if not self.e_entrada_valida(self.estados_finais):
            return

        self.definir_transicoes(e_nfa=True)

        arquivo_nfa = base_module.GerenciadorArquivos.armazenar_arquivo(
            self.pasta_nfa, self.transicoes)
        arquivo_nfa.close()

        arquivo_info_nfa = base_module.GerenciadorArquivos.armazenar_info(
            self.pasta_nfa, self.estado_inicial, self.estados_finais, self.alfabeto
        )
        arquivo_info_nfa.close()

        nova_lista_transicoes = base_module.GerenciadorArquivos.converter_dict_para_lista(
            self.transicoes
        )

        automato_nfa = base_module.Automato(
            self.estado_inicial, self.estados_finais, nova_lista_transicoes
        )
        automato_nfa.desenhar_automato().render(
            self.pasta_nfa + "nfa_automaton", format="png", cleanup=True
        )

    def testar_linguagem(self):
        print("Digite a linguagem a ser reconhecida: ")
        cadeia_entrada = input()
        print("Você quer testar essa linguagem com DFA ou NFA?")
        print("a - dfa")
        print("b - nfa")
        opcao = input("Digite a opção desejada: ")

        if opcao == "a":
            self.executar_teste(cadeia_entrada, self.pasta_dfa)
        elif opcao == "b":
            self.executar_teste(cadeia_entrada, self.pasta_nfa)

    def executar_teste(self, cadeia_entrada, pasta):
        estado_inicial, estados_finais, alfabeto = (
            base_module.GerenciadorArquivos.obter_estados_iniciais_finais_e_alfabeto(
                pasta
            )
        )
        transicoes = base_module.GerenciadorArquivos.converter_txt_para_dict(
            pasta)
        estados_atuais = [estado_inicial]

        for simbolo in cadeia_entrada:
            print(f"Estados atuais: {estados_atuais}")
            novos_estados = []

            for estado_atual in estados_atuais:
                proximos_estados = transicoes.get((estado_atual, simbolo), [])
                novos_estados.extend(proximos_estados)

            estados_atuais = novos_estados

            print(f"Entrada atual: {simbolo}")
            print(f"Próximos estados: {estados_atuais}")

        if any(estado in estados_finais for estado in estados_atuais):
            print("Reconhecido!")
        else:
            print("Não reconhecido!")

    def obter_entrada(self, prompt):
        print(prompt, end="")
        return input().split()

    def e_entrada_valida(self, lista_entrada):
        if (
            any(char in self.caracteres_especiais for char in lista_entrada)
            or not lista_entrada
        ):
            print("Vazio ou contém caracteres inválidos, retornando ao menu de opções.")
            return False
        return True

    def definir_transicoes(self, e_nfa=False):
        print("Defina as funções de transição (delta)")
        for estado in self.estados:
            for simbolo in self.alfabeto:
                print(f"\t {simbolo}")
                print(f"{estado}\t------>\t", end="")
                proximos_estados = input().split() if e_nfa else [input().strip()]
                self.transicoes[(estado, simbolo)] = proximos_estados

