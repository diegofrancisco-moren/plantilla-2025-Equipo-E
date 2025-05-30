# Documento de diseño

## La Odisea

### Introducción
La Odisea será un juego inspirado en los rpgs originales, como podría ser los Zeldas antiguos. Es un genero que nos gusta a todo el grupo, y el cual creemos que es facil de hacer, partiendo de la plantilla "The Python Arcade Community RPG".

### Objetivos
- Hacer que el jugador suba de nivel al personaje.
- Hacer que el jugador avance a través de diferentes niveles y derrote al jefe final.

### Historia
La historia seguirá el camino del heroe típico, pero más simple, ya que no somos guionistas y no tenemos el tiempo suficiente para hacer una historia muy desarrollada.
El jugador aparecerá en la aldea del inicio del juego, se dará cuenta que la aldea está destruida y mediante dialogos de npc's los cuales le irán guiando a través de los niveles, entenderá quien esta detrás de toda esa destrucción e ira aasumiendo su papel, el heroe que derrote al tirano que esta causando tanto dolor. 
Superando nivel trás nivel, irá enfrentando a las dificultades que encuentre, ya sean enemigos o obstaculos que encuentre en el camino, hasta llegar al castillo del tirano. Y tras una dura batalla lograra vencerlo y resturar la paz.

### Personajes
## Heroe
Es el personaje principal que podrá manejar el jugador, podrá elegir entre tres clases diferentes.
- **Caballero**: Una clase basada en la vida y el ataque, perfecto para aguantar con su escudo y lanzar ataques contundentes cuando el enemigo tenga una apertura. Un caballero retirado, los dias en los que marchaba impasible hacía la batalla para defender a su rey quedaron olvidados. Después de jugarse la vida muchas veces, y recibir condecoraciones muchas menos, se fue a vivir a un pueblo perdido en el bosque, buscando la tranquilidad que tanto se había ganado. Ahora el deber le vuelve a llamar.
- **Mago**: Una clase basada en el mana, un personaje perfecto para los que quieren lanzar poderosos hechizos, aunque deberás tener cuidado ya que todo la ventaja que tiene en el mana le falta en la vida. Podría decir que es un archimago de septimo círculo retirado, con una gran barba blanca, y que habla utilizando frases poéticas y proverbios. Pero no, este mago es uno normal, ni flojo ni fuerte, se graduo hace 4 años de la academia de magia. Harto del estres de las grandes urbes, se mudo a un pueblo perdido de la mano de Dios, para poder realizar sus investigaciones tranquilo, pero le sorprendio el desastre. Ahora deberá demostrar que el también puede ser un mago digno de las leyendas.
- **Ladrón/Pícaro**: Una clase basada en la velocidad y el ataque, un personaje para los jugadores que quieren ser siempre los primeros en atacar, pero que luego el golpe se lo lleve otro. No hay nada glorioso que se puede decir de este pillo, sin padres, criado en las calles de una gran ciudad. Llevado por la necesidad tuvo que aprender a ganarse la vida como pudó, aguantaba con las limosnas que le daban y algún robo pequeño, un poco de comida, alguna bolsa de monedas rajada. Con el paso de los años fue volviendose más habil en estas artes, y podríamos decir que ya vivia, en vez de sobrevivir, pero no era una buena vida. Decidio recien cumplida su veintena, que daría un golpe grande y se largaría de la ciudad, a algún pueblo que nadie le conociese, para empezar de cero. Al final se mudo al pueblo, pero en vez de oro tenía una orden de busca y captura sobre su cabeza, y ahora su pueblo estaba asolado, pero decidido a cambiar su vida, quiso dar un ultimo golpe, al hombre que le había hecho eso a su nuevo hogar, seguro que tenía una buena cantidad de oro guardado bajo el colchón.

## Antagonista
  El antagonista, será el jefe final, no aparecerá hasta el final del juego. El personaje sabrá de el a través de los dialogos que le darán los NPC's que encuentre a   lo largo de los niveles. Hasta el final del juego no será que veremos los verdaderos objetivos de este personaje, durante el juego el villano se nos presenta         simplemente como un ser malvado, sin ningún motivo para llevar a cabo esa destrucción más que el dominio del mundo y alimentar su propio ego.
  
  Una vez lleguemos al castillo trás el combate tendremos una conversación con el, donde nos contará que toda esta destrucción era necesaria para su objetivo.
  Este personaje es la antigua mano derecha de un rey ya muerto, siempre le fue leal, pero no por los valores del rey, sino por las ansias de poder y tierras de este   personaje. Lo que le llevaba a siempre estar de campañas, su por entonces mujer de la que estaba profundamente enamorado siempre le esperaba en casa. Le fue bien,    demasiado a ojos del rey, el cual llevado por el miedo y su sentimiento de inferioridad, invito a este personaje a una cena en el castillo, mientras que el           ejercito del rey arrasaba sus tierras y con ellas mataban a su amada. 
  
  Cegado por la ira comenzo una guerra contra el rey, las tropas se dividieron entre los dos bandos, comenzando una guerra civil, de la que fue victorioso              nuestro personaje, pero llevado por la tristeza de perder a su amada, comenzo a estudiar la Piedra de   la Resurreción, que se decía podía traer de vuelta a los      muertos, pero se necesitaba un sacrificio de miles de vidas para salvar una.
  
