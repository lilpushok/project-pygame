import os
import random
import pygame
pygame.init()
pygame.mixer.music.load('фон.mp3')
pygame.mixer.music.play(-1)

def game():
    lvl = 1

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        image = image.convert_alpha()

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image

    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(all_sprites)
            self.add(ball_sprite)
            self.image = load_image('myball.png')
            self.rect = self.image.get_rect()
            self.rect.x = 660
            self.rect.y = 607
            self.vx = 0
            self.vy = 0
            self.x_after = -1
            self.coord_x_stick = 680
            self.start = 0
            self.notmove = True
            self.chx = 0
            self.chy = 0
            self.px = -1
            self.py = -1

        def update(self):
            if self.chx != self.px:
                self.px = self.chx
                self.vx = -self.vx
            if self.py != self.chy:
                self.py = self.chy
                self.vy = -self.vy
            if self.notmove and self.start == 1:
                self.vy = -4
                self.vx = 0
                self.notmove = False
            coord_x_ball = self.rect.x + 10
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            if pygame.sprite.spritecollideany(self, stick_group) and self.rect.y < 623 \
                    and not pygame.sprite.spritecollideany(self, vertical_borders) \
                    and not pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
                if self.coord_x_stick > coord_x_ball:
                    if self.coord_x_stick - coord_x_ball < 12:
                        self.vx = 0
                        self.vy = -4
                    elif self.coord_x_stick - coord_x_ball < 22:
                        self.vx = -1
                        self.vy = -3
                    elif self.coord_x_stick - coord_x_ball < 32:
                        self.vx = -2
                        self.vy = -3
                    else:
                        self.vx = -4
                        self.vy = -2
                else:
                    if self.coord_x_stick - coord_x_ball > -6:
                        self.vx = 0
                        self.vy = -4
                    elif self.coord_x_stick - coord_x_ball > -16:
                        self.vx = 1
                        self.vy = -3
                    elif self.coord_x_stick - coord_x_ball > -26:
                        self.vx = 2
                        self.vy = -3
                    else:
                        self.vx = 4
                        self.vy = -2
            self.rect = self.rect.move(self.vx, self.vy)

    class Border(pygame.sprite.Sprite):
        def __init__(self, x1, y1, x2, y2):
            super().__init__(all_sprites)
            if x1 == x2:
                self.add(vertical_borders)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            else:
                self.add(horizontal_borders)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    class Brick(pygame.sprite.Sprite):
        def __init__(self, hp, x, y):
            super().__init__(all_sprites)
            self.sp_colors = ['brick_1.png', 'brick_2.png', 'brick_3.png', 'brick_4.png',
                              'brick_5.png',
                              'brick_6.png', 'brick_7.png', 'brick_8.png', 'brick_9.png',
                              'brick_10.png']
            self.add(brick_group)
            self.image = load_image(self.sp_colors[hp - 1])
            self.rect = self.image.get_rect()
            self.hp = hp
            self.prev = 0
            self.rect.x = x
            self.rect.y = y
            self.x = x + 15
            self.y = y + 15

        def update(self):
            y = ball.rect.y + 15
            x = ball.rect.x + 15
            x1 = self.x - x
            y1 = self.y - y
            if (x1 ** 2 + y1 ** 2) ** 0.5 <= 45 and abs(x1) <= 35 and abs(y1) <= 35:
                if abs(x1) in range(30, 36):
                    ball.chx += 1
                if abs(y1) in range(30, 36):
                    ball.chy += 1
                if self.prev == 0:
                    self.hp -= 1
                    self.prev = 1
                if self.hp != 0:
                    self.image = load_image(self.sp_colors[self.hp - 1])
            if self.prev == 1:
                if not ((x1 ** 2 + y1 ** 2) ** 0.5 <= 45 and abs(x1) <= 35 and abs(y1) <= 35):
                    self.prev = 0
            if self.hp == 0:
                self.kill()
                brick_group.update()

    class Ban(pygame.sprite.Sprite):

        def __init__(self, pos, a):
            super().__init__(all_sprites)
            self.add(pic_sprites)
            self.move = False
            if a == 1:
                self.image = load_image("youlose.png")
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
                self.rect.x = pos[0]
                self.rect.y = pos[1]
                self.x = 1360
            if a == 0:
                self.image = load_image("youwin.png")
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
                self.rect.x = pos[0]
                self.rect.y = pos[1]
                self.x = 1360

        def update(self):
            if self.x > 0 and self.move:
                self.rect = self.rect.move(5, 0)
                self.x -= 5

    if 1:
        all_sprites = pygame.sprite.Group()
        stick_group = pygame.sprite.Group()
        pic_sprites = pygame.sprite.Group()
        ball_sprite = pygame.sprite.Group()
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()
        brick_group = pygame.sprite.Group()

        size = width, height = 1360, 710
        screen = pygame.display.set_mode(size)

        Border(0, 0, width, 0)
        Border(0, 0, 0, height)
        Border(width, 0, width, height)

        pict1 = Ban([-1359, 0], 1)

        stick_sprite = pygame.sprite.Sprite(stick_group)

        stick_image = load_image('stick.png')
        stick_sprite.image = stick_image
        stick_sprite.rect = stick_sprite.image.get_rect()
        stick_sprite.rect.x = 634
        stick_sprite.rect.y = 640
        stick_group.draw(screen)
        start = False
        ball = Ball()
        t1 = 0

    def generate():
        if lvl == 1:
            for i in range(12):
                for o in range(4):
                    Brick(1, 244 + 32 * o, 32 + 32 * i)
                    Brick(1, 988 + 32 * o, 32 + 32 * i)

            for i in range(11):
                for o in range(4):
                    Brick(1, 616 + 32 * o, 64 + 32 * i)

        if lvl == 2:
            for i in range(12):
                for o in range(1, 15):
                    if o == 7 or o == 8:
                        Brick(2, o * 88, 32 + 32 * i)
                    else:
                        Brick(1, o * 88, 32 + 32 * i)

        elif lvl == 3:
            for o in range(6):
                for i in range(2 + o):
                    Brick(2, 120 + i * 32, 242 + 32 * o)
                    Brick(2, 1208 - i * 32, 242 + 32 * o)
                for i in range(7 - o):
                    Brick(3, 120 + i * 32, 50 + 32 * o)
                    Brick(3, 1208 - i * 32, 50 + 32 * o)
                for i in range(2 + 2 * o):
                    Brick(1, 436 + i * 32 - 32 * o, 50 + 32 * o)
                    Brick(3, 436 + i * 32 - 32 * o, 402 - 32 * o)
                    Brick(1, 856 + i * 32 - 32 * o, 50 + 32 * o)
                    Brick(3, 856 + i * 32 - 32 * o, 402 - 32 * o)
            for o in range(3):
                for i in range(5 - 2 * o):
                    Brick(2, 600 + i * 32 + 32 * o, 50 + 32 * o)

        elif lvl == 4:
            t = 152
            r = 402
            # snake
            Brick(4, t - 32, 82)
            for i in range(1, 18):
                for o in range(11 - i // 2):
                    Brick(2, t + (i - 1) * 64, r - o * 32)
                    if o == 0 and i % 2 == 1:
                        Brick(4, t + 32 + (i - 1) * 64, r - o * 32)
                    elif o == 10 - i // 2 and i % 2 == 0:
                        Brick(4, t + 32 + (i - 1) * 64, r - o * 32)
            # sun
            for i in range(5):
                for o in range(7 - i):
                    Brick(5, 1208 - o * 32, 50 + i * 32)
            Brick(5, 952, 50)
            Brick(5, 920, 50)
            Brick(5, 984, 146)
            Brick(5, 1080, 178)
            Brick(5, 1016, 114)
            Brick(5, 1048, 210)
            Brick(5, 1176, 242)

        elif lvl == 5:
            def glade(t, r, q):
                for o in range(3):
                    for i in range(3):
                        Brick(q, t + i * 32, r + 256 + o * 32)
                        if o != 2 or i != 0:
                            Brick(q, t + 64 + i * 32, r + 192 + o * 32)
                            Brick(q, t + 128 + i * 32, r + 128 + o * 32)
                            Brick(q, t + 192 + i * 32, r + 64 + o * 32)
                            Brick(q, t + 256 + i * 32, r + o * 32)

            glade(120, 100, 4)
            glade(372, 100, 2)
            glade(632, 100, 2)
            glade(888, 100, 4)

            for o in range(3):
                for i in range(3):
                    if i == o and i == 1:
                        Brick(4, 120 + 32 * o, 100 + i * 32)
                        Brick(4, 1144 + o * 32, 356 + i * 32)
                    else:
                        Brick(1, 120 + 32 * o, 100 + i * 32)
                        Brick(1, 1144 + 32 * o, 356 + i * 32)

        elif lvl == 6:
            def logo(t, r):
                Brick(5, t + 224, r + 160)
                Brick(2, t + 192, r)
                Brick(2, t + 224, r + 32)
                for i in range(6):
                    Brick(2, t + i * 32, r)
                for i in range(-1, 6):
                    for o in range(1, 3):
                        if i == 1 and o == 1:
                            Brick(6, t + i * 32, r + o * 32)
                        else:
                            Brick(2, t + i * 32, r + o * 32)
                for i in range(-1, 6):
                    for o in range(1, 3):
                        Brick(2, t + i * 32, r + 96 + o * 32)
                for i in range(3):
                    Brick(2, t - 64, r + 128 + 32 * i)
                for i in range(2):
                    for o in range(3 + 2 * i):
                        Brick(2, t - 128 + i * 32, r + 192 + 32 * (o - i))
                for i in range(2):
                    for o in range(5 - 2 * i):
                        Brick(2, t + 192 + i * 32, r + 32 + (o + i) * 32)
                        Brick(5, t + 256 + i * 32, r + 64 + (o + i) * 32)
                for i in range(-1, 8):
                    for o in range(1, 3):
                        Brick(5, t + i * 32, r + 160 + o * 32)
                for i in range(2):
                    for o in range(4):
                        Brick(5, t - 64 + i * 32, r + 224 + (o + i) * 32)
                for i in range(4):
                    for o in range(3):
                        Brick(5, t + i * 32, r + 288 + o * 32)
                for i in range(3):
                    for o in range(3):
                        if i == 0 and o == 1:
                            Brick(4, t + 128 + i * 32, r + 288 + o * 32)
                        elif i == 2 and o == 2:
                            pass
                        else:
                            Brick(5, t + 128 + i * 32, r + 288 + o * 32)

            logo(200, 50)
            logo(940, 50)

        elif lvl == 7:
            def ladder(t, r, q):
                for i in range(12):
                    for o in range(2):
                        if i > 6:
                            Brick(q, t + (o + i - 7) * 32, r + 64 + i * 32)
                        else:
                            Brick(q, t + (o + i) * 32, r + 256 - i * 32)

            for i in range(7):
                ladder(70 + i * 160, 50, random.randint(1, 5))

        elif lvl == 8:
            r = 82
            t = 100
            # P
            for i in range(1, 4):
                Brick(1, t + 128, r + i * 32)
            for i in range(2):
                Brick(1, t + 64 + i * 32, r)
                Brick(1, t + 64 + i * 32, r + 128)
            for i in range(10):
                Brick(1, t, r + i * 32)
                Brick(1, t + 32, r + i * 32)
            # Y
            Brick(5, t + 224, 338)
            for i in range(2):
                for o in range(9):
                    Brick(5, t + 320 + i * 32, r + o * 32)
            for i in range(3):
                Brick(5, t + 256 + i * 32, 370)
            for i in range(2):
                Brick(5, t + 256 + i * 32, 274)
            for i in range(6):
                Brick(5, t + 224, 242 - i * 32)
            # T
            for i in range(5):
                Brick(4, t + 416 + i * 32, 82)
                Brick(4, t + 416 + i * 32, 114)
            for i in range(1, 9):
                Brick(4, t + 480, 114 + i * 32)
                # H
            for i in range(10):
                Brick(1, t + 640, r + i * 32)
                Brick(1, t + 608, r + i * 32)
                Brick(1, t + 736, r + i * 32)
            for i in range(2):
                Brick(1, t + 672 + i * 32, 274)
            # O
            for i in range(8):
                Brick(3, t + 800, r + 32 + i * 32)
                Brick(3, t + 832, r + 32 + i * 32)
                Brick(3, t + 928, r + 32 + i * 32)
            for i in range(3):
                Brick(3, t + 832 + i * 32, r)
                Brick(3, t + 832 + i * 32, r + 288)
            # N
            for i in range(10):
                Brick(2, t + 992, r + i * 32)
                Brick(2, t + 1120, r + i * 32)
            for i in range(3):
                for o in range(4):
                    Brick(2, t + 1024 + i * 32, r + 32 + (o + 2 * i) * 32)

        elif lvl == 9:
            def flower(t, r):
                Brick(random.randint(4, 5), 96 + t, 96 + r)
                for o in range(3):
                    for i in range(3):
                        if o != 0 or i != 0:
                            Brick(1, t + i * 32, r + o * 32)
                        if o != 2 or i != 0:
                            Brick(1, t + i * 32, 128 + r + o * 32)
                        if o != 0 or i != 2:
                            Brick(1, 128 + t + i * 32, r + o * 32)
                        if o != 2 or i != 2:
                            Brick(1, 128 + t + i * 32, 128 + r + o * 32)

            flower(120, 50)
            flower(1048, 50)
            flower(600, 178)

            for i in range(11):
                Brick(3, 792 + i * 32, 50 + i * 32)
                if random.randint(1, 2) == 1:
                    Brick(3, 792 + i * 32, 18 + i * 32)
                else:
                    Brick(3, 792 + i * 32, 82 + i * 32)
            for i in range(6):
                Brick(3, 600 + i * 32, 50)
            for i in range(11):
                Brick(3, 248 + i * 32, 370 - i * 32)
                if random.randint(1, 2) == 1:
                    Brick(3, 248 + i * 32, 338 - i * 32)
                else:
                    Brick(3, 248 + i * 32, 402 - i * 32)

        elif lvl == 10:
            def puzzle(t, r, q):
                for i in range(6):
                    for o in range(2):
                        Brick(q, t + i * 32, r + o * 32)
                        Brick(q, t + (i + 1) * 32, r + 64 + o * 32)
                        if o == 1 and (i == 3 or i == 2):
                            Brick(q, t + i * 32, r - 64 + o * 32)
                        else:
                            Brick(q, t + i * 32, r + 128 + o * 32)

            for i in range(6):
                for o in range(2):
                    puzzle(100 + 192 * i, 50 + 192 * o, random.randint(1, 6))

        elif lvl == 11:
            # K
            for i in range(11):
                Brick(10, 88, 48 + i * 32)
            Brick(10, 120, 208)
            for i in range(1, 6):
                Brick(10, 120 + i * 32, 208 + i * 32)
                Brick(10, 120 + i * 32, 208 - i * 32)
                # I
            for i in range(7):
                Brick(10, 376 + i * 32, 48)
                Brick(10, 376 + i * 32, 368)
            for i in range(1, 10):
                Brick(10, 472, 48 + i * 32)
            # N
            for i in range(11):
                Brick(10, 664, 48 + i * 32)
                Brick(10, 856, 48 + i * 32)
            for i in range(9):
                Brick(10, 696 + i * 16, 80 + i * 32)
                # G
            for i in range(2, 9):
                Brick(10, 950, 48 + i * 32)
            for i in range(1, 3):
                Brick(10, 950 + i * 32, 112 - i * 32)
                Brick(10, 950 + i * 32, 304 + i * 32)
            for i in range(1, 4):
                Brick(10, 1014 + i * 32, 368)
                Brick(10, 1014 + i * 32, 48)
            Brick(10, 1142, 80)
            for i in range(5):
                Brick(10, 1142, 368 - i * 32)
            for i in range(2):
                Brick(10, 1142 - (i + 1) * 32, 240)
        brick_group.draw(screen)

    generate()
    q = 0
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    a = 0
    fps = 120

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and t1 == 0:
                start = 1
            if event.type == pygame.MOUSEBUTTONUP and t1 == 0:
                ball.start = 1
                t1 = 1
            if event.type == pygame.MOUSEMOTION and start == 1:
                if event.pos[0] < 45:
                    stick_sprite.rect.x = 0 + q
                elif event.pos[0] > 1320:
                    stick_sprite.rect.x = 1290 + q
                else:
                    stick_sprite.rect.x = event.pos[0] - 45 + q
                stick_sprite.rect.y = 640
                ball.coord_x_stick = stick_sprite.rect.x + 40
        screen.fill((30, 25, 40))
        if lvl == 12:
            win_group = pygame.sprite.Group()
            win_sprite = pygame.sprite.Sprite(win_group)
            win_image = load_image('youwin.png')
            win_sprite.image = win_image
            win_sprite.rect = win_sprite.image.get_rect()
            win_sprite.rect.x = 0
            win_sprite.rect.y = 0
            win_group.draw(screen)

        else:
            brick_group.update()
            ball_sprite.update()
            if len(brick_group.sprites()) == 0:
                lvl += 1
                ball.kill()
                t1 = 0
                start = 0
                ball = Ball()
                if lvl != 12:
                    generate()
            if ball.rect.y > 615:
                q = 2000
                pict1.move = True
                if a == 0:
                    a = 1
                pic_sprites.draw(screen)
                pict1.update()
                if pict1.rect.x >= 0:
                    game()
                    break
            else:
                stick_group.draw(screen)
                brick_group.draw(screen)
                ball_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

game()