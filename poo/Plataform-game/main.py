import arcade
import random

from pyglet.math import Vec2

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

def lerp(a, b, t):
    return a + (b - a) * t

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/images.jpg", 0.5)

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
        super().__init__("assets/player_happy_1.png", 2.0, 3.0)

        self.move_left : bool = False
        self.move_right : bool = False
        self.move_up : bool = False
        self.move_down : bool = False

        self.acceleration : float = 1.0
        self.JUMP_FORCE : float = 20.0

        self.speed = 10

        self.jumps : float = 2
        self.JUMP_MAX : float = 2
        self.last_move_up = self.move_up

        self.hot = False

        self.hot_timer = 0.0
        self.HOT_DURATION = 2.0
        self.on_stop = False

    def handle_key_press(self, key):
        if key == arcade.key.A:
            self.move_left = True

        if key == arcade.key.D:
            self.move_right = True
        
        if key == arcade.key.S:
            self.move_down = True

        if key == arcade.key.W:
            self.move_up = True
            

    def handle_key_release(self, key):
        if key == arcade.key.A:
            self.move_left = False

        if key == arcade.key.D:
            self.move_right = False
        
        if key == arcade.key.W:
            self.move_up = False
        
        if key == arcade.key.S:
            self.move_down = False

    def update(self, delta):
        super().update(delta)

        self.state_machine()

        if self.last_move_up != self.move_up and self.move_up:
            self.jump()

        self.last_move_up = self.move_up

        self.update_texture()

        if self.on_stop:
            if self.hot_timer >= self.HOT_DURATION:
                self.on_stop = False
                self.hot_timer = 0.0
            else:
                self.hot_timer += delta

    def set_direction(self):
        if self.on_stop:
            return
        self.direction = Vec2((self.move_right - self.move_left), self.move_up)
        self.scale_x = 1 * self.scale[0] if self.move_right else -1 * self.scale[0] if self.move_left else self.scale_x
    
    def set_change(self, delta):
        self.change_x = lerp(self.change_x, self.direction.x * self.speed, 10 * delta)

    def jump(self):
        if self.on_stop:
            return
        if self.jumps > 0:
            self.change_y = self.JUMP_FORCE
            self.jumps -= 1

    def recharge_jump(self):
        self.jumps = self.JUMP_MAX

    def update_texture(self):
        if self.hot:
            self.texture = arcade.load_texture("assets/player_angry_1.png")
        else:
            self.texture = arcade.load_texture("assets/player_happy_1.png")

    def get_hot(self):
        self.hot = True
        self.on_stop = True

        self.direction = Vec2(0.0, 0.0)

    def state_machine(self):

        if self.change_y != 0:
            self.jump_ani()
            return

        if self.center_x == 0:
            self.idle_ani()
            return
        

        self.walk_ani()

    def walk_ani(self):
        pass

    def jump_ani(self):
        pass

    def idle_ani(self):
        pass


class Player2(Player):
    def handle_key_press(self, key):
        if key == arcade.key.LEFT:
            self.move_left = True

        if key == arcade.key.RIGHT:
            self.move_right = True

        if key == arcade.key.UP:
            self.move_up = True
        
        if key == arcade.key.DOWN:
            self.move_down = True

    def handle_key_release(self, key):
        if key == arcade.key.LEFT:
            self.move_left = False

        if key == arcade.key.RIGHT:
            self.move_right = False
        
        if key == arcade.key.UP:
            self.move_up = False
        
        if key == arcade.key.DOWN:
            self.move_down = False

    
    def update_texture(self):
        if self.hot:
            self.texture = arcade.load_texture("assets/player_angry_2.png")
        else:
            self.texture = arcade.load_texture("assets/player_happy_2.png")
            

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
            game_scene = Map_2()
            self.window.show_view(game_scene)

class GameSceneBase(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.obj_list = arcade.SpriteList()

        self.player = Player()
        self.player2 = Player2()

        self.player.position, self.player2.position = self.set_players_pos()

        self.obj_list.append(self.player)
        self.obj_list.append(self.player2)

        random.seed()
        temp = random.randint(0, 1)

        if temp == 0:
            self.player.hot = True
        else:
            self.player2.hot = True

        self.GRAVITY = 1.0

        
        self.set_blocks()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.list_blocks,
            gravity_constant=self.GRAVITY
        )

        self.physics_engine2 = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player2,
            platforms=self.list_blocks,
            gravity_constant=self.GRAVITY
        )

    def set_blocks(self):
        pass

    def set_players_pos(self):
        return (200, 200), (400, 200)
        
    def on_update(self, delta_time):
        if self.phys_perm:            
            self.obj_list.update(delta_time)
            self.physics_engine.update()
            self.physics_engine2.update()

            if self.physics_engine.can_jump():
                self.player.recharge_jump()

            if self.physics_engine2.can_jump():
                self.player2.recharge_jump()

            if arcade.check_for_collision(self.player, self.player2):
                if self.player.hot and not self.player.on_stop:
                    self.player2.get_hot()
                    self.player.hot = False
                elif self.player2.hot and not self.player2.on_stop:
                    self.player.get_hot()
                    self.player2.hot = False

            self.time -= delta_time

        if self.time <= 0.0:
            self.phys_perm = False
            self.time = 0.0

    def on_draw(self):
        self.clear()
        self.obj_list.draw()
        self.list_blocks.draw()

        arcade.draw_text(
            text=f"Time: {int(self.time)}",
            x=SCREEN_WIDTH - 200,
            y=SCREEN_HEIGHT - 50,
            color=arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
            anchor_y="center",
        )

        if not self.phys_perm:
            jogador = 2 if self.player.hot else 1
            color = arcade.color.RED if self.player.hot else arcade.color.BLUE
            arcade.draw_text(
                f"O jogador {jogador} ganhou!",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                color=color,
                font_size=100,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        self.player2.handle_key_press(key)

        if (key == arcade.key.R or key == arcade.key.ENTER or key == arcade.key.SPACE) and not self.phys_perm:
            game_scene = GameSceneBase()
            self.window.show_view(game_scene)
            
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
        self.player2.handle_key_release(key)

class Map_1(GameSceneBase):
    def set_blocks(self):
        self.time = 60.0
        self.phys_perm = True

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

class Map_2(GameSceneBase):
    def set_blocks(self):
        self.time = 60.0
        self.phys_perm = True

        self.list_blocks = arcade.SpriteList()

        # Chão
        for x in range(32, SCREEN_WIDTH + 32, 64):
            self.bloco = Block(x=x, y=64)
            self.list_blocks.append(self.bloco)

        # Plataformas
        self.bloco = Block(180, 250)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(450, 250)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(720, 400)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(1000, 300)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(750, 600)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(450, 550)
        self.list_blocks.append(self.bloco)

        self.bloco = Block(180, 700)
        self.list_blocks.append(self.bloco)

def execute():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="Frog streak")
    
    start_view = StartView()

    window.show_view(start_view)
    
    arcade.run()

if __name__ == "__main__":
    execute()
