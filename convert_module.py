import os
import base_module


class NFAtoDFAConverter:
    def __init__(self):
        self.pasta_nfa = "NFAs/"
        self.estado_inicial = ""
        self.estados_finais = []
        self.alfabeto = []
        self.estados_dfa = {self.estado_inicial}
        self.transicoes_dfa = {}
        self.transicoes_nfa = {}

    def converter_nfa_para_dfa(self):
        print("Converter NFA -> DFA")

        self.transicoes_nfa = base_module.GerenciadorArquivos.converter_txt_para_dict(
            self.pasta_nfa)
        self.transicoes_nfa = base_module.GerenciadorArquivos.converter_dict_para_lista(
            self.transicoes_nfa)

        self.estado_inicial, self.estados_finais, self.alfabeto = base_module.GerenciadorArquivos.obter_estados_iniciais_finais_e_alfabeto(
            self.pasta_nfa
        )

        print(self.transicoes_nfa)

        chaves_nfa = {estado[0] for estado in self.transicoes_nfa}
        chaves_nfa = list(chaves_nfa)
        print(chaves_nfa)

        estados = chaves_nfa + [''.join(chaves_nfa), ' ']
        print(estados)


if __name__ == "__main__":
    conversor = NFAtoDFAConverter()
    conversor.converter_nfa_para_dfa()
