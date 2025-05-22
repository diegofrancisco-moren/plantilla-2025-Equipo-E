import arcade

INVENTORY_COLS = 6
INVENTORY_ROWS = 3
CELL_WIDTH = 200
CELL_HEIGHT = 150
START_X = 50
START_Y = 100

BUTTON_X = 1000
BUTTON_Y = 600
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 50


class Item():
    def __init__(self, name, color, quantity):
        self.name = name
        self.color = color
        self.quantity = quantity


class InventoryView(arcade.View):
    def __init__(self, player):
        super().__init__()
        self.inventory = [[None for _ in range(INVENTORY_COLS)] for _ in range(INVENTORY_ROWS)]
        self.selected = None
        self.player = player

    def setup(self):
        # ejemplos
        player_inventory = list(self.player.get_inventory().values())
        i_cols = 0
        i_rows = 2
        item_color = None
        for i in range(len(player_inventory)):
            i_cols = i
            if i_cols > 6:
                i_cols = 0
                i_rows -= 1
            if player_inventory[i]["type"] == "Weapon":
                item_color = arcade.color.RED
            elif player_inventory[i]["type"] == "Food":
                item_color = arcade.color.YELLOW
            elif player_inventory[i]["type"] == "Potion":
                item_color = arcade.color.GREEN
            self.inventory[i_rows][i_cols] = Item(player_inventory[i]["name"],
                                                  item_color, player_inventory[i]["quantity"])

    def on_draw(self):

        arcade.start_render()
        arcade.set_background_color(arcade.color.ALMOND)

        # Título
        arcade.draw_text(
            "Inventario",
            self.window.width / 2,
            self.window.height - 40,
            arcade.color.DARK_BROWN,
            40,
            anchor_x="center"
        )

        # Dibujar celdas
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                x = START_X + col * CELL_WIDTH + CELL_WIDTH // 2
                y = START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2
                is_selected = self.selected == (row, col)

                # Celda
                arcade.draw_rectangle_outline(x, y, CELL_WIDTH, CELL_HEIGHT, arcade.color.BONE, 5)

                # Selección
                if is_selected:
                    arcade.draw_rectangle_outline(x, y, CELL_WIDTH + 10, CELL_HEIGHT + 10, arcade.color.YELLOW_ORANGE, 5)

                # Ítem
                item = self.inventory[row][col]
                if item:
                    arcade.draw_circle_filled(x, y, 30, item.color)
                    arcade.draw_text(
                        item.name,
                        x,
                        y - 45,
                        arcade.color.DARK_BROWN,
                        14,
                        anchor_x="center"
                    )
                    arcade.draw_text(
                        f"x{item.quantity}",
                        x,
                        y + 45,
                        arcade.color.DARK_BROWN,
                        14,
                        anchor_x="center"
                    )

        # Información del ítem seleccionado
        if self.selected:
            item = self.inventory[self.selected[0]][self.selected[1]]
            if item:
                arcade.draw_text(
                    f"Seleccionado: {item.name}",
                    self.window.width / 2,
                    50,
                    arcade.color.BLACK,
                    20,
                    anchor_x="center"
                )

        # Dibujar botón de ordenar
        arcade.draw_rectangle_filled(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, arcade.color.LIGHT_GRAY)
        arcade.draw_text(
            "Ordenar A-Z",
            BUTTON_X,
            BUTTON_Y - 10,
            arcade.color.BLACK,
            18,
            anchor_x="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        #  clic en una celda
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                cell_x = START_X + col * CELL_WIDTH + CELL_WIDTH // 2
                cell_y = START_Y + row * CELL_HEIGHT + CELL_HEIGHT // 2

                if abs(x - cell_x) < CELL_WIDTH // 2 and abs(y - cell_y) < CELL_HEIGHT // 2:
                    self.selected = (row, col)
                    return

        #  clic en el botón de ordenar
        if (
            BUTTON_X - BUTTON_WIDTH / 2 < x < BUTTON_X + BUTTON_WIDTH / 2 and
            BUTTON_Y - BUTTON_HEIGHT / 2 < y < BUTTON_Y + BUTTON_HEIGHT / 2
        ):
            self.sort_inventory()

    def sort_inventory(self):
        # Extraer todos los ítems
        items = [item for row in self.inventory for item in row if item]
        # Ordenar por nombre
        items.sort(key=lambda item: item.name.lower())

        # Rellenar inventario vacío con ítems ordenados
        new_inventory = [[None for _ in range(INVENTORY_COLS)] for _ in range(INVENTORY_ROWS)]
        index = 0
        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                if index < len(items):
                    new_inventory[2 - row][col] = items[index]
                    index += 1
        self.inventory = new_inventory
        self.selected = None  # Deselecciona tras ordenar

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.ESCAPE, arcade.key.I):
            self.window.show_view(self.window.views["game"])