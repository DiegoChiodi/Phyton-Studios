import arcade
from pyglet.math import Vec2

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCENE_SPEED = 50.0

class Entity(arcade.Sprite):
    def __init__(self, filename, scale, speed: float = 0.0):
        super().__init__(filename, scale)
        self.direction = Vec2(0.0, 0.0)
        self.speed = speed

    def set_direction(self):
        self.direction = Vec2(0.0, 0.0)

    def update(self, delta_time):
        self.set_direction()

        self.change_x = self.speed * self.direction.x

        self.center_x += (
            self.change_x * delta_time
        )
        
        self.change_y = self.speed * self.direction.y

        self.center_y += (
            self.change_y * delta_time
        )

class EntScene(Entity):
    def __init__(self, filename, scale, speed: float = 0.0):
        super().__init__(filename, scale, speed)
    
    def scene_move(self, delta_time):
        self.center_y -= SCENE_SPEED * delta_time

    def update(self, delta_time):
        super().update(delta_time)
        self.scene_move(delta_time)

class Frog(EntScene):
    def __init__(self):
        super().__init__("frog.png", 0.2, 200.0)
    
    def set_direction(self):
        self.direction = Vec2(1.0, 0.0)

class Player(Entity):           

    def __init__(self):
        super().__init__("player.png", 1.5, 300.0)

        self.move_left : bool = False
        self.move_right : bool = False
        self.move_up : bool = False
        self.move_down : bool = False
        

    def handle_key_press(self, key):
        if key == arcade.key.A:
            self.move_left = True

        if key == arcade.key.D:
            self.move_right = True
        
        if key == arcade.key.W:
            self.move_up = True
        
        if key == arcade.key.S:
            self.move_down = True

    def handle_key_release(self, key):
        if key == arcade.key.A:
            self.move_left = False

        if key == arcade.key.D:
            self.move_right = False
        
        if key == arcade.key.W:
            self.move_up = False
        
        if key == arcade.key.S:
            self.move_down = False
    
    def set_direction(self):
        self.direction = Vec2((self.move_right - self.move_left) * 1.4, self.move_up - self.move_down)

class Game(arcade.Window):

    def __init__(self):
        super().__init__(fullscreen=True, title="Frog streak")

        arcade.set_background_color(arcade.color.GRAY)

        self.obj_list = arcade.SpriteList()

        self.player = Player()
        self.player.position = (SCREEN_WIDTH / 2, 100.0)

        for i in range(4):
            frog = Frog()
            frog.position = ((SCREEN_HEIGHT / 2 + i * 300.0), SCREEN_HEIGHT - 100)
            self.obj_list.append(frog)

        self.obj_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.obj_list.draw()
    
    def on_update(self, delta_time):
        self.obj_list.update(delta_time)

        for obj in self.obj_list:
            if isinstance(obj, Frog) and arcade.check_for_collision(self.player, obj):
                self.obj_list.remove(obj)
    
    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)         

def execute():
    window = Game()
    arcade.run()

if __name__ == "__main__":
    execute()