from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.core.audio import SoundLoader
from kivmob import KivMob   # DİQQƏT: Sənin modulunda ad kiumob/KiuMob-dur
import random

# Sənin AdMob ID-lərin
APP_ID = "ca-app-pub-6525217937280813~1393662594"
BANNER_ID = "ca-app-pub-6525217937280813/9272692614"
INTERSTITIAL_ID = "ca-app-pub-6525217937280813/8148365599"
REWARDED_ID = "ca-app-pub-6525217937280813/7309926649"

class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Oyun parametrləri
        self.snake_size = 20
        self.food_size = 20
        self.reset_game()

        # Klaviatura
        self._keyboard = Window.request_keyboard(None, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self.on_key_down)

        # Update dövrü
        Clock.schedule_interval(self.update, 0.35)

        # Səslər (yoxdursa, None olacaq, crash etməyəcək)
        self.eat_sound = SoundLoader.load("beep-03.wav")
        self.over_sound = SoundLoader.load("beep-05.wav")

        # KiuMob reklam inteqrasiyası
        self.ads = KivMob(APP_ID)

        # Banner: yarad → request → göstər
        # Mövqe olaraq 'bottom' daha uyğundur; 'top' da mümkündür
        self.ads.new_banner(BANNER_ID, 'bottom')
        self.ads.request_banner()
        self.ads.show_banner()

        # Interstitial: yarad → request → sonradan hazır olanda göstər
        self.ads.new_interstitial(INTERSTITIAL_ID)
        self.ads.request_interstitial()

        # Rewarded: öncədən yüklə, Game Over-da göstər
        self.ads.load_rewarded_ad(REWARDED_ID)

        # Rewarded hadisə dinləyicisi (opsional, amma faydalıdır)
        # Listener string event-lər qaytara bilər: 'rewarded', 'closed', 'failed' və s.
        try:
            self.ads.set_rewarded_ad_listener(self.on_rewarded_event)
        except Exception:
            pass  # əgər listener parametrləri fərqlidirsə, kod davam etsin

        # Oyun sayğacı (interstitial üçün)
        self.round_ticks = 0

        # Ekran ölçüləri
        if Window.width < 480:
            Window.size = (480, 800)

    def reset_game(self):
        self.snake = [[100, 100]]  # baş
        self.snake_dir = [self.snake_size, 0]  # sağa
        self.food_pos = [200, 200]
        self.score = 0
        self.game_over = False

        # Score label
        self.label = CoreLabel(text=f"Score: {self.score}", font_size=24)
        self.label.refresh()

        # İlk çəkiliş
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.text_rect = Rectangle(texture=self.label.texture,
                                       pos=(10, Window.height - 35),
                                       size=self.label.texture.size)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if self.game_over:
            if key == 'r':
                self.reset_game()
                # Rewarded və interstitial-i yenidən hazırlayaq
                try:
                    self.ads.request_interstitial()
                except Exception:
                    pass
                try:
                    self.ads.load_rewarded_ad(REWARDED_ID)
                except Exception:
                    pass
            return

        if key == 'up' and self.snake_dir[1] == 0:
            self.snake_dir = [0, self.snake_size]
        elif key == 'down' and self.snake_dir[1] == 0:
            self.snake_dir = [0, -self.snake_size]
        elif key == 'left' and self.snake_dir[0] == 0:
            self.snake_dir = [-self.snake_size, 0]
        elif key == 'right' and self.snake_dir[0] == 0:
            self.snake_dir = [self.snake_size, 0]

    def update(self, dt):
        if self.game_over:
            return

        # Yeni baş koordinatı
        new_head = [self.snake[0][0] + self.snake_dir[0],
                    self.snake[0][1] + self.snake_dir[1]]

        # Divara və ya özünə dəyibsə, Game Over
        if (new_head[0] < 0 or new_head[0] >= Window.width or
            new_head[1] < 0 or new_head[1] >= Window.height or
            new_head in self.snake):
            self.game_over = True
            if self.over_sound:
                try:
                    self.over_sound.play()
                except Exception:
                    pass
            self.show_game_over()
            return

        # İrəlilə
        self.snake.insert(0, new_head)

        # Yem yeyilibsə
        if new_head[0] == self.food_pos[0] and new_head[1] == self.food_pos[1]:
            self.score += 1
            if self.eat_sound:
                try:
                    self.eat_sound.play()
                except Exception:
                    pass
            # Yeni yem
            self.food_pos = [
                random.randrange(0, Window.width // self.food_size) * self.food_size,
                random.randrange(0, Window.height // self.food_size) * self.food_size
            ]
        else:
            # Quyruqdan sil
            self.snake.pop()

        # Rəsm
        self.canvas.clear()
        with self.canvas:
            # İlan
            Color(0, 1, 0, 1)
            for segment in self.snake:
                Rectangle(pos=segment, size=(self.snake_size, self.snake_size))
            # Yem
            Color(1, 0, 0, 1)
            Rectangle(pos=self.food_pos, size=(self.food_size, self.food_size))
            # Score
            Color(1, 1, 1, 1)
            self.label.text = f"Score: {self.score}"
            self.label.refresh()
            self.text_rect = Rectangle(texture=self.label.texture,
                                       pos=(10, Window.height - 35),
                                       size=self.label.texture.size)

        # Interstitial lojiqası: hər ~120 tikdə yoxla (təxminən 40-45 saniyə)
        self.round_ticks += 1
        if self.round_ticks >= 120:
            self.round_ticks = 0
            try:
                if self.ads.is_interstitial_loaded():
                    self.ads.show_interstitial()
                else:
                    # Hazır deyilsə, bir daha request et
                    self.ads.request_interstitial()
            except Exception:
                pass

    def show_game_over(self):
        # Game Over yazıları
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0, 1)
            go_label = CoreLabel(text="GAME OVER", font_size=48)
            go_label.refresh()
            Rectangle(texture=go_label.texture,
                      pos=(Window.width/2 - go_label.texture.size[0]/2, Window.height/2 + 40),
                      size=go_label.texture.size)

            Color(1, 1, 1, 1)
            score_label = CoreLabel(text=f"Final Score: {self.score}", font_size=28)
            score_label.refresh()
            Rectangle(texture=score_label.texture,
                      pos=(Window.width/2 - score_label.texture.size[0]/2, Window.height/2 - 10),
                      size=score_label.texture.size)

            tip_label = CoreLabel(text="Press R to Restart", font_size=22)
            tip_label.refresh()
            Rectangle(texture=tip_label.texture,
                      pos=(Window.width/2 - tip_label.texture.size[0]/2, Window.height/2 - 50),
                      size=tip_label.texture.size)

        # Rewarded reklamı göstər (yüklənmişsə)
        try:
            self.ads.show_rewarded_ad()
        except Exception:
            # Əgər hazır deyilsə, sonrakı oyuna hazır olsun
            try:
                self.ads.load_rewarded_ad(REWARDED_ID)
            except Exception:
                pass

    # Rewarded listener (opsional)
    def on_rewarded_event(self, event_name=None, *args, **kwargs):
        # Burada event-ləri izləyə bilərik (məsələn, 'rewarded', 'closed', 'failed' və s.)
        # İstəsən, burada oyunda bonus verə bilərik (məs: 1 can)
        # İndi sadəcə logika sadə saxlanır.
        if event_name == 'rewarded':
            # Bonus verə bilərsən, misal üçün 1 yem əlavə et
            self.score += 1
        elif event_name == 'closed':
            # Bağlandıqdan sonra növbəti üçün preload et
            try:
                self.ads.load_rewarded_ad(REWARDED_ID)
            except Exception:
                pass

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == "__main__":
    SnakeApp().run()
