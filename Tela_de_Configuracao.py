import json

from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.graphics import Rectangle
from kivy.core.text import LabelBase
from Componentes import BotaoRetangular, LabelPersonalizadoCinzaDraculaReto

LabelBase.register(
    name='NotoSansSymbols2',
    fn_regular='fonts/NotoSansSymbols2-Regular.ttf'
)

class TelaConfig(Screen):
    def on_enter(self):

        self.App = App.get_running_app() 
        self.App.lertreino()
        #Guarda o treino cadastrado na memória em execução no atributo "treino" da classe App
        self.exibir_treino()

    def exibir_treino(self):

        with open(self.App.exercicios_json_path, 'r', encoding="utf-8") as exercicios_base:
            exerciciosbase = json.load(exercicios_base)
            chaveexercicios = list(exerciciosbase.keys())
            exerciciosbase[chaveexercicios[0]].sort()
        
        dias_da_semana = list(self.App.treino.keys())

        # CRIAÇÃO DO DROPDOWN ###################################################################
        dropdown = DropDown()

        apagaropcao = BotaoRetangular(text='', height=dp(44), size_hint_y=None)
        apagaropcao.bind(on_release=lambda instance: dropdown.select(instance.text))
        dropdown.add_widget(apagaropcao)

        for exercicio in exerciciosbase[chaveexercicios[0]]:
            opcoesdisponiveis = BotaoRetangular(text=f'{exercicio}', height=dp(44), size_hint_y=None)
            # 'bind' ANEXA A CADA BOTÃO O EVENTO SELECT DO DROPDOWN E PASSA O TEXTO DO BOTÃO
            # COMO ARGUMENTO.
            opcoesdisponiveis.bind(on_release=lambda instance: dropdown.select(instance.text))
            dropdown.add_widget(opcoesdisponiveis)
        #########################################################################################
        
        #CRIAÇÃO DE COLUNAS
        for dia in dias_da_semana:
            label = LabelPersonalizadoCinzaDraculaReto(text=dia + '[sub][size=21][font=NotoSansSymbols2]⮧[/font][/size][/sub]', font_size=sp(26), markup=True)
            #SINTAXE DO PRÓPRIO KIVY PARA ADIÇÃO DINÂMICA DE WIDGETS, ANÁLOGO A exec('comando')
            self.ids[dia].add_widget(label)
            #CRIAÇÃO DE LINHAS
            for x in range(0, 7):
                try:
                    textobotao = f'{self.App.treino[dia][x]}'
                except IndexError:
                    textobotao = ''

                botaopai = BotaoRetangular(text=f'{textobotao}')
                botaopai.id=f"{dia}"+f"{x}"
                self.ids[dia].add_widget(botaopai)
                #ADICIONA-SE CADA BOTÃO A UM DICIONÁRIO PARA REFERENCIARMOS CADA UM 
                #POSTERIORMENTE.
                self.App.identificadores[botaopai.id]=botaopai

                botaopai.bind(on_release=lambda btn: self.abrir_dropdown_para_botao(btn, dropdown))

    
    def abrir_dropdown_para_botao(self, botao, objeto_dropdown):
        #1. LIMPA QUALQUER BIND ANTERIOR DO DROPDOWN PARA NÃO ACUMULAR.
        #*NOTA CASO NÃO LIMPEMOS, AO SELECIONAR UM SEGUNDO BOTÃO, O ANTERIOR 
        #TAMBÉM TERÁ SEU TEXTO ALTERADO.
        objeto_dropdown.unbind(
            on_select=objeto_dropdown.callback_atual if hasattr(objeto_dropdown, 'callback_atual') else lambda *x: None)

        # 2. FUNÇÃO QUE ATUALIZA O BOTÃO ESPECÍFICO QUE FOI CLICADO
        #*NOTA: O PRIMEIRO PARÂMETRO É SEMPRE O OBJETO QUE CHAMOU O EVENTO, NO CASO,
        #O DROPDOWN. 
        def atualizar_texto(instance_dropdown, texto_selecionado):
            botao.text = texto_selecionado
            
            #CHAMA A FUNÇÃO receberinput DO APP E USA O botaopai QUE TEVE O TEXTO
            #ALTERADO COMO PARÂMETRO.
            self.App.receberinput(botao)
        # 3. SALVA A REFERÊNCIA PARA PODERMOS LIMPAR NO PRÓXIMO CLIQUE 
        objeto_dropdown.callback_atual = atualizar_texto

        # 4. ASSOCIA O EVENTO E ABRE O DROPDOWN NO LOCAL DO BOTÃO 
        objeto_dropdown.bind(on_select=atualizar_texto)
        objeto_dropdown.open(botao)
     
    def on_leave(self, *args):
        for dia in self.App.treino.keys():
            self.ids[dia].clear_widgets()

        return super().on_leave(*args)

    pass
