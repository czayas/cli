cli - Módulo Python para interfaces de línea de comando
=======================================================

# Introducción

El módulo **cli** (de *Command Line Interface*) es un conjunto de funciones y clases escritas en Python para la creación de interfaces de usuario basadas en línea de comandos con autocompletado y menús de opciones con captura de teclas.

Este módulo es compatible con las versiones 2.7.x y 3.3.x de Python, y aunque fue desarrollado y probado en plataforma GNU/Linux, se ha previsto su uso en plataforma Windows, y probablemente funcione sin problemas en este sistema operativo.

El módulo está disponible para la descarga en su página de GitHub:

[https://github.com/czayas/cli](https://github.com/czayas/cli)

Para usar el módulo, basta con colocar el archivo ```cli.py``` en la misma carpeta que el programa que va a importarlo.

El siguiente listado de código pretende ser un muestrario de la funcionalidad principal del módulo:

```python
from cli import *

# Limpiar la pantalla:
clear()

# Reemplazo de print para compatibilidad entre Python 2 y 3:
out('Presione dos veces TAB para obtener una lista de opciones.\n')

# Línea de comandos con autocompletado:
opciones = ['start', 'stop', 'list', 'print']
salir = opciones[1]  # El comando 'stop' se usará para salir del ciclo
p = Prompt(opciones, salir).ciclo()

# Ciclo REPL (Read, Eval, Print, Loop):
l = ''  # Línea introducida por el usuario
while l != salir:
    l = next(p)
    # A partir de aquí se procesa la línea:
    if l:
        out('Recibido: {}\n'.format(l))

# Para crear un menú, se usa un diccionario de funciones:
opciones = {
    'a': ['Opción A', funcion_a],
    'b': ['Opción B', funcion_b],
    'c': ['Opción C', funcion_c]
}

# Este tipo de menú utiliza un "prompt" (indicador de ingreso):
opcion = Menu(opciones).pedir()
if opcion:
    opcion()  # Se ejecuta la función elegida

# Esta variante sólo requiere de la pulsación de una tecla:
opcion = Menu(opciones).pedir('', True)  # (mensaje, tecla)
opcion()  # Se ejecuta la función elegida
```

Una manera rápida de experimentar lo que ofrece este módulo es ejecutando el archivo ```cli.py```, lo que iniciará una demostración equivalente al listado anterior.

Se ha intentado hacer de ```cli```un módulo util, práctico, multiversión y multiplataforma. Se recibirá con agrado cualquier comentario o sugerencia. Favor escribir a ```carlos@zayas.org```
