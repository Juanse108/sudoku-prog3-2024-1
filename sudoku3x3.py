from flask import Flask, jsonify, request
import json

app = Flask(__name__)


class Cuadros():
    def _init_(self):
        self.cuadrito = 0
        self.number = 0
        self.fila = 0
        self.columnas = 0

    def validador(self, sudoku):
        # Reiniciar variables de instancia
        self.cuadrito = 0
        self.fila = 0

        for All_Sudoku in sudoku:
            fila = All_Sudoku["fila"]
            self.fila += 1
            for cuadro in All_Sudoku["columnas"]:
                self.cuadrito += 1

                numeros_vistos = set()
                for fila_cuadro in cuadro:
                    for numero in fila_cuadro:
                        if numero not in numeros_vistos or numero == 0:
                            numeros_vistos.add(numero)
                        else:
                            return False

        return True




