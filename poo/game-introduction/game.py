import arcade
import random

from pyglet.math import Vec2

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCENE_SPEED = 100.0

frog_sound = arcade.load_sound("frog_sound.mp3")

def lerp(a, b, t):
    return a + (b - a) * t

class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("Pressione enter para jogar", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.GREEN, 20)
        return super().on_draw()

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

        self.check_exit_x()
        self.check_exit_y()

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

class EntScene(Entity):
    def __init__(self, filename, scale, speed: float = 0.0):
        super().__init__(filename, scale, speed)
    
    def scene_move(self, delta):
        self.center_y -= SCENE_SPEED * delta

    def update(self, delta):
        super().update(delta)
        self.scene_move(delta)
    
    def check_exit_y(self):
        if (self.bottom < 0):
            self.change_y = 0
            self.bottom = 0
            self.on_exit_window()
    
class Frog(EntScene):
    def __init__(self, speed : float = 0.0):
        super().__init__("frog.png", 0.2, speed)
        self.exit_window = False
    
    def on_exit_window(self):        
        self.remove_from_sprite_lists()
        return super().on_exit_window()

    def set_direction(self):
        pass

class Enemy(EntScene):
    def __init__(self, scale, speed : float = 0.0):
        texture = ""

        ale = random.randint(1, 3)

        match(ale):
            case 1:
                texture = r"cars\blue_cart.png"
            case 2:
                texture = r"cars\brow_cart.png"
            case 3:
                texture = r"cars\green_cart.png"


        super().__init__("player.png", scale, speed)
    
    def update(self, delta):
        super().update(delta)
    
    def set_direction(self):
        self.direction = Vec2(0, -1.0)

    def check_exit_y(self):
        if (self.top < 0):
            self.remove_from_sprite_lists()

class Player(Entity):           
    def __init__(self):
        super().__init__("player.png", 1.5, 300.0)

        self.move_left : bool = False
        self.move_right : bool = False
        self.move_up : bool = False
        self.move_down : bool = False

        self.acceleration : float = 1.0
        

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
    
    def set_change(self, delta):
        self.change_x = lerp(self.change_x, self.direction.x * self.speed, 2 * delta)
        self.change_y = lerp(self.change_y, self.direction.y * self.speed, 2 * delta)

class GameScene(arcade.View):
    def __init__(self, max_score : int = 0):
        super().__init__()

        arcade.set_background_color(arcade.color.GRAY)

        self.obj_list = arcade.SpriteList()

        self.player = Player()
        self.player.position = (SCREEN_WIDTH / 2, 100.0)
        self.obj_list.append(self.player)
        self.score = 0
        self.max_score = max_score

    def on_update(self, delta_time):
        self.obj_list.update(delta_time)         

        self.spawn_frogs()
        self.spawn_enemy()

        for obj in self.obj_list:
            if isinstance(obj, Frog) and arcade.check_for_collision(self.player, obj):
                self.obj_list.remove(obj)
                self.score += 1
                arcade.play_sound(frog_sound)
        for obj in self.obj_list:
            if isinstance(obj, Enemy) and arcade.check_for_collision(self.player, obj):
                self.player.remove_from_sprite_lists()
                self.window.show_view(GameOverView(self.score, self.max_score))

    def on_draw(self):
        self.clear()
        self.obj_list.draw()
        score_txt = arcade.Text(str(self.score), 50, SCREEN_HEIGHT - 50)
        score_txt.draw()
    
    def spawn_frogs(self):
        if (random.randint(1, 90) == 1):
            if (random.randint(1, 2) == 1):
                frog = Frog(random.randint(40 , 70))
                frog.position = ((SCREEN_HEIGHT / 2 - 200), SCREEN_HEIGHT)
                self.obj_list.append(frog)
                frog.angle = 90
                frog.direction = Vec2(1, 0)
            else:
                frog = Frog(random.randint(40 , 70))
                frog.position = ((SCREEN_HEIGHT / 2 + 800), SCREEN_HEIGHT)
                self.obj_list.append(frog)
                frog.angle = 270
                frog.direction = Vec2(-1, 0)
    
    def spawn_enemy(self):
        if (random.randint(1, 90) == 1):
            rua = random.randint(1,4)
            enemy_speed = enemy_speed = random.randint(50,100)
            enemy_angle = 0
            if (rua > 2):
                enemy_angle = 180
                enemy_speed *= 2
            enemy = Enemy(2, enemy_speed)
            enemy.position =  ((SCREEN_HEIGHT / 2 + (rua * 220.0) - 100), SCREEN_HEIGHT)
            enemy.angle = enemy_angle
            self.obj_list.append(enemy)
    
    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        if key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)
        elif key == arcade.key.R:
            game_scene = GameScene(self.max_score)
            self.window.show_view(game_scene)
    
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
    
class StartView(arcade.View):
    def __init__(self, window = None, background_color = arcade.color.GRAY):
        super().__init__(window, background_color)
    
    def on_draw(self):
        self.clear()
        
        start_txt = arcade.Text(
            "Pressione [Enter] para jogar",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.GREEN_YELLOW
        )
        start_txt.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            game_scene = GameScene()
            self.window.show_view(game_scene)

class GameOverView(arcade.View):
    def __init__(self, score, max_score):
        super().__init__(window = None, background_color = arcade.color.GRAY)
        self.score = score
        self.max_score = max_score
    
    def on_draw(self):
        self.clear()

        start_txt = arcade.Text(
            "Foi por pouco, pressione [Enter] para tentar novamente",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.RED
        )
        
        txt_motivation = ""

        if (self.score < self.max_score):
            txt_motivation = f"Está quase lá, você fez {self.score} e seu recorede é {self.max_score}!"
        else:
            txt_motivation = f"Parabéns! Seu novo recorde é {self.score}!"
            self.max_score = self.score

        motivation_txt = arcade.Text(
            txt_motivation,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  - 20, arcade.color.RED
        )
        start_txt.draw()
        motivation_txt.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            game_scene = GameScene(self.max_score)
            self.window.show_view(game_scene)


def execute():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="Frog streak")
    
    start_view = StartView()

    window.show_view(start_view)
    
    arcade.run()

if __name__ == "__main__":
    execute()