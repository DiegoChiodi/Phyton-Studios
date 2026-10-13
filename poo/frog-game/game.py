import arcade
import random
import peewee

from pyglet.math import Vec2

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
SCENE_SPEED = 80.0

ROAD_1 = 600

frog_sound = arcade.load_sound("frog_sound.mp3")

#------------------------------------------------
db = peewee.SqliteDatabase("ranking.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = peewee.CharField(unique=True)
    max_score = peewee.IntegerField()

db.connect()
db.create_tables([User])
#------------------------------------------------

def search_top_10():
    top_10 = User.select().order_by(User.max_score.desc()).limit(10)
    return top_10

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
    def __init__(self, filename, scale : float = 1.0, speed: float = 0.0):
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

class Landscape(EntScene):
    def check_exit_y(self):
        pass

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
                texture = r"cars\brown_cart.png"
            case 3:
                texture = r"cars\brown_cart.png" #Se eu deixar isso aq dps vou ter dor de cabeça <----------------------------------

        super().__init__(texture, scale * 0.9 , speed)

    
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

        self.acceleration : float = 3.0
        self.dying : bool = False

    def handle_key_press(self, key):
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.move_left = True

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.move_right = True
        
        if key == arcade.key.W or key == arcade.key.UP:
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
        self.direction = Vec2((self.move_right - self.move_left) * 1.4, self.move_up - self.move_down)
    
    def set_change(self, delta):
        self.change_x = lerp(self.change_x, self.direction.x * self.speed, 2 * delta)
        self.change_y = lerp(self.change_y, self.direction.y * self.speed, 2 * delta)

        if self.center_x < 500:
            self.center_x = 500
            self.change_x = 0
        elif self.center_x > 1400:
            self.center_x = 1400
            self.change_x = 0

class GameScene(arcade.View):
    def __init__(self, max_score : int = 0, nickname : str = ""):
        super().__init__()

        arcade.set_background_color(arcade.color.GRAY)

        self.obj_list = arcade.SpriteList()

        self.cam = arcade.Camera2D()

        self.player_dead = False

        self.player = Player()
        self.player.position = (SCREEN_WIDTH / 2, 100.0)
        self.score = 0
        self.max_score = max_score
        self.nickname = nickname
        print(f"Nickname: {self.nickname}, Max Score: {self.max_score}")

        self.cam.position = self.player.position

        self.rua = Landscape("Assets/road2.png")
        self.rua.center_x = SCREEN_WIDTH // 2
        self.rua.bottom = 0
        self.rua2 = Landscape("Assets/road2.png")
        self.rua2.center_x = SCREEN_WIDTH // 2
        self.rua2.bottom = self.rua.top

        self.landscape_l_1 = Landscape("Assets/landscape.png")
        self.landscape_l_1.left = 0
        self.landscape_l_1.bottom = 0

        self.landscape_r_1 = Landscape("Assets/landscape.png")
        self.landscape_r_1.right = SCREEN_WIDTH
        self.landscape_r_1.bottom = 0

        self.landscape_l_2 = Landscape("Assets/landscape.png")
        self.landscape_l_2.left = 0
        self.landscape_l_2.bottom = self.landscape_l_1.top

        self.landscape_r_2 = Landscape("Assets/landscape.png")
        self.landscape_r_2.right = SCREEN_WIDTH
        self.landscape_r_2.bottom = self.landscape_r_1.top

        self.obj_list.append(self.rua)
        self.obj_list.append(self.rua2)
        self.obj_list.append(self.player)

        self.obj_list.append(self.landscape_l_1)
        self.obj_list.append(self.landscape_r_1)
        self.obj_list.append(self.landscape_l_2)
        self.obj_list.append(self.landscape_r_2)

        landscape_scale = 5.0

        self.landscape_r_1.scale = landscape_scale
        self.landscape_l_1.scale = landscape_scale
        self.landscape_r_2.scale = landscape_scale
        self.landscape_l_2.scale = landscape_scale

        self.landscape_r_1.scale_x = -1 * landscape_scale
        self.landscape_r_2.scale_x = -1 * landscape_scale

        self.explosion = EntScene("Assets/explosion.png", 1.0, 0.0)
        self.obj_list.append(self.explosion)
        self.explosion.visible = False

    def on_update(self, delta_time):
        if self.player_dead:
            self.explosion.scale = tuple(
                value * 1.1 for value in self.explosion.scale
            )
            if self.explosion.scale[0] > 50.0:
                self.window.show_view(GameOverView(self.score, max_score=self.max_score, nickname=self.nickname))

            self.shake_camera(delta_time)
    
            return
        

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
                self.player_dead = True
                self.explosion.position = self.player.position
                self.explosion.visible = True
        if self.rua.top < 0.0:
            self.rua.bottom = self.rua2.top - 100

        if self.rua2.top < 0.0:
            self.rua2.bottom = self.rua.top - 100

        if self.landscape_l_1.top < 0.0:
            self.landscape_l_1.bottom = self.landscape_l_2.top

        if self.landscape_l_2.top < 0.0:
            self.landscape_l_2.bottom = self.landscape_l_1.top

        if self.landscape_r_1.top < 0.0:
            self.landscape_r_1.bottom = self.landscape_r_2.top

        if self.landscape_r_2.top < 0.0:
            self.landscape_r_2.bottom = self.landscape_r_1.top

    def on_draw(self):
        self.clear()
        self.cam.use()
        self.obj_list.draw()
        score_txt = arcade.Text(str(self.score), 50, SCREEN_HEIGHT - 50, arcade.color.WHITE, 25)
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
                enemy_speed *= 2
            else:
                enemy_angle = 180
            enemy = Enemy(0.75, enemy_speed)
            enemy.center_y = SCREEN_HEIGHT

            match(rua):
                case 1:
                    enemy.center_x = 600.0
                case 2:
                    enemy.center_x = 825.0
                case 3:
                    enemy.center_x = 1090.0
                case 4:
                    enemy.center_x = 1325
            enemy.angle = enemy_angle
            self.obj_list.append(enemy)

    def shake_camera(self, delta):
        self.cam.position += Vec2(random.randint(-10, 10), random.randint(-10, 10)) * 10
    
    def on_key_press(self, key, modifiers):
        self.player.handle_key_press(key)
        if key == arcade.key.ESCAPE:
            start_view = StartView(max_score=self.max_score, nickname=self.nickname)
            self.window.show_view(start_view)
        elif key == arcade.key.R:
            game_scene = GameScene(max_score=self.max_score, nickname=self.nickname)
            self.window.show_view(game_scene)
    
    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)
    
