import json
import sqlite3

from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from Componentes import BotaoArredondado, BotaoRetangular
from kivy_garden.graph import Graph, LinePlot

class TelaEvo(Screen):
    def on_enter(self):
        self.app = App.get_running_app()
        self.dados = []
        dropdown = DropDown()
        with open(self.app.exercicios_json_path, "r", encoding="utf-8") as exercicios_txt:
            exercicios=json.load(exercicios_txt)
            exercicios[list(exercicios.keys())[0]].sort()

            for exercicio in exercicios[list(exercicios.keys())[0]]:
                botao= BotaoRetangular(text=exercicio, size_hint_y=None, height=dp(44))
                dropdown.add_widget(botao)
                botao.bind(on_release=lambda instance: dropdown.select(instance.text))
                botao.bind(on_release=self.pegardados)

        self.botaopai= BotaoRetangular(text='',
                                   size_hint=(.45, .08),
                                   pos_hint={'center_x': 0.35, 'center_y': 0.85}
                                   )
        self.ids.layoutevo.add_widget(self.botaopai)
        self.botaopai.bind(on_release= dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.botaopai, 'text', x))

        self.botaodografico= BotaoArredondado(text='GERAR GRÁFICO',
                                         size_hint=(.4, .08),
                                         pos_hint={'center_x': 0.80, 'center_y': 0.85}
                                         )
        self.botaodografico.bind(on_release=self.gerargrafico)
        self.ids.layoutevo.add_widget(self.botaodografico)



    def pegardados(self, botao):
        exercicio = botao.text
        with sqlite3.connect(self.app.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT carga_Kg, data FROM cargas 
                              WHERE exercicio= ? ORDER BY data ASC''', ( exercicio,))
            self.dados=cursor.fetchall()
            

    def gerargrafico(self, *args):
        if not self.dados:
            self.ids.conteiner_grafico.clear_widgets()
            self.ids.conteiner_grafico.add_widget(Label(
                text='Selecione um exercício antes de gerar o gráfico.',
                font_size=sp(14)
                )
            )
            return

        cargas=[tupla[0] for tupla in self.dados]
        pontos_do_grafico = [(i, carga) for i, (carga, data) in enumerate(self.dados)]

        self.ids.conteiner_grafico.clear_widgets()

        if cargas:
            grafico = Graph(
                xlabel='Data',
                ylabel='Carga',
                x_ticks_minor=1,
                y_ticks_minor=min(cargas),
                xmin=0, xmax=len(self.dados) + 1,
                ymin=0, ymax=max(cargas) + 1,
                x_grid_label=True,
                y_grid_label=True,
                y_grid=True
            )
            plot = LinePlot(
                color=[0, 0, 1, 1],
                )
            plot.points = pontos_do_grafico 
            grafico.add_plot(plot)
            
            self.ids.conteiner_grafico.add_widget(grafico)
            
        else:
            self.ids.conteiner_grafico.add_widget(Label(
                text='ERRO: Ainda não existem dados desse exercício armazenados',
                font_size=sp(14)
                )
            )

    def on_leave(self, *args):
        self.ids.layoutevo.remove_widget(self.botaopai)
        self.ids.layoutevo.remove_widget(self.botaodografico)
        self.ids.conteiner_grafico.clear_widgets()
