import curses
from os import listdir
import sys
import csv
import pathlib

import subprocess

title = "      /\\     /\\ \n     {  `---'  }\n     {  O   O  }\n╭────╮╭─╮╭─╮╭────╮╭────╮╭─╮\n│ ╭╮ ││ ││ ││ ╭╮ ││ ╭╮ ││ ╰─╮\n│ ╰╯ ││ ╰╯ ││ ╰╯ ││ ╰╯ ││ ╭─╯\n│ ╭──╯╰──╮ ││ ╭──╯│ ╭──╯│ │\n│ │   ╭──╯ ││ │   │ ╰──╮│ │\n╰─╯   ╰────╯╰─╯   ╰────╯╰─╯\n"

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.clear()
    
    main_menu_opciones = ["Nueva mascota", "Cargar mascota guardada", "Salir"]
    main_menu_seleccion = 0
    
    while True:
        stdscr.clear()
        stdscr.addstr(1, 0, title)
        for i, option in enumerate(main_menu_opciones):
            if i == main_menu_seleccion:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and main_menu_seleccion > 0:
            main_menu_seleccion -= 1
        elif key == curses.KEY_DOWN and main_menu_seleccion < len(main_menu_opciones) - 1:
            main_menu_seleccion += 1
        elif key == ord("\n"):  # enter
            if main_menu_seleccion == 0:
                new_pet(stdscr)
                stdscr.getch()
            elif main_menu_seleccion == 1:
                load_pet_menu(stdscr)
            elif main_menu_seleccion == 2:
                break

def new_pet(stdscr):

    stdscr.clear()
    stdscr.addstr(1, 0, title)
    stdscr.addstr("> Elige un nombre:")
    stdscr.refresh()

    curses.echo()
    name = stdscr.getstr(10,19,20).decode('utf-8')
    curses.noecho()

    create_pet(name)
    load_pet(name)



def load_pet_menu(stdscr):
    stdscr.clear()
    stdscr.refresh()

    save_dir = pathlib.Path("./save/")
    pets_saves = [file for file in save_dir.iterdir() if file.is_file()]
    for i in range(len(pets_saves)):
        pets_saves[i] = pets_saves[i].stem
    pets_list_options = ["Back"]
    pets_list_options += pets_saves
    pets_list_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 0, title)
        stdscr.addstr("Elige tu mascota:\n")

        # print options
        for save, option in enumerate(pets_list_options):
            if save == pets_list_selection:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {option}\n")

        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_UP and pets_list_selection > 0:
            pets_list_selection -= 1
        elif key == curses.KEY_DOWN and pets_list_selection < len(pets_list_options) - 1:
            pets_list_selection += 1
        elif key == ord("\n"):  # enter
            if pets_list_selection == 0:
                break
            else:
                load_pet(pets_list_options[pets_list_selection])
                stdscr.getch()
                break

def load_pet(name):
    subprocess.run(f"python3 pet.py -n {name}", shell=True)
    sys.exit()

def create_pet(name):
    # initial stats
    data = [
            ["name", "health", "hunger"],
            [name, 75, 15]
    ]

    path = f"./save/{name}.csv"

    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    curses.wrapper(main)
