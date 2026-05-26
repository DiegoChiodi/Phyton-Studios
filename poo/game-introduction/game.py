import arcade

WIDTH = 800
HEIGHT = 600
TITLE = "Meu Jogo"


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__("steve_head.png", 0.5)

        self.direction = 0

        self.left = False
        self.right = False

        self.speed = 100.0

    def handle_key_press(self, key):

        if key == arcade.key.A:
            self.left = True

        if key == arcade.key.D:
            self.right = True

    def handle_key_release(self, key):

        if key == arcade.key.A:
            self.left = False

        if key == arcade.key.D:
            self.right = False

    def update_player(self, delta_time):

        self.direction = (
            int(self.right) -
            int(self.left)
        )

        self.center_x += (
            100 * delta_time
        )
        print(self.direction)

class Game(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)

        arcade.set_background_color(arcade.color.GRAY)

        self.player_list = arcade.SpriteList()

        self.player = Player()
        self.player.position = (400,300)

        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw() 
    
    def on_update(self, delta_time):
        self.player.update_player(delta_time)
    
    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)



def executar():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    executar()