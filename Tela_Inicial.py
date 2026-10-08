from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import sp
from Componentes import LabelPersonalizadoCinzaDracula
import asyncio

class TelaInicial(Screen):

    def on_enter(self):
        
        self.App = App.get_running_app()
        self.App.verificar_datas()
        Clock.schedule_once(self.inicializacao, 1.5)
        
        pass
        
    def inicializacao(self, *args):

        treino_atual = self.App.treino[self.App.diadasemana]
        #tecsa = Treino e carga da semana anterior ( Corresponde ao mesmo dia da semana, porém da semana anterior )
        tecsa = self.App.treino_e_cargas_semana_anterior
        self.lista_de_label=[]
        if len(tecsa) != 0:
            for tupla in tecsa:
                label=LabelPersonalizadoCinzaDracula(text=f"{tupla[0]} : {tupla[1]}",
                                                     font_size=sp(13),
                                                     size_hint_y=0.2)
                self.ids.layout_cargas_recentes.add_widget(label)
                self.lista_de_label.append(label)
        
    def on_leave(self):
        for label in self.lista_de_label:
            self.ids.layout_cargas_recentes.remove_widget(label)
                          
         
    pass
