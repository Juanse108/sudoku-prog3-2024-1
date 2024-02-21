from flask import Flask, jsonify, request


class Cuadros():

    def validador(self, sudoku):

        for All_Sudoku in sudoku:
            fila = All_Sudoku["fila"]
            for cuadro in All_Sudoku["columnas"]:
                numeros_vistos = set()
                for fila_cuadro in cuadro:
                    for numero in fila_cuadro:
                        if numero not in numeros_vistos or numero == 0:
                            numeros_vistos.add(numero)
                        else:
                            return False

        return True




