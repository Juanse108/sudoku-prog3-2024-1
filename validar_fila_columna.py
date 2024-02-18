import json
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("ejemploTablero.json") as sudoku:
    tablero = json.load(sudoku)


def validar_fila_columna(sudoku, numero, fila, columna):
    fila = (fila - 1) // 3
    columna1 = (columna - 1) // 3
    columna2 = (columna - 1) % 3
    columna3 = (fila - 1) % 3

    if sudoku[fila]["columnas"][columna1][columna2][columna3] == numero:
        return False

    for i in range(3):
        for j in range(3):
            if sudoku[i]["columnas"][columna1][columna2][j] == numero:
                return False

    for k in range(3):
        for l in range(3):
            if sudoku[fila]["columnas"][columna1][l][columna3] == numero:
                return False

    return True


@app.route('/validar', methods=['POST'])
def validar_numero():
    data = request.json
    numero = data['numero']
    fila = data['fila']
    columna = data['columna']

    if validar_fila_columna(tablero, numero, fila, columna):
        return jsonify({'message': 'Dato ubicado correctamente'}), 200
    else:
        return jsonify({'message': 'El dato no puede ser ubicado, cambie de posición'}), 400


if __name__ == '__main__':
    app.run(debug=True)