class StartView(arcade.View):
    def __init__(self, window = None, background_color = arcade.color.GRAY, is_login = False, max_score = 0, nickname = ""):
        super().__init__(window, background_color)
        self.is_login = is_login
        self.max_score = max_score
        self.nickname = nickname
    
    def on_draw(self):
        self.clear()

        if self.is_login:
            text = arcade.Text(
                text="Pressione Enter para jogar",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                color=arcade.color.GREEN,
                font_size=100,
                anchor_x="center",
                anchor_y="center",
            )

            text.draw()
        else:
            text = arcade.Text(
                text="Digite seu nickname para jogar",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                color=arcade.color.GREEN,
                font_size=100,
                anchor_x="center",
                anchor_y="center",
            )

            text.draw()

            text_nickname = arcade.Text(
                text=self.nickname,
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 - 100,
                color=arcade.color.GREEN,
                font_size=50,
                anchor_x="center",
                anchor_y="center",
            )
            text_nickname.draw()

    def on_key_press(self, key, modifiers):
        if self.is_login:
            if (key == arcade.key.J or key == arcade.key.ENTER):
                game_scene = GameScene(max_score=self.max_score, nickname=self.nickname)
                self.window.show_view(game_scene)
        else:
            if key == arcade.key.ENTER:
                if self.nickname.strip() == "":
                    return
                self.is_login = True
                self.nickname = self.nickname.strip()
                user = User.get_or_none(User.name == self.nickname)
                if user is None:
                    User.create(name=self.nickname, max_score=0)
            elif key == arcade.key.BACKSPACE:
                self.nickname = self.nickname[:-1]

    def on_text(self, text):
        if not self.is_login:
            self.nickname += text

class RankingView(arcade.View):
    def __init__(self, window = None, background_color = arcade.color.GRAY, max_score = 0, nickname = ""):
        super().__init__(window, background_color)
        self.nickname = nickname
        self.max_score = max_score
        self.top_10 = search_top_10()
    
    def on_draw(self):
        self.clear()

        title_txt = arcade.Text(
            "Ranking Top 10",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.GREEN,
            100,
            anchor_x="center",
            anchor_y="center"
        )
        title_txt.draw()

        for i, user in enumerate(self.top_10):
            user_txt = arcade.Text(
                f"{i + 1}. {user.name} - {user.max_score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 200 - (i * 50),
                arcade.color.GREEN,
                50,
                anchor_x="center",
                anchor_y="center"
            )
            user_txt.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            start_view = StartView(max_score=self.max_score, nickname=self.nickname)
            self.window.show_view(start_view)

class GameOverView(arcade.View):
    def __init__(self, score, max_score = 0, nickname = ""):
        super().__init__(window = None, background_color = arcade.color.GRAY)
        self.score = score
        self.max_score = max_score
        self.nickname = nickname
        print("Game Over")
        print(self.nickname)
        self.user = User.get_or_none(User.name == self.nickname)
        if self.user is not None and self.score > self.user.max_score:
            self.user.max_score = self.score
            self.user.save()

    def on_draw(self):
        self.clear()

        start_txt = arcade.Text(
            "Foi por pouco, pressione [Enter] para tentar novamente",
            SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2, arcade.color.GREEN, 40
        )
        
        txt_motivation = ""

        if (self.score < self.max_score):
            txt_motivation = f"Está quase lá, você fez {self.score} e seu recorede é {self.max_score}!"
        else:
            txt_motivation = f"Parabéns! Seu novo recorde é {self.score}!"
            self.max_score = self.score

        #aaaaaaaaaaaaa

        motivation_txt = arcade.Text(
            txt_motivation,
            SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2  - 200, arcade.color.GREEN, 40
        )
        ranking_infm_txt = arcade.Text(
            "Pressione [T] para ver o ranking",
            SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2  - 300, arcade.color.GREEN, 40
        )

        start_txt.draw()
        motivation_txt.draw()
        ranking_infm_txt.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J or key == arcade.key.ENTER:
            game_scene = GameScene(max_score=self.max_score, nickname=self.nickname)
            self.window.show_view(game_scene)

        if key == arcade.key.T:
            ranking_view = RankingView(max_score=self.max_score, nickname=self.nickname)
            self.window.show_view(ranking_view)

def execute():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, title="Frog streak")
    
    start_view = StartView(max_score=0, nickname="")

    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    execute()