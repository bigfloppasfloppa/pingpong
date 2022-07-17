# 1. подключение библиотек и модулей
from pygame import *
from random import *
import time as t # t - time из питона, а time - time из pygame

# 2. создание классов
# есть уже готовый основной класс для игровых спрайтов, и мы наследуем от него
class GameSprite(sprite.Sprite):
    def __init__(self, xcor, ycor, width, height, speed, player_image):
        super().__init__()
        # трансформируем картинку спрайта под его размеры
        self.image = transform.scale(image.load(player_image), (width, height))
        # получаем хитбокс по картинке
        self.rect = self.image.get_rect()
        self.rect.x = xcor
        self.rect.y = ycor
        self.speed = speed

    # метод обновления спрайта
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):

    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

# 3. создание переменных и объектов
win_height = 500
win_width = 700
background = transform.scale(image.load("media/background.jpg"), (win_width, win_height))
window = display.set_mode((win_width, win_height))
window.blit(background, (0,0))

racket_left_image = "media/floppa.jpg"
racket_right_image = "media/chmonya.jpg"
ball_image = "media/pelmen.jpg"

timer = time.Clock()

mixer.init()
mixer.music.load("media/music.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(loops=-1)
border_sound = mixer.Sound("media/border_sound.mp3")
racket_sound = mixer.Sound("media/racket_sound.mp3")
end_sound = mixer.Sound("media/end_sound.mp3")

font.init()
game_font = font.SysFont('Times New Roman', 36)
lose_left = game_font.render('Шлёпа проиграл. Перезагрузка...', True, (180, 0, 0))
lose_right = game_font.render('Чмоня проиграл. Перезагрузка...', True, (180, 0, 0))

game = True # переменная, отвечающая за работу окна
finish = False # переменная, отвечающая за окончание игры в окне
# скорости мяча
ball_speed_x = randint(-10,10)
ball_speed_y = randint(-10,10)

# 4. создание объектов классов
# координаты (х и у), размеры (ширина, высота), скорость, картинка
ball = GameSprite(350, 250, 50, 50, 5, ball_image)
left_racket = Player(30, 200, 50, 150, 5, racket_left_image)
right_racket = Player(620, 200, 50, 150, 5, racket_right_image)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0,0))

        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y
        left_racket.update_left()
        right_racket.update_right()

        # обработка столкновений
        if ball.rect.y < 5 or ball.rect.y > win_height - 50:
            ball_speed_y *= -1
            border_sound.play()

        if sprite.collide_rect(ball, left_racket) or sprite.collide_rect(ball, right_racket):
            for e in event.get():
                if e.type == KEYDOWN:
                    # прогрессивная физика в разработке :)
                    if e.key == K_w or e.key == K_UP:
                        ball_speed_x *= -1
                    elif e.key == K_s or e.key == K_DOWN:
                        ball_speed_x *= -1
                    else:
                        ball_speed_x *= -1

            racket_sound.play()

        # победа и проигрыш
        if ball.rect.x < left_racket.rect.x:
            window.blit(lose_left, (100, 10))
            end_sound.play()
            finish = True

        if ball.rect.x > right_racket.rect.x:
            window.blit(lose_right, (100, 10))
            end_sound.play()
            finish = True

        ball.reset()
        left_racket.reset()
        right_racket.reset()
    else:
        # перезапуск игры
        t.sleep(5)
        finish = False
        ball.kill()
        ball_speed_x = randint(-10,10)
        ball_speed_y = randint(-10,10)
        ball = GameSprite(350, 250, 50, 50, 5, ball_image)

    display.update()
    timer.tick(120)