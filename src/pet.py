import curses
from os import name
import textwrap
import time
import sys
from ascii.cat.cat import ascii as animation
import argparse
import csv

animation_fps = 1

parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", type=str, help="name of the pet to load. must be an existing pet")
args = parser.parse_args()

save_name = args.name

class Pet:
    def __init__(self, name, health=100, hunger=0):
        self.name = name
        self.health = health
        self.hunger = hunger

        self.frame_counter = 0

        self._last_update = time.time()
        self._last_frame_time = time.time()

    def process(self):
        now = time.time()
        delta_time = now - self._last_update
        self._last_update = now

        self.hunger += 0.03
        self.health -= 0.01

        self.hunger = max(0, min(100, self.hunger))
        self.health = max(0, min(100, self.health))

        # todo - morir, etc

    def alimentar(self):
        self.hunger -= 10
        self.health += 5

    def jugar(self):
        self.hunger += 5
        self.health += 10

    def _aumentar_hunger(self):
        time.sleep(5)
        self.hunger += 5


#    def mostrar_estado(self):
#        return f"{self.nombre}:\nSalud: {round(self.health)}/100\nHambre: {round(self.hunger)}/100"

def render(stdscr, pet):
    """muestra el estado"""
    # obtener el tamaño de la ventana
    height, width = stdscr.getmaxyx()
    
    # limpiar lineas de estado
    for i in range(3):
        stdscr.addstr(i, 0, " " * (width-1))

    # mostrar el estado del Tamagotchi
    stdscr.addstr(0, 0, f"{pet.name}:\nSalud: {round(pet.health)}/100\nHambre: {round(pet.hunger)}/100")

    # mostrar animacion del bicho
    animation_handler(stdscr, animation, animation_fps, pet)

    for i in range(1, 3):
        if height - i >= 0:
            stdscr.addstr(height - i, 0, " " * (width-1)) 
    # mostrar el mensaje en la parte inferior de la ventana
    tutorial = "'a': alimentar, 'j': jugar, 'q': salir."
    tutorial_wrapped = textwrap.wrap(tutorial, width)
    for i, line in enumerate(reversed(tutorial_wrapped)):
        line_position = height - 1 - i
        if line_position >= 0:
            stdscr.addstr(line_position, 0, line)
        else:
            break

def animation_handler(stdscr, ascii, fps, pet):
    height, width = stdscr.getmaxyx()

    current_time = time.time()
    if current_time - pet._last_frame_time >= animation_fps:
        pet.frame_counter += 1
        pet._last_frame_time = current_time

    animation_frames = ascii.split("split")
    current_frame = pet.frame_counter % len(animation_frames)
    frame = animation_frames[current_frame]

    lines = frame.splitlines()

    for i, line in enumerate(lines):
        y_pos = 3 + i
        if y_pos < height - 1:
            line = line[:width-1]
            try:
                stdscr.addstr(y_pos, 0, line)
            except curses.error:
                pass

    stdscr.refresh()

def input_handler(stdscr, pet):
    """gestiona los inputs"""

    key = stdscr.getch()
    if key == ord('q'):
        exit_game(pet)
    elif key == ord('a'):
        pet.alimentar()
    elif key == ord('j'):
        pet.jugar()

    render(stdscr, pet)

    return True

def exit_game(pet=None):
    """guarda el estado y sale del programa"""
    if pet:
        save(pet)
    sys.exit()

def save(pet):
    data = [
            ["name", "health", "hunger"],
            [pet.name, pet.health, pet.hunger]
    ]

    path = f"./save/{pet.name}.csv"

    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def load_pet(name):
    with open(f"./save/{name}.csv", mode="r") as file:
        pet_csv = csv.reader(file)
        pet_data = list(pet_csv)[-1]

        name, health, hunger = pet_data
        return name, int(float(health)), int(float(hunger))

def main(stdscr):
    name, health, hunger = load_pet(save_name)
    pet = Pet(name, health, hunger)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)
    stdscr.timeout(100)

    running = True

    while True:
        pet.process()
        render(stdscr, pet)

        try:
            running = input_handler(stdscr, pet)
            if not running:
                break
        except curses.error:
            pass

        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
