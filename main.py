import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from azure.communication.email import EmailClient

app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

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


def generate_sudoku_table(sudoku):
    html = '<html><body><table border="1">'
    for row in sudoku:
        html += '<tr>'
        for cell in row:
            html += '<td>{}</td>'.format(cell)
        html += '</tr>'
    html += '</table></body></html>'
    return html


@app.route('/validar', methods=['POST'])
def validar_numero():
    data = request.json
    numero = data['numero']
    fila = data['fila']
    columna = data['columna']
    email = data['email']

    if validar_fila_columna(tablero, numero, fila, columna):
        send_email(email, generate_sudoku_table(tablero))
        return jsonify({'message': 'Dato ubicado correctamente. Correo electrónico enviado'}), 200
    else:
        return jsonify({'message': 'El dato no puede ser ubicado, cambie de posición'}), 400


def send_email(email, body):
    connection_string = os.environ.get("CONNECTION_STRING")
    client = EmailClient.from_connection_string(connection_string)

    message = {
        "senderAddress": os.environ.get("SENDER_ADDRESS"),
        "recipients": {
            "to": [{"address": email}],
        },
        "content": {
            "subject": "Tablero de Sudoku",
            "html": body
        }
    }

    poller = client.begin_send(message)
    result = poller.result()


if __name__ == '__main__':
    # Utiliza Waitress como servidor en lugar del servidor de desarrollo de Flask para producción
    from waitress import serve

    print("Server running ")
    serve(app, host='0.0.0.0', port=5000)
