import play
import pygame
from random import choice

# Oyun Ayarları
FRAMES = 45
BALL_SPEED = 35
PLATFORM_SPEED = 20

# Ses Ayarları
pygame.mixer.init()
ses = pygame.mixer.Sound("coin.wav")

# Metinler
lose = play.new_text(words='KAYBETTİNİZ', font_size=100, color='red')
win = play.new_text(words='KAZANDINIZ', font_size=100, color='yellow')

# Top ve Platform
player = play.new_circle(color="green", y=-150, radius=15, angle=45)
platform = play.new_box(color="brown", y=-250, width=150, height=15)

# Skor
skor_yazi = play.new_text(words="Skor = ", x=330, y=-270, font_size=30)
skor = play.new_text(words="0", x=380, y=-270, font_size=30)

# Tuğla Listesi
tugla_listesi = []

def create_bricks():
    """Tuğlaları oluşturur."""
    tugla_x = play.screen.left + 75  # x ekseni yatay eksen sağ ve sola hareket için kullanılır  210
    tugla_y = play.screen.top - 50   # y ekseni dikey eksen yukarı ve aşagı hareket

    colors = ["purple", "pink", "blue", "orange"]
    
    for _ in range(3):
        for _ in range(7):
            tugla = play.new_box(color=choice(colors), x=tugla_x, y=tugla_y,
                                 width=110, height=30, border_color="black", border_width=1)
            tugla_listesi.append(tugla)  #aapend=eklemek 
            tugla_x = tugla_x + tugla.width #satır satır ilerleniyor o yüzden tüzden x ekseni
 
        tugla_x = play.screen.left + 75
        tugla_y = tugla.y - tugla.height

@play.when_program_starts
def start():
    """Oyunu başlatır."""
    lose.hide()
    win.hide()
    create_bricks()

    platform.start_physics(stable=True, obeys_gravity=False, can_move=True)
    player.start_physics(x_speed=BALL_SPEED, y_speed=BALL_SPEED, obeys_gravity=False)


@play.repeat_forever
async def game():
    """Ana oyun döngüsü."""
    s = int(skor.words)
    
    # Platform Hareketi
    if play.key_is_pressed("right", 'a'):
        platform.physics.x_speed = PLATFORM_SPEED
    elif play.key_is_pressed("left",'d'):
        platform.physics.x_speed = -PLATFORM_SPEED
    else:
        platform.physics.x_speed = 0

    # Tuğlaların Yok Olması
    for t in tugla_listesi[:]:
        if t.is_touching(player):
            player.physics.x_speed *= -1
            player.physics.y_speed *= -1
            t.hide()
            tugla_listesi.remove(t)
            s += 1
            skor.words = str(s)
            ses.play()
    
    # Kaybetme
    if player.y <= platform.y:
        lose.show()
        player.physics.x_speed = 0
        player.physics.y_speed = 0

    # Kazanma
    if not tugla_listesi:
        win.show()
        player.physics.x_speed = 0
        player.physics.y_speed = 0

    await play.timer(seconds=1/FRAMES)


play.start_program()

