# G.E.T — Gym Evo Tracker

A mobile workout tracker built with Python and Kivy, designed to run on Android.  
Log your exercise loads each day, review recent performance, and visualize progress over time through line charts.

---

## Features

- **Workout configuration** — Set up your weekly training split (Mon–Sun), up to 7 exercises per day
- **Load logging** — Record weights for each exercise on the current day; pre-fills last known load automatically
- **Performance analysis** — Generate line charts per exercise using historical data from the local database
- **Local storage** — All data is stored on-device: workout config in JSON, load history in SQLite

---

## Project Structure

```
get-app/
├── main.py                  # App entry point, MainApp class, DB logic
├── main.kv                  # Kivy layout definitions for all screens
├── Tela_Inicial.py          # Home screen
├── Tela_de_Anotacao.py      # Load logging screen
├── Tela_de_Evolucao.py      # Performance chart screen
├── Tela_de_Configuracao.py  # Workout setup screen
├── Componentes.py           # Reusable custom widgets
├── exercicios_base.json     # Base exercise list used in the chart screen
├── images/
│   └── icon.png             # App icon
└── buildozer.spec           # Android build configuration
```

---

## Requirements

### Python

- **Python 3.11.9**

### Python packages

```
kivy
kivy_garden.graph
```

Install with pip:

```bash
pip install kivy
pip install kivy_garden.graph
```

> `sqlite3` and `json` are part of the Python standard library — no separate installation needed.

### For Android builds (Buildozer)

- **Buildozer** (Linux/WSL recommended)
- **Android SDK** (auto-downloaded by Buildozer)
- **Android NDK** (auto-downloaded by Buildozer)
- Target API: **33** | Minimum API: **24**
- Architectures: `arm64-v8a`, `armeabi-v7a`
- python-for-android branch: `v2024.01.21`

Install Buildozer:

```bash
pip install buildozer
```

---

## Running Locally (Desktop)

Uncomment the `Window.size` line in `main.py` to simulate a phone screen:

```python
Window.size = (393, 873)
```

Then run:

```bash
python main.py
```

---

## Building for Android

From the project root (inside WSL/Linux):

```bash
buildozer android debug
```

The `.apk` will be output to the `bin/` directory.

---

## Notes

- `Tela_de_Configuracao.py` is imported in `main.py` but not included in this repo — add it to complete the build.
- The app creates its data files (`bancodedados.db`, `treino_cadastrado.json`) on first run inside the platform's user data directory.
- The performance analysis screen is still under development.
