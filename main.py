# Estrutura dos dados -- Colunas: id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                   exercicio TEXT NOT NULL,
#                                 carga FLOAT,
#                                 data TEXT NOT NULL.
# No código abaixo foi criado o atributo id para alguns widgets para que
# fosse possível identifica-los quando criados de forma dinâmica.

from datetime import datetime
import sqlite3
import json
import os
from json import JSONDecodeError

# BIBLIOTECAS KIVY (BASE) ###############################################
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown                              
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy_garden.graph import Graph, LinePlot
from kivy.core.window import Window 
from kivy.clock import Clock

# TELAS #############################################################
from Tela_Inicial import TelaInicial
from Tela_de_Configuracao import TelaConfig
from Tela_de_Anotacao import TelaAnotar
from Tela_de_Evolucao import TelaEvo

#####################################################################

#import sys
#if sys.platform != 'android':
    #Window.size = (393, 873)




class MainApp (App):
    def build(self):
        self.treino = {dia : ['' for x in range(0,7)] for dia in ['SEG','TER','QUA','QUI','SEX','SAB','DOM']}
        self.cargas = {}
        self.dataatual = datetime.now().strftime("%Y-%m-%d")
        #GUARDA O DIA ATUAL DA SEMANA NO ATRIBUTO diadasemana
        self.diadasemana = list(self.treino.keys())[datetime.now().weekday()]
        self.identificadores = {}

        # CAMINHOS DE ARQUIVO ABSOLUTOS — NECESSÁRIO PARA FUNCIONAR NO ANDROID
        self.data_dir = self.user_data_dir
        self.db_path = os.path.join(self.data_dir, 'bancodedados.db')
        self.treino_json_path = os.path.join(self.data_dir, 'treino_cadastrado.json')
        print(self.db_path)

        # COPIA exercicios_base.json DO BUNDLE PARA A PASTA DE DADOS NA PRIMEIRA EXECUÇÃO
        self.exercicios_json_path = os.path.join(os.path.dirname(__file__), 'exercicios_base.json')

        self.lertreino()
        
        return Gerenciador()
    
    def verificar_datas(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                                        ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                          exercicio TEXT NOT NULL,
                                          carga_Kg FLOAT, 
                                          data TEXT NOT NULL)''')
            
            #VERIFICA DE JÁ EXISTA ALGUM DADO COM A DATA ATUAL.
            
            placeholders = ','.join(['?']*len(self.treino[self.diadasemana]))
            
            cursor.execute(f'''SELECT data FROM cargas WHERE data = ? AND exercicio IN ({placeholders})''',
                                [self.dataatual] + self.treino[self.diadasemana])

            self.datas=cursor.fetchall()

            #QUERY PARA RECUPERAR ÚLTIMA CARGA UTILIZADA DE CADA EXERCÍCIO DENTRO DO TREINO CADASTRADO
            # CRIA LISTA SEM POSSÍVEIS ESPAÇOS VAZIOS NA LISTA DE TREINO.
            lista_sem_espacos=[exercicio for exercicio in self.treino[self.diadasemana] if exercicio != '']
            # CRIA STRING PARA TUPLA DENTRO DA QUERY
            lista_de_exercicios_em_string=','.join(['?']*len(lista_sem_espacos))

            cursor.execute(f'''SELECT exercicio, carga_kg FROM cargas WHERE id IN
                                        (SELECT MAX(id) FROM cargas WHERE exercicio IN ({lista_de_exercicios_em_string})
                                        GROUP BY exercicio)''', lista_sem_espacos)
            dados_recentes = self.treino_e_cargas_semana_anterior = cursor.fetchall()
            # RESULTADO OBTIDO NA FORMA [(Linha1),(Linha2),(Linha3),...,(LinhaN)]
            # ORGANIZA AS TUPLAS POR ORDEM ALFABÉTICA DO EXERCÍCIO
            dados_recentes.sort()

            print(dados_recentes)
            print(self.cargas)


    #FORMATO DO ID DE CADA BOÃO: {<dia/coluna>} + {<numero/linha>}
    #EX: 'SEG2' - Coluna da segunda-feira, terceira linha.
    #É USADO ESPECIFICAMENTE PARA A TELA TelaConfig.
    #        ,--> RECEBE ENTRADAS NA TELA DE CONFIGURAÇÃO E SALVA EM self.treino ( Salva do que ficou escrito para o dicionário na ram )
    def receberinput(self, botao):
        texto_do_botao = botao.text
        dia = botao.id[:3]
        posicao = int(botao.id[3])
        
        self.treino[dia][posicao]= texto_do_botao

    def guardartreino(self,*args):
        #ESCREVE O TREINO CADASTRADO DA MEMÓRIA PARA UM ARQUIVO JSON
        with open(self.treino_json_path, "w", encoding="utf-8") as treino:
            json.dump(self.treino, treino, indent=4, ensure_ascii=False)

    def lertreino(self):
        try:
            with open(self.treino_json_path, "r", encoding="utf-8") as treino:
                self.treino = json.load(treino)

        except (FileNotFoundError, JSONDecodeError):
            with open(self.treino_json_path, "w", encoding="utf-8") as treino:
                json.dump(self.treino, treino, indent=4, ensure_ascii=False)

    def limpartreino(self):
        self.treino = {dia : ['' for x in range(0,7)] for dia in ['SEG','TER','QUA','QUI','SEX','SAB','DOM']}
        for botao in self.identificadores.values():
            botao.text=''

    def guardarcargas(self, *args):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              exercicio TEXT NOT NULL,
                              carga_Kg FLOAT, 
                              data TEXT NOT NULL)'''
            )

            for exercicio, carga in self.cargas.items():

                cursor.execute('''INSERT INTO cargas (exercicio, carga_Kg, data) 
                                          VALUES (?, ?, ?)''',
                               (exercicio, carga, self.dataatual))


    def alterarcargas(self, *args):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 exercicio TEXT NOT NULL,
                                 carga_Kg FLOAT,
                                 data TEXT NOT NULL)'''
            )

            print('Iniciando alteração no banco de dados... \n')
            print('Dados que serão atribuidos:')
            print(self.cargas)

            dados_para_alteracao = [(carga, exercicio, self.dataatual) for exercicio, carga in self.cargas.items()]

            print('Dados que serão atribuídos organizados:')
            print(dados_para_alteracao)

            cursor.executemany('''UPDATE cargas
                                SET carga_Kg = ?
                                WHERE exercicio = ? AND data = ?''',
                                dados_para_alteracao)

            print('Alteração finalizada!')



class Gerenciador(ScreenManager):
    pass




if __name__ == '__main__':
    app = MainApp()
    app.run()
