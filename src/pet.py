import curses
import textwrap
import time
import sys
from ascii.cat.cat import ascii as animation

animation_fps = 1

class Pet:
    def __init__(self, nombre):
        self.frame_counter = 0

        self.nombre = nombre
        self.salud = 100
        self.hambre = 0
        self._last_update = time.time()
        self._last_frame_time = time.time()

    def process(self):
        now = time.time()
        delta_time = now - self._last_update
        self._last_update = now

        self.hambre += 0.03
        self.salud -= 0.01

        self.hambre = max(0, min(100, self.hambre))
        self.salud = max(0, min(100, self.salud))

        # TODO - morir, etc

    def alimentar(self):
        self.hambre -= 10
        self.salud += 5

    def jugar(self):
        self.hambre += 5
        self.salud += 10

    def _aumentar_hambre(self):
        time.sleep(5)
        self.hambre += 5


#    def mostrar_estado(self):
#        return f"{self.nombre}:\nSalud: {round(self.salud)}/100\nHambre: {round(self.hambre)}/100"

def render(stdscr, pet):
    """muestra el estado"""
    stdscr.clear()
    # obtener el tamaño de la ventana
    height, width = stdscr.getmaxyx()
    
    # mostrar el estado del Tamagotchi
    stdscr.addstr(0, 0, f"{pet.nombre}:\nSalud: {round(pet.salud)}/100\nHambre: {round(pet.hambre)}/100")

    # mostrar animacion del bicho
    animation_handler(stdscr, animation, animation_fps, pet)
              
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
        exit_game()
    elif key == ord('a'):
        pet.alimentar()
    elif key == ord('j'):
        pet.jugar()

    render(stdscr, pet)

    return True

def exit_game(pet=None):
    """guarda el estado y sale del programa"""
    if pet:
        save()
    sys.exit()

def save():
    # todo - guardar estado
    pass

def main(stdscr):
    # todo - cargar estado
    pet = Pet("Tama")
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
