import tkinter as tk
import random
from random import choice
from time import sleep
from turtle import *
import pygame
import subprocess
import time
from freegames import floor, square, vector
def coloraleat():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color_hex
def cambiarcolor():
    nuevo_color = coloraleat()
    app.configure(background=nuevo_color)

def eleccion(boton_enter):
    if comando.get() == "multiplayer_match":
        puntuaciones()
    elif comando.get() == "color":
        boton_color()
    elif comando.get() == "symon":
        simonsays()

def puntuaciones():
    etiqueta1 = tk.Label(app, text="Jugador 1")
    etiqueta1.place(x=10, y=10)
    entrada1 = tk.Entry(app)
    entrada1.place(x=100, y=10)
    etiqueta2 = tk.Label(app, text="Jugador 2")
    etiqueta2.place(x=10, y=40)
    entrada2 = tk.Entry(app)
    entrada2.place(x=100, y=40)

    etiqueta3 = tk.Label(app, text="Jugador 3")
    etiqueta3.place(x=10, y=70)
    entrada3 = tk.Entry(app)
    entrada3.place(x=100, y=70)
    etiqueta4 = tk.Label(app, text="Jugador 4")
    etiqueta4.place(x=10, y=100)
    entrada4 = tk.Entry(app)
    entrada4.place(x=100, y=100)

def boton_color():
    boton_color = tk.Button(
        app,
        text="CAMBIAR COLOR",
        font=("Double_Struck", 15),
        bg="#00a8e8",
        fg="black",
        command=cambiarcolor
    )
    boton_color.pack(side="top", anchor="ne")

app = tk.Tk()
app.geometry("800x600")
color_fondo_aleatorio = coloraleat()
app.configure(background=color_fondo_aleatorio)
app.title("SYMON SAYS")

etiq = tk.Label(app, text="SYMON SAYS", fg="white", bg="black")
etiq.place(x=375, y=285)

comando = tk.StringVar()
entry = tk.Entry(app, textvariable=comando)
entry.place(x=320, y=310)

boton_enter = tk.Button(
    app,
    text="ENTER",
    font=("Double_Struck", 8),
    bg="white",
    fg="black",
    command=lambda: eleccion(boton_enter)  # Usando una función lambda para pasar el botón
)
boton_enter.place(x=385, y=345)



def simonsays():
    error_image_path = "images/error_image.png"
    # Inicialización de Pygame para reproducir sonidos
    pygame.mixer.init()
    # Carga de los sonidos
    sound_dict = {
        'red': pygame.mixer.Sound("sounds/red_sound.wav"),
        'blue': pygame.mixer.Sound("sounds/blue_sound.wav"),
        'green': pygame.mixer.Sound("sounds/green_sound.wav"),
        'yellow': pygame.mixer.Sound("sounds/yellow_sound.wav"),
        'error': pygame.mixer.Sound("sounds/error_sound.wav"),
    }
    pattern = []
    guesses = []
    tiles = {
        vector(0, 0): ('red', 'dark red'),
        vector(0, -200): ('blue', 'dark blue'),
        vector(-200, 0): ('green', 'dark green'),
        vector(-200, -200): ('yellow', 'khaki'),
    }
    def grid():
        """Draw grid of tiles."""
        square(0, 0, 200, 'dark red')
        square(0, -200, 200, 'dark blue')
        square(-200, 0, 200, 'dark green')
        square(-200, -200, 200, 'khaki')
        update()

    def flash(tile):
        """Flash tile in grid."""
        color, _ = tiles[tile]
        sound_dict[color].play()  # Reproduce el sonido asociado al color
        square(tile.x, tile.y, 200, color)
        update()
        sleep(0.5)
        if color == 'yellow':
            square(tile.x, tile.y, 200, 'khaki')
        else:
            square(tile.x, tile.y, 200, 'dark ' + color)
        update()
        sleep(0.5)

    def grow():
        """Grow pattern and flash tiles."""
        tile = choice(list(tiles))
        pattern.append(tile)

        for tile in pattern:
            flash(tile)

        print('Pattern length:', len(pattern))
        guesses.clear()
    def tap(x, y):
        """Respond to screen tap."""
        onscreenclick(None)
        x = floor(x, 200)
        y = floor(y, 200)
        tile = vector(x, y)
        index = len(guesses)

        if tile not in tiles:  # Verifica si el clic está fuera de las áreas coloreadas
            onscreenclick(tap)  # Vuelve a habilitar el clic en la pantalla
            return

        if tile != pattern[index]:
            sound_dict['error'].play()  # Reproduce el sonido de error
            show_error_image()  # Muestra la imagen de error y cierra las ventanas después de 2 segundos
            return

        guesses.append(tile)
        flash(tile)

        if len(guesses) == len(pattern):
            grow()

        onscreenclick(tap)
    def start(x, y):
        """Start game."""
        grow()
        onscreenclick(tap)

    def show_error_image():
        """Mostrar la imagen de error en la aplicación predeterminada."""
        # Abrir la imagen en una ventana independiente
        subprocess.Popen(["open", error_image_path])

        # Esperar un tiempo antes de cerrar las ventanas
        time.sleep(2)  # Espera 2 segundos

        # Cerrar la ventana principal
        bye()

    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    grid()
    onscreenclick(start)
    done()

app.mainloop()