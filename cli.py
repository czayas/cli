#!/usr/bin/env python3
# Para Python 2, agregar: #-*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Módulo: cli - Version 0.2 - 30/10/2014 (Rev. 19/03/2018)
# Carlos Zayas Guggiari - czayas(at)gmail.com
# python --version : Python 2.7.14 & 3.6.4
# -----------------------------------------------------------------------------

"""Funciones y clases para implementar una interfaz de línea de comandos."""

import os
import sys
try:
    import readline
except ImportError:
    pass


try:
    # DOS, Windows
    import msvcrt
    getkey = msvcrt.getch
except ImportError:
    # Se asume Unix
    import tty
    import termios

    def getkey():
        """Retorna una tecla presionada."""
        archivo = sys.stdin.fileno()
        mode = termios.tcgetattr(archivo)
        try:
            tty.setraw(archivo, termios.TCSANOW)
            caracter = sys.stdin.read(1)
        finally:
            termios.tcsetattr(archivo, termios.TCSANOW, mode)
        return caracter


if os.name == 'nt':
    import ctypes

    class _CursorInfo(ctypes.Structure):
        """Información sobre el cursor de texto."""

        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


def cursoroff():
    """Oculta el cursor."""
    if os.name == 'nt':
        cur = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cur))
        cur.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cur))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def cursoron():
    """Muestra el cursor."""
    if os.name == 'nt':
        cur = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cur))
        cur.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cur))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def clear(linea=100):
    """Borra la pantalla de texto."""
    if os.name == 'posix':
        # Unix, Linux, MacOS, BSD, etc.
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        # DOS, Windows
        os.system('CLS')
    else:
        # Otros sistemas operativos
        out('\n' * linea)


def out(cadena):
    """Envía una cadena a stdout y limpia el buffer (imprime más rápido)."""
    sys.stdout.write(cadena)
    sys.stdout.flush()


# noinspection PyUnusedLocal
def pedir(prompt='> '):
    """Solicita el ingreso de una cadena de caracteres (Python 2 y 3)."""
    cadena = ''
    try:
        cadena = raw_input(prompt)
    except NameError:
        cadena = input(prompt)
    return cadena


class Completador(object):
    """Autocompletado con tabulación."""

    def __init__(self, opciones):
        """Constructor."""
        self.opciones = sorted(opciones)
        self.opc = self.opciones[:]

    def completar(self, texto, estado):
        """Event handler para completer de readline."""
        if estado == 0:
            if texto:
                self.opc = [opc for opc in self.opciones
                            if opc and opc.startswith(texto)]
            else:
                self.opc = self.opciones[:]
        return None if estado >= len(self.opc) else self.opc[estado]


class Prompt(object):
    """Inductor o línea de comandos."""

    def __init__(self, opciones, salir='quit', prompt='> '):
        """Constructor."""
        self.salir = salir
        self.prompt = prompt
        try:
            readline.set_completer(Completador(opciones).completar)
            readline.parse_and_bind('tab: complete')
        except NameError:
            pass

    def ciclo(self):
        """Lectura del REPL (Read-Eval-Print Loop)."""
        linea = ''
        while linea != self.salir:
            try:
                linea = pedir(self.prompt)         # Inductor (Prompt)
                yield linea
            except (KeyboardInterrupt, EOFError):  # Control+D o fin de archivo
                sys.exit(0)                        # Salir sin errores


class Menu(object):
    """Menú de opciones."""

    def __init__(self, opciones):
        """Constructor."""
        self.opciones = opciones
        indice = sorted(opciones)
        for opcion in indice:
            out('{}: {}\n'.format(opcion, opciones[opcion][0]))

    def pedir(self, mensaje='', tecla=False):
        """Pedir una opción por getkey o raw_input."""
        salir = False
        eleccion = None
        while not salir:
            if tecla:
                cursoroff()
                entrada = getkey().lower()
                cursoron()
            else:
                entrada = pedir(mensaje).lower()
            if not entrada:
                salir = True
            else:
                if entrada in self.opciones:
                    eleccion = self.opciones[entrada][1]
                    salir = True
        return eleccion


class Demo(object):
    """Demostración del módulo 'cli'."""

    def __init__(self):
        """Constructor."""
        clear()
        out('Este es un ejemplo de la clase Prompt con Completador.\n')
        out('Presione dos veces TAB para obtener una lista de opciones.\n')
        prompt = Prompt(['start', 'stop', 'list', 'print'], 'stop').ciclo()
        linea = ''
        while linea != 'stop':
            linea = next(prompt)
            if linea:
                out('Recibido: {}\n'.format(linea))
        out('Este es un ejemplo de uso de la clase Menu.\n')
        out('Primero, vamos a usar un prompt.\n')
        opciones = {
            'a': ['Opción A', self.opcion_a],
            'b': ['Opción B', self.opcion_b],
            'c': ['Opción C', self.opcion_c]
        }
        opcion = Menu(opciones).pedir('> ')
        if opcion:
            out('Ha sido elegida la opción "{}"\n'.format(opcion()))
        out('Ahora sólo presione una tecla.\n')
        opcion = Menu(opciones).pedir('', True)
        if opcion:
            out('Ha sido elegida la opción "{}"\n'.format(opcion()))

    @staticmethod
    def opcion_a():
        """Método estático de prueba (A)."""
        return 'a'

    @staticmethod
    def opcion_b():
        """Método estático de prueba (B)."""
        return 'b'

    @staticmethod
    def opcion_c():
        """Método estático de prueba (C)."""
        return 'c'


if __name__ == '__main__':
    Demo()
