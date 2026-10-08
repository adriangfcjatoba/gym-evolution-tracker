from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.metrics import sp, dp

#Personalizações geradas com IA ;)
class BotaoArredondado(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', sp(14))
        super().__init__(**kwargs)

        # 1. Configurações básicas de transparência
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''

        # 2. Desenho do fundo arredondado
        with self.canvas.before:
            Color(0.10, 0.10, 0.10, 1)  # A cor que você definiu
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15), ]  # Arredondamento dos cantos
            )

        # 3. Vínculo crucial: se o botão mudar de lugar ou tamanho, redesenha o fundo
        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class BotaoArredondadoComBorda(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', sp(14))
        super().__init__(**kwargs)

        # 1. Configurações básicas de transparência
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''

        # 2. Desenho do fundo e da borda sutil
        with self.canvas.before:
            # Cor de fundo (cinza escuro principal)
            Color(0.10, 0.10, 0.10, 1)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )
            
            # Cor da borda (sutilmente mais escura: 0.05)
            Color(0.05, 0.05, 0.05, 1)
            self.line = Line(
                rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15)),
                width=dp(1.2)  # Espessura sutil da borda
            )

        # 3. Vínculo para atualizar posição e tamanho do fundo e da borda
        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        # Atualiza a linha contornando o retângulo arredondado
        self.line.rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15))


class BotaoRetangular(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', sp(13))
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''

        with self.canvas.before:
            Color(0.10, 0.10, 0.10, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

            # Use um cinza um pouco mais claro (0.3) para testar se aparece,
            # depois você volta para o 0.05 se preferir.
            Color(0.08, 0.08, 0.08, 1)
            self.linha_borda = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.2)

        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        # CORREÇÃO: O nome deve ser EXATAMENTE o mesmo que você criou no __init__
        self.linha_borda.rectangle = (self.x, self.y, self.width, self.height)

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class LabelPersonalizadoCinzaDracula(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', sp(13))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(44))
        super().__init__(**kwargs)
        
        # Define a cor de fundo (valores em RGBA de 0.0 a 1.0)
        # Ajuste os valores caso deseje alterar a opacidade/tom exato
        with self.canvas.before:
            Color(0.14, 0.14, 0.18, 1)  # Seu RGBA em escala 0-1
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15), ]  # Arredondamento dos cantos
            )
        
        # Garante que o fundo acompanhe o redimensionamento e reposicionamento do widget
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp

class LabelPersonalizadoCinzaDraculaReto(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', sp(13))
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(44))
        super().__init__(**kwargs)
        
        # Define a cor de fundo e o retangulo reto
        with self.canvas.before:
            Color(0.14, 0.14, 0.18, 1)  # RGBA escala 0-1
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )
        
        # Atualiza a posição e tamanho do retangulo ao redimensionar
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size