from PIL import Image, ImageSequence
import pygame as pg
import random
import os

GIF_PATHS = ["dancingbaby.gif", "calamardo.gif", "calamardo_anim.gif"
            ]
GIF_DELAYS = [50, 50, 20]
FPS = 60

class AnimatedGIF:
    def __init__(self, path, position, velocity, frame_delay):
        self.frames = []
        self.load_gif(path)
        self.index = 0
        self.timer = 0
        self.frame_delay = frame_delay 
        self.rect = self.frames[0].get_rect(topleft = position)
        self.velocity = velocity

    def load_gif(self, path):
        pil_gif = Image.open(path)
        for frame in ImageSequence.Iterator(pil_gif):
            frame = frame.convert("RGBA")
            pg_image = pg.image.fromstring(frame.tobytes(), 
                                           frame.size, "RGBA")
            self.frames.append(pg_image)

    def update(self, dt, WIDTH, HEIGHT):
        self.timer += dt
        if self.timer >= self.frame_delay:
            self.index = (self.index + 1) % len(self.frames)
            self.timer = 0
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.left <= 0:
            self.rect.x -= 2*self.rect.left
            self.velocity[0] *= -1
        elif self.rect.right >= WIDTH:
            self.rect.x += 2*(WIDTH - self.rect.right)
            self.velocity[0] *= -1
        if self.rect.top <= 0:
            self.rect.y -= 2*self.rect.top
            self.velocity[1] *= -1
        elif self.rect.bottom >= HEIGHT:
            self.rect.y += 2*(HEIGHT - self.rect.bottom)
            self.velocity[1] *= -1

    def draw(self, surface):
        surface.blit(self.frames[self.index], self.rect)

def toggle_fullscreen(is_fullscreen, WIDTH, HEIGHT):
    if is_fullscreen:
        screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode((WIDTH, HEIGHT))

def main():
    pg.init()
    info = pg.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h

    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    clock = pg.time.Clock()
    running = True

    gifs = []
    for i,path in enumerate(GIF_PATHS):
        x = random.randint(200, WIDTH - 200)
        y = random.randint(200, HEIGHT - 200)
        dx, dy = random.random()*6-3,  random.choice([-3, 3])
        gifs.append(AnimatedGIF(path, (x,y), [dx,dy], GIF_DELAYS[i]))

    vivalinux_img = pg.image.load("vivalinux.jpg").convert()
    blink_on = 10
    blink_off = 50
    vivalinux_timer = 0
    modo_vivalinux = False
    show_image = False 

    party_mode = False
    background_color = (0,0,0)

    while running:
        dt = clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_p:
                    party_mode = not party_mode
                elif event.key == pg.K_f:
                    is_fullscreen = not is_fullscreen
                    toggle_fullscreen(is_fullscreen, WIDTH, HEIGHT)
                elif event.key == pg.K_l:
                    modo_vivalinux = not modo_vivalinux 
                    show_image = False

        if modo_vivalinux:
            vivalinux_timer += dt
            if show_image:
                if vivalinux_timer >= blink_on:
                    show_image = not show_image
                    vivalinux_timer = 0 
            else:
                if vivalinux_timer >= blink_off:
                    show_image = not show_image
                    vivalinux_timer = 0 

        
        if party_mode:
            background_color = [random.randint(0, 255)
                                for _ in range(3)]
        else:
            background_color = (0,0,0)

        screen.fill(background_color)

        for gif in gifs:
            gif.update(dt, WIDTH, HEIGHT)
            gif.draw(screen)
        
        if show_image:
            screen.blit(vivalinux_img,
                        (
                            WIDTH // 2 - vivalinux_img.get_width() // 2,
                            HEIGHT // 2 - vivalinux_img.get_height() // 2,
                       )
                    )

        pg.display.flip()
    pg.quit()


if __name__ == "__main__":
    for path in GIF_PATHS:
        if not os.path.exists(path):
            print(f"Falta el archivo: {path}")
            exit(1)
    main()