### Mecánicas
- **Combate turnos**
  El combate en el juego será por turnos, el jugador podrás seleccionar una de las cuatro acciones posibles:
  - Ataque Mágico: Gasta mana para llevarse a cabo.
  - Ataque Físico: No gasta nada para llevarse a cabo.
  - Usar un Item
  - Huir de la batalla
  Se aprovechara la pantalla de batalla, ya implementada en la plantilla. Se hará una remodelación de esa pantalla, para así utilizarla en el combate por turnos.

- **Sistema de niveles | Estadísticas**: 
  El personaje tendrá diferentes estadísticas:
  - Salud (Health): Indica la cantidad de vida que tiene el jugador. Si esta por debajo de cero, el personaje morira.
  - Ataque (Attack): Cantidad de ataque, mejorando esta estadística los ataques del personaje serán más potentes, dando igual si son mágicos o físicos.
  - Mana: Indica la cantidad de mana que tiene el personaje. Si esta por debajo de cero, el personaje no podrá lanzar hechizos.
  - Velocidad (Speed): Indica como de rápido es el personaje, si el personaje es más rapido que el enemigo atacará antes.
  - Defensa (Defense): Cantidad de daño que puede mitigar el personaje al ser atacado.
  Además el jugador podrá subir de nivel acumulando experiencia a través de los combates, mejorando así estas estadísticas, y aprendiendo habilidades nuevas en         ciertos niveles.

- **Acompañantes**
  Personaje jugable en la pantalla de lucha que ayudarán en el combate y tendrán estadísticas propias. En la pantalla de juego (GameView), seguirán al personaje.
  El juagador podrá encontrar a su acompañante pasada la mitad del juego. Al igual que el personaje principal podrá subir de nivel, el aspecto de este acompañante
  será una de las dos clases restantes que no se haya elegido al inicio del juego, es decir, si el jugador elige al caballero, su acompañante será el mago o el         pícaro.

- **Equipamiento**
  A lo largo del juego el jugador podrá recoger diferentes objetos, entre ellos piezas de equipamiento. Podrán ser:
  - Armas
  - Armaduras
  - Amuletos
  En base a los objetos equipados las estadísticas del personaje cambiarán, pudiendo afectar a cualquiera de ellas.

- **Selección de clase básica inicial**
  Como se dijo en el apartado de personajes, al comienzo del juego se podrá elegir entre tres clases diferentes, cada una de ellas tendrá un escalado diferente de      estadísticas al subir de nivel, y aprenderán habilidades diferentes al subir de nivel. También habrá items que el jugador encontrará que solo podrá equipar si son    de su clase.

- **Sistema de comercio**
  Al terminar los combates aparte de la experiencia ganada se podrá ganar una moneda, que posteriormente en una tienda se podrá gastar a cambio de items como
  items usables (pociones, comida...) o piezas de equipamiento.

- **NPC’s | Conversaciones con elección**
  A lo largo del juego, el jugador se encontrará con personajes no jugables. Al interactuar con ellos le darán información sobre el nivel o más información sobre la    historia. Además algunos de estos personajes, en puntos clave del juego podrán tener conversaciones en las que el jugador deberá elegir la respuesta del personaje,
  lo que le puede llevar a una recompensa o castigo.

- **Gancho**
  Se implementará una mecánica de gancho, con la que el jugador podrá acceder a zonas inaccesibles. El jugador no tendrá la mecánica desde el comienzo del juego, la    desbloqueará al llegar a un punto avanzado de la historia. Cuando el jugador pueda usar el gancho se le indicará con alguna clase de distintivo que esta en una       zona  en la que existe algún anclaje.

- **Puzle/Desafio en los niveles**
  En algunos niveles el jugador deberá resolver un puzzle para poder seguir avanzando por el nivel y poder pasar al siguiente.

- **Inventario**
  Se creará un sistema de inventario funcional, aprovechando la pantalla de inventario que trae la plantilla.

- **Sistema de Guardado**
  Crear uns sistema de guardado funcional, que permita guardar la partida y retomarla desde el mismo punto. Para así no tener que empezar una nueva partida siempre.

### Fisicas
Las físicas que se implementarán en el juego, son las convencionales de su genero. Es decir se implementarán las colisiones con los diferentes enemigos que haya en los mapas, y que con los diferentes obstaculos del camino. Debido a la camara que tiene el juego, no hay necesidad de implementar gravedad o saltos.

### Secuencia de niveles
Se implementarán dos niveles intermedios, conectados por un nexo y un nivel final. Se saldrá del nivel inicial del juego, para llegar al primer nivel, al salir de ese nivel se llegará a un nexo (campamento o pequeño asentamiento), del que podrá ir al segundo nivel y de allí al nivel final. La dificultad de los enemigos y el numero de ellos ira en aumento a lo largo de los niveles, aumentando así la dificultad del juego acorde con el aumento de nivel del personaje.

### Estética del juego
Para el aspecto del juego se seguirá la estética de la plantilla proporcionada para el proyecto, utilizando el estilo pixelart. Al ser un estilo relativamente facil de crear, perfecto para hacer un juego con baja demanda gráfica, del que se pueden encontrar muchos recursos para utilizar en la creación de mapas y escenarios. Y con el que nos sentimos comodos a la hora de trabajar.


