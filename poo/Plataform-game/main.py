import arcade
import random

from pyglet.math import Vec2

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

def lerp(a, b, t):
    return a + (b - a) * t

class Entity(arcade.Sprite):
    def __init__(self, filename, scale, speed: float = 0.0):
        super().__init__(filename, scale)
        self.direction = Vec2(0.0, 0.0)
        self.speed = speed

    def set_direction(self):
        pass
    
    def set_change(self, delta : float):
        self.change_x = self.speed * self.direction.x
        self.change_y = self.speed * self.direction.y

    def update(self, delta):
        self.set_direction()

        self.set_change(delta)

        self.center_x += (
            self.change_x * delta
        )

        self.center_y += (
            self.change_y * delta
        )
    
    def check_exit_x(self):
        if (self.right > SCREEN_WIDTH):
            self.change_x = 0
            self.right = SCREEN_WIDTH
            self.on_exit_window()
        elif (self.left < 0):
            self.change_x = 0
            self.left = 0
            self.on_exit_window()

    def check_exit_y(self):
        if (self.top > SCREEN_HEIGHT):
            self.change_y = 0
            self.top = SCREEN_HEIGHT
            self.on_exit_window()
        elif (self.bottom < 0):
            self.change_y = 0
            self.bottom = 0
            self.on_exit_window()

    def on_exit_window(self):
        pass

class Block(arcade.Sprite):
    def __init__(self, x: float, y: float):

        super().__init__("assets/block.png")

        self.center_x = x
        self.center_y = y

class Player(Entity):           
    def __init__(self):
        super().__init__("assets/player.png", 0.5, 3.0)

        self.move_left : bool = False
        self.move_right : bool = False
        self.move_up : bool = False
        self.move_down : bool = False

        self.acceleration : float = 1.0
        self.JUMP_FORCE : float = 20.0

        self.speed = 10

    def handle_key_press(self, key):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.move_left = True

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.move_right = True
            
            self.move_up = True
        
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.move_down = True

    def handle_key_release(self, key):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.move_left = False

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.move_right = False
        
        if key == arcade.key.W or key == arcade.key.UP:
            self.move_up = False
        
        if key == arcade.key.S or key == arcade.key.DOWN:
            self.move_down = False

    def set_direction(self):
        self.direction = Vec2((self.move_right - self.move_left), self.move_up)
    
    def set_change(self, delta):
        self.change_x = lerp(self.change_x, self.direction.x * self.speed, 10 * delta)

            
class StartView(arcade.View):
    def __init__(self, window = None, background_color = arcade.color.GRAY):
        super().__init__(window, background_color)
    
    def on_draw(self):
        self.clear()
        
        arcade.draw_text(
            text="Pressione Enter para jogar",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            color=arcade.color.GREEN,
            font_size=100,
            anchor_x="center",
            anchor_y="center",
        )
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            game_scene = GameScene()
            self.window.show_view(game_scene)

class GameScene(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.GRAY)

        self.obj_list = arcade.SpriteList()

        self.player = Player()
        self.player.position = (200, 200)
        self.obj_list.append(self.player)
        
        self.GRAVITY = 1.0

        self.list_blocks = arcade.SpriteList()
        for x in range(32, SCREEN_WIDTH + 32, 64):
            self.bloco = Block(x=x, y=64)
            self.list_blocks.append(self.bloco)

        self.bloco = Block(SCREEN_WIDTH / 2, 350)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(SCREEN_WIDTH / 2 + 250, 600)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(SCREEN_WIDTH / 2 + 500, 850)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(SCREEN_WIDTH / 2 - 250, 600)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(SCREEN_WIDTH / 2 - 500, 850)
        self.list_blocks.append(self.bloco)

        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.list_blocks,
            gravity_constant=self.GRAVITY
       )
        

        
        self.jump : float = 2
        self.JUMP_MAX : float = 2


        
        
    def on_update(self, delta_time):
        self.obj_list.update(delta_time)
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            self.jump = self.JUMP_MAX

    def on_draw(self):
        self.clear()
        self.obj_list.draw()
        self.list_blocks.draw()

    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        
        if key == arcade.key.W or key == arcade.key.UP:
            if self.jump > 0:
                self.player.change_y = self.player.JUMP_FORCE
                self.jump -= 1

    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)


def execute():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="Frog streak")
    
    start_view = StartView()

    window.show_view(start_view)
    
    arcade.run()

if __name__ == "__main__":
    execute()