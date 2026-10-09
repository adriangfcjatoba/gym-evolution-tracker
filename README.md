# G.E.T — Gym Evo Tracker

Um aplicativo mobile de acompanhamento de treinos feito com Python e Kivy, projetado para rodar no Android.  
Registre as cargas dos exercícios a cada dia, veja o desempenho recente e visualize a evolução ao longo do tempo por meio de gráficos de linha.

---

## Funcionalidades

- **Configuração de treino** — Monte sua divisão semanal (Seg–Dom), com até 7 exercícios por dia
- **Registro de cargas** — Anote os pesos de cada exercício no dia atual; a última carga conhecida é preenchida automaticamente
- **Análise de desempenho** — Gere gráficos de linha por exercício com base no histórico armazenado localmente
- **Armazenamento local** — Todos os dados ficam no dispositivo: configuração de treino em JSON e histórico de cargas em SQLite

---

## Estrutura do Projeto

```
get-app/
├── main.py                  # Ponto de entrada do app, classe MainApp, lógica do banco de dados
├── main.kv                  # Definições de layout Kivy para todas as telas
├── Tela_Inicial.py          # Tela inicial
├── Tela_de_Anotacao.py      # Tela de registro de cargas
├── Tela_de_Evolucao.py      # Tela de gráficos de desempenho
├── Tela_de_Configuracao.py  # Tela de configuração do treino
├── Componentes.py           # Widgets personalizados reutilizáveis
├── exercicios_base.json     # Lista base de exercícios usada na tela de análise
├── images/
│   └── icon.png             # Ícone do aplicativo
└── buildozer.spec           # Configuração de build para Android
```

---

## Requisitos

### Python

- **Python 3.11.9**

### Pacotes Python

```
kivy
kivy_garden.graph
```

Instale com pip:

```bash
pip install kivy
pip install kivy_garden.graph
```

> `sqlite3` e `json` fazem parte da biblioteca padrão do Python — não precisam ser instalados separadamente.

### Para builds Android (Buildozer)

- **Buildozer** (recomendado usar Linux ou WSL)
- **Android SDK** (baixado automaticamente pelo Buildozer)
- **Android NDK** (baixado automaticamente pelo Buildozer)
- API alvo: **33** | API mínima: **24**
- Arquiteturas: `arm64-v8a`, `armeabi-v7a`
- Branch do python-for-android: `v2024.01.21`

Instale o Buildozer:

```bash
pip install buildozer
```

---

## Executando Localmente (Desktop)

Descomente a linha `Window.size` no `main.py` para simular a tela de um celular:

```python
Window.size = (393, 873)
```

Em seguida, execute:

```bash
python main.py
```

---

## Gerando o APK para Android

A partir da raiz do projeto (dentro do WSL/Linux):

```bash
buildozer android debug
```

O arquivo `.apk` será gerado na pasta `bin/`.

---

## Observações

- `Tela_de_Configuracao.py` é importado no `main.py`, mas não está incluído neste repositório — adicione o arquivo antes de publicar para que o projeto funcione corretamente.
- Na primeira execução, o app cria os arquivos de dados (`bancodedados.db`, `treino_cadastrado.json`) no diretório de dados do usuário da plataforma.
- A tela de análise de desempenho ainda está em desenvolvimento.
