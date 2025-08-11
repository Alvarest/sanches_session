import arcade
import random
import os

GIF_PATHS = ["dancingbaby.gif", "calamardo.gif", "calamardo_anim.gif"
            ]
GIF_DELAYS = [50, 50, 20]
FPS = 60
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
SCREEN_TITLE = "Background"

class AnimatedGIF(arcade.Sprite):
    def __init__(self, gif_path):
        super().__init__()
        self.textures = arcade.load_animated_gif(gif_path)
        self.center_x = random.randint(200, SCREEN_WIDTH - 200)
        self.center_y = random.randint(200, SCREEN_WIDTH - 200)
        self.vel_x = random.random() * 6 - 3
        self.vel_y = random.random() * 6 - 3

    def update(self):
        super().update()
        self.center_x *= self.vel_x
        self.center_y += self.vel_y

        if self.left <= 0:
            self.center_x -= 2*self.left
            self.vel_x = -self.vel_x
        elif self.right >= SCREEN_WIDTH:
            self.center_x -= 2*(self.right - SCREEN_WIDTH)
            self.vel_x = -self.vel_x
        if self.bottom <= 0:
            self.center_y -= 2*self.bottom
            self.vel_y = -self.vel_y
        elif self.top >= SCREEN_HEIGHT:
            self.center_y -= 2*(self.top - SCREEN_HEIGHT)
            self.vel_y = -self.vel_y

class BackgroundGame(arcade.View):
    def __init__(self):
        self.sprite_list = arcade.SpriteList()
        self.party_mode = False
        self.vivalinux_mode = False
        self.background_color = arcade.color.BLACK
        self.show_image = False 
        self.time_since_blink = 0

        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = self.get_size()

        self.vivalinux_texture = arcade.load_texture("vivalinux.jpg")
        
    def setup(self):
        for gif_path in GIF_PATHS:
            sprite = AnimatedGIF(gif_path)
            self.sprite_list.append(sprite)
        print("Setup!")

    def on_draw(self):
        self.clear()
        arcade.set_background_color(self.background_color)
        self.sprite_list.draw()

        if self.show_image:
            width = self.vivalinux_texture.width
            height = self.vivalinux_texture.height
            x = SCREEN_WIDTH // 2
            y = SCREEN_HEIGHT // 2
            arcade.draw_scaled_texture_rectangle(
                x, y,
                self.vivalinux_texture,
                scale = self.vivalinux_scale
            )

        def on_update(self, delta_time):
            self.sprite_list.update_animation()
            self.sprite_list.update()

            if vivalinux_mode:
                self.time_since_blink += delta_time
                if self.time_since_blink >= BLINK_INTERVAL:
                    self.show_image = not self.show_image
                    self.time_since_blink = 0

            if self.party_mode:
                self.background_color = (
                        random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255)
                    )
            else:
                self.background_color = arcade.color.BLACK

            print("On_draw!")

        def on_key_press(self, key, modifiers):
            if key == arcade.key.P:
                self.party_mode = not self.party_mode
            elif key == arcade.key.L:
                self.vivalinux_mode = not self.vivalinux_mode
                self.show_image = False
            elif key == arcade.key.F:
                self.set_fullscreen(not self.fullscreen)
                global SCREEN_WIDTH, SCREEN_HEIGHT
                SCREEN_WIDTH, SCREEN_HEIGHT = self.get_size()
            elif key == arcade.key.ESCAPE:
                arcade.close_window()
            print("On_key_press!")

if __name__ == "__main__":
    for gif in set(GIF_PATHS):
        if not os.path.exists(gif):
            print(f"Error: El GIF {gif} no existe.")
            exit(1)
        
    if not os.path.exists("vivalinux.jpg"):
        print(f"Error: No eres un verdadero amante de Linux.")
        exit(1)
    
    window = arcade.Window( title = SCREEN_TITLE,
                         resizable = True)

    window = BackgroundWindow()
    window.setup()
    arcade.run()
