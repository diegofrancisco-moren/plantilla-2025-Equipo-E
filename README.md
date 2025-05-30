# La Odisea

## Equipo
- Diego Francisco Moreno - Jefe de Proyecto | Programador
- Miguel Arcas Morcillo - Programador 
- Rubén Tostón Carrero - Diseño de Niveles | Diseño Gráfico
- Yulen García Sacedo - Diseño Gráfico | Programador
- David Martínez Sánchez - Diseño Gráfico | Creación Sprites
- Maxim Sazonov - Diesño de Niveles | Diseño Gráfico
- Mario Fernández - Programador | Diseño Gráfico

##Controles
###Controles en la GameView 
- Movimiento: WASD / Arrow Keys
- Recogida Objetos: Tecla E
- Inventario: Tecla I
- Linterna: Tecla L
- Gancho: Tecla Q
  Para poder usarse se deberá estar cerca de un enganche.
- Menu: Tecla Esc
- Inventario Rápido:
  Se podrá utilizar mientras se este en la GameView, con las teclas del 1 al 9.
  La mecánica del hacha para poder cortar el tronco de la aldea inicial, se hace al pulsar la casilla en la que este el objeto Axe, después de recogerlo.

**Controles Especiales**
- Menu Debugger: Tecla G
  Se abrirá un menu para poder aumentar la velocidad del personaje, y desactivar las colisiones.

### Controles Ventana Batalla:
- Ataque: Tecla A
- Ataque Mágico: Tecla M
- Usar un Item: Tecla I
- Huir: Tecla H
  Con la excepción de la Huida, donde huyes del combate, al pulsar el resto de teclas se abre un menu, en el que se puede navegar con las flechas arriba/abajo. Para   seleccionar un ataque o item, basta con pulsar la tecla Enter. Si se quiere volver atrás se pulsa la tecla Esc.
  
###Controles en la ventana de Inventario:
- Arrastrar y Soltar
  Unicamente se podrá realizar esta acción mediante el uso del ratón
- Ordén Alfabetico
  Se podrá pulsar el botón con el ratón, para ordenar alfabeticamente los objetos dentro del inventario

  **El orden en el que se dejen los objetos en el inventario se reflejara en el inventario del jugador, pudiendose ver en el inventario rápido de la ventana de juego**

### Inicio del juego
1. El juego se inicia desde el main dentro de la carpeta rpg, lo que lanzará la ventana de inicio.
2. Dentro de esta ventana habrá dos opciones claras, New Game, para comenzar una partida nueva o Load Game para cargar una partida
3a. Si se elige New Game se le llevará al jugador a la ventana de selección de personaje, para poder elegir que clase crear, para después lanzar la ventana de carga.
3b. Si se elige Load Game se le llevará al jugador a la ventana de partidas guardadas, donde habrá tres slots de partidas, pudiendo estar vacios o con una partida previa, en caso de tener una partida previa y querer cargarla se podrá hacer mediante un click del ratón. Lo que lanzará la ventana de carga. En caso de querer volver a atras se puede pulsar la tecla Esc.
4. Una vez lanzada la ventana de carga, se estará cargando el juego desde el princio (en el caso de New Game) o desde el punto donde estaba la partida guardada (en el caso de Load Game). Al terminar la carga se lanzará la ventana de Game_View para poder jugar.

### Guardado Juego
1. En caso de querer guardar el juego se deberá pulsar la tecla Esc estando en la GameView. Lo que lanzará la pantalla de pausa o menu del juego.
2. Pulsando la opción Save Game, se lanzará la ventana de partidas guardadas, teniendo que elegir uno de los 3 slots disponibles para guardar la partida. En caso de elegir un slot que tuviese una partida guardada, se destruirá la partida antigua y se guardará la partida nueva.

### Cerrar Juego
1. Para cerrar el juego, desde la GameView, se deberá pulsar la tecla Esc. Lo que lanzará la pantalla de pausa o menu del juego.
2. Dentro de esta ventana se deberá pulsar el botón Quit Game, terminando la ejecución del juego.

### Superación puzles
- Puzle bosque:
  Se tendrá que seguir una flor rosa que hay cerca de los accesos a las siguientes pantalla.
  Ruta desde el inicio: Izquierda-izquierda-arriba-derecha-arriba-abajo-derecha-abajo-izquierda-arriba
- Puzle hacha:
  El hacha se podrá encontrar en la siguiente casa:
![image](https://github.com/user-attachments/assets/1ce7fc00-8daa-4c88-b992-8cf50bec3f6d)

# Welcome to The Python Arcade Community RPG
![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-success)
![First Timer Friendly](https://img.shields.io/badge/First%20Timer-friendly-informational)
![License MIT](https://img.shields.io/badge/license-MIT-success)

![Screenshot](/screenshot.png)

This is an open-source RPG game.

* Everything is open-source, under the permissive MIT license.
* Libraries Used:
  * [Arcade](https://github.com/pythonarcade/arcade)
  * [Pyglet](https://github.com/pyglet/pyglet)
  * [pytiled_parser](https://github.com/pythonarcade/pytiled_parser)
* Maps are created with the [Tiled Map Editor](https://mapeditor.org)
* All code is written in Python

Graphics Assets From:

* [Pipoya Free RPG Tileset 32x32](https://pipoya.itch.io/pipoya-rpg-tileset-32x32)
* [Pipoya Free RPG Character Sprites 32x32](https://pipoya.itch.io/pipoya-free-rpg-character-sprites-32x32)
* [Kenney Input Prompts Pixel 16x16](https://kenney.nl/assets/input-prompts-pixel-16)

## Gameplay

The game is in extremely early stages. For discussion on future direction, see:
* [the github discussion board](https://github.com/pythonarcade/community-rpg/discussions).
* [the #community-ideas channel on Arcade's discord server](https://discord.com/channels/458662222697070613/704736572603629589)


## Development

This project targets Python 3.7 or greater.

To install the project and all development dependencies run the following command, this should ideally be done in a [virtual environment](https://docs.python.org/3/tutorial/venv.html):

```bash
pip install -e ".[dev]"
```

The game can then be ran with:

```bash
python -m rpg
```

## Contact The Maintainer

paul@cravenfamily.com
