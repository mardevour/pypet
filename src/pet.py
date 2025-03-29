import curses
import textwrap
import time
import sys

class Pet:
    def __init__(self, nombre):
        self.nombre = nombre
        self.salud = 100
        self.hambre = 0
        self._last_update = time.time()

    def process(self):
        now = time.time()
        delta_time = now - self._last_update
        self._last_update = now

        self.hambre += 0.03
        self.salud -= 0.01

        self.hambre = max(0, min(100, self.hambre))
        self.salud = max(0, min(100, self.salud))

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

    # mostrar bicho
    with open("./ascii/cat/cat.txt", "r", encoding="utf-8") as ascii:
        bicho = ascii.read()
        
    stdscr.addstr(3, 0, bicho)
    
    # mostrar el mensaje en la parte inferior de la ventana
    tutorial = "'a': alimentar, 'j': jugar, 'q': salir."
    tutorial_wrapped = textwrap.wrap(tutorial, width)
    for i, line in enumerate(reversed(tutorial_wrapped)):
        line_position = height - 1 - i
        if line_position >= 0:
            stdscr.addstr(line_position, 0, line)
        else:
            break

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

def exit_game():
    save()
    sys.exit()

def save():
    pass

def main(stdscr):
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
        except curses.error:
            pass

        time.sleep(0.1)

        # esperar input 
#        key = stdscr.getch()
#        if key == ord('q'):
#            break
#        elif key == ord('a'):
#            tama.alimentar()
#        elif key == ord('j'):
#            tama.jugar()

if __name__ == "__main__":
    curses.wrapper(main)
