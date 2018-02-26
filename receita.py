#!/usr/bin/python
# -*- coding: utf-8 -*-
class Receita:
    
    def __init__(self, nome, descricao, restricoes, dificuldade, tempoPreparacao, dose, ingredientes, preparacao):
        self.nome = nome
        self.descricao = descricao
        self.restricoes = restricoes
        self.dificuldade = dificuldade
        self.tempoPreparacao = tempoPreparacao
        self.dose = dose
        self.ingredientes = []
        for ing in ingredientes:
            self.ingredientes.append(ing)
        self.preparacao = preparacao
