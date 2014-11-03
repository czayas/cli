#!/usr/bin/env python
#-*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Módulo: cli - Version 0.1 - 30/10/2014 (Rev. 31/10/2014)
# Carlos Zayas Guggiari <carlos@zayas.org>
# python --version : Python 2.7.5
# -----------------------------------------------------------------------------

import os
import sys
import readline


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
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(archivo, termios.TCSANOW, mode)
        return ch


if os.name == 'nt':
    import ctypes

    class _CursorInfo(ctypes.Structure):
        """Información sobre el cursor de texto."""
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


def cursoroff():
    """Oculta el cursor."""
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def cursoron():
    """Muestra el cursor."""
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def clear(l=100):
    """Borra la pantalla de texto."""
    if os.name == 'posix':
        # Unix, Linux, MacOS, BSD, etc.
        os.system('clear')
    elif os.name in ('nt', 'dos', 'ce'):
        # DOS, Windows
        os.system('CLS')
    else:
        # Otros sistemas operativos
        print '\n' * l


def out(cadena):
    """Envía una cadena a stdout y limpia el buffer (imprime más rápido)."""
    sys.stdout.write(cadena)
    sys.stdout.flush()


class Completador(object):
    def __init__(self, opciones):
        """Autocompletado con tabulación."""
        self.opciones = sorted(opciones)
        self.o = self.opciones[:]

    def completar(self, texto, estado):
        """Event handler para completer de readline."""
        if estado == 0:
            if texto:
                self.o = [o for o in self.opciones
                          if o and o.startswith(texto)]
            else:
                self.o = self.opciones[:]
        return None if estado >= len(self.o) else self.o[estado]


class Prompt(object):
    def __init__(self, opciones, salir='quit', prompt='> '):
        """Inductor o línea de comandos."""
        self.salir = salir
        self.prompt = prompt
        readline.set_completer(Completador(opciones).completar)
        readline.parse_and_bind('tab: complete')

    def ciclo(self):
        """Lectura del REPL (Read-Eval-Print Loop)."""
        linea = ''
        while linea != self.salir:
            try:
                linea = raw_input(self.prompt)     # Inductor (Prompt)
                yield linea
            except (KeyboardInterrupt, EOFError):  # Control+D o fin de archivo
                sys.exit(0)                        # Salir sin errores


class Menu(object):
    def __init__(self, opciones):
        """Menú de opciones."""
        self.opciones = opciones
        indice = sorted(opciones)
        for opcion in indice:
            print opcion + ':', opciones[opcion][0]

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
                entrada = raw_input(mensaje).lower()
            if not entrada:
                salir = True
            else:
                if entrada in self.opciones:
                    eleccion = self.opciones[entrada][1]
                    salir = True
        return eleccion


class Demo(object):
    def __init__(self):
        """Demostración del módulo 'cli'."""
        clear()
        print 'Este es un ejemplo de la clase Prompt con Completador.'
        print 'Presione dos veces TAB para obtener una lista de opciones.'
        p = Prompt(['start', 'stop', 'list', 'print'], 'stop').ciclo()
        l = ''
        while l != 'stop':
            l = p.next()
            if l:
                print 'Recibido: %s' % l
        print 'Este es un ejemplo de uso de la clase Menu.'
        print 'Primero, vamos a usar un prompt.'
        opciones = {
            'a': ['Opción A', self.opcion_a],
            'b': ['Opción B', self.opcion_b],
            'c': ['Opción C', self.opcion_c]
        }
        opcion = Menu(opciones).pedir('> ')
        if opcion:
            print 'Ha sido elegida la opción "%s"' % opcion()
        print 'Ahora sólo presione una tecla.'
        opcion = Menu(opciones).pedir('', True)
        if opcion:
            print 'Ha sido elegida la opción "%s"' % opcion()

    @staticmethod
    def opcion_a():
        return 'a'

    @staticmethod
    def opcion_b():
        return 'b'

    @staticmethod
    def opcion_c():
        return 'c'


if __name__ == '__main__':
    Demo()
