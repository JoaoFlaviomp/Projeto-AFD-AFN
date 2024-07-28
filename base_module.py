import os
import time
from graphviz import Digraph

class Automato:
    def __init__(self, estado_inicial, estados_finais, transicoes):
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.transicoes = transicoes
        self.estados = set()
        self.alfabeto = set()
        self._gerar_estados_e_alfabeto()

    def _gerar_estados_e_alfabeto(self):
        for (estado_de, simbolo, estado_para) in self.transicoes:
            self.estados.add(estado_de)
            self.estados.add(estado_para)
            self.alfabeto.add(simbolo)

    def desenhar_automato(self):
        automato = Digraph()
        automato.attr(rankdir='LR')
        automato.attr('node', shape='circle')

        automato.node('->', shape='none', width='0', height='0', label='')
        automato.edge('->', self.estado_inicial)

        for estado_final in self.estados_finais:
            automato.node(estado_final, shape='doublecircle',
                          fontsize='19', fontcolor='green')
        for estado_de, simbolo, estado_para in self.transicoes:
            automato.edge(estado_de, estado_para, label=simbolo)

        return automato

class GerenciadorArquivos:
    @staticmethod
    def armazenar_arquivo(pasta, transicoes):
        arquivo_transicoes = open(pasta + "transitions.txt", "w")
        for chave, valor in transicoes.items():
            estado, simbolo = chave
            linha = f"{estado} {simbolo} {' '.join(valor)}\n"
            arquivo_transicoes.write(linha)
        return arquivo_transicoes

    @staticmethod
    def armazenar_info(pasta, estado_inicial, estados_finais, alfabeto):
        arquivo_info = open(pasta + "info.txt", "w")
        arquivo_info.write(f"Estado inicial: {estado_inicial}\n")
        arquivo_info.write(f"Estados finais: {' '.join(estados_finais)}\n")
        arquivo_info.write(f"Alfabeto: {' '.join(alfabeto)}\n")
        return arquivo_info

    @staticmethod
    def converter_dict_para_lista(transicoes):
        lista_transicoes = [
            [estado, simbolo, *proximos_estados]
            for (estado, simbolo), proximos_estados in transicoes.items()
        ]
        return lista_transicoes

    @staticmethod
    def converter_txt_para_dict(pasta):
        arquivo_transicoes = open(pasta + "transitions.txt", "r")
        transicoes = {}
        for linha in arquivo_transicoes:
            partes = linha.strip().split()
            estado, simbolo = partes[0], partes[1]
            proximos_estados = partes[2:]
            transicoes[(estado, simbolo)] = proximos_estados
        return transicoes

    @staticmethod
    def obter_estados_iniciais_finais_e_alfabeto(pasta):
        with open(pasta + "info.txt", "r") as arquivo_info:
            estado_inicial = arquivo_info.readline().strip().split(": ")[1]
            estados_finais = arquivo_info.readline().strip().split(": ")[1].split()
            alfabeto = arquivo_info.readline().strip().split(": ")[1].split()
        return estado_inicial, estados_finais, alfabeto

    @staticmethod
    def converter_dict_para_lista(transicoes_dict):
        return [(estado_de, simbolo, estado_para)
                for (estado_de, simbolo), estados_para in transicoes_dict.items()
                for estado_para in estados_para]

class VerificadorExistencia:
    @staticmethod
    def verificar_existencia():
        time.sleep(1)
        if os.path.exists('DFAs'):
            print(
                "\nUma DFA foi encontrada. Você já pode usar as funções: testar, converter e minimizar.\n")
        if os.path.exists('NFAs'):
            print(
                "\nUma NFA foi encontrada. Você já pode usar as funções: testar, converter e minimizar.\n")
        else:
            print("\nNão encontrado (Vazio)... Crie uma DFA ou NFA\n")
