#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json
from ingrediente import Ingrediente
from receita import Receita
from pymongo import MongoClient

client = MongoClient('connection url')
db = client.receitas

f = open('urls.dat', 'r')

receitas = []

def parseResponse(htmlResponse):
    soup = BeautifulSoup(htmlResponse.content, 'html.parser')
    
    title = soup.find('h1', {'class': 'main-slide-title'}).text
    description = soup.find('div', {'class': 'description'}).text
    restricoesStr = soup.find('div', {'class': 'recipe-types'}).text
    dificuldade = ""
    try:
        dificuldade = soup.find('label', {'class':'dificulty'}).text
    except:
        pass
    tempoPreparacao = soup.find('label', {'class':'preptime'}).text
    dose = soup.find('label', {'class':'nr_persons'}).text

    ingredientes = []
    ingredientsHTML = soup.findAll('li', {'class':'ingredient-wrapper'})
    for ingredientHTML in ingredientsHTML:
        soup_ing = BeautifulSoup(str(ingredientHTML), 'html.parser')
        quantidade = soup_ing.find('span', {'class':'ingredient-quantity'}).text
        unidade = soup_ing.find('span', {'class':'ingredient-unit'}).text
        desc = soup_ing.find('span', {'class':'ingredient-product'}).text
        desc = desc.replace("\t", "")
        desc = desc.replace("\n", "")
        desc = desc.replace("\r", "")
        ingrediente = Ingrediente(quantidade, unidade, desc)
        ingrediente = {
            'quantidade':quantidade,
            'unidade':unidade,
            'desc':desc
        }
        ingredientes.append(ingrediente)
    
    instrucoes = []
    instrucoesHTML = soup.findAll('span', {'class':'instruction-body'})
    for instrucaoHTML in instrucoesHTML:
        instrucoes.append(instrucaoHTML.text)
    
    restricoesStr = restricoesStr.replace(" |", ",")
    restricoesStr = restricoesStr.replace(" | ", ",")
    restricoesStr = restricoesStr.strip()
    
    restricoes = []
    for restricao in restricoesStr.split(","):
        restricoes.append(restricao.strip())
    
    receita = Receita(title, description, restricoes, dificuldade, tempoPreparacao, dose, ingredientes, instrucoes)
    db.pingo_doce.insert_one(receita.__dict__)

def main():
    currCount = 0
    errCount = 0
    for url in f.readlines():
        htmlResponse = requests.get(url)
        try:
            parseResponse(htmlResponse)
            currCount+=1
        except:
            print("oh shit")
    
if __name__ == '__main__':
    main()


