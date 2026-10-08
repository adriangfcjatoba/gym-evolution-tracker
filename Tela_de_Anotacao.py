from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from Componentes import BotaoArredondado

class TelaAnotar(Screen):

    def on_enter(self):

        self.App=App.get_running_app()
        self.App.verificar_datas()
        
        self.aviso=Label()
        diccarga = {}

        treino_cadastrado=self.App.treino
        dia_da_semana=self.App.diadasemana
        datas_anteriores=self.App.datas

                
        # tecsa = TREINO E CARGA DA SEMANA ANTERIOR 
        tecsa = self.App.treino_e_cargas_semana_anterior
        print('TECSA: ',tecsa)
        print('D_A: ', datas_anteriores)

        def pre_salvamento(*args):
                    
                for exercicio in treino_cadastrado[dia_da_semana]:        
                    if exercicio != '' and diccarga[exercicio].text != '':
                        # CONVERTEMOS OS DADOS PARA FLOAT POIS PRECISAMOS DE VALORES
                        # NÚMERICOS E SALVAMOS NO self.cargas DO MAINAPP
                        self.App.cargas[exercicio] = float(diccarga[exercicio].text)
                    elif exercicio != '':
                        self.App.cargas[exercicio] = 0
                self.pop_up_confirmacao()

        
        if treino_cadastrado[dia_da_semana]:
            
            c=0
            for exercicio in sorted(treino_cadastrado[dia_da_semana]):
                if exercicio != "":
                    Colunaexercicios= Label(text=exercicio,
                                        font_size=sp(14),
                                        size_hint_y=None,
                                        height=dp(50)
                                        )
                    self.ids.boxtexto.add_widget(Colunaexercicios)

                    if len(self.App.treino_e_cargas_semana_anterior) > c:
                        print('Entrei no loop...' + '\nExercicio:',exercicio,'\nTecsa',self.App.treino_e_cargas_semana_anterior[c][0])

                        carga_ja_anotada = self.App.treino_e_cargas_semana_anterior[c][1]
                    
                    else: 
                        carga_ja_anotada = 0
                    
                    caixainput= TextInput(text=str(carga_ja_anotada),
                                        font_size=sp(14),
                                        size_hint_y=None,
                                        height=dp(50)
                                        )
                    self.ids.boxentrada.add_widget(caixainput)

                    # ADICIONA-SE TODO O LABEL COMO VALOR, POIS PRECISAMOS
                    # DA PROPRIEDADE DE ATUALIZAÇÃO EM TEMPO REAL QUE OS 
                    # WIDGETS POSSUEM. CASO PASSEMOS SOMENTE O TEXTO AGORA
                    # O VALOR DE diccarga[exercicio] SERÁ SEMPRE ''. 
                    diccarga[exercicio]=caixainput
                    c = c + 1
                    


            botao_salvar= BotaoArredondado(text='SALVAR',
                                           size_hint=(.3, .08),
                                           pos_hint={'center_x': 0.5, 'y': 0.02}
                                           )
            botao_salvar.bind(on_release= pre_salvamento)

            self.ids.layoutanotar.add_widget(botao_salvar)


        else:
            self.aviso= Label(text='HOJE É DIA DE DESCANSO, VOLTE AMANHÃ!\n (Atenção:'
                                  'caso não seja dia de descanso, por favor verifique'
                                  'o treino cadastrado nas configurações)',
                              font_size=sp(14),
                              size_hint=(.4,.2)
                             )
            self.ids.layoutanotar.add_widget(self.aviso)

    
    def pop_up_confirmacao(self, *args):

        layoutconfirmacaoscroll = ScrollView()
        layoutconfirmacaobox1 = BoxLayout(orientation='vertical',
                                         size_hint_y=None
                                         )


        layoutconfirmacaobox1.bind(minimum_height=layoutconfirmacaobox1.setter('height'))
        layoutconfirmacaoscroll.add_widget(layoutconfirmacaobox1)

        for exercicio, carga in self.App.cargas.items():
            label=Label(text=f'{exercicio}: {carga} Kg',
                        font_size=sp(14),
                        size_hint_y=None,
                        height=dp(44))
            layoutconfirmacaobox1.add_widget(label)

        pop_up= Popup(title='CONFIRMAÇÃO:',
                      content=layoutconfirmacaoscroll,
                      size_hint=(0.85, 0.55),
                      )
        botaosalvar = BotaoArredondado(text='SALVAR',
                                       size_hint_y=None,
                                       height=dp(50)
                                       )
        def fecharpopup(*args):

            print(self.App.cargas)
            self.App.guardarcargas() if len(self.App.datas) == 0 else self.App.alterarcargas()
            self.App.root.current = 'tela_inicial'
            pop_up.dismiss()

        botaosalvar.bind(on_release=fecharpopup)
        layoutconfirmacaobox1.add_widget(botaosalvar)

        pop_up.open()

        


    def on_leave(self):
        self.ids.layoutanotar.remove_widget(self.aviso)
        self.ids.boxtexto.clear_widgets()
        self.ids.boxentrada.clear_widgets()

        self.App.verificar_datas()
